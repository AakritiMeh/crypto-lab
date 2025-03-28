#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main()
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    char plaintext[BUFFER_SIZE] = {0};
    char buffer[BUFFER_SIZE] = {0};
    int key[BUFFER_SIZE];
    int key_len;

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\nSocket creation error\n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary form
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0)
    {
        printf("\nInvalid address/Address not supported\n");
        return -1;
    }

    // Connect to server
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed\n");
        return -1;
    }

    // Input plaintext
    printf("Enter the plaintext: ");
    fgets(plaintext, BUFFER_SIZE, stdin);
    plaintext[strcspn(plaintext, "\n")] = '\0'; // Remove newline character

    // Input key
    printf("Enter the key length: ");
    scanf("%d", &key_len);

    printf("Enter the key (e.g., for '4312567', enter '4 3 1 2 5 6 7'): ");
    for (int i = 0; i < key_len; i++)
    {
        scanf("%d", &key[i]);
    }

    // Send key length to server
    send(sock, &key_len, sizeof(key_len), 0);

    // Send key to server
    send(sock, key, key_len * sizeof(int), 0);

    // Send plaintext to server
    send(sock, plaintext, strlen(plaintext), 0);

    // Receive ciphertext from server
    read(sock, buffer, BUFFER_SIZE);
    printf("Ciphertext received: %s\n", buffer);

    close(sock);

    return 0;
}
