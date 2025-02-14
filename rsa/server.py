import socket

def power(base, expo, m):
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res


def modInverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return -1


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generateKeys():
    p = 7919
    q = 1009
    
    n = p * q
    phi = (p - 1) * (q - 1)

   
    e = 0
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            break

 
    d = modInverse(e, phi)

    return e, d, n


def decrypt(c, d, n):
    return power(c, d, n)


def receive_data(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}...")

    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    conn.close()
    return int(data)


if __name__ == "__main__":

    e, d, n = generateKeys()
    print(f"Public Key (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})")


    encrypted_message = receive_data("127.0.0.1", 12345)
    print(f"Received Encrypted Message: {encrypted_message}")

 
    decrypted_message = decrypt(encrypted_message, d, n)
    print(f"Decrypted Message: {decrypted_message}")