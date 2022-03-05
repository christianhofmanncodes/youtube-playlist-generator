from definitions import *


def option_one():
    if is_empty_csv("video_ids.csv"):
        reset_playlist()

    elif ask_if_playlist_should_be_deleted():
        reset_playlist()
    else:
        print("You didn't choose to create a new playlist.")
        exit(0)

def option_two():
    pass


def option_three():
    pass


def option_four():
    pass


def option_five():
    pass