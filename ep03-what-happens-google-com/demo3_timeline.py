# demo3_timeline.py - every step of loading https://www.google.com, measured in milliseconds
import socket, ssl, time

host = "www.google.com"
t0 = time.perf_counter()
ip = socket.gethostbyname(host);                        t_dns = time.perf_counter()
sock = socket.create_connection((ip, 443));             t_tcp = time.perf_counter()
tls = ssl.create_default_context().wrap_socket(sock, server_hostname=host); t_tls = time.perf_counter()
tls.sendall(f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode())
first = tls.recv(1);                                    t_first = time.perf_counter()
data = first
while chunk := tls.recv(65536):
    data += chunk
t_done = time.perf_counter()
tls.close()

ms = lambda a, b: f"{(b - a) * 1000:6.1f} ms"
print(f"1. DNS lookup   (name -> {ip})  {ms(t0, t_dns)}")
print(f"2. TCP connect  (handshake)          {ms(t_dns, t_tcp)}")
print(f"3. TLS / HTTPS  (the lock)           {ms(t_tcp, t_tls)}")
print(f"4. Wait for the first byte (TTFB)    {ms(t_tls, t_first)}")
print(f"5. Download {len(data) // 1024} KB                    {ms(t_first, t_done)}")
print(f"   TOTAL                              {ms(t0, t_done)}")
