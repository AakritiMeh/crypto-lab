# import random
# import socket


# class Client:
#     def __init__(self, p, g):
#         self.p = p 
#         self.g = g  
#         self.a = random.randint(1, p)  
#         self.public_value = None  
#         self.secret_key = None  

#     def generate_public_value(self):
       
#         self.public_value = (self.g ** self.a) % self.p
#         return self.public_value

#     def compute_secret_key(self, server_public_value):
       
#         self.secret_key = (server_public_value ** self.a) % self.p
#         return self.secret_key

#     def start(self, host, port):
        
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect((host, port))
#         print(f"Connected to server (Bob) at {host}:{port}")

       
#         alice_public_value = self.generate_public_value()
#         client_socket.send(str(alice_public_value).encode())
#         print(f"Alice's public value (ga): {alice_public_value}")

        
#         bob_public_value = int(client_socket.recv(1024).decode())
#         print(f"Received Bob's public value (gb): {bob_public_value}")

        
#         secret_key = self.compute_secret_key(bob_public_value)
#         print(f"Alice's computed secret key: {secret_key}")

#         client_socket.close()


# if __name__ == "__main__":

#     p = int(input("Enter a prime number (p): "))
#     g = int(input("Enter a number (g): "))


#     client = Client(p, g)
#     client.start("127.0.0.1", 12345)
import socket

SERVER_ADDRESS = 'localhost'
PORT = 12345

def main():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((SERVER_ADDRESS, PORT))
        print("Connected to the server.")
        
        # Identify as Alice
        client_socket.send("Alice\n".encode())
        
        # Receive q and alpha from the server
        data = client_socket.recv(1024).decode()
        lines = data.strip().split('\n')
        q = int(lines[0])
        alpha = int(lines[1])
        print(f"Received q = {q} and alpha = {alpha} from server.")
        
        # Take Alice's private key from user
        Xa = int(input("Enter Alice's private key (Xa): "))
        print(f"Alice's private key (Xa): {Xa}")
        
        # Compute Alice's public key
        Ya = pow(alpha, Xa, q)  # Using pow() with 3 args for modular exponentiation
        print(f"Alice's public key (Ya): {Ya}")
        
        # Send Ya to the server
        client_socket.send(f"{Ya}\n".encode())
        
        # Receive Yd2 from the server
        Yd2 = int(client_socket.recv(1024).decode().strip())
        print(f"Received Yd2 from Eve: {Yd2}")
        
        # Compute shared key
        K = pow(Yd2, Xa, q)
        print(f"Alice computed shared key (K): {K}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
