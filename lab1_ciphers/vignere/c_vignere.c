#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

// Vigenère cipher decryption function
void decrypt(char *message, const char *key)
{
    int messageLen = strlen(message);
    int keyLen = strlen(key);
    char extendedKey[messageLen + 1];

    // Repeat the key to match the size of the ciphertext
    for (int i = 0; i < messageLen; i++)
    {
        extendedKey[i] = key[i % keyLen];
    }
    extendedKey[messageLen] = '\0';

    // Perform the Vigenère cipher decryption
    for (int i = 0; i < messageLen; i++)
    {
        if (message[i] >= 'a' && message[i] <= 'z') // Assuming lowercase letters
        {
            int ci = message[i] - 'a';
            int ki = extendedKey[i] - 'a';
            message[i] = ((ci - ki + 26) % 26) + 'a';
        }
    }
}

int main()
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE] = {0};

    // Creating socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("Socket creation error");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Converting IP address to binary
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0)
    {
        perror("Invalid address or address not supported");
        return -1;
    }

    // Connecting to server
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        perror("Connection failed");
        return -1;
    }

    // Receiving encrypted message
    int valread = read(sock, buffer, BUFFER_SIZE);
    buffer[valread] = '\0';
    printf("Encrypted message received: %s\n", buffer);

    // Decrypting message
    const char key[] = "deceptive"; // Same key used for encryption
    decrypt(buffer, key);
    printf("Decrypted message: %s\n", buffer);

    close(sock);
    return 0;
}
