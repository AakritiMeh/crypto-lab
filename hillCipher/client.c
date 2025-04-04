

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024
#define MATRIX_SIZE 2

// Matrix multiplication for decryption
void matrix_multiply(int ciphertext[MATRIX_SIZE][MATRIX_SIZE], int key_inverse[MATRIX_SIZE][MATRIX_SIZE], int plaintext[MATRIX_SIZE][MATRIX_SIZE])
{
    for (int i = 0; i < MATRIX_SIZE; i++)
    {
        for (int j = 0; j < MATRIX_SIZE; j++)
        {
            plaintext[i][j] = 0;
            for (int k = 0; k < MATRIX_SIZE; k++)
            {
                plaintext[i][j] += ciphertext[i][k] * key_inverse[k][j];
            }
            plaintext[i][j] = (plaintext[i][j] % 26 + 26) % 26; // Modulo 26 to handle negatives
        }
    }
}

// Convert text to a matrix representation
void text_to_matrix(char *text, int matrix[MATRIX_SIZE][MATRIX_SIZE])
{
    for (int i = 0; i < MATRIX_SIZE; i++)
    {
        for (int j = 0; j < MATRIX_SIZE; j++)
        {
            matrix[i][j] = text[i * MATRIX_SIZE + j] - 'A';
        }
    }
}

// Convert matrix to text representation
void matrix_to_text(int matrix[MATRIX_SIZE][MATRIX_SIZE], char *text)
{
    for (int i = 0; i < MATRIX_SIZE; i++)
    {
        for (int j = 0; j < MATRIX_SIZE; j++)
        {
            text[i * MATRIX_SIZE + j] = matrix[i][j] + 'A';
        }
    }
    text[MATRIX_SIZE * MATRIX_SIZE] = '\0';
}

int main()
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    char ciphertext[BUFFER_SIZE];
    char plaintext[BUFFER_SIZE];

    // Predefined inverse key matrix
    int key_inverse[MATRIX_SIZE][MATRIX_SIZE] = {{5, 12}, {15, 25}};

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

    // Receiving ciphertext
    int valread = read(sock, ciphertext, BUFFER_SIZE);
    ciphertext[valread] = '\0';
    printf("Ciphertext received: %s\n", ciphertext);

    // Decrypt ciphertext using Hill cipher
    int ciphertext_matrix[MATRIX_SIZE][MATRIX_SIZE];
    int plaintext_matrix[MATRIX_SIZE][MATRIX_SIZE];

    text_to_matrix(ciphertext, ciphertext_matrix);
    matrix_multiply(ciphertext_matrix, key_inverse, plaintext_matrix);
    matrix_to_text(plaintext_matrix, plaintext);

    printf("Decrypted message: %s\n", plaintext);

    close(sock);
    return 0;
}
