import random
import socket


class Server:
    def __init__(self, p, g):
        self.p = p  
        self.g = g  
        self.b = random.randint(1, p)  
        self.public_value = None  
        self.secret_key = None  

    def generate_public_value(self):
      
        self.public_value = (self.g ** self.b) % self.p
        return self.public_value

    def compute_secret_key(self, client_public_value):
      
        self.secret_key = (client_public_value ** self.b) % self.p
        return self.secret_key

    def start(self, host, port):
    
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server (Bob) listening on {host}:{port}...")

       
        conn, addr = server_socket.accept()
        print(f"Connected to client (Alice) at {addr}")

    
        bob_public_value = self.generate_public_value()
        conn.send(str(bob_public_value).encode())
        print(f"Bob's public value (gb): {bob_public_value}")

     
        alice_public_value = int(conn.recv(1024).decode())
        print(f"Received Alice's public value (ga): {alice_public_value}")

      
        secret_key = self.compute_secret_key(alice_public_value)
        print(f"Bob's computed secret key: {secret_key}")

        conn.close()


if __name__ == "__main__":

    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a number (g): "))

   
    server = Server(p, g)
    server.start("127.0.0.1", 12345)