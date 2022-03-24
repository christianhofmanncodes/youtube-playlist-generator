import csv
import os
import ssl
from urllib import request
import webbrowser
import pandas as pd
import config


basedir = os.path.dirname(__file__)


def input_url_or_id():
    message = "\nPlease enter a new ID or URL of a YouTube video: "
    return get_input(message)


def get_input(message):
    return str(input(message))


def is_string_valid_url(string):
    if "http://" in string or "https://" in string:
        return True


def is_string_valid_youtube_url(string):
    if "watch?" in string or "be/" in string:
        return True


def cut_url_to_id(url):
    if "v=" in url:
        get_id = url.split("v=")
    elif "be/" in url:
        get_id = url.split("be/")
    return get_id[-1]


def read_csv_and_add_content_to_tuple():
    with open(
        f"{os.path.join(basedir, 'data', 'video_ids.csv')}",
        "r",
        newline="",
        encoding="UTF-8",
    ) as read_obj:
        return tuple(csv.reader(read_obj))


def join_tuple(content_tuple):
    return list(map(" ".join, content_tuple))


def is_empty_csv(path):
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
    return ",".join(content_list)


def read_content_from_file(path):
    with open(
        path,
        "r",
        encoding="UTF-8",
    ) as reader:
        return reader.read()


def read_csv_and_add_content_to_list():
    with open(
        f"{os.path.join(basedir, 'data', 'video_ids.csv')}",
        "r",
        encoding="UTF-8",
    ) as read_obj:
        return list(csv.reader(read_obj))


def remove_duplicates_from_list(content_list):
    return list(dict.fromkeys(content_list))


def add_id_to_csv(video_id):
    print(f"\nAdding new ID '{video_id}' to playlist...")
    with open(
        f"{os.path.join(basedir, 'data', 'video_ids.csv')}",
        "a",
        newline="",
        encoding="UTF-8",
    ) as writer:
        return writer.write(f"{video_id}\n")


def convert_list_to_table(content_list):
    return pd.DataFrame(data=content_list, columns=["video_ids"])


def count_items_in_table(pandas_dataframe):
    return str(pandas_dataframe.shape[0])


def delete_items_from_playlist(content_list):
    message = "Which item do you want to delete from the playlist?: "
    try:
        id_to_be_removed = get_input(message)
        content_list.remove(id_to_be_removed)
        with open(
            f"{os.path.join(basedir, 'data', 'video_ids.csv')}",
            "w",
            newline="",
            encoding="UTF-8",
        ) as file:
            for video_id in content_list:
                file.write(video_id + "\n")
        print(f"\nItem '{id_to_be_removed}' succesfully deleted from playlist.\n")
    except ValueError:
        print(f"\nThere is no item '{id_to_be_removed}' in the playlist!\n")


def want_another_video_added():
    print("Do you want to add another video to the playlist?\n")
    message = "Press [y] for yes and [n] for no: "
    return get_input(message) == "y"


def has_space_in_title(title):
    if " " in title:
        return True


def replace_space_in_title(title_with_space):
    return title_with_space.replace(" ", "%20")


def get_human_readable_title(title):
    return title.replace("%20", " ")


def has_no_playlist_title(playlist_title):
    if playlist_title == "":
        print("\nThere is no title for your playlist yet. Would you like to add one?\n")
        return True


def has_playlist_title():
    print(
        f"\nThere is already a title for your YouTube playlist: {config.YOUTUBE_PLAYLIST_TITLE}"
    )
    print("Do you want to change it?\n")
    if want_playlist_title():
        change_title_from_playlist()


def want_playlist_title():
    message = "Press [y] for yes and [n] for no: "
    return get_input(message) == "y"


def get_title_for_playlist():
    message = "\nWhat title do you want to choose for your playlist?\n"
    title = get_input(message)

    if has_space_in_title(title):
        title = replace_space_in_title(title)
    return title


def add_title_to_playlist(playlist_title):
    if has_no_playlist_title(playlist_title) is True:
        if want_playlist_title() is False:
            config.YOUTUBE_PLAYLIST_TITLE = ""
        else:
            config.YOUTUBE_PLAYLIST_TITLE = get_title_for_playlist()
            print(
                f"\nPlaylist title '{get_human_readable_title(config.YOUTUBE_PLAYLIST_TITLE)}'",
                "successfully added.\n",
            )
    else:
        has_playlist_title()


def change_title_from_playlist():
    config.YOUTUBE_PLAYLIST_TITLE = get_title_for_playlist()
    print(
        f"\nTitle '{get_human_readable_title(config.YOUTUBE_PLAYLIST_TITLE)}'",
        "successfully changed.\n",
    )


def want_playlist_deleted():
    print("\nDo you really want to create a new playlist?")
    print("That deletes all of your videos!\n")
    message = "Press [y] yes or [n] for no: "
    user_input = get_input(message)
    return user_input == "y"


def reset_playlist():
    print("\nRemoving all videos from playlist...")
    with open(
        f"{os.path.join(basedir, 'data', 'video_ids.csv')}",
        "w+",
        encoding="UTF-8",
    ) as writer:
        writer.write("")
    print("\nA new playlist was successfully created.")
    print("\nYou can now add videos to your playlist.\n")


def create_playlist_url_with_title(video_ids, playlist_title):
    return f"{config.YOUTUBE_PLAYLIST_BASE_URL}{video_ids}&title={playlist_title}"


def create_playlist_url_without_title(video_ids):
    return f"{config.YOUTUBE_PLAYLIST_BASE_URL}{video_ids}"


def open_url_in_webbrowser(url):
    print(f"\nOpening {url} in new Web browser tab...\n")
    webbrowser.open_new_tab(url)


def generate_video_ids_url(comma_seperated_string):
    if config.YOUTUBE_PLAYLIST_TITLE != "":
        config.YOUTUBE_GENERATED_VIDEO_IDS_URL = create_playlist_url_with_title(
            comma_seperated_string, config.YOUTUBE_PLAYLIST_TITLE
        )
    else:
        config.YOUTUBE_GENERATED_VIDEO_IDS_URL = create_playlist_url_without_title(
            comma_seperated_string
        )


def generate_playlist_url(video_ids_url):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        response = request.urlopen(video_ids_url)

        playlist_link = response.geturl()
        playlist_link = playlist_link.split("list=")[1]

        config.YOUTUBE_GENERATED_PLAYLIST_URL = (
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
    print(f"Here's your URL for the playlist: {config.YOUTUBE_GENERATED_PLAYLIST_URL}")


def open_playlist_url_in_webbrowser():
    open_url_in_webbrowser(config.YOUTUBE_GENERATED_PLAYLIST_URL)
