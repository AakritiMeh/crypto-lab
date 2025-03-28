import socket

HOST = '127.0.0.1'  # Localhost (same as server)
PORT = 65432        # Same port as server

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(message.encode())

        # Receive response from the server
        hashed_response = client_socket.recv(1024).decode()
        print(f"SHA-128 Hash: {hashed_response}")

if __name__ == "__main__":
    message = input("Enter a message to hash: ")
    send_message(message)
