# Episode 3 demos: What happens when you type google.com

Everything here runs from a normal terminal. Windows has `nslookup`, `tracert` and `ping` built in.
For `dig` on Windows, use WSL, or Docker: `docker run --rm -it alpine sh -c "apk add bind-tools && sh"`.
Your numbers will differ from mine (Toronto, home Wi-Fi). That's the point: compare them in the comments.

| # | Demo | Command |
|---|---|---|
| 1a | Your computer's DNS cache | Windows: `ipconfig /displaydns` (newer Windows 11 builds need an admin terminal). Mac: there is no list command; use demo 1b |
| 1b | Cache speed-up | `python demo1_dns.py` (first lookup vs cached lookup) |
| 2 | Be the resolver: root, then .com, then Google | `dig @198.41.0.4 google.com` (a.root-servers.net) then `dig @a.gtld-servers.net google.com` then `dig @ns1.google.com google.com` |
| 3 | TTL countdown | `dig google.com +noall +answer`, wait 10 seconds, run it again. The second number went down |
| 4 | Traceroute + physics check | Windows: `tracert -d google.com`. Mac/Linux: `traceroute -n google.com` |
| 5 | Same name, different address | `dig @ns1.google.com google.com +short +subnet=81.2.69.0/24` (London). Others I used: `200.160.0.0/24` Sao Paulo, `1.128.0.0/24` Sydney, `49.36.0.0/24` Mumbai. Then `ping` each answer |
| 6 | Anycast | Open https://www.cloudflare.com/cdn-cgi/trace and find `colo=` (an airport code). Bonus: `ping 8.8.8.8` |

## Physics check
Light in fiber travels about 200,000 km per second. Round trip time can't be shorter than
`2 x distance / 200,000 km/s`. Toronto to Mountain View is about 3,600 km, so at least about 36 ms.
I measured 15 ms to google.com, so that server is not in California.

## Privacy when you share results
- `ipconfig /displaydns` lists sites you visited. Don't post the whole list.
- The first traceroute hops show your router and internet provider. Blur them.
- The cdn-cgi/trace page shows your public IP (`ip=`) and country (`loc=`). Crop those lines.

## Also in this folder (used in Episode 4)
`demo2_raw_http.py` (an HTTP request typed by hand), `demo3_timeline.py` (DNS, TCP, TLS, first byte, in ms),
`demo4_certificate.py` (read a site's certificate).
