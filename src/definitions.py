import csv
import config


def input_url_or_id():
    print("Please input new ID or URL from YouTube Video:")
    return get_input()


def get_input():
    return str(input())


def check_if_string_is_valid_url(string):
    if "http://" in string or "https://" in string:
        return True


def check_if_string_is_youtube_url(string):
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


def read_content_from_file():
    with open("youtube_url.txt", "r") as reader:
        return reader.read()


def read_csv_and_add_content_to_list():
    with open("video_ids.csv", "r") as read_obj:
        return list(csv.reader(read_obj))


def add_id_to_csv(id):
    print("Adding new ID to list...")
    with open("video_ids.csv", "a", newline="") as writer:
        return writer.write(f"{id}\n")


def delete_items_from_playlist(list):
    print("Which item do you want to delete from the playlist?")
    list.remove(get_input())
    print(list)
    with open("video_ids.csv", "w", newline="") as file:
        file.writerow(list)  # todo: fix not writing in new lines


def check_if_another_video_should_be_added():
    print("Do you want to add another video to the playlist?")
    print("Press [y] for yes and [n] for no.")
    if get_input() == "y":
        main()


def check_if_space_in_title(title):
    if " " in title:
        return True


def replace_space_in_title(title):
    return title.replace(" ", "%20")


def check_if_youtube_url_contains_no_playlist_title(string):
    if config.youtube_playlist_title == "":
        return True


def check_if_playlist_title_should_be_added():
    print("There is no title for your playlist yet. Do you want to add one?")
    print("Press [y] for yes and [n] for no.")
    if get_input() == "y":
        return True


def add_title_to_playlist():
    print("What title do you want to choose for your playlist?")
    title = get_input()

    if check_if_space_in_title(title):
        title = replace_space_in_title(title)
    return title


def ask_if_playlist_should_be_deleted():
    print("Do you really want to create a new playlist?")
    print("That deletes all of your videos!")
    print("Press [y] yes or [n] for no.")
    input = get_input()
    if input == "y":
        return True


def reset_playlist():
    print("Removing all videos from playlist...")
    with open("video_ids.csv", "w+") as writer:
        writer.write("")
    print("A new playlist was sucessfully created.")
    print("You can now add videos to your playlist.")


def create_playlist_url(video_ids, playlist_title):
    return f"{config.youtube_playlist_url}{video_ids}&title={playlist_title}"
