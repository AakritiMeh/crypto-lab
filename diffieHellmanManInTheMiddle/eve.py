# import socket
# import random

# HOST = '127.0.0.1'
# PORT_ALICE = 12345  # Alice connects to this
# PORT_BOB = 12346    # Eve connects to Bob

# class MITM:
#     def __init__(self, p, g):
#         self.p = p
#         self.g = g

#         # Eve's secret key for both connections
#         self.ae = random.randint(1, p - 2)  # For Alice
#         self.be = random.randint(1, p - 2)  # For Bob

#     def powmod(self, base, exp, mod):
#         result = 1
#         base %= mod
#         while exp > 0:
#             if exp % 2 == 1:
#                 result = (result * base) % mod
#             base = (base * base) % mod
#             exp //= 2
#         return result

#     def start(self):
#         # Step 1: Accept connection from Alice
#         alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         alice_socket.bind((HOST, PORT_ALICE))
#         alice_socket.listen(1)
#         print(f"[+] Waiting for Alice on {HOST}:{PORT_ALICE}...")
#         conn_alice, addr_alice = alice_socket.accept()
#         print(f"[+] Connected to Alice at {addr_alice}")

#         # Step 2: Receive Alice's public value
#         ga = int(conn_alice.recv(1024).decode())
#         print(f"[>] Received Alice's public value ga: {ga}")

#         # Step 3: Connect to Bob
#         bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         bob_socket.connect((HOST, PORT_BOB))
#         print(f"[+] Connected to Bob on {HOST}:{PORT_BOB}")

#         # Step 4: Send fake ga to Bob (Eve generates ge_b)
#         ge_b = self.powmod(self.g, self.be, self.p)
#         bob_socket.send(str(ge_b).encode())
#         print(f"[<] Sent fake public value to Bob (ge_b): {ge_b}")

#         # Step 5: Receive Bob's real public value
#         gb = int(bob_socket.recv(1024).decode())
#         print(f"[<] Received Bob's public value gb: {gb}")

#         # Step 6: Send fake gb to Alice (Eve generates ge_a)
#         ge_a = self.powmod(self.g, self.ae, self.p)
#         conn_alice.send(str(ge_a).encode())
#         print(f"[<] Sent fake public value to Alice (ge_a): {ge_a}")

#         # Step 7: Eve computes secret keys with both
#         secret_with_alice = self.powmod(ga, self.ae, self.p)
#         secret_with_bob = self.powmod(gb, self.be, self.p)
#         print(f"[!] Eve's secret with Alice: {secret_with_alice}")
#         print(f"[!] Eve's secret with Bob: {secret_with_bob}")

#         # Cleanup
#         conn_alice.close()
#         alice_socket.close()
#         bob_socket.close()

# if __name__ == "__main__":
#     p = int(input("Enter a prime number (p): "))
#     g = int(input("Enter a generator (g): "))

#     mitm = MITM(p, g)
#     mitm.start()
import socket
import threading
import math

PORT = 12345
HOST = '0.0.0.0'  # Listen on all available interfaces

def handle_client(client_socket, q, alpha, Yd1, Yd2, Xd1, Xd2):
    try:
        # Read the client's name
        client_name = client_socket.recv(1024).decode().strip()
        print(f"{client_name} has connected.")

        # Send q and alpha to the client
        client_socket.send(f"{q}\n{alpha}\n".encode())

        # Read the public key from the client
        public_key = int(client_socket.recv(1024).decode().strip())
        print(f"Received public key from {client_name}: {public_key}")

        if client_name == "Alice":
            # Send Yd2 to Alice
            client_socket.send(f"{Yd2}\n".encode())
            print(f"Sent Yd2 to Alice: {Yd2}")

            # Compute K2 = Ya^Xd2 mod q (Eve's shared key with Alice)
            K2 = pow(public_key, Xd2, q)  # Using pow() with 3 args for modular exponentiation
            print(f"Eve computed shared key with Alice (K2): {K2}")
        
        elif client_name == "Bob":
            # Send Yd1 to Bob
            client_socket.send(f"{Yd1}\n".encode())
            print(f"Sent Yd1 to Bob: {Yd1}")

            # Compute K1 = Yb^Xd1 mod q (Eve's shared key with Bob)
            K1 = pow(public_key, Xd1, q)  # Using pow() with 3 args for modular exponentiation
            print(f"Eve computed shared key with Bob (K1): {K1}")
    
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Eve (Server) is listening on port {PORT}")
    
    # Take q and alpha from Eve
    q = int(input("Enter prime number (q): "))
    alpha = int(input("Enter primitive root (alpha): "))
    
    # Take Eve's private keys
    Xd1 = int(input("Enter Eve's private key for Alice (Xd1): "))
    Xd2 = int(input("Enter Eve's private key for Bob (Xd2): "))
    
    # Compute Eve's public keys
    Yd1 = pow(alpha, Xd1, q)
    Yd2 = pow(alpha, Xd2, q)
    print(f"Eve's public key for Alice (Yd1): {Yd1}")
    print(f"Eve's public key for Bob (Yd2): {Yd2}")
    
    try:
        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            print(f"New client connected from {client_address}")
            
            # Handle client request in a new thread
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, q, alpha, Yd1, Yd2, Xd1, Xd2)
            )
            client_thread.daemon = True
            client_thread.start()
    
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()

