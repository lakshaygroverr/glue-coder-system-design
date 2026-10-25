# demo4_chat_server.py - your laptop becomes an AI server. Chat from your phone.
import json, socket
import requests
from flask import Flask, request, Response

OLLAMA = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

app = Flask(__name__)

PAGE = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>My AI</title><style>
body{font-family:sans-serif;margin:0;background:#0f172a;color:#fff}
#log{padding:16px;height:75vh;overflow:auto}.me{color:#facc15;margin:10px 0}.ai{margin:10px 0;white-space:pre-wrap}
form{display:flex;padding:12px;gap:8px}input{flex:1;padding:12px;font-size:16px;border-radius:8px;border:0}
button{padding:12px 16px;font-size:16px;border-radius:8px;border:0;background:#f97316;color:#fff}
</style></head><body><div id="log"></div>
<form id="f"><input id="q" placeholder="Ask my laptop..." autocomplete="off"><button>Send</button></form>
<script>
const history = [];
f.onsubmit = async (e) => {
  e.preventDefault();
  const text = q.value.trim(); if (!text) return; q.value = "";
  history.push({role: "user", content: text});
  log.innerHTML += `<div class="me">You: ${text}</div>`;
  const ai = document.createElement("div"); ai.className = "ai"; ai.textContent = "AI: "; log.appendChild(ai);
  const res = await fetch("/chat", {method: "POST", headers: {"Content-Type": "application/json"},
                                    body: JSON.stringify({messages: history})});
  const reader = res.body.getReader(); const dec = new TextDecoder(); let full = "";
  while (true) { const {done, value} = await reader.read(); if (done) break;
    const piece = dec.decode(value); full += piece; ai.textContent += piece; log.scrollTop = log.scrollHeight; }
  history.push({role: "assistant", content: full});
};
</script></body></html>"""

@app.route("/")
def home():
    return PAGE

@app.route("/chat", methods=["POST"])
def chat():
    messages = request.json["messages"]  # the client sends the WHOLE history every time
    print(f"Request: {len(messages)} messages of history received")

    def stream():
        with requests.post(OLLAMA, json={"model": MODEL, "messages": messages, "stream": True},
                           stream=True) as r:
            for line in r.iter_lines():
                if line:
                    chunk = json.loads(line)
                    yield chunk.get("message", {}).get("content", "")

    return Response(stream(), mimetype="text/plain")

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        s.close()
    print(f"Open on your phone (same Wi-Fi): http://{ip}:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)
