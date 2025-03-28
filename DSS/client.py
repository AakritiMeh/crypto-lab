
import socket

def exteuclid(a, b):
    r1, r2 = a, b
    s1, s2 = 1, 0
    t1, t2 = 0, 1
    while r2 > 0:
        q = r1 // r2
        r1, r2 = r2, r1 - q * r2
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2
    if t1 < 0:
        t1 += a
    return r1, t1

# Private Key
p, q = 823, 953
n = p * q
Pn = (p - 1) * (q - 1)
e = 313
r, d = exteuclid(Pn, e)

M = int(input())
S = pow(M, d, n)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
message = f"{M},{S}"
client_socket.send(message.encode())

response = client_socket.recv(1024).decode()
print("Server Response:", response)
client_socket.close()
