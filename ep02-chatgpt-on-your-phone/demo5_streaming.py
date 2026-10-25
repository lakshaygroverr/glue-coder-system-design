# demo5_streaming.py - same question, two ways: all at once vs streaming
import json, sys, time
import requests

OLLAMA = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"
question = [{"role": "user", "content": "Explain what a server is in 5 sentences."}]

print("=== 1) NO streaming: wait for the whole answer ===")
start = time.time()
r = requests.post(OLLAMA, json={"model": MODEL, "messages": question, "stream": False})
print(f"(waited {time.time() - start:.1f} seconds staring at nothing...)")
print(r.json()["message"]["content"])

print("\n=== 2) STREAMING: tokens arrive as soon as they're ready ===")
start = time.time(); first = None
with requests.post(OLLAMA, json={"model": MODEL, "messages": question, "stream": True}, stream=True) as r:
    for line in r.iter_lines():
        if not line:
            continue
        piece = json.loads(line).get("message", {}).get("content", "")
        if piece and first is None:
            first = time.time() - start
        sys.stdout.write(piece); sys.stdout.flush()
print(f"\n\nFirst word appeared after {first:.2f} seconds. Total {time.time() - start:.1f} seconds.")
