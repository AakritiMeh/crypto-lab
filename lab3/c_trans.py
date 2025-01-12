import socket

def decrypt_rail_fence(cipher, rails):
    rail = [['\n' for _ in range(len(cipher))] for _ in range(rails)]
    dir_down = None
    row, col = 0, 0

    for i in range(len(cipher)):
        if (row == 0) or (row == rails - 1):
            dir_down = not dir_down
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    index = 0
    for i in range(rails):
        for j in range(len(cipher)):
            if (rail[i][j] == '*') and (index < len(cipher)):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if (row == 0):
            dir_down = True
        if (row == rails - 1):
            dir_down = False
        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1

    return "".join(result)

# Client setup
HOST = '127.0.0.1'  # Server's hostname or IP address
PORT = 65432        # Port used by the server

plaintext = "HELLO I AM WORKING WELL"
rails = 3

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(f"{plaintext}|{rails}".encode())
    encrypted_text = client_socket.recv(1024).decode()
    print(f"Encrypted Text from Server: {encrypted_text}")

    # Decrypt the encrypted text locally
    decrypted_text = decrypt_rail_fence(encrypted_text, rails)
    print(f"Decrypted Text: {decrypted_text}")
