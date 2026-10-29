# Episode 4 demos: HTTP vs HTTPS (what the lock icon means)

Python 3 only, no extra packages. Docker is used for the sniffer so it only ever sees its own container's traffic.
On Windows PowerShell, type `curl.exe` (plain `curl` is an alias for something else).

| # | Demo | Command |
|---|---|---|
| 1 | An HTTP request is just text | `python demo1_raw_http.py` (sends GET / to example.com on port 80 and prints the answer) |
| 2 | Watch your browser speak HTTP | Guest window, F12, Network tab, load http://example.com, click the first row. Bonus: `curl -I http://github.com` (301 to https) |
| 3 | Be the snooper | see below |
| 4 | The TLS handshake | `docker run --rm alpine sh -c "apk add -q curl && curl -sv -o /dev/null https://www.google.com"` then `python demo4_timeline.py` |
| 5 | The certificate | `python demo5_certificate.py` then `python demo5_certificate.py wrong.host.badssl.com` (hostname mismatch error). In the browser: https://wrong.host.badssl.com/ |

## Demo 3: sniff plain HTTP vs HTTPS (inside a container only)
```
docker run --rm --cap-add NET_RAW --cap-add NET_ADMIN alpine sh -c "apk add -q tcpdump curl && (tcpdump -i eth0 -n -A -s0 'tcp port 80' &) && sleep 2 && curl -s http://example.com >/dev/null && sleep 2"
docker run --rm --cap-add NET_RAW --cap-add NET_ADMIN alpine sh -c "apk add -q tcpdump curl && (tcpdump -i eth0 -n -A -s0 'tcp port 443' &) && sleep 2 && curl -s https://example.com >/dev/null && sleep 2"
```
Port 80: the GET line, Host header, status line and HTML are readable. Port 443: gibberish, except the site name
in the very first message (SNI), which is why your provider can still see which site you visited.

## Pro mode
`curl -sI https://github.com | grep -i strict-transport-security` (HSTS) · https://crt.sh (Certificate Transparency logs)

## Privacy
Use a guest browser window: request headers on a logged-in site include your cookies. Never sniff your real Wi-Fi.
