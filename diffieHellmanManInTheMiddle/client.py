import random
import socket


class Client:
    def __init__(self, p, g):
        self.p = p 
        self.g = g  
        self.a = random.randint(1, p)  
        self.public_value = None  
        self.secret_key = None  

    def generate_public_value(self):
       
        self.public_value = (self.g ** self.a) % self.p
        return self.public_value

    def compute_secret_key(self, server_public_value):
       
        self.secret_key = (server_public_value ** self.a) % self.p
        return self.secret_key

    def start(self, host, port):
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to server (Bob) at {host}:{port}")

       
        alice_public_value = self.generate_public_value()
        client_socket.send(str(alice_public_value).encode())
        print(f"Alice's public value (ga): {alice_public_value}")

        
        bob_public_value = int(client_socket.recv(1024).decode())
        print(f"Received Bob's public value (gb): {bob_public_value}")

        
        secret_key = self.compute_secret_key(bob_public_value)
        print(f"Alice's computed secret key: {secret_key}")

        client_socket.close()


if __name__ == "__main__":

    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a number (g): "))


    client = Client(p, g)
    client.start("127.0.0.1", 12345)