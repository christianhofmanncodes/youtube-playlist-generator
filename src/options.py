from definitions import *
import config


def option_one():
    if is_empty_csv("video_ids.csv"):
        reset_playlist()

    elif ask_if_playlist_should_be_deleted():
        reset_playlist()
    else:
        print("You didn't choose to create a new playlist.")
        exit(0)


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


def option_three():
    if (
        check_if_youtube_url_contains_no_playlist_title(config.youtube_playlist_title)
        and check_if_playlist_title_should_be_added()
    ):
        config.youtube_playlist_title = add_title_to_playlist()
        print(f"Title {config.youtube_playlist_title} successfully added.")
    else:
        print(
            f"There is already a title for your YouTube playlist: {config.youtube_playlist_title}"
        )
        print("Do you want to change it?")
        if check_if_playlist_title_should_be_added():
            option_four()


def option_four():
    if not check_if_youtube_url_contains_no_playlist_title(
        config.youtube_playlist_title
    ):
        config.youtube_playlist_title = add_title_to_playlist()
        print(f"Title {config.youtube_playlist_title} successfully changed.")
    elif check_if_playlist_title_should_be_added():
        option_three()


def option_five():
    tuple = read_csv_and_add_content_to_tuple()
    list = join_tuple(tuple)

    print(list)
    delete_items_from_playlist(list)


def option_six():
    if (
        check_if_youtube_url_contains_no_playlist_title(config.youtube_playlist_title)
        and check_if_playlist_title_should_be_added()
    ):
        config.youtube_playlist_title = add_title_to_playlist()
        print(f"Title {config.youtube_playlist_title} successfully added.")

    if not is_empty_csv("video_ids.csv"):
        tuple = read_csv_and_add_content_to_tuple()
        list = join_tuple(tuple)
        comma_seperated_string = create_comma_seperated_string(list)
        playlist_title = config.youtube_playlist_title
        if check_if_space_in_title(config.youtube_playlist_title):
            playlist_title = replace_space_in_title(playlist_title)
        print(create_playlist_url(comma_seperated_string, playlist_title))


def option_seven():
    exit(0)
