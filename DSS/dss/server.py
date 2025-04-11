import socket
from utils import powmod, modinv, simple_hash

p = 283
q = 47  # 160-bit prime would be bigger; simplified for demo
g = 60
x=24
y = powmod(g, x, p)  # same public key

def verify_signature(M, r, s):
    H = M
    w = modinv(s, q)
    u1 = (H * w) % q
    u2 = (r * w) % q
    v = ((powmod(g, u1, p) * powmod(y, u2, p)) % p )% q
    return v == r

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Server listening on port 8080...")

    conn, addr = server_socket.accept()
    with conn:
        data = conn.recv(1024).decode()
        M, r, s = data.split('|')
        M, r, s = int(M),int(r), int(s)

        if verify_signature(M, r, s):
            print("Signature verified ✅")
        else:
            print("Signature invalid ❌")
