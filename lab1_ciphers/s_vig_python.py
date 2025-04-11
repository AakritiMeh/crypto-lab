import socket

PORT = 8080
BUFFER_SIZE = 1024

# Vigenère cipher decryption function
def decrypt(message, key):
    message = message.lower()
    key = key.lower()
    decrypted = ""

    for i in range(len(message)):
        if 'a' <= message[i] <= 'z':
            ci = ord(message[i]) - ord('a')
            ki = ord(key[i % len(key)]) - ord('a')
            decrypted += chr(((ci - ki + 26) % 26) + ord('a'))
        else:
            decrypted += message[i]
    
    return decrypted

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(1)

print(f"Server listening on port {PORT}...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Receive data
data = conn.recv(BUFFER_SIZE).decode()
if "::" in data:
    ciphertext, key = data.split("::")
    print(f"Received ciphertext: {ciphertext}")
    print(f"Key: {key}")

    plaintext = decrypt(ciphertext, key)
    print(f"Decrypted message: {plaintext}")
else:
    print("Error: Invalid message format.")

conn.close()
server_socket.close()

