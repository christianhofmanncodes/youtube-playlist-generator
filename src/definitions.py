import csv
import config
import pandas as pd


def input_url_or_id():
    print("\nPlease input new ID or URL from YouTube Video:\n")
    return get_input()


def get_input():
    return str(input())


def is_string_valid_url(string):
    if "http://" in string or "https://" in string:
        return True


def is_string_valid_youtube_url(string):
    if "watch?" in string:
        return True


def cut_url_to_id(url):
    get_id = url.split("v=")
    return get_id[-1]


def read_csv_and_add_content_to_tuple():
    with open("video_ids.csv", "r", newline="") as read_obj:
        return tuple(csv.reader(read_obj))


def join_tuple(tuple):
    return list(map(" ".join, tuple))


def is_empty_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for i, _ in enumerate(reader):
            if i:  # found the second row
                return False
    return True


def create_comma_seperated_string(list):
    return ",".join(list)


def read_content_from_file(path):
    with open(path, "r") as reader:
        return reader.read()


def read_csv_and_add_content_to_list():
    with open("video_ids.csv", "r") as read_obj:
        return list(csv.reader(read_obj))


def add_id_to_csv(id):
    print("\nAdding new ID to list...\n")
    with open("video_ids.csv", "a", newline="") as writer:
        return writer.write(f"{id}\n")


def convert_list_to_table(list):
    return pd.DataFrame(data=list)


def delete_items_from_playlist(list):
    print("\nWhich item do you want to delete from the playlist?\n")
    try:
        id = get_input()
        list.remove(id)
        with open("video_ids.csv", "w", newline="") as file:
            for id in list:
                file.write(id + "\n")
        print(f"\nItem {id} succesfully deleted from playlist.\n")
    except IndexError:
        print(f"\nThere is no item {id} in the list you specified!\n")
    except Exception:
        print("\nAn error accured while writing to the file!\n")


def want_another_video_added():
    print("\nDo you want to add another video to the playlist?\n")
    print("Press [y] for yes and [n] for no.")
    if get_input() == "y":
        return True


def has_space_in_title(title):
    if " " in title:
        return True


def replace_space_in_title(title_with_space):
    return title_with_space.replace(" ", "%20")


def get_human_readable_title(title):
    return title.replace("%20", " ")


def has_no_playlist_title(playlist_title):
    print("\nThere is no title for your playlist yet. Do you want to add one?\n")
    if playlist_title == "":
        return True
    print(
        f"\nThere is already a title for your YouTube playlist: {config.youtube_playlist_title}\n"
    )
    print("Do you want to change it?")
    if want_playlist_title():
        change_title_from_playlist()


def want_playlist_title():
    print("Press [y] for yes and [n] for no.")
    if get_input() == "y":
        return True


def get_title_for_playlist():
    print("\nWhat title do you want to choose for your playlist?\n")
    title = get_input()

    if has_space_in_title(title):
        title = replace_space_in_title(title)
    return title


def add_title_to_playlist(playlist_title):
    if has_no_playlist_title(playlist_title):
        if not want_playlist_title():
            return False
        config.youtube_playlist_title = get_title_for_playlist()
        print(f"\nPlaylist title {config.youtube_playlist_title} successfully added.\n")
        return True


def change_title_from_playlist():
    if not check_if_youtube_url_contains_no_playlist_title(
        config.youtube_playlist_title
    ):
        config.youtube_playlist_title = add_title_to_playlist()
        print(f"\nTitle {config.youtube_playlist_title} successfully changed.\n")
    elif check_if_playlist_title_should_be_added():
        add_title_to_playlist()


def want_playlist_title_deleted():
    print("\nDo you really want to create a new playlist?\n")
    print("That deletes all of your videos!")
    print("Press [y] yes or [n] for no.")
    input = get_input()
    if input == "y":
        return True


def reset_playlist():
    print("\nRemoving all videos from playlist...\n")
    with open("video_ids.csv", "w+") as writer:
        writer.write("")
    print("\nA new playlist was sucessfully created.\n")
    print("\nYou can now add videos to your playlist.\n")


def create_playlist_url_with_title(video_ids, playlist_title):
    return f"{config.youtube_playlist_url}{video_ids}&title={playlist_title}"


def create_playlist_url_without_title(video_ids):
    return f"{config.youtube_playlist_url}{video_ids}"
