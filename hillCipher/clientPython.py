# client.py
import socket
import numpy as np

PORT = 8080
BUFFER_SIZE = 1024
MATRIX_SIZE = 2

# Predefined inverse of the key matrix (mod 26)
key_inverse = np.array([[5, 12], [15, 25]])

def text_to_matrix(text):
    matrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            matrix[i][j] = ord(text[i * MATRIX_SIZE + j]) - ord('A')
    return matrix

def matrix_multiply(ciphertext, key_inv):
    result = np.dot(ciphertext, key_inv) % 26
    result = (result + 26) % 26  # to handle any negatives
    return result

def matrix_to_text(matrix):
    text = ''
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            text += chr(int(matrix[i][j]) + ord('A'))
    return text

# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', PORT))

ciphertext = client_socket.recv(BUFFER_SIZE).decode()
print("Ciphertext received:", ciphertext)

ciphertext_matrix = text_to_matrix(ciphertext)
plaintext_matrix = matrix_multiply(ciphertext_matrix, key_inverse)
plaintext = matrix_to_text(plaintext_matrix)

print("Decrypted message:", plaintext)

client_socket.close()
