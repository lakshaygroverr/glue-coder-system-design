# Episode 1: Build a server, crash it, then fix it like Netflix

You build a tiny app, crash it with 100 fake users, then fix it three ways: a bigger server, a cache, and a load balancer.

## Setup (once)

```
pip install flask waitress locust aiohttp
```

(or `pip install -r requirements.txt`). On Mac/Linux you may need `python3` instead of `python`.

## 1. Run the server

```
python server.py
```

Open http://localhost:8000/feed. It takes a moment: that's the 300 ms fake database.

## 2. Crash it with 100 users

Keep the server running. In a second terminal:

```
locust -f locustfile.py --host http://localhost:8000
```

Open http://localhost:8089, set **100 users**, ramp up **20 per second**, press **Start**. Watch the response time climb and the failures go red.

## 3. Fix 1: a bigger server (vertical scaling)

In `server.py`, change `threads=1` to `threads=10`, restart the server, and run the same test. Better, but still slow.

## 4. Fix 2: a cache

Stop the old server and run:

```
python server_cached.py
```

Refresh http://localhost:8000/feed: the `"from"` field goes from `"database"` to `"cache"`. Run the 100-user test again.

## 5. Fix 3: more servers + a load balancer (horizontal scaling)

Stop the old server. Start three servers and the load balancer, each in its own terminal:

```
python server_cached.py 8001
python server_cached.py 8002
python server_cached.py 8003
python load_balancer.py
```

Refresh http://localhost:8000/feed and watch `"server"` go 8001, 8002, 8003, 8001... Run the 100-user test again.

Now kill server 8002 (Ctrl+C in its terminal). Refresh: still working. The load balancer prints `server 8002 is down, skipping`.

## Homework

1. Change `CACHE_SECONDS` from 10 to 1 in `server_cached.py` and run the test again. What happens to the speed?
2. Try 500 users instead of 100. Which setup survives?
3. Kill two servers instead of one. Does the app still work?

Tell me your results in the comments.

## Measured on my machine

See [results.md](results.md). To re-run every test yourself: `python results/run_benchmarks.py`.
