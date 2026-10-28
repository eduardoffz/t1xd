# servidor_web.py — Interface web para o xadrez simplificado
# Usa apenas biblioteca padrão (http.server + json)

import os
import sys
import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

from main import executar_jogada, partida_demo
from tabuleiro import criar_tabuleiro, tabuleiro_para_texto

# Estado do jogo (apenas neste arquivo)
estado_jogo = {
    "tabuleiro": None,
    "turno": "brancas",
    "mensagem": "Bem-vindo! Brancas começam.",
    "historico": []
}


def reiniciar_jogo():
    """
    Reinicia o estado do jogo com um tabuleiro novo.
    Retorna:
        None
    """
    estado_jogo["tabuleiro"] = criar_tabuleiro()
    estado_jogo["turno"] = "brancas"
    estado_jogo["mensagem"] = "Jogo reiniciado. Brancas começam."
    estado_jogo["historico"] = []


# Inicializa o jogo ao importar
reiniciar_jogo()


# Mapa de peças para Unicode
UNICODE_BRANCAS = {"R": "\u2654", "D": "\u2655", "T": "\u2656", "B": "\u2657", "C": "\u2658", "P": "\u2659"}
UNICODE_PRETAS = {"R": "\u265A", "D": "\u265B", "T": "\u265C", "B": "\u265D", "C": "\u265E", "P": "\u265F"}


PAGINA_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Xadrez Simplificado</title>
<style>
  :root {
    --bg: #f5f5f5; --fg: #222; --card: #fff; --border: #ccc;
    --clara: #f0d9b5; --escura: #b58863; --sel: #ffff0088;
    --ok: #4caf50; --erro: #f44336;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #1a1a1a; --fg: #eee; --card: #2a2a2a; --border: #555;
      --clara: #e8c98e; --escura: #8b6331;
    }
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: system-ui, sans-serif; background: var(--bg); color: var(--fg);
    display: flex; flex-direction: column; align-items: center; padding: 10px;
    min-height: 100vh;
  }
  h1 { font-size: 1.3em; margin: 8px 0; }
  #turno { font-size: 1.1em; margin: 6px 0; font-weight: bold; }
  #mensagem {
    padding: 8px 16px; border-radius: 6px; margin: 6px 0;
    font-weight: bold; min-height: 36px; text-align: center;
  }
  .msg-ok { background: var(--ok); color: #fff; }
  .msg-erro { background: var(--erro); color: #fff; }
  .msg-info { background: var(--border); color: var(--fg); }

  #tabuleiro {
    display: grid; grid-template-columns: repeat(8, 1fr);
    width: min(95vw, 480px); aspect-ratio: 1;
    border: 2px solid var(--border); margin: 8px 0;
  }
  .casa {
    display: flex; align-items: center; justify-content: center;
    font-size: min(8vw, 48px); cursor: pointer; user-select: none;
    aspect-ratio: 1; position: relative;
  }
  .casa-clara { background: var(--clara); }
  .casa-escura { background: var(--escura); }
  .casa.selecionada { background: var(--sel) !important; }

  .botoes { display: flex; gap: 8px; margin: 8px 0; flex-wrap: wrap; justify-content: center; }
  .botoes button {
    padding: 8px 16px; border: 1px solid var(--border); border-radius: 6px;
    background: var(--card); color: var(--fg); cursor: pointer; font-size: 0.9em;
  }
  .botoes button:hover { opacity: 0.8; }

  #historico-container {
    width: min(95vw, 480px); max-height: 200px; overflow-y: auto;
    background: var(--card); border: 1px solid var(--border); border-radius: 6px;
    padding: 8px; margin: 8px 0; font-size: 0.85em;
  }
  #historico-container p { margin: 2px 0; }

  #demo-container, #testes-container {
    width: min(95vw, 600px); max-height: 400px; overflow-y: auto;
    background: var(--card); border: 1px solid var(--border); border-radius: 6px;
    padding: 10px; margin: 8px 0; font-size: 0.85em; white-space: pre-wrap;
    font-family: monospace; display: none;
  }

  .coord-label {
    position: absolute; font-size: 0.35em; opacity: 0.6;
    bottom: 1px; right: 3px;
  }
</style>
</head>
<body>
<h1>&#9819; Xadrez Simplificado</h1>
<div id="turno">Turno: brancas</div>
<div id="mensagem" class="msg-info">Clique em uma peça para começar</div>
<div id="tabuleiro"></div>
<div class="botoes">
  <button onclick="reiniciar()">&#x21bb; Reiniciar</button>
  <button onclick="rodarDemo()">&#9654; Partida Demo</button>
  <button onclick="rodarTestes()">&#x2714; Rodar Testes</button>
