import socket

PORT = 8080
BUFFER_SIZE = 1024

# Vernam cipher decryption function
def decrypt(ciphertext, key):
    plaintext = ''
    for c, k in zip(ciphertext, key):
        decrypted_char = ((ord(c) ^ ord(k)) % 26) + ord('A')
        plaintext += chr(decrypted_char)
    return plaintext

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(1)

    print(f"Server is listening on port {PORT}")
    client_socket, address = server_socket.accept()

    data = client_socket.recv(BUFFER_SIZE).decode()
    ciphertext = data[:3]  # You can modify this if using dynamic length
    key = data[3:]

    print(f"Ciphertext received: {ciphertext}")
    print(f"Key received: {key}")

    plaintext = decrypt(ciphertext, key)
    print(f"Decrypted message: {plaintext}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()

