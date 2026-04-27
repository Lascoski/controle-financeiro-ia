from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from google import genai

# =========================
# 🔥 CARREGAR .ENV PRIMEIRO
# =========================
load_dotenv()

# =========================
# 🚀 INICIAR APP
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# 🔑 GEMINI CLIENT
# =========================
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# =========================
# 🤖 IA
# =========================
@app.route("/ia", methods=["POST"])
def usar_ia():
    data = request.json
    pergunta = data.get("pergunta")

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=pergunta
        )

        return jsonify({"resposta": response.text})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# =========================
# 🌐 ROTAS FRONTEND
# =========================
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/app")
def app_page():
    return render_template("app.html")


# =========================
# 🗄️ BANCO DE DADOS
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/financas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =========================
# 👤 MODELOS
# =========================
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


# =========================
# 🏗️ CRIAR TABELAS
# =========================
with app.app_context():
    db.create_all()


# =========================
# 🔐 LOGIN
# =========================
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


# =========================
# 💰 CRUD
# =========================
@app.route("/dados/<int:user_id>", methods=["GET", "POST"])
def dados(user_id):

    # CREATE
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

    # READ
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


# =========================
# ✏️ UPDATE
# =========================
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


# =========================
# ❌ DELETE
# =========================
@app.route("/deletar/<int:id>", methods=["DELETE"])
def deletar(id):
    t = Transacao.query.get(id)

    if not t:
        return jsonify({"erro": "não encontrado"}), 404

    db.session.delete(t)
    db.session.commit()

    return jsonify({"status": "ok"})


# =========================
# 🚀 START
# =========================
if __name__ == "__main__":
    app.run(debug=True)