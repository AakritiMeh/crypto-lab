import socket
from utils import powmod, modinv, simple_hash

p = 283
q = 47  # 160-bit prime would be bigger; simplified for demo
g = 60
x = 24  # private key
k = 15 # ephemeral key, random per signature
y = powmod(g, x, p)


H = 41

r = powmod(g, k, p) % q
s = (modinv(k, q) * (H + x * r)) % q

print(f"Message: {H}")
print(f"Signature: (r={r}, s={s})")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(('localhost', 8080))
    data = f"{H}|{r}|{s}".encode()
    client_socket.sendall(data)
