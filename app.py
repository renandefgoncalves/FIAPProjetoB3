from flask import Flask, request, jsonify, render_template, session
import time
from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import credentials, chromadb

# Modeling libs
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages.ai import AIMessage
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.agents.initialize import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

app = Flask(__name__, template_folder='templates', static_folder='static')
message_history = []
app.secret_key = 'sua_chave_secreta'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    start_time = time.time()
    data = request.json
    prompt = data.get('prompt')

    chat = ChatOpenAI(model='gpt-4o-2024-08-06',
                      temperature=0.0,
                      api_key=credentials.api_key)

    def update_history(role, content):
        message_history.append(HumanMessage(content=content) if role == 'human' else AIMessage(content=content))

        if len(message_history) > 5:
            del message_history[0]

    def process_question(input):
        update_history('human', f"Pergunta: {input}")

        description = [HumanMessage(content=f"""
                Decida qual ferramenta usar com base na pergunta do usuário.

                Pergunta: {input}
                
                Se for uma pergunta sobre finanças e documentos PDF, responda com 'RAG'.
                Se for uma pergunta sobre cotação de ações, responda com 'Cotação'.
                Se for uma pergunta sobre notícias recentes sobre o mundo das finanças, responda com 'Yahoo'.
        """)]

        router_answer = chat.invoke(description + message_history)
        update_history('ai', router_answer.content)

        # Log da resposta do modelo
        print(f"Resposta do modelo: {router_answer.content}")

        if 'rag' in router_answer.content.lower():
            client = chromadb.PersistentClient(path="vectordb_fundos_net")
            embeddings = OpenAIEmbeddingFunction(api_key=credentials.api_key, model_name="text-embedding-3-small")
            collection = client.get_or_create_collection(name="fundos_net", embedding_function=embeddings)

            results = collection.query(query_texts=[input], n_results=10)
            update_history('human', f"Usando esses dados: {results['documents']}.")
            description = [HumanMessage(content=f"Responda a esse prompt: {input} usando esses dados: {results['documents']}")]
            answer = chat.invoke(description + message_history)
            update_history('ai', answer.content)
            return answer.content

        elif 'cotação' in router_answer.content.lower():
            df = pd.read_csv("data.csv")
            agent = create_pandas_dataframe_agent(chat, df, agent_type=AgentType.OPENAI_FUNCTIONS, allow_dangerous_code=True)
            answer = agent.invoke([input] + message_history)
            update_history('ai', answer['output'])
            return answer['output']

        elif 'yahoo' in router_answer.content.lower():
            agent_chain = initialize_agent([YahooFinanceNewsTool()], chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, return_intermediate_steps=True)
            answer = agent_chain.invoke([input] + message_history)
            update_history('ai', answer['output'])
            return answer['output']

        else:
            update_history('ai', router_answer.content)
            return router_answer.content

    print(f"tamanho do histórico {len(message_history)}")
    print(message_history)

    answer_content = process_question(prompt)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tempo de execução da função get_answer: {execution_time:.6f} segundos")

    # Defina seus rótulos verdadeiros (y_true) e ajuste a lógica para y_pred
    y_true = [1, 0, 1, 1, 0]  # Exemplo de rótulos verdadeiros
    # Lógica para determinar relevância da resposta
    relevant_keywords = ["relevante", "importante", "notícia", "cotação", "financeiro"]
    y_pred = [1 if any(keyword in answer_content.lower() for keyword in relevant_keywords) else 0 for _ in range(len(y_true))]

    # Verificando se y_pred tem o mesmo comprimento que y_true
    if len(y_pred) != len(y_true):
        print("Erro: y_pred deve ter o mesmo comprimento que y_true.")
        return jsonify({'error': 'Inconsistência no comprimento das previsões.'}), 400

    # Cálculo das métricas com zero_division
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    # Exibição das métricas
    print(f"Precisão: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")

    return jsonify({'answer': answer_content})

if __name__ == '__main__':
    app.run(debug=True)
