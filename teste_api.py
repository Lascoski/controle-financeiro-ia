import requests

url = "http://127.0.0.1:5000/ia"

data = {
    "pergunta": "Me dê uma dica de economia financeira pessoal."
}

res = requests.post(url, json=data)

print("Status:", res.status_code)
print("Resposta:", res.json())