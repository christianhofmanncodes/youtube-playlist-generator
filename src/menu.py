from options import option_one, option_two, option_three, option_four, option_five


def main_menu():
    print("Please choose the action you want to take:\n")
    print("[1] for creating a new playlist")
    print("[2] for adding videos to the playlist")
    print("[3] for adding a title to the playlist")
    print("[4] for changing or deleting the title of the playlist")
    print("[5] for deleting certain videos from the playlist")
    print("[6] for quitting the program")

    option = input("Enter your choice: ")
    if option == "1":
        option_one()
    elif option == "2":
        option_two()
    elif option == "3":
        option_three()
    elif option == "4":
        option_four()
    elif option == "5":
        option_five()
    elif option == "6":
        exit(0)
    else:
        print("Invalid option. Please enter a number between 1 and 5. Or hit [6] for quitting the program.\n")
        main_menu()