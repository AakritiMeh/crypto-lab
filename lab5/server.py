import socket
from aes_implementation import AES

def start_server():
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                
                
                key_data = conn.recv(16)
                key = list(key_data)
                
                data = conn.recv(16)
                plaintext = list(data)
                
                aes = AES(key)
                
                ciphertext = aes.encrypt(plaintext)
                
              
                print("Received Plaintext:", plaintext)
                print("Encrypted Ciphertext:", ciphertext)
                
           
                conn.sendall(bytes(ciphertext))

if __name__ == "__main__":
    start_server()