import socket

# Import the SHA-128 function
from impl import sha128

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Received message: {message}")

                # Compute SHA-128 hash
                hashed_message = sha128(message)
                print(f"Sending hashed output: {hashed_message}")

                # Send back the hash
                conn.sendall(hashed_message.encode())

if __name__ == "__main__":
    start_server()
