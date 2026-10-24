# Our tiny app: one endpoint, /feed, backed by a slow fake database.
import os, sys, time
from flask import Flask, jsonify
from waitress import serve

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8000))
app = Flask(__name__)


def get_feed_from_database():
    time.sleep(0.3)  # a real database takes time to answer: 300 ms
    return [{"id": i, "user": f"user{i}", "text": f"Post number {i}"} for i in range(1, 6)]


@app.get("/feed")
def feed():
    return jsonify({"server": PORT, "from": "database", "posts": get_feed_from_database()})


if __name__ == "__main__":
    print(f"Server running on http://localhost:{PORT}/feed")
    serve(app, listen=f"localhost:{PORT}", threads=1)  # threads=1: one worker, like a McDonald's with one cashier
