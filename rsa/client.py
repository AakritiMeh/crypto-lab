import socket

# Function to compute power under modulo
def power(base, expo, m):
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res

# Function to encrypt the message using public key (e, n)
def encrypt(m, e, n):
    return power(m, e, n)

# Function to send data to the server
def send_data(host, port, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(str(data).encode())
    client_socket.close()

# Main execution
if __name__ == "__main__":
    # Public key (e, n) received from the server or pre-shared
    e = 65537  # Common value for e
    n = 7995071  # Example value for n (p=7919, q=1009)

    # Message to encrypt
    M = 123
    print(f"Original Message: {M}")

    # Encrypt the message
    C = encrypt(M, e, n)
    print(f"Encrypted Message: {C}")

    # Send the encrypted message to the server
    send_data("127.0.0.1", 12345, C)