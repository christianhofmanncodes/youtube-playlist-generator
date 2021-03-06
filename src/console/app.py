"""app module"""
import sys
from os import name, path, system

import config.config
from definitions.definitions import (
    add_id_to_csv,
    add_title_to_playlist,
    convert_list_to_table,
    count_items_in_table,
    create_comma_seperated_string,
    cut_url_to_id,
    delete_items_from_playlist,
    generate_playlist_url,
    generate_video_ids_url,
    input_url_or_id,
    is_empty_csv,
    is_string_valid_url,
    is_string_valid_youtube_url,
    join_tuple,
    open_playlist_url_in_webbrowser,
    output_generated_playlist_url,
    read_csv_and_add_content_to_tuple,
    remove_duplicates_from_list,
    reset_playlist,
    want_another_video_added,
    want_playlist_deleted,
)


BASE_DIR = path.dirname(__file__)


def clear():
    """Remove text from console."""
    _ = system("cls") if name == "nt" else system("clear")


def welcome_message():
    """First execute clear() and then print out welcome message."""
    clear()
    print("-" * 62)
    print("Welcome to the YouTube Playlist Generator by Christian Hofmann")
    print("-" * 62)


def main_menu():
    """Print out choices and get user input. If choice exists go to the function."""
    print("[0] to view current playlist")
    print("[1] to create a new playlist")
    print("[2] to add videos to the playlist")
    print("[3] to delete certain videos from the playlist")
    print("[4] to generate the URL for the playlist")
    print("[5] to exit the program")

    choice = input("\nPlease select an option: ")
    if choice == "0":
        option_zero()
    elif choice == "1":
        option_one()
    elif choice == "2":
        option_two()
    elif choice == "3":
        option_three()
    elif choice == "4":
        option_four()
    elif choice == "5":
        option_five()
    else:
        print(
            "\nInvalid option. Please enter a number between [0] and [4].",
            "Or press [5] to exit the program.\n",
        )
        main_menu()


def option_zero():
    """View current playlist as a table."""
    clear()
    content_tuple = read_csv_and_add_content_to_tuple()
    content_list = join_tuple(content_tuple)
    list_without_duplicates = remove_duplicates_from_list(content_list)

    list_with_video_ids = convert_list_to_table(list_without_duplicates)

    if len(list_with_video_ids) != 0:
        print(
            f"\nThese video ids are currently in your playlist: {list_with_video_ids}\n"
        )
        print(f"sum of video ids: {count_items_in_table(list_with_video_ids)}\n")
    else:
        print("There are no videos in your playlist yet.\n")
    main_menu()


def option_one():
    """Create a new playlist (delete all items in playlist) if user accepts it."""
    clear()
    if is_empty_csv(f"{path.join(BASE_DIR, 'data', 'video_ids.csv')}"):
        print("\nYour playlist is already empty!\n")
    elif want_playlist_deleted():
        reset_playlist()
    else:
        print("\nYou didn't choose to create a new playlist.\n")
    main_menu()


def option_two():
    """Add new videos to playlist either by their URL or ID."""
    clear()
    user_input = input_url_or_id()
    if is_string_valid_url(user_input) and is_string_valid_youtube_url(
        user_input
    ):  # if input is a valid YouTube URL
        video_id = cut_url_to_id(user_input)
    else:
        video_id = user_input
    add_id_to_csv(video_id)
    print(f"\nVideo '{video_id}' was successfully added to the playlist.\n")
    if want_another_video_added():
        option_two()
    main_menu()


def option_three():
    """
    View current items in playlist as a table
    and delete video id from user input if it exists.
    """
    clear()
    content_tuple = read_csv_and_add_content_to_tuple()
    content_list = join_tuple(content_tuple)
    list_without_duplicates = remove_duplicates_from_list(content_list)

    list_with_video_ids = convert_list_to_table(list_without_duplicates)

    if len(list_with_video_ids) != 0:
        print(
            "\nThese video ids are currently in your playlist:",
            f"{convert_list_to_table(list_without_duplicates)}\n",
        )
        delete_items_from_playlist(list_without_duplicates)
    else:
        print("There are no videos in your playlist yet.\n")
    main_menu()


def option_four():
    """Generate playlist URL if more than two ids are in the current playlist."""
    clear()
    if not is_empty_csv(f"{path.join(BASE_DIR, 'data', 'video_ids.csv')}"):
        content_tuple = read_csv_and_add_content_to_tuple()
        content_list = join_tuple(content_tuple)
        comma_seperated_string = create_comma_seperated_string(content_list)
        playlist_title = config.config.YOUTUBE_PLAYLIST_TITLE
        add_title_to_playlist(playlist_title)

        generate_video_ids_url(comma_seperated_string)
        if generate_playlist_url(config.config.YOUTUBE_GENERATED_VIDEO_IDS_URL):
            output_generated_playlist_url()
            open_playlist_url_in_webbrowser()
    else:
        print(
            "\nYour playlist is empty!",
            "Add at least two videos in order to generate a playlist URL.\n",
        )
    main_menu()


def option_five():
    """Exit application."""
    sys.exit(0)


def run():
    """Check if first start bool is true, output welcome message. Otherwise execute main_menu()."""
    if config.config.FIRST_START is True:
        welcome_message()
        config.config.FIRST_START = False
    main_menu()
