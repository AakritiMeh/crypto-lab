// // #include <stdio.h>
// // #include <stdlib.h>
// // #include <string.h>
// // #include <arpa/inet.h>
// // #include <unistd.h>

// // #define PORT 8080
// // #define MATRIX_SIZE 2

// // // Function to calculate the modular inverse of a number modulo 26
// // int mod_inverse(int a, int mod)
// // {
// //     for (int x = 0; x < mod; x++)
// //     {
// //         if ((a * x) % mod == 1)
// //         {
// //             return x;
// //         }
// //     }
// //     return -1; // Return -1 if no modular inverse exists
// // }

// // // Function to compute the inverse of the key matrix modulo 26
// // void compute_inverse_key(int key[MATRIX_SIZE][MATRIX_SIZE], int inverse_key[MATRIX_SIZE][MATRIX_SIZE])
// // {
// //     int det = key[0][0] * key[1][1] - key[0][1] * key[1][0];
// //     det = (det % 26 + 26) % 26; // Ensure determinant is positive modulo 26
// //     int det_inv = mod_inverse(det, 26);
// //     if (det_inv == -1)
// //     {
// //         printf("Key matrix is not invertible modulo 26.\n");
// //         exit(EXIT_FAILURE);
// //     }

// //     // Compute the inverse key matrix
// //     inverse_key[0][0] = (key[1][1] * det_inv) % 26;
// //     inverse_key[0][1] = (-key[0][1] * det_inv + 26) % 26;
// //     inverse_key[1][0] = (-key[1][0] * det_inv + 26) % 26;
// //     inverse_key[1][1] = (key[0][0] * det_inv) % 26;
// // }

// // // Hill Cipher decryption function
// // void hill_cipher_decrypt(char *ciphertext, int inverse_key[MATRIX_SIZE][MATRIX_SIZE], char *plaintext)
// // {
// //     int i, j;
// //     int length = strlen(ciphertext);
// //     for (i = 0; i < length; i += MATRIX_SIZE)
// //     {
// //         for (j = 0; j < MATRIX_SIZE; j++)
// //         {
// //             int sum = 0;
// //             for (int k = 0; k < MATRIX_SIZE; k++)
// //             {
// //                 sum += inverse_key[j][k] * (ciphertext[i + k] - 'A');
// //             }
// //             plaintext[i + j] = (sum % 26 + 26) % 26 + 'A';
// //         }
// //     }
// //     plaintext[length] = '\0';
// // }

// // int main()
// // {
// //     int sock = 0;
// //     struct sockaddr_in serv_addr;
// //     char plaintext[1024] = {0};
// //     char ciphertext[1024] = {0};
// //     char decrypted[1024] = {0};

// //     // Key matrix for encryption (should match the server)
// //     int key[MATRIX_SIZE][MATRIX_SIZE] = {{9, 4}, {5, 7}};
// //     int inverse_key[MATRIX_SIZE][MATRIX_SIZE];

// //     // Compute the inverse key matrix
// //     compute_inverse_key(key, inverse_key);

// //     if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
// //     {
// //         printf("\nSocket creation error\n");
// //         return -1;
// //     }

// //     serv_addr.sin_family = AF_INET;
// //     serv_addr.sin_port = htons(PORT);

// //     if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0)
// //     {
// //         printf("\nInvalid address/ Address not supported\n");
// //         return -1;
// //     }

// //     if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
// //     {
// //         printf("\nConnection Failed\n");
// //         return -1;
// //     }

// //     printf("Enter plaintext (length must be a multiple of 2): ");
// //     scanf("%s", plaintext);

// //     send(sock, plaintext, strlen(plaintext), 0);
// //     printf("Plaintext sent: %s\n", plaintext);

// //     read(sock, ciphertext, 1024);
// //     printf("Encrypted text received: %s\n", ciphertext);

// //     // Decrypt the received ciphertext
// //     hill_cipher_decrypt(ciphertext, inverse_key, decrypted);
// //     printf("Decrypted text: %s\n", decrypted);

// //     close(sock);
// //     return 0;
// // }

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
