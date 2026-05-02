Precisa criar o arquvi .env para colocar sua chave para teste: 
GEMINI_API_KEY=SUA_CHAVE_AQUI
instalar as dependencias para funcionamento: pip install flask flask-cors flask-sqlalchemy python-dotenv google-genai psycopg2
https://github.com/Lascoski/controle-financeiro-ia/commit/63a57213b30bd02ee4bea8507c2cded9fe3b5e20
O banco foi implementado com PostgreSQL, integrado via SQLAlchemy, e o backup está disponível no repositório em formato .sql
sistema online atravez: http://56.125.192.93/
O sistema utiliza a API do Google Gemini para responder perguntas do usuário
Como rodar o projeto (Docker):
1. Clone o repositório
git clone https://github.com/Lascoski/controle-financeiro-ia.git
cd controle-financeiro-ia
2. Crie o arquivo .env
GEMINI_API_KEY=sua_chave_aqui
3. Suba os containers
docker-compose up --build -d
4. Acesse no navegador
http://localhost
O backend roda na porta 5000 e é acessado via proxy /api pelo Nginx
A aplicação foi testada em ambiente com Docker em servidor Linux
Este projeto foi desenvolvido para fins educacionais.
