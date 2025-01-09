#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

// Function to perform Columnar Transposition Encryption
void columnarEncrypt(char *plaintext, char *ciphertext, int *key, int key_len)
{
    int text_len = strlen(plaintext);
    int rows = (text_len + key_len - 1) / key_len; // Calculate the number of rows
    char matrix[rows][key_len];
    int index = 0;

    // Fill the matrix row by row
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < key_len; j++)
        {
            if (index < text_len)
            {
                matrix[i][j] = plaintext[index++];
            }
            else
            {
                matrix[i][j] = 'X'; // Fill empty spaces with 'X'
            }
        }
    }

    // Read the matrix column by column according to the key
    index = 0;
    for (int k = 0; k < key_len; k++)
    {
        int col = key[k] - 1; // Convert key to zero-based column index
        for (int i = 0; i < rows; i++)
        {
            ciphertext[index++] = matrix[i][col];
        }
    }
    ciphertext[index] = '\0'; // Null-terminate the ciphertext
}

int main()
{
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    char ciphertext[BUFFER_SIZE] = {0};
    int key[BUFFER_SIZE];
    int key_len;

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind the socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for connections
    if (listen(server_fd, 3) < 0)
    {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %d...\n", PORT);

    // Accept client connection
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
    {
        perror("Accept failed");
        exit(EXIT_FAILURE);
    }

    // Receive key length
    read(new_socket, &key_len, sizeof(key_len));

    // Receive key from client
    read(new_socket, key, key_len * sizeof(int));

    // Receive plaintext from client
    read(new_socket, buffer, BUFFER_SIZE);
    printf("Plaintext received: %s\n", buffer);

    // Encrypt plaintext
    columnarEncrypt(buffer, ciphertext, key, key_len);

    // Send ciphertext back to client
    send(new_socket, ciphertext, strlen(ciphertext), 0);
    printf("Ciphertext sent: %s\n", ciphertext);

    close(new_socket);
    close(server_fd);

    return 0;
}
