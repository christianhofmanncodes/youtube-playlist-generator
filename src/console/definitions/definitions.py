"""definitions module"""
import csv
import os
import ssl
import webbrowser
from urllib import request

import config.config
import pandas as pd


PARENT_DIR = os.path.join(os.path.dirname(__file__), "..")


def input_url_or_id():
    """Output message and return user input as a string."""
    message = "\nPlease enter a new ID or URL of a YouTube video: "
    return get_input(message)


def get_input(message):
    """Return user input as a string."""
    return str(input(message))


def is_string_valid_url(string):
    """Check if http:// or https:// in string and return bool value."""
    return "http://" in string or "https://" in string


def is_string_valid_youtube_url(string):
    """Check if watch? or be/ in string and return bool value."""
    return "watch?" in string or "be/" in string


def cut_url_to_id(url):
    """Return id from video URL."""
    if "v=" in url:
        get_id = url.split("v=")
    elif "be/" in url:
        get_id = url.split("be/")
    return get_id[-1]


def read_csv_and_add_content_to_tuple():
    """Get content from csv-file and return it as a tuple."""
    with open(
        f"{os.path.join(PARENT_DIR, 'data', 'video_ids.csv')}",
        "r",
        newline="",
        encoding="UTF-8",
    ) as read_obj:
        return tuple(csv.reader(read_obj))


def join_tuple(content_tuple):
    """Convert tuple to list."""
    return list(map(" ".join, content_tuple))


def is_empty_csv(path):
    """Check if no second line exists in csv-file and return bool value."""
    with open(
        path,
        encoding="UTF-8",
    ) as csvfile:
        reader = csv.reader(csvfile)
        for i, _ in enumerate(reader):
            if i:  # found the second row
                return False
    return True


def create_comma_seperated_string(content_list):
    """Add commas after each item from list and return it as a string."""
    return ",".join(content_list)


def read_content_from_file(path):
    """Get content from any file and return it."""
    with open(
        path,
        "r",
        encoding="UTF-8",
    ) as reader:
        return reader.read()


def read_csv_and_add_content_to_list():
    """Get content from csv-file and return it as a list."""
    with open(
        f"{os.path.join(PARENT_DIR, 'data', 'video_ids.csv')}",
        "r",
        encoding="UTF-8",
    ) as read_obj:
        return list(csv.reader(read_obj))


def remove_duplicates_from_list(content_list):
    """Remove duplicate entries from list."""
    return list(dict.fromkeys(content_list))


def add_id_to_csv(video_id):
    """Write new video id to csv-file."""
    print(f"\nAdding new ID '{video_id}' to playlist...")
    with open(
        f"{os.path.join(PARENT_DIR, 'data', 'video_ids.csv')}",
        "a",
        newline="",
        encoding="UTF-8",
    ) as writer:
        return writer.write(f"{video_id}\n")


def convert_list_to_table(content_list):
    """Convert list to pandas DataFrame."""
    return pd.DataFrame(data=content_list, columns=["video_ids"])


def count_items_in_table(pandas_dataframe):
    """Return sum of items in table."""
    return str(pandas_dataframe.shape[0])


def delete_items_from_playlist(content_list):
    """Ask for specific item in playlist and delete it if it exists."""
    message = "Which item do you want to delete from the playlist?: "
    try:
        id_to_be_removed = get_input(message)
        content_list.remove(id_to_be_removed)
        with open(
            f"{os.path.join(PARENT_DIR, 'data', 'video_ids.csv')}",
            "w",
            newline="",
            encoding="UTF-8",
        ) as file:
            for video_id in content_list:
                file.write(video_id + "\n")
        print(f"\nItem '{id_to_be_removed}' successfully deleted from playlist.\n")
    except ValueError:
        print(f"\nThere is no item '{id_to_be_removed}' in the playlist!\n")


def want_another_video_added():
    """Check if another video should be added."""
    print("Do you want to add another video to the playlist?\n")
    message = "Press [y] for yes and [n] for no: "
    return get_input(message) == "y"


def has_space_in_title(title):
    """Return True if space in title."""
    return " " in title


def replace_space_in_title(title_with_space):
    """Add URL encoding to playlist title."""
    return title_with_space.replace(" ", "%20")


def get_human_readable_title(title):
    """Remove URL encoding from playlist title."""
    return title.replace("%20", " ")


def has_no_playlist_title(playlist_title):
    """If no playlist title exists print it out and return bool value."""
    if playlist_title != "":
        return False
    print("\nThere is no title for your playlist yet. Would you like to add one?\n")
    return True


