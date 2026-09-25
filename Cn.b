#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
struct Book {
    int Book_ID;
    char Title[50];
    char Author[50];
    float Price;
    char Status[10]; // Available / Issued
};
 
struct Book *books;
int n;
 
void create() {
    printf("Enter number of books: ");
    scanf("%d", &n);
    books = (struct Book *) malloc(n * sizeof(struct Book));
 
    for (int i = 0; i < n; i++) {
        printf("\nEnter details of book %d\n", i + 1);
        printf("Book ID: ");
        scanf("%d", &books[i].Book_ID);
        printf("Title: ");
        scanf("%s", books[i].Title);
        printf("Author: ");
        scanf("%s", books[i].Author);
        printf("Price: ");
        scanf("%f", &books[i].Price);
        strcpy(books[i].Status, "Available");
    }
}
 
void display() {
    if (n == 0) {
        printf("No books to display.\n");
        return;
    }
    printf("\n%-8s%-15s%-15s%-10s%-10s\n", "ID", "Title", "Author", "Price", "Status");
    for (int i = 0; i < n; i++) {
        printf("%-8d%-15s%-15s%-10.2f%-10s\n", books[i].Book_ID, books[i].Title,
               books[i].Author, books[i].Price, books[i].Status);
    }
}
 
int search(int id) {
    for (int i = 0; i < n; i++) {
        if (books[i].Book_ID == id) {
            printf("\nBook Found:\n");
            printf("ID: %d\nTitle: %s\nAuthor: %s\nPrice: %.2f\nStatus: %s\n",
                   books[i].Book_ID, books[i].Title, books[i].Author,
                   books[i].Price, books[i].Status);
            return i;
        }
    }
    printf("Book not found.\n");
    return -1;
}
 
void issueBook() {
    int id;
    printf("Enter Book ID to issue: ");
    scanf("%d", &id);
    int i = search(id);
    if (i != -1) {
        if (strcmp(books[i].Status, "Issued") == 0)
            printf("Book is already issued.\n");
        else {
            strcpy(books[i].Status, "Issued");
            printf("Book issued successfully.\n");
        }
    }
}
 
void returnBook() {
    int id;
    printf("Enter Book ID to return: ");
    scanf("%d", &id);
    int i = search(id);
    if (i != -1) {
        if (strcmp(books[i].Status, "Available") == 0)
            printf("Book was not issued.\n");
        else {
            strcpy(books[i].Status, "Available");
            printf("Book returned successfully.\n");
        }
    }
}
 
int main() {
    int choice, id;
    n = 0;
 
    do {
        printf("\n----- LIBRARY MENU -----\n");
        printf("1. Add Book Records\n");
        printf("2. Display all Book Records\n");
        printf("3. Search Book by Book ID\n");
        printf("4. Issue a Book\n");
        printf("5. Return a Book\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
 
        switch (choice) {
            case 1: create(); break;
            case 2: display(); break;
            case 3:
                printf("Enter Book ID to search: ");
                scanf("%d", &id);
                search(id);
                break;
            case 4: issueBook(); break;
            case 5: returnBook(); break;
            case 6: printf("Exiting program.\n"); break;
            default: printf("Invalid choice.\n");
        }
    } while (choice != 6);
 
    free(books);
    return 0;
}
