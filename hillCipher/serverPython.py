# server.py
import socket
import numpy as np

PORT = 8080
BUFFER_SIZE = 1024
MATRIX_SIZE = 2

# Hill cipher key matrix (encryption)
key = np.array([[9, 4], [5, 7]])

def text_to_matrix(text):
    matrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            matrix[i][j] = ord(text[i * MATRIX_SIZE + j]) - ord('A')
    return matrix

def matrix_multiply(plaintext, key):
    result = np.dot(plaintext, key) % 26
    return result

def matrix_to_text(matrix):
    text = ''
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            text += chr(int(matrix[i][j]) + ord('A'))
    return text

# Start TCP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(1)
print(f"Server is listening on port {PORT}")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

plaintext = "MEET"
plaintext_matrix = text_to_matrix(plaintext)
ciphertext_matrix = matrix_multiply(plaintext_matrix, key)
ciphertext = matrix_to_text(ciphertext_matrix)

print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)

client_socket.send(ciphertext.encode())
print("Ciphertext sent to client.")

client_socket.close()
server_socket.close()
