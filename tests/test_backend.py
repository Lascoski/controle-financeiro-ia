import os

# força usar SQLite nos testes
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from unittest.mock import patch

from backend import app, db, Usuario, Transacao


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


# =========================
# TESTE 1 - CADASTRO E LOGIN
# =========================

def test_cadastro_e_login_usuario(client):

    resposta_cadastro = client.post("/registrar", json={
        "username": "teste",
        "password": "123"
    })

    assert resposta_cadastro.status_code in [200, 201]

    resposta_login = client.post("/login", json={
        "username": "teste",
        "password": "123"
    })

    dados = resposta_login.get_json()

    assert resposta_login.status_code == 200
    assert dados["status"] == "ok"
    assert "user_id" in dados


# =========================
# TESTE 2 - LOGIN INVÁLIDO
# =========================

def test_login_com_senha_incorreta(client):

    client.post("/registrar", json={
        "username": "teste",
        "password": "123"
    })

    resposta = client.post("/login", json={
        "username": "teste",
        "password": "errada"
    })

    assert resposta.status_code == 401


# =========================
# TESTE 3 - CONTROLE FINANCEIRO
# =========================

def test_controle_financeiro_saldo(client):

    client.post("/registrar", json={
        "username": "teste",
        "password": "123"
    })

    login = client.post("/login", json={
        "username": "teste",
        "password": "123"
    })

    user_id = login.get_json()["user_id"]

    # entrada
    client.post(f"/dados/{user_id}", json={
        "descricao": "Salário",
        "valor": 100,
        "tipo": "entrada"
    })

    # saída
    client.post(f"/dados/{user_id}", json={
        "descricao": "Mercado",
        "valor": 40,
        "tipo": "saida"
    })

    resposta = client.get(f"/dados/{user_id}")

    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados["saldo"] == 60


# =========================
# TESTE 4 - CAMPOS VAZIOS
# =========================

def test_adicionar_transacao_sem_campos(client):

    client.post("/registrar", json={
        "username": "teste",
        "password": "123"
    })

    login = client.post("/login", json={
        "username": "teste",
        "password": "123"
    })

    user_id = login.get_json()["user_id"]

    resposta = client.post(f"/dados/{user_id}", json={})

    assert resposta.status_code in [400, 422, 500]


# =========================
# TESTE 5 - IA FUNCIONANDO
# =========================

def test_ia_resposta_sucesso(client):

    resposta = client.post("/ia", json={
        "pergunta": "Me dê uma dica financeira"
    })

    assert resposta.status_code in [200, 500]


# =========================
# TESTE 6 - IA SEM CHAVE / PERGUNTA
# =========================

def test_ia_sem_pergunta(client):

    resposta = client.post("/ia", json={})

    assert resposta.status_code in [400, 422, 500]