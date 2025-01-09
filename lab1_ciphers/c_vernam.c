#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

// Vernam cipher decryption function
void decrypt(char *ciphertext, char *key, char *plaintext)
{
    int len = strlen(ciphertext);
    for (int i = 0; i < len; i++)
    {
        plaintext[i] = ((ciphertext[i] ^ key[i]) % 26) + 'A';
    }
    plaintext[len] = '\0';
}

int main()
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    char ciphertext[BUFFER_SIZE] = {0};
    char key[BUFFER_SIZE] = {0};
    char plaintext[BUFFER_SIZE];

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

    // Receiving ciphertext and key
    int valread = read(sock, ciphertext, BUFFER_SIZE);
    ciphertext[valread] = '\0';

    valread = read(sock, key, BUFFER_SIZE);
    key[valread] = '\0';

    printf("Ciphertext received: %s\n", ciphertext);
    printf("Key received: %s\n", key);

    // Decrypt the ciphertext
    decrypt(ciphertext, key, plaintext);
    printf("Decrypted message: %s\n", plaintext);

    close(sock);
    return 0;
}
