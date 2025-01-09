#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

// Function to perform Rail Fence Encryption
void railFenceEncrypt(char *plaintext, char *ciphertext, int key)
{
    int len = strlen(plaintext);
    char rail[key][len];
    int direction_down = 0;
    int row = 0, col = 0;

    // Initialize the rail matrix with '\0'
    for (int i = 0; i < key; i++)
    {
        for (int j = 0; j < len; j++)
        {
            rail[i][j] = '\0';
        }
    }

    // Fill the rail matrix in a zigzag manner
    for (int i = 0; i < len; i++)
    {
        rail[row][col++] = plaintext[i];

        // Change direction if top or bottom rail is reached
        if (row == 0 || row == key - 1)
        {
            direction_down = !direction_down;
        }

        row += (direction_down) ? 1 : -1;
    }

    // Read the rail matrix row by row to get the ciphertext
    int k = 0;
    for (int i = 0; i < key; i++)
    {
        for (int j = 0; j < len; j++)
        {
            if (rail[i][j] != '\0')
            {
                ciphertext[k++] = rail[i][j];
            }
        }
    }
    ciphertext[k] = '\0'; // Null-terminate the ciphertext
}

int main()
{
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    char ciphertext[BUFFER_SIZE] = {0};
    int key;

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

    // Receive key from client
    read(new_socket, &key, sizeof(key));
    printf("Key received from client: %d\n", key);

    // Receive plaintext from client
    read(new_socket, buffer, BUFFER_SIZE);
    printf("Plaintext received from client: %s\n", buffer);

    // Encrypt plaintext
    railFenceEncrypt(buffer, ciphertext, key);

    // Send ciphertext back to client
    send(new_socket, ciphertext, strlen(ciphertext), 0);
    printf("Ciphertext sent to client: %s\n", ciphertext);

    close(new_socket);
    close(server_fd);

    return 0;
}
