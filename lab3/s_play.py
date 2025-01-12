import socket
import numpy as np

def to_lower_case(text):
    return text.lower()

def remove_spaces(text):
    return text.replace(" ", "")

def generate_key_table(key):
    key = remove_spaces(to_lower_case(key))
    key = key.replace('j', 'i')
    key = ''.join(dict.fromkeys(key))  # Remove duplicate letters

    alphabet = "abcdefghiklmnopqrstuvwxyz"  # 'j' is excluded
    key_table = [c for c in key if c in alphabet]

    for char in alphabet:
        if char not in key_table:
            key_table.append(char)

    key_table = np.array(key_table).reshape(5, 5)
    return key_table

def find_positions(char1, char2, key_table):
    row1, col1 = np.where(key_table == char1)
    row2, col2 = np.where(key_table == char2)
    return row1[0], col1[0], row2[0], col2[0]

def encrypt_playfair(plaintext, key_table):
    plaintext = remove_spaces(to_lower_case(plaintext)).replace('j', 'i')
    
    # Make plaintext length even by padding with 'x' if needed
    if len(plaintext) % 2 != 0:
        plaintext += 'x'

    # Split plaintext into pairs of characters
    pairs = []
    i = 0
    while i < len(plaintext):
        char1 = plaintext[i]
        char2 = plaintext[i + 1] if i + 1 < len(plaintext) else 'x'
        if char1 == char2:
            pairs.append((char1, 'x'))
            i += 1
        else:
            pairs.append((char1, char2))
            i += 2

    # Encrypt each pair
    encrypted_text = ""
    for char1, char2 in pairs:
        row1, col1, row2, col2 = find_positions(char1, char2, key_table)
        if row1 == row2:  # Same row
            encrypted_text += key_table[row1][(col1 + 1) % 5]
            encrypted_text += key_table[row2][(col2 + 1) % 5]
        elif col1 == col2:  # Same column
            encrypted_text += key_table[(row1 + 1) % 5][col1]
            encrypted_text += key_table[(row2 + 1) % 5][col2]
        else:  # Rectangle
            encrypted_text += key_table[row1][col2]
            encrypted_text += key_table[row2][col1]

    return encrypted_text

# Server setup
HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    
    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode()
            if data:
                plaintext, key = data.split('|')
                key_table = generate_key_table(key)
                encrypted_text = encrypt_playfair(plaintext, key_table)
                conn.sendall(encrypted_text.encode())
