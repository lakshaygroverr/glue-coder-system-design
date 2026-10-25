# demo6_stateless.py - the server does NOT remember you
import requests

OLLAMA = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

def ask(messages):
    r = requests.post(OLLAMA, json={"model": MODEL, "messages": messages, "stream": False,
                                    "options": {"temperature": 0}})
    return r.json()["message"]["content"]

first = {"role": "user", "content": "Hi! My name is Kanika and my favourite colour is orange. Just say nice to meet you."}
reply = ask([first])
print("Request 1:", first["content"]); print("AI:", reply, "\n")

question = {"role": "user", "content": "What is my name and my favourite colour?"}

print("Request 2 WITHOUT history (just the new question):")
print("AI:", ask([question]), "\n")

print("Request 2 WITH history (client sends everything again):")
print("AI:", ask([first, {"role": "assistant", "content": reply}, question]))
