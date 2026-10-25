# demo2_tiny_server.py - you are the server. Open it from your phone.
import socket
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    device = request.headers.get("User-Agent", "unknown")
    print(f"Request from {request.remote_addr}: {device[:60]}")
    return {
        "message": "Hello from the server!",
        "server_time": datetime.now().strftime("%H:%M:%S"),
        "you_are": request.remote_addr,
    }

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        s.close()
    print(f"On this computer: http://localhost:5000")
    print(f"On your phone (same Wi-Fi): http://{ip}:5000")
    app.run(host="0.0.0.0", port=5000)
