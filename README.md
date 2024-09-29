Grupo 5 

Kauan Alves Batista - RM555082
Lancelot Chagas Rodrigues - RM554707
Leandro Nakauê de Almeida - RM554580
Pablo Menezes Barreto - RM556389
Renan de França Gonçalves - RM558413

# Introdução

Este projeto foi desenvolvido com o objetivo de resolver um problema específico da B3 - A Bolsa do Brasil. A dor central que buscamos solucionar é [construir um chatbot, usando LPN (Linguagem de Processamento Natural) para dinamizar 
o site FundosNet https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM para que o usuário não precise buscar informações dentro de cada arquivo hospedado e sim efetuando perguntas de forma natural ]. Essa dificuldade impacta 
[ao usuário que perde muito tempo buscando arquivos de forma não intuitiva], resultando em uma [perda de tempo e falta de dinamismo].

O objetivo deste projeto é criar uma solução que [torne de forma prática a interatividade entre os arquivos hospedados dos Fundos de Investimento e o usuário final]. Com isso, esperamos atingir [uma diminuição no tempo perdido ao buscar informações pertinentes aos
Fundos de Investimento], proporcionando uma [melhoria visual, economia de tempo e praticidade].

# Desenvolvimento
Abaixo o link com o vídeo explicativo do desenvolvimento do aplicativo, desde os primeiros contatos com a B3
https://www.youtube.com/watch?v=hGaba4ybX2E


### Arquitetura

A arquitetura da solução foi planejada utilizando o **Draw.io**, e o **Excel**, com componentes distribuídos para otimizar a eficiência e escalabilidade do sistema. A seguir, descrevemos a arquitetura visual:

![Visual WebPage](https://i.postimg.cc/02dC6GnH/avcb.png)

### Tecnologias Utilizadas

A aplicação foi desenvolvida utilizando as seguintes tecnologias:
- **Linguagens e Frameworks**: [Python com Flask].
- **Bibliotecas**: [Langchain, ChromaDB, Selenium, PyPDF, BeautifulSoup e OpenAI].

### Funcionamento

O sistema funciona da seguinte forma:
1. [Passo 1: Ao acessar o site, executar o webscraper].
2. [Passo 2: Processar os PDFs].
3. [Passo 3: Após o processamento dos PDF, efetuar a pergunta desejada e aguardar a resposta condizendo com os PDFs].


# Código-Fonte

O código-fonte utilizado para o desenvolvimento deste projeto contém todos os scripts necessários para a execução e desenvolvimento da aplicação.

(https://github.com/renandevbr/FIAPProjetoB3/blob/main/app.py))

# Demonstração

Veja o funcionamento da aplicação no vídeo a seguir:

(https://www.youtube.com/watch?v=EXEMPLO](https://www.youtube.com/watch?v=hGaba4ybX2E)




