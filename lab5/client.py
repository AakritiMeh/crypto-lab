import socket
from aes_implementation import AES

def start_client():
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
    
        key = bytes([
            0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 
            0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c
        ])
        
      
        s.sendall(key)
        
     
        plaintext = bytes([
            0x6b, 0xc1, 0xbe, 0xe2, 0x2e, 0x40, 0x9f, 0x96, 
            0xe9, 0x3d, 0x7e, 0x11, 0x73, 0x93, 0x17, 0x2a
        ])
        
      
        s.sendall(plaintext)
        
       
        ciphertext = s.recv(16)
        
        print("Sent Plaintext:", list(plaintext))
        print("Received Ciphertext:", list(ciphertext))

if __name__ == "__main__":
    start_client()