import socket

PORT = 8080
BUFFER_SIZE = 1024

# Vernam cipher encryption function
def encrypt(plaintext, key):
    ciphertext = ''
    for p, k in zip(plaintext, key):
        encrypted_char = ((ord(p) ^ ord(k)) % 26) + ord('A')
        ciphertext += chr(encrypted_char)
    return ciphertext

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', PORT))

    plaintext = "HAI"
    key = "SAY"

    ciphertext = encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext}")
    print(f"Key: {key}")

    # Send ciphertext
    client_socket.sendall(ciphertext.encode())
    # Small pause or separate call to ensure key is sent separately
    client_socket.sendall(key.encode())

    client_socket.close()

if __name__ == "__main__":
    main()

