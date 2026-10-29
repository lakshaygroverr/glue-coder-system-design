# demo1_raw_http.py - an HTTP request is just text. Send one by hand over a plain socket.
import socket

host = "example.com"
request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
print("WHAT WE SEND:\n" + request)

s = socket.create_connection((host, 80))   # port 80 = plain HTTP (no lock)
s.sendall(request.encode())
response = b""
while chunk := s.recv(4096):
    response += chunk
s.close()

head, _, body = response.decode(errors="replace").partition("\r\n\r\n")
print("WHAT COMES BACK (headers):\n" + head)
print(f"\n...then {len(body)} characters of HTML. First line of the page:")
print(body.strip().splitlines()[0])
