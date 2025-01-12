import socket

def encrypt_rail_fence(text, rails):
    rail = [['\n' for _ in range(len(text))] for _ in range(rails)]
    dir_down = False
    row, col = 0, 0

    for i in range(len(text)):
        if (row == 0) or (row == rails - 1):
            dir_down = not dir_down
        rail[row][col] = text[i]
        col += 1
        row += 1 if dir_down else -1

    result = []
    for i in range(rails):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)

# Server setup
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(1024).decode()
        if data:
            plaintext, rails = data.split('|')
            rails = int(rails)
            encrypted_text = encrypt_rail_fence(plaintext, rails)
            conn.sendall(encrypted_text.encode())
