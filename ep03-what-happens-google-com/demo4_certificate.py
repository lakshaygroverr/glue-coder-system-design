# demo4_certificate.py - the lock icon: who says this server really is google.com?
import socket, ssl

host = "google.com"
with socket.create_connection((host, 443)) as sock:
    with ssl.create_default_context().wrap_socket(sock, server_hostname=host) as tls:
        cert = tls.getpeercert()
        print("Encryption:", tls.version(), "|", tls.cipher()[0])
subject = dict(x[0] for x in cert["subject"])
issuer = dict(x[0] for x in cert["issuer"])
print("Issued to:  ", subject.get("commonName"))
print("Issued by:  ", issuer.get("organizationName"), "-", issuer.get("commonName"))
print("Valid until:", cert["notAfter"])
names = [v for k, v in cert.get("subjectAltName", []) if k == "DNS"]
print(f"Also valid for {len(names)} names, like:", ", ".join(names[:4]))
