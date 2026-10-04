from server import register_user, verify
from client import generate_code

while True:

    print("\n------ TOTP SYSTEM ------")
    print("1 Register user")
    print("2 Generate TOTP")
    print("3 Login")
    print("4 Exit")

    choice = input("Choose option: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        register_user(username, password)

    elif choice == "2":
        secret = input("Enter secret: ")
        generate_code(secret)

    elif choice == "3":
        username = input("Username: ")
        password = input("Password: ")
        code = input("Enter TOTP code: ")
        verify(username, password, code)

    elif choice == "4":
        print("Goodbye")
        break

    else:
        print("Invalid option")
