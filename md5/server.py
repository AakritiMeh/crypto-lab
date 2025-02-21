import socket
import struct
from math import floor, sin
from bitarray import bitarray

# MD5 Constants
MD5_BUFFER = {
    'A': 0x67452301,
    'B': 0xEFCDAB89,
    'C': 0x98BADCFE,
    'D': 0x10325476,
}

# MD5 Functions
def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

def rotate_left(x, n):
    return (x << n) | (x >> (32 - n))

def modular_add(a, b):
    return (a + b) % pow(2, 32)

def md5_hash(message):
    # Step 1: Pad the message
    bit_array = bitarray(endian="big")
    bit_array.frombytes(message.encode("utf-8"))
    bit_array.append(1)
    while len(bit_array) % 512 != 448:
        bit_array.append(0)

    # Step 2: Append the length
    length = (len(message) * 8) % pow(2, 64)
    length_bit_array = bitarray(endian="little")
    length_bit_array.frombytes(struct.pack("<Q", length))
    bit_array.extend(length_bit_array)

    # Step 3: Initialize buffers
    buffers = MD5_BUFFER.copy()

    # Step 4: Process chunks
    T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]
    N = len(bit_array) // 32

    for chunk_index in range(N // 16):
        start = chunk_index * 512
        X = [bit_array[start + (x * 32): start + (x * 32) + 32] for x in range(16)]
        X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]

        A, B, C, D = buffers['A'], buffers['B'], buffers['C'], buffers['D']

        for i in range(64):
            if 0 <= i <= 15:
                k = i
                s = [7, 12, 17, 22]
                temp = F(B, C, D)
            elif 16 <= i <= 31:
                k = ((5 * i) + 1) % 16
                s = [5, 9, 14, 20]
                temp = G(B, C, D)
            elif 32 <= i <= 47:
                k = ((3 * i) + 5) % 16
                s = [4, 11, 16, 23]
                temp = H(B, C, D)
            elif 48 <= i <= 63:
                k = (7 * i) % 16
                s = [6, 10, 15, 21]
                temp = I(B, C, D)

            temp = modular_add(temp, X[k])
            temp = modular_add(temp, T[i])
            temp = modular_add(temp, A)
            temp = rotate_left(temp, s[i % 4])
            temp = modular_add(temp, B)

            A, B, C, D = D, temp, B, C

        buffers['A'] = modular_add(buffers['A'], A)
        buffers['B'] = modular_add(buffers['B'], B)
        buffers['C'] = modular_add(buffers['C'], C)
        buffers['D'] = modular_add(buffers['D'], D)

    # Step 5: Output the hash
    A = struct.unpack("<I", struct.pack(">I", buffers['A']))[0]
    B = struct.unpack("<I", struct.pack(">I", buffers['B']))[0]
    C = struct.unpack("<I", struct.pack(">I", buffers['C']))[0]
    D = struct.unpack("<I", struct.pack(">I", buffers['D']))[0]

    return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"

# Server Setup
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Server is listening on port 12345...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established.")
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received message: {message}")

        hashed_message = md5_hash(message)
        print(f"Hashed message: {hashed_message}")

        client_socket.send(hashed_message.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_server()