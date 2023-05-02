from entities.gmail.Gmail import Gmail

def menu():
    print("1. Get email labels")
    print("2. Get emails")
    print("3. Search for emails")
    print("4. Quit")

if __name__ == "__main__":
    while True:
        menu()
        #choice = input("Input your choice: ")
        choice = "2"

        if choice == "1":
            gmail = Gmail()
            gmail.getLabels()
        elif choice == "2":
            gmail = Gmail()
            gmail.getEmails(2)
            break
        elif choice == "3":
            gmail = Gmail()
            gmail.searchEmails(["application", "CKAD", "april"], 5)
            break
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
