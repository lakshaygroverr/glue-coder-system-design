# Same app, plus a cache: keep the feed in memory for 10 seconds.
import os, sys, time
from flask import Flask, jsonify
from waitress import serve

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8000))
CACHE_SECONDS = 10
app = Flask(__name__)
cache = {"feed": None, "saved_at": 0}


def get_feed_from_database():
    time.sleep(0.3)  # a real database takes time to answer: 300 ms
    return [{"id": i, "user": f"user{i}", "text": f"Post number {i}"} for i in range(1, 6)]


@app.get("/feed")
def feed():
    # still fresh? hand out the saved copy, no database trip
    if cache["feed"] and time.time() - cache["saved_at"] < CACHE_SECONDS:
        return jsonify({"server": PORT, "from": "cache", "posts": cache["feed"]})
    cache["feed"], cache["saved_at"] = get_feed_from_database(), time.time()
    return jsonify({"server": PORT, "from": "database", "posts": cache["feed"]})


if __name__ == "__main__":
    print(f"Cached server running on http://localhost:{PORT}/feed")
    serve(app, listen=f"localhost:{PORT}", threads=1)  # still just one cashier
