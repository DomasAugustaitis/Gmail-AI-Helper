from controllers.GmailController import GmailController

def menu():
    print("1. Option 1")
    print("2. Option 2")
    print("3. Option 3")
    print("4. Quit")

def main():
    gmailController = GmailController()
    #gmailController.getTitles()
    gmailController.fetch_emails(7)

if __name__ == "__main__":
    main()