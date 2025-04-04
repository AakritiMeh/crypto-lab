import socket

PORT = 8080
BUFFER_SIZE = 1024

# Vernam cipher encryption function
def encrypt(plaintext, key):
    ciphertext = ""  # Initialize an empty string for ciphertext

    for p, k in zip(plaintext, key):  # Iterate through each character pair in plaintext and key
        p_ascii = ord(p)  # Convert plaintext character to ASCII
        k_ascii = ord(k)  # Convert key character to ASCII

        # XOR operation between plaintext and key character
        xor_result = p_ascii ^ k_ascii

        # Modulo 26 to keep within the English alphabet range
        mod_result = xor_result % 26

        # Convert back to a printable character (A-Z)
        cipher_char = chr(mod_result + ord('A'))

        # Append encrypted character to ciphertext
        ciphertext += cipher_char
    return ciphertext

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(3)

print(f"Server is listening on port {PORT}")

client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Prepare plaintext and key
plaintext = "HAI"
key = "SAY"

# Encrypt plaintext
ciphertext = encrypt(plaintext, key)
print(f"Plaintext: {plaintext}")
print(f"Key: {key}")
print(f"Ciphertext: {ciphertext}")

# Send ciphertext and key as a single message separated by "::"
message = f"{ciphertext}::{key}"
client_socket.sendall(message.encode())

print("Encrypted message and key sent to client.")

client_socket.close()
server_socket.close()
