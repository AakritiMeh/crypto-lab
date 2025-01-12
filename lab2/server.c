// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>
// #include <arpa/inet.h>
// #include <unistd.h>

// #define PORT 8080
// #define MATRIX_SIZE 2 // 2x2 key matrix for simplicity

// // Hill Cipher encryption function
// void hill_cipher_encrypt(char *plaintext, int key[MATRIX_SIZE][MATRIX_SIZE], char *ciphertext)
// {
//     int i, j;
//     int length = strlen(plaintext);
//     for (i = 0; i < length; i += MATRIX_SIZE)
//     {
//         for (j = 0; j < MATRIX_SIZE; j++)
//         {
//             int sum = 0;
//             for (int k = 0; k < MATRIX_SIZE; k++)
//             {
//                 sum += key[j][k] * (plaintext[i + k] - 'A');
//             }
//             ciphertext[i + j] = (sum % 26 + 26) % 26 + 'A';
//         }
//     }
//     ciphertext[length] = '\0';
// }

// int main()
// {
//     int server_fd, new_socket;
//     struct sockaddr_in address;
//     int addrlen = sizeof(address);
//     char buffer[1024] = {0};
//     char encrypted[1024] = {0};

//     // Key matrix for encryption
//     int key[MATRIX_SIZE][MATRIX_SIZE] = {{9, 4}, {5, 7}};

//     if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
//     {
//         perror("Socket failed");
//         exit(EXIT_FAILURE);
//     }

//     address.sin_family = AF_INET;
//     address.sin_addr.s_addr = INADDR_ANY;
//     address.sin_port = htons(PORT);

//     if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
//     {
//         perror("Bind failed");
//         exit(EXIT_FAILURE);
//     }
//     if (listen(server_fd, 3) < 0)
//     {
//         perror("Listen failed");
//         exit(EXIT_FAILURE);
//     }

//     printf("Server is listening on port %d...\n", PORT);
//     if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
//     {
//         perror("Accept failed");
//         exit(EXIT_FAILURE);
//     }

//     read(new_socket, buffer, 1024);
//     printf("Received plaintext: %s\n", buffer);

//     hill_cipher_encrypt(buffer, key, encrypted);

//     printf("Sending encrypted text: %s\n", encrypted);
//     send(new_socket, encrypted, strlen(encrypted), 0);

//     close(new_socket);
//     close(server_fd);
//     return 0;
// }

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024
#define MATRIX_SIZE 2

// Matrix multiplication for encryption
void matrix_multiply(int plaintext[MATRIX_SIZE][MATRIX_SIZE], int key[MATRIX_SIZE][MATRIX_SIZE], int ciphertext[MATRIX_SIZE][MATRIX_SIZE])
{
    for (int i = 0; i < MATRIX_SIZE; i++)
    {
        for (int j = 0; j < MATRIX_SIZE; j++)
        {
            ciphertext[i][j] = 0;
            for (int k = 0; k < MATRIX_SIZE; k++)
            {
                ciphertext[i][j] += plaintext[i][k] * key[k][j];
            }
            ciphertext[i][j] %= 26; // Modulo 26
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
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    // Predefined key matrix
    int key[MATRIX_SIZE][MATRIX_SIZE] = {{9, 4}, {5, 7}};

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

    // Encrypt plaintext using Hill cipher
    char plaintext[] = "MEET";
    int plaintext_matrix[MATRIX_SIZE][MATRIX_SIZE];
    int ciphertext_matrix[MATRIX_SIZE][MATRIX_SIZE];
    char ciphertext[BUFFER_SIZE];

    text_to_matrix(plaintext, plaintext_matrix);
    matrix_multiply(plaintext_matrix, key, ciphertext_matrix);
    matrix_to_text(ciphertext_matrix, ciphertext);

    printf("Plaintext: %s\n", plaintext);
    printf("Ciphertext: %s\n", ciphertext);

    // Send ciphertext to client
    send(new_socket, ciphertext, strlen(ciphertext), 0);
    printf("Ciphertext sent to client.\n");

    close(new_socket);
    close(server_fd);
    return 0;
}
