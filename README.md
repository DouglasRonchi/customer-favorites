# customer-favorites
Projeto criado por Douglas Buss Ronchi
Definição da stack utilizada no projeto:

Linguagem: Python
Framework: FastAPI
Banco de Dados: Mongo utilizado com mongoengine no python
Autenticação: JWT
Testes: Pytest / Unittest
Mock da API de Produtos: Endpoint dentro da API para mockar as respostas

PS.: Adicionei um Redis para cache de rota, mas caso precise de mais velocidade eu
traria duas sugestões:
- Colocar um cache no APIGateway, por que dessa forma, a requisição
nem entra na API, já volta direto pro cliente, sendo muito mais rápida a resposta.
- Colocar as requisições pesadas em rotas assíncronas, garantindo mais velocidade
de execução.

Criando o Ambiente Virtual

- python -m venv venv
- source venv/bin/activate  # Linux/Mac
- venv\Scripts\activate # Windows
Instalando as dependências
- pip install -r requirements.txt

Envs do Projeto (.env):
MONGO_URI=(URI do mongo que você criar na sua máquina)
ACCESS_TOKEN_EXPIRE_MINUTES=(Tempo que o token expira em minutos: INT)
SECRET_KEY=(Chave secreta para gerar os tokens, pode adicionar qualquer palavra para teste)
ALGORITHM=(Algoritmo utilizado para a criptografia, geralmente "HS256")
REDIS_URI=(URI da conexão com redis)
REDIS_EXPIRE_MINUTES=(Tempo que o dado do cache expira em minutos: INT)


Rodar com Docker-Compose:
- Instale e Inicie o Docker Desktop
- Rode a seguinte linha no terminal:
- docker-compose up -d --build
- Esse comando inicia o mongo, o redis e a API dentro de containers
- para parar os containers rode:
- docker-compose down -v

Para Rodar Manualmente:
- Instale e Inicie o Docker Desktop
- siga os comandos abaixo no terminal:
- docker pull mongo
- docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin mongo
- Vai criar uma instância no mongo com user=admin e senha=admin
- docker pull redis
- docker run --name redis -p 6379:6379 -d redis
- crie um arquivo .env com as variáveis citadas acima
- Após criar a instância do Mongo e do Redis, na raíz do projeto temos o arquivo run.py
- rode esse arquivo, ele irá iniciar a API

* Caso não rode por algum problemas com portas, rode o seguinte:
- docker-compose down -v
- docker system prune -f
- docker-compose up -d --build

- Na raíz do projeto temos o arquivo customer-favorites.postman_collection.json, ele é a collection exportada do postman
- Importe esta collection no postman caso queira fazer testes de mesa

- Para rodar os unittests rode o seguinte comando:
- pytest --cov=app/
- O projeto está sendo entregue com 80% de cobertura de testes
