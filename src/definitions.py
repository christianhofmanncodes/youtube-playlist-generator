import csv
import config
import pandas as pd
import webbrowser


def input_url_or_id():
    message = "\nPlease enter a new ID or URL of a YouTube video: "
    return get_input(message)


def get_input(message):
    return str(input(message))


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


def remove_duplicates_from_list(x):
    return list(dict.fromkeys(x))


def add_id_to_csv(id):
    print(f"\nAdding new ID '{id}' to playlist...")
    with open("video_ids.csv", "a", newline="") as writer:
        return writer.write(f"{id}\n")


def convert_list_to_table(list):
    return pd.DataFrame(data=list)


def delete_items_from_playlist(list):
    message = "Which item do you want to delete from the playlist?: "
    try:
        id_to_be_removed = get_input(message)
        list.remove(id_to_be_removed)
        with open("video_ids.csv", "w", newline="") as file:
            for id in list:
                file.write(id + "\n")
        print(f"\nItem '{id_to_be_removed}' succesfully deleted from playlist.\n")
    except Exception:
        print(f"\nThere is no item {id_to_be_removed} in the playlist!\n")


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
        f"\nThere is already a title for your YouTube playlist: {config.youtube_playlist_title}"
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
    if has_no_playlist_title(playlist_title) == True:
        if want_playlist_title() == False:
            config.youtube_playlist_title = ""
        else:
            config.youtube_playlist_title = get_title_for_playlist()
            print(
                f"\nPlaylist title '{get_human_readable_title(config.youtube_playlist_title)}' successfully added.\n"
            )
    else:
        has_playlist_title()


def change_title_from_playlist():
    config.youtube_playlist_title = get_title_for_playlist()
    print(
        f"\nTitle '{get_human_readable_title(config.youtube_playlist_title)}' successfully changed.\n"
    )


def want_playlist_deleted():
    print("\nDo you really want to create a new playlist?")
    print("That deletes all of your videos!\n")
    message = "Press [y] yes or [n] for no: "
    input = get_input(message)
    return input == "y"


def reset_playlist():
    print("\nRemoving all videos from playlist...")
    with open("video_ids.csv", "w+") as writer:
        writer.write("")
    print("\nA new playlist was successfully created.")
    print("\nYou can now add videos to your playlist.\n")


def create_playlist_url_with_title(video_ids, playlist_title):
    return f"{config.youtube_playlist_url}{video_ids}&title={playlist_title}"


def create_playlist_url_without_title(video_ids):
    return f"{config.youtube_playlist_url}{video_ids}"


def open_url_in_webbrowser(url):
    print(f"\nOpening {url} in new Web browser tab...\n")
    webbrowser.open_new_tab(url)


def output_generated_playlist_url(comma_seperated_string):
    if config.youtube_playlist_title != "":
        config.youtube_generated_playlist_url = create_playlist_url_with_title(
            comma_seperated_string, config.youtube_playlist_title
        )
    else:
        config.youtube_generated_playlist_url = create_playlist_url_without_title(
            comma_seperated_string
        )
    print(f"Here's your URL for the playlist: {config.youtube_generated_playlist_url}")
    open_url_in_webbrowser(config.youtube_generated_playlist_url)
