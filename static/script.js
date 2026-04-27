// script.js
let user_id = localStorage.getItem("user_id");


// 🔐 se não estiver logado, volta pro login
if (!user_id) {
    window.location.href = "login.html";
}
let grafico;

window.onload = () => {
    const ctx = document.getElementById('grafico').getContext('2d');

    grafico = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Entradas', 'Saídas'],
            datasets: [{
                data: [0, 0],
                backgroundColor: ['#22c55e', '#ef4444']
            }]
        }
    });

    carregarDados(); // 🔥 CARREGA AO ABRIR
};

async function adicionar() {
    const descricao = document.getElementById("descricao").value;
    const valor = document.getElementById("valor").value;
    const tipo = document.getElementById("tipo").value;

    if (!descricao || !valor) {
        alert("Preencha os campos!");
        return;
    }

    await fetch(`http://127.0.0.1:5000/dados/${user_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ descricao, valor, tipo, user_id })
    });

    document.getElementById("descricao").value = "";
    document.getElementById("valor").value = "";

    carregarDados(); // 🔥 ATUALIZA DEPOIS DE ADICIONAR
}

async function carregarDados() {
    const res = await fetch(`http://127.0.0.1:5000/dados/${user_id}`);
    const data = await res.json();

    document.getElementById("saldo").innerText = data.saldo.toFixed(2);

    const ul = document.getElementById("lista");
    ul.innerHTML = "";

    // Entradas
    data.entradas.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `<span style="color: #22c55e">+ R$ ${item.valor}</span> - ${item.descricao}`;
        ul.appendChild(li);
    });

    // Saídas
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

    const res = await fetch("http://127.0.0.1:5000/ia", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ pergunta })
    });

    const data = await res.json();

    document.getElementById("respostaIA").innerText = data.resposta;
}

