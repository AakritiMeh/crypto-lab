import socket

PORT = 8080
BUFFER_SIZE = 1024

# Vigenère cipher encryption function
def encrypt(message, key):
    message = message.lower()
    key = key.lower()
    encrypted = ""

    for i in range(len(message)):
        if 'a' <= message[i] <= 'z':
            pi = ord(message[i]) - ord('a')
            ki = ord(key[i % len(key)]) - ord('a')
            encrypted += chr(((pi + ki) % 26) + ord('a'))
        else:
            encrypted += message[i]
    
    return encrypted

message = "wearediscovered"
key = "deceptive"
ciphertext = encrypt(message, key)
payload = f"{ciphertext}::{key}"

# Create socket and send message
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", PORT))
client_socket.send(payload.encode())

print(f"Sent ciphertext: {ciphertext}")
print(f"With key: {key}")

client_socket.close()
