# import random
# import socket


# class Server:
#     def __init__(self, p, g):
#         self.p = p  
#         self.g = g  
#         self.b = random.randint(1, p)  
#         self.public_value = None  
#         self.secret_key = None  

#     def generate_public_value(self):
      
#         self.public_value = (self.g ** self.b) % self.p
#         return self.public_value

#     def compute_secret_key(self, client_public_value):
      
#         self.secret_key = (client_public_value ** self.b) % self.p
#         return self.secret_key

#     def start(self, host, port):
    
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind((host, port))
#         server_socket.listen(1)
#         print(f"Server (Bob) listening on {host}:{port}...")

       
#         conn, addr = server_socket.accept()
#         print(f"Connected to client (Alice) at {addr}")

    
#         bob_public_value = self.generate_public_value()
#         conn.send(str(bob_public_value).encode())
#         print(f"Bob's public value (gb): {bob_public_value}")

     
#         alice_public_value = int(conn.recv(1024).decode())
#         print(f"Received Alice's public value (ga): {alice_public_value}")

      
#         secret_key = self.compute_secret_key(alice_public_value)
#         print(f"Bob's computed secret key: {secret_key}")

#         conn.close()


# if __name__ == "__main__":

#     p = int(input("Enter a prime number (p): "))
#     g = int(input("Enter a number (g): "))

   
#     server = Server(p, g)
#     server.start("127.0.0.1", 12346)
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
        
        # Identify as Bob
        client_socket.send("Bob\n".encode())
        
        # Receive q and alpha from the server
        data = client_socket.recv(1024).decode()
        lines = data.strip().split('\n')
        q = int(lines[0])
        alpha = int(lines[1])
        print(f"Received q = {q} and alpha = {alpha} from server.")
        
        # Take Bob's private key from user
        Xb = int(input("Enter Bob's private key (Xb): "))
        print(f"Bob's private key (Xb): {Xb}")
        
        # Compute Bob's public key
        Yb = pow(alpha, Xb, q)  # Using pow() with 3 args for modular exponentiation
        print(f"Bob's public key (Yb): {Yb}")
        
        # Send Yb to the server
        client_socket.send(f"{Yb}\n".encode())
        
        # Receive Yd1 from the server
        Yd1 = int(client_socket.recv(1024).decode().strip())
        print(f"Received Yd1 from Eve: {Yd1}")
        
        # Compute shared key
        K = pow(Yd1, Xb, q)
        print(f"Bob computed shared key (K): {K}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
