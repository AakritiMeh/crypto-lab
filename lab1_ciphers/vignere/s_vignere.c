#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024
#define SHIFT 5 // Shift value (k)

// Vigenère cipher encryption function
void encrypt(char *message, const char *key)
{
    int messageLen = strlen(message);
    int keyLen = strlen(key);
    char extendedKey[messageLen + 1];

    // Repeat the key to match the size of the plaintext
    for (int i = 0; i < messageLen; i++)
    {
        extendedKey[i] = key[i % keyLen];
    }
    extendedKey[messageLen] = '\0';

    // Perform the Vigenère cipher encryption
    for (int i = 0; i < messageLen; i++)
    {
        if (message[i] >= 'a' && message[i] <= 'z') // Assuming lowercase letters
        {
            int pi = message[i] - 'a';
            int ki = extendedKey[i] - 'a';
            message[i] = ((pi + ki) % 26) + 'a';
        }
    }
}

int main()
{
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8080
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)))
    {
        perror("Setsockopt failed");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Binding socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listening for connections
    if (listen(server_fd, 3) < 0)
    {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %d\n", PORT);

    // Accepting connection
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
    {
        perror("Accept failed");
        exit(EXIT_FAILURE);
    }

    // Encrypt and send a message
    char message[] = "wearediscovered";
    const char key[] = "deceptive";
    printf("Original message: %s\n", message);
    encrypt(message, key); // Encrypt the message using Vigenère cipher
    send(new_socket, message, strlen(message), 0);
    printf("Encrypted message sent: %s\n", message);

    close(new_socket);
    close(server_fd);
    return 0;
}