</div>
<div id="historico-container"><strong>Histórico:</strong></div>
<div id="demo-container"></div>
<div id="testes-container"></div>

<script>
const UNICODE = {
  "Rb": "\\u2654","Db": "\\u2655","Tb": "\\u2656","Bb": "\\u2657","Cb": "\\u2658","Pb": "\\u2659",
  "Rp": "\\u265A","Dp": "\\u265B","Tp": "\\u265C","Bp": "\\u265D","Cp": "\\u265E","Pp": "\\u265F"
};
const COLUNAS = "abcdefgh";
let origem = null;

function pecaUnicode(p) { return UNICODE[p] || ""; }

function atualizarTabuleiro(dados) {
  const div = document.getElementById("tabuleiro");
  div.innerHTML = "";
  for (let l = 0; l < 8; l++) {
    for (let c = 0; c < 8; c++) {
      const casa = document.createElement("div");
      casa.className = "casa " + ((l + c) % 2 === 0 ? "casa-clara" : "casa-escura");
      casa.dataset.l = l;
      casa.dataset.c = c;
      casa.textContent = pecaUnicode(dados.tabuleiro[l][c]);
      // Coordenada de xadrez
      const label = document.createElement("span");
      label.className = "coord-label";
      label.textContent = COLUNAS[c] + (8 - l);
      casa.appendChild(label);
      casa.onclick = () => clicar(l, c);
      div.appendChild(casa);
    }
  }
  document.getElementById("turno").textContent = "Turno: " + dados.turno;
  if (dados.mensagem) {
    const msgEl = document.getElementById("mensagem");
    msgEl.textContent = dados.mensagem;
  }
}

function atualizarHistorico(hist) {
  const div = document.getElementById("historico-container");
  div.innerHTML = "<strong>Histórico:</strong>";
  for (let i = 0; i < hist.length; i++) {
    const p = document.createElement("p");
    p.textContent = hist[i];
    div.appendChild(p);
  }
  div.scrollTop = div.scrollHeight;
}

function setMsg(texto, tipo) {
  const el = document.getElementById("mensagem");
  el.textContent = texto;
  el.className = tipo === "ok" ? "msg-ok" : (tipo === "erro" ? "msg-erro" : "msg-info");
}

async function carregarEstado() {
  const res = await fetch("/api/estado");
  const dados = await res.json();
  atualizarTabuleiro(dados);
  atualizarHistorico(dados.historico);
}

function clicar(l, c) {
  if (origem === null) {
    origem = [l, c];
    // Destacar casa selecionada
    const casas = document.querySelectorAll(".casa");
    casas.forEach(ca => ca.classList.remove("selecionada"));
    casas[l * 8 + c].classList.add("selecionada");
    setMsg("Origem selecionada: " + COLUNAS[c] + (8 - l) + ". Clique no destino.", "info");
  } else {
    enviarJogada(origem, [l, c]);
    origem = null;
  }
}

async function enviarJogada(orig, dest) {
  const res = await fetch("/api/jogada", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({origem: orig, destino: dest})
  });
  const dados = await res.json();
  atualizarTabuleiro(dados);
  atualizarHistorico(dados.historico);
  if (dados.ok) {
    setMsg(dados.msg, "ok");
  } else {
    setMsg(dados.msg, "erro");
  }
}

async function reiniciar() {
  await fetch("/api/reiniciar", {method: "POST"});
  await carregarEstado();
  setMsg("Jogo reiniciado. Brancas começam.", "info");
  document.getElementById("demo-container").style.display = "none";
  document.getElementById("testes-container").style.display = "none";
}

async function rodarDemo() {
  const div = document.getElementById("demo-container");
  div.style.display = "block";
  div.textContent = "Rodando partida demo...";
  const res = await fetch("/api/demo", {method: "POST"});
  const passos = await res.json();
  let texto = "=== PARTIDA DEMO ===\\n\\n";
  for (let i = 0; i < passos.length; i++) {
    const p = passos[i];
    const status = p.resultado.ok ? "OK" : "FALHOU";
    texto += "Jogada: " + p.origem_txt + " -> " + p.destino_txt;
    texto += "  (Turno: " + p.turno + ") [" + status + "] " + p.resultado.msg + "\\n";
    texto += p.tabuleiro_texto + "\\n";
  }
  div.textContent = texto;
  // Recarregar estado após demo
  await carregarEstado();
}

async function rodarTestes() {
  const div = document.getElementById("testes-container");
  div.style.display = "block";
  div.textContent = "Rodando testes...";
  const res = await fetch("/api/testes", {method: "POST"});
  const dados = await res.json();
  const icone = dados.codigo === 0 ? "\\u2705 TODOS OS TESTES PASSARAM" : "\\u274C ALGUNS TESTES FALHARAM";
  div.textContent = icone + "\\n\\nCódigo de saída: " + dados.codigo + "\\n\\n" + dados.saida;
}

