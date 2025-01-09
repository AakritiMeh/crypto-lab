#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

char keyMatrix[5][5];

// Function to remove duplicates and generate the key matrix
void generateKeyMatrix(char *key)
{
    int alphabet[26] = {0};
    int k = 0;

    for (int i = 0; key[i] != '\0'; i++)
    {
        if (key[i] == 'J')
            key[i] = 'I';
        if (!alphabet[key[i] - 'A'])
        {
            keyMatrix[k / 5][k % 5] = key[i];
            alphabet[key[i] - 'A'] = 1;
            k++;
        }
    }

    for (char c = 'A'; c <= 'Z'; c++)
    {
        if (c == 'J')
            continue;
        if (!alphabet[c - 'A'])
        {
            keyMatrix[k / 5][k % 5] = c;
            alphabet[c - 'A'] = 1;
            k++;
        }
    }
}

// Function to find position of a character in the key matrix
void findPosition(char ch, int *row, int *col)
{
    if (ch == 'J')
        ch = 'I';
    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            if (keyMatrix[i][j] == ch)
            {
                *row = i;
                *col = j;
                return;
            }
        }
    }
}

// Function to encrypt the plaintext
void encrypt(char *plaintext, char *ciphertext)
{
    int len = strlen(plaintext);
    char preparedText[BUFFER_SIZE] = {0};
    int k = 0;

    // Prepare plaintext
    for (int i = 0; i < len; i++)
    {
        if (plaintext[i] == ' ')
            continue;
        if (k > 0 && plaintext[i] == preparedText[k - 1])
        {
            preparedText[k++] = 'X';
        }
        preparedText[k++] = plaintext[i];
    }
    if (k % 2 != 0)
        preparedText[k++] = 'X';

    // Encrypt using Playfair cipher
    for (int i = 0; i < k; i += 2)
    {
        int r1, c1, r2, c2;
        findPosition(preparedText[i], &r1, &c1);
        findPosition(preparedText[i + 1], &r2, &c2);

        if (r1 == r2)
        {
            ciphertext[i] = keyMatrix[r1][(c1 + 1) % 5];
            ciphertext[i + 1] = keyMatrix[r2][(c2 + 1) % 5];
        }
        else if (c1 == c2)
        {
            ciphertext[i] = keyMatrix[(r1 + 1) % 5][c1];
            ciphertext[i + 1] = keyMatrix[(r2 + 1) % 5][c2];
        }
        else
        {
            ciphertext[i] = keyMatrix[r1][c2];
            ciphertext[i + 1] = keyMatrix[r2][c1];
        }
    }
    ciphertext[k] = '\0';
}

// Server main function
int main()
{
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    char ciphertext[BUFFER_SIZE] = {0};

    // Key for the Playfair cipher
    char key[] = "MONARCHY";

    // Generate key matrix
    generateKeyMatrix(key);

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

    // Read plaintext from client
    read(new_socket, buffer, BUFFER_SIZE);
    printf("Received plaintext: %s\n", buffer);

    // Encrypt the plaintext
    encrypt(buffer, ciphertext);
    printf("Encrypted ciphertext: %s\n", ciphertext);

    // Send ciphertext to client
    send(new_socket, ciphertext, strlen(ciphertext), 0);
    printf("Ciphertext sent to client.\n");

    close(new_socket);
    close(server_fd);

    return 0;
}
