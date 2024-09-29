from flask import Flask, request, jsonify, render_template, session
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import credentials
import os
import warnings
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'sua_chave_secreta'  # Necessário para usar sessões

client = chromadb.Client()
embeddings = embedding_functions.OpenAIEmbeddingFunction(api_key=credentials.api_key, model_name="text-embedding-3-small")
collection = client.get_or_create_collection(name="fundos_net", embedding_function=embeddings)

# Função scrapper para realizar o scraping
def scrapper(download_path: str = r"C:\Users\Renan\Desktop\B3 - ProjetoG5\FundosNet",
             start_date: str = '', 
             end_date: str = '', 
             category: str = '',
             n_pages: str = ''):
    
    # Verifique se a pasta FundosNet existe, caso contrário, crie-a
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # FundosNET URLs
    url = "https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM"

    # Chrome Options
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,  # Impede a exibição da caixa de diálogo 'Salvar como'
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,  # Habilita o Safe Browsing para permitir downloads
    })
    
    # Usando o webdriver-manager para instalar e gerenciar o ChromeDriver
    service = Service(executable_path='chromedriver64.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Acessando a página
    print(f"Acessando a URL: {url}")
    driver.get(url)
    sleep(1)

    # Aplicando o filtro de datas e categoria
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="showFiltros"]'))).click()  # Pressiona "Mostrar Filtros"
    sleep(1)
    driver.find_element(By.ID, 'dataInicial').send_keys(start_date)  # Preenche a data inicial
    driver.find_element(By.ID, 'dataFinal').send_keys(end_date)  # Preenche a data final
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="s2id_categoriaDocumento"]'))).click()  # Pressiona "Categoria"
    driver.find_element(By.ID, 's2id_autogen2_search').send_keys(category)  # Preenche a categoria
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-results-2"]'))).click()  # Seleciona a categoria
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filtrar"]'))).click()  # Pressiona "Filtrar"
    sleep(1)
    
    # Obtendo o HTML da página e criando o BeautifulSoup
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    
    # Obtendo o limite de páginas
    if n_pages:
        pages = int(n_pages)
    else:
        pages = int([i.text for i in soup.find_all("a", {"class": "paginate_button"})][-2])

        for page in range(1, pages + 1):
            print(f"Processando página {page}")
            if page > 1:
                print(f"Indo para a página {page}")
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                span = [i['data-dt-idx'] for i in soup.find_all("a", {"class": "paginate_button"}) if i.text == str(page)][0]
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="tblDocumentosEnviados_paginate"]/span/a[{span}]'))).click()
        
        sleep(1)

    # Tentando baixar os arquivos
    for i in range(1, 11):
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="tblDocumentosEnviados"]/tbody/tr[{i}]/td[10]/div/a[2]/i'))).click()
        except Exception as e:
            print(f"Arquivo {i} não foi baixado: {e}")
            continue

    # Fechando o navegador
    driver.quit()

# Função para processar PDFs e adicioná-los ao ChromaDB
def process_pdfs():
    pdf_dir = r"C:\Users\Renan\Desktop\B3 - ProjetoG5\FundosNet"
    if not os.path.exists(pdf_dir):
        print("Pasta FundosNet não encontrada.")
        return

    files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    if not files:
        print("Nenhum arquivo PDF encontrado na pasta FundosNet.")
        return

    content = []
    metadata = []
    ids = []
    id_item = 0

    for file in files:
        loader = PyPDFLoader(os.path.join(pdf_dir, file))
        pages = loader.load_and_split()
        for page in pages:
            id_item += 1
            content.append(page.page_content)
            metadata.append(page.metadata)
            ids.append(f"{id_item}")

    collection.add(documents=content, metadatas=metadata, ids=ids)
    print(f"{len(ids)} documentos adicionados ao ChromaDB.")

# Função para listar os PDFs no diretório FundosNet
def list_pdfs():
    pdf_dir = r"C:\Users\Renan\Desktop\B3 - ProjetoG5\FundosNet"
    if not os.path.exists(pdf_dir):
        return []

    return [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')  # Serve o arquivo index.html

# Rota para executar o scraping real
@app.route('/run_scraper', methods=['POST'])
def run_scraper():
    try:
        scrapper(
            download_path=r"C:\Users\Renan\Desktop\B3 - ProjetoG5\FundosNet",  # Salva os PDFs na pasta FundosNet
            start_date='17/06/2024',  # Data de início para o scraping
            end_date='17/06/2024',  # Data de término para o scraping
            category='Relatórios',  # Categoria de documentos a ser raspada
            n_pages='1'  # Número de páginas a serem raspadas
        )
        return jsonify({'message': 'Scraping executado com sucesso!'})
    except Exception as e:
        return jsonify({'message': f'Erro ao executar scraping: {str(e)}'})

# Rota para processar os PDFs
@app.route('/process_pdfs', methods=['POST'])
def process_pdfs_route():
    process_pdfs()
    return jsonify({'message': 'PDFs processados com sucesso!'})

# Rota para obter a lista de documentos
@app.route('/get_documents', methods=['GET'])
def get_documents():
    documents = list_pdfs()
    return jsonify(documents)

# Função para configurar o modelo de linguagem
def set_llm(engine: str = 'gpt-4o-2024-05-13', temperature: float = 0.0, tokens: int = None):
    return ChatOpenAI(model=engine, temperature=temperature, api_key=credentials.api_key, max_tokens=tokens)

# Rota para obter resposta da IA considerando o histórico
@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.json
    prompt = data.get('prompt')

    # Atualiza a lista de documentos antes de responder
    documents = list_pdfs()
    session['documents'] = documents

    # Recupera o histórico da sessão
    if 'history' not in session:
        session['history'] = []

    history = session['history']

    # Adiciona a nova entrada ao histórico
    history.append(f"Você: {prompt}")

    # Responde à pergunta sobre a quantidade de documentos
    if "quantos documentos" in prompt.lower():
        answer_content = f"Você me enviou um total de {len(documents)} documentos."
    else:
        full_prompt = "\n".join(history)
        results = collection.query(query_texts=[full_prompt], n_results=3)
        chat = set_llm(tokens=100)
        description = [HumanMessage(content=f"Usando esses dados: {results}. Responda a esse prompt: {prompt}.")]
        answer = chat(description)
        answer_content = answer.content

    # Adiciona a resposta ao histórico
    history.append(f"AVFundosNet: {answer_content}")

    # Atualiza o histórico na sessão
    session['history'] = history

    return jsonify({'answer': answer_content})

if __name__ == '__main__':
    app.run(debug=True)
