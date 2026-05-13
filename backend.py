from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# IMPORTS DO LANGCHAIN
# ChatGoogleGenerativeAI conecta o LangChain ao Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

# ChatPromptTemplate permite criar um prompt estruturado
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

# Verifica se a chave foi carregada
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("CHAVE USADA:", api_key[:12])
else:
    print("ERRO: GEMINI_API_KEY não encontrada no .env")


# INICIAR APP
app = Flask(__name__)
CORS(app)


# CONFIGURAÇÃO DO LANGCHAIN COM GEMINI
# Aqui substituímos o uso direto do google.genai.Client
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.7
)

# PROMPT PADRÃO USADO PELA IA
# O LangChain permite organizar melhor a pergunta enviada para o modelo
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma IA assistente de um sistema de controle financeiro. Responda de forma clara, objetiva e útil."),
    ("human", "{pergunta}")
])

# CRIA A CHAIN
# A pergunta passa pelo prompt e depois pelo modelo Gemini
chain = prompt | llm


# IA COM LANGCHAIN
@app.route("/ia", methods=["POST"])
def usar_ia():
    data = request.json
    pergunta = data.get("pergunta")

    if not pergunta:
        return jsonify({"erro": "Pergunta não enviada"}), 400

    try:
        # ALTERAÇÃO PRINCIPAL:
        # Antes: client.models.generate_content(...)
        # Agora: chain.invoke(...) usando LangChain
        response = chain.invoke({
            "pergunta": pergunta
        })

        print("RESPOSTA IA:", response.content)

        return jsonify({"resposta": response.content})

    except Exception as e:
        print("ERRO NA IA:", e)
        return jsonify({"erro": str(e)}), 500


# ROTAS FRONTEND
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/app")
def app_page():
    return render_template("app.html")


# BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@db:5432/financas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# MODELOS
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Transacao(db.Model):
    __tablename__ = "transacoes"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))
    valor = db.Column(db.Float)
    descricao = db.Column(db.String(200))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))


# CRIAR TABELAS
with app.app_context():
    db.create_all()


# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = Usuario.query.filter_by(
        username=data["username"],
        password=data["password"]
    ).first()

    if user:
        return jsonify({"status": "ok", "user_id": user.id})

    return jsonify({"status": "erro"}), 401


@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json

    if Usuario.query.filter_by(username=data["username"]).first():
        return jsonify({"status": "usuario_existente"}), 400

    novo = Usuario(
        username=data["username"],
        password=data["password"]
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({"status": "ok"})


# CRUD
@app.route("/dados/<int:user_id>", methods=["GET", "POST"])
def dados(user_id):

    if request.method == "POST":
        data = request.json

        nova = Transacao(
            tipo=data["tipo"],
            valor=data["valor"],
            descricao=data["descricao"],
            usuario_id=user_id
        )

        db.session.add(nova)
        db.session.commit()

        return jsonify({"status": "ok"})

    transacoes = Transacao.query.filter_by(usuario_id=user_id).all()

    entradas = [t for t in transacoes if t.tipo == "entrada"]
    saidas = [t for t in transacoes if t.tipo == "saida"]

    total_entradas = sum(t.valor for t in entradas)
    total_saidas = sum(t.valor for t in saidas)

    return jsonify({
        "entradas": [{"id": t.id, "valor": t.valor, "descricao": t.descricao} for t in entradas],
        "saidas": [{"id": t.id, "valor": t.valor, "descricao": t.descricao} for t in saidas],
        "saldo": total_entradas - total_saidas,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas
    })


# UPDATE
@app.route("/editar/<int:id>", methods=["PUT"])
def editar(id):
    data = request.json
    t = Transacao.query.get(id)

    if not t:
        return jsonify({"erro": "não encontrado"}), 404

    t.descricao = data["descricao"]
    t.valor = data["valor"]

    db.session.commit()

    return jsonify({"status": "ok"})


# DELETE
@app.route("/deletar/<int:id>", methods=["DELETE"])
def deletar(id):
    t = Transacao.query.get(id)

    if not t:
        return jsonify({"erro": "não encontrado"}), 404

    db.session.delete(t)
    db.session.commit()

    return jsonify({"status": "ok"})


# START
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)