def has_playlist_title():
    """Check if playlist title already exists."""
    print(
        f"\nThere is already a title for your YouTube playlist: {config.config.YOUTUBE_PLAYLIST_TITLE}"
    )
    print("Do you want to change it?\n")
    if want_playlist_title():
        change_title_from_playlist()


def want_playlist_title():
    """Ask if playlist title should be added."""
    message = "Press [y] for yes and [n] for no: "
    return get_input(message) == "y"


def get_title_for_playlist():
    """Receive user input and set it as a playlist title."""
    message = "\nWhat title do you want to choose for your playlist?\n"
    title = get_input(message)

    if has_space_in_title(title):
        title = replace_space_in_title(title)
    return title


def add_title_to_playlist(playlist_title):
    """Add a title to the playlist."""
    if has_no_playlist_title(playlist_title) is True:
        if want_playlist_title() is False:
            config.config.YOUTUBE_PLAYLIST_TITLE = ""
        else:
            config.config.YOUTUBE_PLAYLIST_TITLE = get_title_for_playlist()
            print(
                f"\nPlaylist title '{get_human_readable_title(config.config.YOUTUBE_PLAYLIST_TITLE)}'",
                "successfully added.\n",
            )
    else:
        has_playlist_title()


def change_title_from_playlist():
    """Change title from the playlist."""
    config.config.YOUTUBE_PLAYLIST_TITLE = get_title_for_playlist()
    print(
        f"\nTitle '{get_human_readable_title(config.config.YOUTUBE_PLAYLIST_TITLE)}'",
        "successfully changed.\n",
    )


def want_playlist_deleted():
    """Ask if playlist should be deleted."""
    print("\nDo you really want to create a new playlist?")
    print("That deletes all of your videos!\n")
    message = "Press [y] yes or [n] for no: "
    user_input = get_input(message)
    return user_input == "y"


def reset_playlist():
    """Delete all videos from playlist."""
    print("\nRemoving all videos from playlist...")
    with open(
        f"{os.path.join(PARENT_DIR, 'data', 'video_ids.csv')}",
        "w+",
        encoding="UTF-8",
    ) as writer:
        writer.write("")
    print("\nA new playlist was successfully created.")
    print("\nYou can now add videos to your playlist.\n")


def create_playlist_url_with_title(video_ids, playlist_title):
    """Create playlist URL with a title from video ids and title."""
    return (
        f"{config.config.YOUTUBE_PLAYLIST_BASE_URL}{video_ids}&title={playlist_title}"
    )


def create_playlist_url_without_title(video_ids):
    """Create playlist URL without a title from video ids."""
    return f"{config.config.YOUTUBE_PLAYLIST_BASE_URL}{video_ids}"


def open_url_in_webbrowser(url):
    """Open a URL in Webbrowser in a new tab."""
    print(f"\nOpening {url} in new Web browser tab...\n")
    webbrowser.open_new_tab(url)


def generate_video_ids_url(comma_seperated_string):
    """Generate the video ids URL from a comma seperated string."""
    if config.config.YOUTUBE_PLAYLIST_TITLE != "":
        config.config.YOUTUBE_GENERATED_VIDEO_IDS_URL = create_playlist_url_with_title(
            comma_seperated_string, config.config.YOUTUBE_PLAYLIST_TITLE
        )
    else:
        config.config.YOUTUBE_GENERATED_VIDEO_IDS_URL = (
            create_playlist_url_without_title(comma_seperated_string)
        )


def generate_playlist_url(video_ids_url):
    """Generate the playlist URL from the video ids URL."""
    try:
        context = ssl._create_unverified_context()
        with request.urlopen(video_ids_url, context=context) as response:
            playlist_link = response.geturl()
            playlist_link = playlist_link.split("list=")[1]

        config.config.YOUTUBE_GENERATED_PLAYLIST_URL = (
            f"https://www.youtube.com/playlist?list={playlist_link}"
            + "&disable_polymer=true"
        )
        return True
    except IndexError:
        print(
            "\nThere was an error with creating the playlist url.",
            "Check if all video ids are valid and correct.\n",
        )
        return False


def output_generated_playlist_url():
    """Print out the generated playlist URL."""
    print(
        f"Here's your URL for the playlist: {config.config.YOUTUBE_GENERATED_PLAYLIST_URL}"
    )


def open_playlist_url_in_webbrowser():
    """Open the generated playlist URL in Webbrowser."""
    open_url_in_webbrowser(config.config.YOUTUBE_GENERATED_PLAYLIST_URL)
