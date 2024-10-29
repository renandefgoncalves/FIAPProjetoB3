# Grupo 5
- Kauan Alves Batista - RM555082
- Lancelot Chagas Rodrigues - RM554707
- Pablo Menezes Barreto - RM556389
- Renan de França Gonçalves - RM558413

## Introdução
Este projeto foi desenvolvido com o objetivo de resolver um problema específico da B3 - A Bolsa do Brasil. A dor central que buscamos solucionar é construir um chatbot, usando LPN (Linguagem de Processamento Natural), para dinamizar 
o site [FundosNet](https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM) para que o usuário não precise buscar informações dentro de cada arquivo hospedado, mas sim efetuando perguntas de forma natural. Essa dificuldade impacta o usuário, que perde muito tempo buscando arquivos de forma não intuitiva, resultando em uma perda de tempo e falta de dinamismo.

O objetivo deste projeto é criar uma solução que torne prática a interatividade entre os arquivos hospedados dos Fundos de Investimento e o usuário final. Com isso, esperamos atingir uma diminuição no tempo perdido ao buscar informações pertinentes aos Fundos de Investimento, proporcionando uma melhoria visual, economia de tempo e praticidade.

## Desenvolvimento
Abaixo o link com o vídeo explicativo do desenvolvimento do aplicativo, desde os primeiros contatos com a B3:
<br>
[Vídeo Explicativo](https://github.com/user-attachments/assets/981e31dc-891b-4271-a6d1-f4ef289ec2b4)

## Tecnologias Utilizadas
A aplicação foi desenvolvida utilizando as seguintes tecnologias:
- **Linguagens e Frameworks**: Python com Flask.
- **Bibliotecas**: Langchain, ChromaDB, Selenium, PyPDF, BeautifulSoup e OpenAI.

## Funcionamento
O sistema funciona da seguinte forma:
1. **Passo 1**: Ao acessar o site, efetue uma pergunta.
2. **Passo 2**: Pressione Enter ou clique no botão da seta e aguarde a resposta.
3. **Passo 3**: Após receber a resposta, você já pode efetuar outra pergunta.

## Código-Fonte
O código-fonte utilizado para o desenvolvimento deste projeto contém todos os scripts necessários para a execução e desenvolvimento da aplicação:
[Link do Google Drive com Todos Arquivos utilizados](https://drive.google.com/drive/folders/1Nvmlpqp2vKUZvPscPsSVNbItFhNr0vvC?usp=drive_link)

## Demonstração
Veja o funcionamento da aplicação no vídeo a seguir:
[Video Explicativo](https://www.youtube.com/watch?v=hGaba4ybX2E)

## Testes de Desempenho

##### Definição da Ferramenta de Teste
- Nós utilizamos a biblioteca do scikit-learn para calcular métricas como precisão, recall e F1-score, além da biblioteca time que mostra o tempo gasto na execução da tarefa (no nosso caso, da requisição da pergunta, até a resposta)

##### Evidências de Testes
- [Relatório de Desempenho](https://drive.google.com/file/d/1wNz_l0NSLuOIodhmTUl8jT0rtKq_HaD7/view?usp=sharing)

##### Discussão dos Resultados
- Os teste foram muito satisfatórios, pois, serviram pra identificar que o ChatGPT 4o mini, tem uma resposta muito mais rápida do que o ChatGPT 3.5, além de ter uma base maior e ser mais assertivo.

##### Soluções Futuras 
 - Postetiormente, gostariamos de usar a biblioteca locust para verificar o uso em várias máquinas simultâneas, trazendo o resultado de carga.
