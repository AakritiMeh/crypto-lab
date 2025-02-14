import socket
import codecs

MOD = 256

def KSA(key):
    key_length = len(key)
    S = list(range(MOD))
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % MOD]
        yield K

def get_keystream(key):
    S = KSA(key)
    return PRGA(S)

def encrypt_logic(key, text):
    key = [ord(c) for c in key]
    keystream = get_keystream(key)
    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))
        res.append(val)
    return ''.join(res)

def encrypt(key, plaintext):
    plaintext = [ord(c) for c in plaintext]
    return encrypt_logic(key, plaintext)

def decrypt(key, ciphertext):
    ciphertext = codecs.decode(ciphertext, 'hex_codec')
    res = encrypt_logic(key, ciphertext)
    return codecs.decode(res, 'hex_codec').decode('utf-8')

def send_encrypted_message(message, host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        key = 'not-so-random-key'
        encrypted_message = encrypt(key, message)
        print(f"Sending encrypted message: {encrypted_message}")
        s.sendall(encrypted_message.encode('utf-8'))
        data = s.recv(1024)
        print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    send_encrypted_message("Hello, this is a secret message!")