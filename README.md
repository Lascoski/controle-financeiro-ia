# Controle Financeiro com IA

Sistema de controle financeiro desenvolvido para fins educacionais.

O projeto permite gerenciar informações financeiras e utiliza a **API Google Gemini** para disponibilizar recursos de inteligência artificial dentro do sistema.

O banco de dados utilizado é **PostgreSQL**, integrado ao backend através do **SQLAlchemy**.

## Tecnologias utilizadas

* Python, Flask, PostgreSQL, SQLAlchemy, Docker, Nginx, Google Gemini API, HTML, CSS e JavaScript

## Pré-requisitos

Para executar o projeto, é necessário ter instalado:

* Git
* Docker Desktop

Não é necessário instalar Python, PostgreSQL ou as bibliotecas do projeto manualmente caso seja utilizado o Docker.

## Como baixar e executar o projeto

### 1. Clone o projeto
git clone https://github.com/Lascoski/controle-financeiro-ia.git
cd controle-financeiro-ia
2. Configure a API do Gemini

Crie um arquivo .env na pasta do projeto:

GEMINI_API_KEY=SUA_CHAVE_AQUI
3. Inicie o sistema

Com o Docker Desktop aberto, execute:

docker compose up --build -d

Verifique se os containers estão funcionando:
docker compose ps

4. Acesse Abra no navegador:

http://localhost

O frontend utiliza a porta 80, o backend 5000 e o PostgreSQL 5432.

Para encerrar:

docker compose down
Observações

O banco de dados utiliza PostgreSQL integrado com SQLAlchemy e possui um backup .sql disponível no repositório.

O projeto utiliza modelos do Google Gemini para responder às solicitações do usuário.

Projeto desenvolvido para fins educacionais.
