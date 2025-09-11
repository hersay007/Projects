#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Swap function
void swap(char *x, char *y) {
    char temp = *x;
    *x = *y;
    *y = temp;
}

// Convert string to lowercase
void toLowercase(char str[]) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

// Check if two strings are anagrams (using sorting)
int areAnagrams(char str1[], char str2[]) {
    int len1 = strlen(str1);
    int len2 = strlen(str2);

    if (len1 != len2) return 0;

    // Convert both to lowercase
    toLowercase(str1);
    toLowercase(str2);

    // Sort str1
    for (int i = 0; i < len1 - 1; i++) {
        for (int j = i + 1; j < len1; j++) {
            if (str1[i] > str1[j]) swap(&str1[i], &str1[j]);
        }
    }

    // Sort str2
    for (int i = 0; i < len2 - 1; i++) {
        for (int j = i + 1; j < len2; j++) {
            if (str2[i] > str2[j]) swap(&str2[i], &str2[j]);
        }
    }

    // Compare
    return strcmp(str1, str2) == 0;
}

// Function to check if character is already used at a position
int isUsed(char str[], int start, int curr) {
    for (int i = start; i < curr; i++) {
        if (str[i] == str[curr]) return 1;
    }
    return 0;
}

// Recursive function to generate all anagrams
void generateAnagrams(char str[], int start, int end) {
    if (start == end) {
        printf("%s\n", str);
        return;
    }

    for (int i = start; i <= end; i++) {
        if (isUsed(str, start, i)) continue;  // skip duplicates
        swap(&str[start], &str[i]);
        generateAnagrams(str, start + 1, end);
        swap(&str[start], &str[i]);  // backtrack
    }
}

// Main menu-driven program
int main() {
    int choice;
    char word[50], word1[50], word2[50];

    do {
        printf("\n--- Anagram Program ---\n");
        printf("1. Check if two words are anagrams\n");
        printf("2. Generate all anagrams of a word\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
        case 1:
            printf("Enter first word: ");
            scanf("%s", word1);
            printf("Enter second word: ");
            scanf("%s", word2);

            if (areAnagrams(word1, word2))
                printf("✅ Yes, they are anagrams.\n");
            else
                printf("❌ No, they are not anagrams.\n");
            break;

        case 2:
            printf("Enter a word: ");
            scanf("%s", word);
            printf("All possible anagrams:\n");
            generateAnagrams(word, 0, strlen(word) - 1);
            break;

        case 3:
            printf("Exiting...\n");
            break;

        default:
            printf("Invalid choice! Try again.\n");
        }
    } while (choice != 3);

    return 0;
}
