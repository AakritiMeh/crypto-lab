import socket

PORT = 8080
BUFFER_SIZE = 1024

# Vernam cipher decryption function
def decrypt(ciphertext, key):
    plaintext = ''.join(chr(((ord(c) ^ ord(k)) % 26) + ord('A')) for c, k in zip(ciphertext, key))
    return plaintext

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", PORT))

# Receive full message
data = client_socket.recv(BUFFER_SIZE).decode()

# Ensure the message is correctly split into ciphertext and key
if "::" in data:
    ciphertext, key = data.split("::")
else:
    print("Error: Message format incorrect.")
    client_socket.close()
    exit(1)

print(f"Ciphertext received: {ciphertext}")
print(f"Key received: {key}")

# Decrypt the ciphertext
plaintext = decrypt(ciphertext, key)
print(f"Decrypted message: {plaintext}")

client_socket.close()
