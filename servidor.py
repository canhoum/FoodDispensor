from flask import Flask, request, render_template_string, jsonify, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'segredo_super_seguro'

historico = []
USERNAME = 'gato'
PASSWORD = 'comida123'

@app.route('/registo', methods=['GET'])
def registo():
    peso = request.args.get("peso")
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📥 Peso recebido: {peso}g às {hora}")
    historico.insert(0, {"hora": hora, "peso": peso})
    return "OK", 200

@app.route('/', methods=['GET', 'POST'])
def login():
    erro = ""
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['user'] = USERNAME
            return redirect(url_for('dashboard'))
        else:
            erro = "Credenciais inválidas"

    return render_template_string("""
    <html><head><title>Login</title><style>
    body { font-family: sans-serif; background: #e8f0fe; display: flex; justify-content: center; align-items: center; height: 100vh; }
    .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.2); width: 300px; }
    input { width: 100%; padding: 10px; margin: 10px 0; }
    button { width: 100%; padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 5px; }
    .erro { color: red; font-size: 0.9em; }
    </style></head><body>
    <form method="POST">
        <div class="card">
            <h2>🔐 Login</h2>
            <input type="text" name="username" placeholder="Utilizador" required>
            <input type="password" name="password" placeholder="Palavra-passe" required>
            <button type="submit">Entrar</button>
            <p class="erro">{{ erro }}</p>
        </div>
    </form></body></html>
    """, erro=erro)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    html = """
    <!DOCTYPE html><html><head>
    <title>🐱 Painel de Refeições</title>
    <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>
    <style>
    body { font-family: sans-serif; padding: 20px; background: #f4f4f4; }
    h1 { color: #2c3e50; }
    .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .peso { float: right; color: #4CAF50; font-weight: bold; }
    .bloqueado { background: #ffdddd; color: #b00; }
    .popup {
        background: #f8d7da; color: #721c24; padding: 10px 15px;
        border: 1px solid #f5c6cb; border-radius: 6px; margin-bottom: 15px;
    }
    </style></head><body>
    <h1>🐾 Histórico de Refeições</h1>
    <div id=\"popup\"></div>
    <p>Total de refeições: <strong id=\"total\">0</strong></p>
    <canvas id=\"grafico\" width=\"400\" height=\"150\"></canvas>
    <div id=\"historico\"></div>

    <script>
    function atualizar() {
        fetch('/historico').then(r => r.json()).then(data => {
            document.getElementById("total").innerText = data.length;
            const div = document.getElementById("historico");
            div.innerHTML = "";
            const labels = [], pesos = [];

            let bloqueioDetectado = false;

            data.slice().reverse().forEach(e => {
                const c = document.createElement("div");
                const isBloq = e.peso.includes("Bloqueado");
                if (isBloq) bloqueioDetectado = true;
                c.className = "card" + (isBloq ? " bloqueado" : "");
                c.innerHTML = `<span>${e.hora}</span> <span class='peso'>${e.peso}</span>`;
                div.appendChild(c);

                if (!isBloq) {
                    labels.push(e.hora.split(" ")[1]);
                    pesos.push(parseFloat(e.peso));
                }
            });

            if (bloqueioDetectado) {
                document.getElementById("popup").innerHTML = "<div class='popup'>🚫 O gato já comeu as 5 vezes de hoje!</div>";
            } else {
                document.getElementById("popup").innerHTML = "";
            }

            const ctx = document.getElementById("grafico").getContext("2d");
            if (window.meuGrafico) window.meuGrafico.destroy();
            window.meuGrafico = new Chart(ctx, {
                type: 'line', data: {
                    labels: labels,
                    datasets: [{ label: 'Peso (g)', data: pesos, backgroundColor: 'rgba(76, 175, 80, 0.2)', borderColor: '#4CAF50', borderWidth: 2 }]
                },
                options: { scales: { y: { beginAtZero: true } } }
            });
        });
    }
    setInterval(atualizar, 3000);
    atualizar();
    </script>
    </body></html>
    """
    return render_template_string(html)

@app.route('/historico')
def historico_json():
    return jsonify(historico[:20])

port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
