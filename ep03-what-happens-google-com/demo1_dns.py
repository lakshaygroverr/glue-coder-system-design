# demo1_dns.py - step 1: DNS turns a name into an address (the internet's phone book)
import socket, time

for name in ["google.com", "google.com", "youtube.com", "glue-coder-does-not-exist-12345.com"]:
    start = time.time()
    try:
        ip = socket.gethostbyname(name)
    except socket.gaierror:
        ip = "no such name (NXDOMAIN)"
    print(f"{name:40} -> {ip:24} {(time.time() - start) * 1000:7.1f} ms")
print("\nThe second google.com is faster: the answer was cached (saved) after the first lookup.")
