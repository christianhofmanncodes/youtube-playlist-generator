from definitions import *
import config


def main_menu():
    print("[1] to create a new playlist")
    print("[2] to add videos to the playlist")
    print("[3] to delete certain videos from the playlist")
    print("[4] to generate the URL for the playlist")
    print("[5] to exit the program")

    option = input("Please select an option: ")
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
    else:
        print(
            "\nInvalid option. Please enter a number between 1 and 4. Or press [5] to exit the program.\n"
        )
        main_menu()


def option_one():
    if is_empty_csv("video_ids.csv"):
        reset_playlist()

    elif ask_if_playlist_should_be_deleted():
        reset_playlist()
    else:
        print("You didn't choose to create a new playlist.")
    main_menu()


def option_two():
    input = input_url_or_id()
    if check_if_string_is_valid_url(input) and check_if_string_is_youtube_url(
        input
    ):  # if input is a valid YouTube URL
        id = cut_url_to_id(input)
    else:
        id = input

    add_id_to_csv(id)
    print(f"Video added successfully to playlist {config.youtube_playlist_title}.")
    main_menu()


def option_three():
    tuple = read_csv_and_add_content_to_tuple()
    list = join_tuple(tuple)

    print(list)
    delete_items_from_playlist(list)
    main_menu()


def option_four():
    if not is_empty_csv("video_ids.csv"):
        tuple = read_csv_and_add_content_to_tuple()
        list = join_tuple(tuple)
        comma_seperated_string = create_comma_seperated_string(list)
        playlist_title = config.youtube_playlist_title
        if add_title_to_playlist(playlist_title):
            print(create_playlist_url_with_title(comma_seperated_string, config.youtube_playlist_title))
        else:
            print(create_playlist_url_without_title(comma_seperated_string))
    main_menu()


def option_five():
    exit(0)


def main():
    print("\nWelcome to the YouTube Playlist Generator by Christian Hofmann\n")
    main_menu()


if __name__ == "__main__":
    main()