carregarEstado();
</script>
</body>
</html>
"""


class ManipuladorXadrez(BaseHTTPRequestHandler):
    """
    Manipulador HTTP para as rotas do servidor de xadrez.
    """

    def do_GET(self):
        """
        Trata requisições GET.
        Retorna:
            None
        """
        if self.path == "/":
            # Página HTML principal
            self.enviar_resposta(200, "text/html", PAGINA_HTML)
        elif self.path == "/api/estado":
            # Estado atual do jogo
            dados = {
                "tabuleiro": estado_jogo["tabuleiro"],
                "turno": estado_jogo["turno"],
                "mensagem": estado_jogo["mensagem"],
                "historico": estado_jogo["historico"]
            }
            self.enviar_json(dados)
        else:
            self.enviar_resposta(404, "text/plain", "Não encontrado")

    def do_POST(self):
        """
        Trata requisições POST.
        Retorna:
            None
        """
        if self.path == "/api/jogada":
            # Recebe e processa uma jogada
            corpo = self.ler_corpo()
            dados = json.loads(corpo)
            origem = tuple(dados["origem"])
            destino = tuple(dados["destino"])
            resultado = executar_jogada(
                estado_jogo["tabuleiro"], origem, destino, estado_jogo["turno"]
            )
            # Atualiza estado
            if resultado["ok"]:
                estado_jogo["turno"] = resultado["turno"]
            estado_jogo["mensagem"] = resultado["msg"]

            # Formata texto do histórico
            colunas = "abcdefgh"
            orig_txt = colunas[origem[1]] + str(8 - origem[0])
            dest_txt = colunas[destino[1]] + str(8 - destino[0])
            status_txt = "OK" if resultado["ok"] else "FALHOU"
            hist_txt = orig_txt + " -> " + dest_txt + " [" + status_txt + "] " + resultado["msg"]
            estado_jogo["historico"].append(hist_txt)

            resposta = {
                "tabuleiro": estado_jogo["tabuleiro"],
                "turno": estado_jogo["turno"],
                "mensagem": estado_jogo["mensagem"],
                "historico": estado_jogo["historico"],
                "ok": resultado["ok"],
                "msg": resultado["msg"],
                "captura": resultado["captura"]
            }
            self.enviar_json(resposta)

        elif self.path == "/api/reiniciar":
            # Reinicia o jogo
            reiniciar_jogo()
            self.enviar_json({
                "tabuleiro": estado_jogo["tabuleiro"],
                "turno": estado_jogo["turno"],
                "mensagem": estado_jogo["mensagem"],
                "historico": estado_jogo["historico"]
            })

        elif self.path == "/api/demo":
            # Roda a partida demo
            passos = partida_demo()
            self.enviar_json(passos)

        elif self.path == "/api/testes":
            # Roda os testes
            try:
                # Roda os testes no diretório do projeto
                diretorio = os.path.dirname(os.path.abspath(__file__))
                resultado = subprocess.run(
                    [sys.executable, os.path.join(diretorio, "testes.py")],
                    capture_output=True, text=True, timeout=60,
                    cwd=diretorio
                )
                self.enviar_json({
                    "codigo": resultado.returncode,
                    "saida": resultado.stdout + resultado.stderr
                })
            except Exception as e:
                self.enviar_json({
                    "codigo": 1,
                    "saida": "Erro ao rodar testes: " + str(e)
                })
        else:
            self.enviar_resposta(404, "text/plain", "Não encontrado")

    def ler_corpo(self):
        """
        Lê o corpo da requisição HTTP.
        Retorna:
            str: corpo da requisição.
        """
        tamanho = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(tamanho).decode("utf-8")

    def enviar_resposta(self, codigo, tipo, conteudo):
        """
        Envia uma resposta HTTP.
        Parâmetros:
            codigo (int): código HTTP.
            tipo (str): tipo MIME.
            conteudo (str): corpo da resposta.
        Retorna:
            None
        """
        self.send_response(codigo)
        self.send_header("Content-Type", tipo + "; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(conteudo.encode("utf-8"))

    def enviar_json(self, dados):
        """
        Envia uma resposta JSON.
        Parâmetros:
            dados: dados a serializar em JSON.
        Retorna:
            None
        """
        self.enviar_resposta(200, "application/json", json.dumps(dados, ensure_ascii=False))

    def log_message(self, formato, *args):
        """Suprime log padrão para manter terminal limpo."""
        pass


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8000))
    servidor = HTTPServer(("0.0.0.0", porta), ManipuladorXadrez)
    print(f"Servidor rodando em http://localhost:{porta}")
    print("Pressione Ctrl+C para parar.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        servidor.server_close()
