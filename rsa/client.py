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


def encrypt(m, e, n):
    return power(m, e, n)


def send_data(host, port, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(str(data).encode())
    client_socket.close()


if __name__ == "__main__":
  
    e = 5
    n = 7990271 

  
    M = 1234
    print(f"Original Message: {M}")

    C = encrypt(M, e, n)
    print(f"Encrypted Message: {C}")

    send_data("127.0.0.1", 12345, C)