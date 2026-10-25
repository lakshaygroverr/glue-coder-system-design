# Episode 2 demos: Why ChatGPT can't run on your phone

Tested with Python 3 and Ollama (model: llama3.2:1b).

## One-time setup (Windows)
1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Install Ollama from https://ollama.com/download (Windows installer).
3. Download a small model (about 1.3 GB):
   ```
   ollama pull llama3.2:1b
   ```
4. Phone and laptop must be on the **same Wi-Fi**.
5. The first time you run a server, Windows Firewall will ask. Click **Allow** (Private networks).
6. Optional, to show your Android phone on screen: install **scrcpy**.

## Demo order for recording
| # | Command | What to show |
|---|---|---|
| 1 | `python demo1_request.py` | A real request and response: status 200, time, JSON, then a 404 |
| 2 | `python demo2_tiny_server.py` | Open the printed address on your PHONE. Terminal shows your phone's request arriving |
| 3 | `python demo3_model_size.py` | Model size math. Change PHONE_RAM_GB to your phone's RAM |
| 4 | `ollama run llama3.2:1b` | Chat with AI in the terminal, on your own laptop |
| 5 | `python demo4_chat_server.py` | Open the printed address on your PHONE. Chat with the AI running on your laptop. Watch the terminal: "Request: 1, 3, 5 messages of history" |
| 6 | `python demo5_streaming.py` | No streaming (long wait) vs streaming (first word almost instantly) |
| 7 | `python demo6_stateless.py` | Server forgets your name without history, remembers with it |
| 8 | Phone only | Google AI Edge Gallery: download Gemma, turn on airplane mode, chat |

## My test results (laptop with no GPU, so yours will be faster)
- Streaming: first word after 0.2 seconds. Without streaming: waited about 30 seconds for the full answer.
- Stateless: without history the AI said it had no information about the user. With history it answered "Your name is Glue Coder, and your favourite colour is orange."

Tip: if demo 4 or 5 says "Connection refused", Ollama isn't running. Open the Ollama app, or run `ollama serve`.
