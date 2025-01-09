#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

// Vernam cipher encryption function
void encrypt(char *plaintext, char *key, char *ciphertext)
{
    int len = strlen(plaintext);
    for (int i = 0; i < len; i++)
    {
        ciphertext[i] = ((plaintext[i] ^ key[i]) % 26) + 'A';
    }
    ciphertext[len] = '\0';
}

int main()
{
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

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

    // Prepare plaintext and key
    char plaintext[] = "HAI";
    char key[] = "SAY"; // Key must have the same size as plaintext
    char ciphertext[BUFFER_SIZE];

    // Encrypt the plaintext
    encrypt(plaintext, key, ciphertext);
    printf("Plaintext: %s\n", plaintext);
    printf("Key: %s\n", key);
    printf("Ciphertext: %s\n", ciphertext);

    // Send the ciphertext and key to the client
    send(new_socket, ciphertext, strlen(ciphertext), 0);
    send(new_socket, key, strlen(key), 0);

    printf("Encrypted message and key sent to client.\n");

    close(new_socket);
    close(server_fd);
    return 0;
}
