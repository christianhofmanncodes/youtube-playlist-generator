def input_url_or_id():
    print("Please input new ID or URL from YouTube Video:")
    return get_input()


def get_input():
    return str(input())


def check_if_string_is_valid_url(string):
    if 'http://' in string or 'https://' in string:
        return True


def check_if_string_is_youtube_url(string):
    if 'watch?' in string:
        return True


def cut_url_to_id(url):
    get_id = url.split("v=")
    return get_id[-1]


def read_content_from_file():
    with open("youtube_url.txt", "r") as reader:
        return reader.read()


def append_id_to_url(id):
    print("Adding new ID to URL...")
    with open("youtube_url.txt", "a") as writer:
        return writer.write(f'{id},')


def insert_id_to_url(id):
    title = id.find('&title=')
    print("Inserting new ID to URL...")
    with open("youtube_url.txt", "a") as writer:
        return writer.write(id[:title] + id + id[title:])


def check_if_another_video_should_be_added():
    print('Do you want to add another video to the playlist?')
    print('Press [y] for yes and [n] for no.')
    if get_input() == "y":
        main()


def check_if_space_in_title(title):
    if " " in title:
        return title.replace(" ", "%20")


def check_if_youtube_url_contains_playlist_title(string):
    if '&title=' in string:
        return True


def add_title_to_playlist():
    print('What title do you want to choose for your playlist?')
    title = get_input()
    with open("youtube_url.txt", "a") as writer:
        return writer.write(f'&title={check_if_space_in_title(title)}')


def output_new_youtube_url():
    print(f'Here is your new Playlist URL: {read_content_from_file()}')


def main():
    input = input_url_or_id()
    if check_if_string_is_valid_url(input) and check_if_string_is_youtube_url(input):
        id = cut_url_to_id(input)
        if check_if_youtube_url_contains_playlist_title(read_content_from_file()):
            insert_id_to_url(id)
        else:
            print("There is no title for your playlist yet. Do you want to add one?")
            print('Press [y] for yes and [n] for no.')
            if get_input() == "y":
                add_title_to_playlist()
                insert_id_to_url(id)
            append_id_to_url(id)
    elif check_if_youtube_url_contains_playlist_title(read_content_from_file()):
        insert_id_to_url(input)
    else:
        print("There is no title for your playlist yet. Do you want to add one?")
        print('Press [y] for yes and [n] for no.')
        if get_input() == "y":
            add_title_to_playlist()
            insert_id_to_url(input)
        append_id_to_url(input)
    check_if_another_video_should_be_added()
    output_new_youtube_url()


if __name__ == "__main__":
    main()