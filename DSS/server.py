
import socket

def euclid(m, n):
    if n == 0:
        return m
    else:
        return euclid(n, m % n)

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

p, q = 823, 953
n = p * q
Pn = (p - 1) * (q - 1)
e = 313
r, d = exteuclid(Pn, e)

def verify_message(M, S):
    M1 = pow(S, e, n)
    return M == M1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
print("Server listening on port 12345...")

conn, addr = server_socket.accept()
print("Connected by", addr)

data = conn.recv(1024).decode()
M, S = map(int, data.split(','))
print(f"Received M: {M}, S: {S}")

if verify_message(M, S):
    response = "Valid Signature. Accepting the message."
else:
    response = "Invalid Signature. Rejecting the message."

conn.send(response.encode())
conn.close()
server_socket.close()

