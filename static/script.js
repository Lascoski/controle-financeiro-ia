// script.js
let user_id = localStorage.getItem("user_id");

if (!user_id) {
    window.location.href = "/";
}

let grafico;

window.onload = () => {
    const ctx = document.getElementById("grafico").getContext("2d");

    grafico = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Entradas", "Saídas"],
            datasets: [{
                data: [0, 0],
                backgroundColor: ["#22c55e", "#ef4444"]
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false
        }
    });

    carregarDados();
};

async function adicionar() {
    const descricao = document.getElementById("descricao").value;
    const valor = document.getElementById("valor").value;
    const tipo = document.getElementById("tipo").value;

    if (!descricao || !valor) {
        alert("Preencha os campos!");
        return;
    }

    await fetch(`/api/dados/${user_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ descricao, valor, tipo, user_id })
    });

    document.getElementById("descricao").value = "";
    document.getElementById("valor").value = "";

    carregarDados();
}

async function carregarDados() {
    const res = await fetch(`/api/dados/${user_id}`);
    const data = await res.json();

    document.getElementById("saldo").innerText = data.saldo.toFixed(2);

    const ul = document.getElementById("lista");
    ul.innerHTML = "";

    data.entradas.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `<span style="color: #22c55e">+ R$ ${item.valor}</span> - ${item.descricao}`;
        ul.appendChild(li);
    });

    data.saidas.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `<span style="color: #ef4444">- R$ ${item.valor}</span> - ${item.descricao}`;
        ul.appendChild(li);
    });

    grafico.data.datasets[0].data = [
        data.total_entradas,
        data.total_saidas
    ];

    grafico.update();
}

async function perguntarIA() {
    const pergunta = document.getElementById("pergunta").value;
    const respostaIA = document.getElementById("respostaIA");

    if (!pergunta) {
        respostaIA.innerText = "Digite uma pergunta primeiro.";
        return;
    }

    respostaIA.innerText = "Consultando IA...";

    const res = await fetch("/api/ia", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ pergunta })
    });

    const data = await res.json();

    if (data.resposta) {
        respostaIA.innerText = data.resposta;
    } else {
        respostaIA.innerText = "Erro: " + data.erro;
    }
}
