import socket

# Client setup
HOST = '127.0.0.1'
PORT = 65432

plaintext = input("Enter the plaintext: ")
key = input("Enter the key: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(f"{plaintext}|{key}".encode())
    encrypted_text = client_socket.recv(1024).decode()
    print(f"Encrypted Text from Server: {encrypted_text}")
