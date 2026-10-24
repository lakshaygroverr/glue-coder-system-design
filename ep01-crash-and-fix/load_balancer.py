# A tiny load balancer: sends each request to the next server in turn (round robin)
# and skips any server that doesn't answer.
import itertools
import aiohttp
from aiohttp import web

SERVERS = ["http://localhost:8001", "http://localhost:8002", "http://localhost:8003"]
next_server = itertools.cycle(SERVERS)


async def handle(request):
    for _ in SERVERS:  # try each server at most once
        server = next(next_server)
        try:
            async with request.app["http"].get(server + request.path_qs, timeout=aiohttp.ClientTimeout(total=1)) as r:
                return web.Response(body=await r.read(), status=r.status, content_type=r.content_type)
        except (aiohttp.ClientError, TimeoutError):
            print(f"server {server.rsplit(':', 1)[1]} is down, skipping", flush=True)
    return web.Response(status=503, text="All servers are down")


async def start(app):
    app["http"] = aiohttp.ClientSession()


async def stop(app):
    await app["http"].close()


app = web.Application()
app.router.add_get("/{path:.*}", handle)
app.on_startup.append(start)
app.on_cleanup.append(stop)

if __name__ == "__main__":
    print("Load balancer running on http://localhost:8000/feed")
    web.run_app(app, port=8000, print=None)
