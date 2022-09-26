"""module playlist.playlist"""

import logging
import random

from strings import check_string, replace_string
from url import generate_url, open_url, url
from dialogs import dialogs


def shuffle(self) -> None:
    """
    The shuffle function shuffles the playlist with random.shuffle().

    :param self: Used to Access the class attributes.
    :return: None.
    """
    logging.debug("Shuffle playlist...")
    playlist = output_list_from_playlist_ids(self)
    random.shuffle(playlist)

    ytplaylist_dict = generate_dict_from_fields(
        self.lineEdit_playlist_title.text(),
        playlist,
    )

    self.listWidget_playlist_items.clear()
    import_from_dict(self, ytplaylist_dict)


def number_of_playlist_items(self) -> int:
    """
    The number_of_playlist_items function returns the number of items in the playlist as an integer.

    :param self: Used to Access the attributes and methods of the class in python.
    :return: The number of items in the playlist.
    """
    playlist = self.listWidget_playlist_items
    return len([playlist.item(x) for x in range(playlist.count())])


def playlist_widget_has_x_or_more_items(self, number: int) -> bool:
    """
    The playlist_widget_has_x_or_more_items function returns True
    if the number of items in the playlist is greater than or equal to x.

    :param self: Used to Access the class attributes.
    :param number:int: Used to Specify the minimum number
    of items that should be in the playlist.
    :return: True if the number of items in the playlist is greater than
    or equal to a specified number.
    """
    return number_of_playlist_items(self) >= number


def is_playlist_widget_empty(self) -> bool:
    """
    The is_playlist_widget_empty function returns True if no items are in the playlist.
    Otherwise, it returns False.

    :param self: Used to Access the attributes and methods of the class in which it is used.
    :return: True if the number of items in the playlist is 0.
    """
    return number_of_playlist_items(self) == 0


def make_item_editable(self) -> None:
    """
    The make_item_editable function makes the selected item in the playlist editable.
    The function is called when a user double clicks on an item in the playlist.

    :param self: Used to Access the attributes and methods of the class in which it is used.
    :return: None.
    """
    index = self.listWidget_playlist_items.currentIndex()
    if index.isValid():
        item = self.listWidget_playlist_items.itemFromIndex(index)
        if not item.isSelected():
            item.setSelected(True)
        self.listWidget_playlist_items.edit(index)


def output_list_from_playlist_ids(self) -> list:
    """
    The output_list_from_playlist_ids function returns a list of the items in the playlist.
    It is called by other functions to get a list of the items in the playlist.

    :param self: Used to Access the class attributes.
    :return: A list of all the playlist items in the playlist.
    """
    playlist = self.listWidget_playlist_items
    return [playlist.item(x).text() for x in range(playlist.count())]


def remove_duplicates_from_playlist(self) -> None:
    """
    The remove_duplicates_from_playlist function removes any duplicates from the playlist.
    It does this by creating a list of all the items in the playlist,
    and then removing any duplicates from that list.
    The function then generates a dictionary containing only those items which are not duplicated,
    and finally imports those back into the GUI.

    :param self: Used to Access the objects and methods of the class.
    :return: None.
    """
    logging.debug("Remove duplicates from playlist:")
    playlist = output_list_from_playlist_ids(self)
    logging.debug(playlist)

    playlist_without_duplicates = list(dict.fromkeys(playlist))

    ytplaylist_dict = generate_dict_from_fields(
        self.lineEdit_playlist_title.text(),
        playlist_without_duplicates,
    )

    self.listWidget_playlist_items.clear()
    import_from_dict(self, ytplaylist_dict)
    dialogs.show_info_dialog(self, "Success!", "Any duplicates have been deleted.")

    if not playlist_widget_has_x_or_more_items(self, 1):
        self.actionClear_all_items.setEnabled(False)

    if not playlist_widget_has_x_or_more_items(self, 2):
        self.actionRemove_duplicates.setEnabled(False)
        self.menuSort_items.setEnabled(False)
        self.actionAscending.setEnabled(False)
        self.actionDescending.setEnabled(False)

    if not playlist_widget_has_x_or_more_items(self, 3):
        self.pushButton_shuffle_playlist.setEnabled(False)


def import_from_dict(self, ytplaylist_dict: dict) -> None:
    """
    The import_from_dict function takes a dictionary as an argument
    and loads the values into the fields in the application.

    :param self: Used to Access the class attributes.
    :param ytplaylist_dict:dict: Used to Get the content from the dictionary.
    :return: None.
    """
    playlist_title = ytplaylist_dict["playlistTitle"]
    playlist_ids = ytplaylist_dict["playlistIDs"]

    self.lineEdit_playlist_title.setText(playlist_title)
    logging.debug(playlist_ids)
    self.listWidget_playlist_items.addItems(playlist_ids)


def check_if_items_in_playlist(self) -> bool:
    """
    The check_if_items_in_playlist function checks if there are any items in the playlist.
    It returns True if there is at least one item, and False otherwise.

    :param self: Used to Access the attributes of the class.
    :return: A boolean value.
    """
    number_of_items = self.listWidget_playlist_items.count()
    logging.debug("Playlist items count: %s", number_of_items)
    return number_of_items >= 1


def generate_dict_from_fields(playlist_title: str, playlist_ids: list) -> dict:
    """
    The generate_dict_from_fields function takes a playlist title and list of IDs as arguments.
    It returns a dictionary with the playlist title as the key and the list of IDs as its value.

    :param playlist_title:str: Used to Store the playlist title.
    :param playlist_ids:list: Used to Store the list of song ids that are to be added to a playlist.
    :return: A dictionary with the playlist title and a list of ids.
    """
    return {"playlistTitle": playlist_title, "playlistIDs": playlist_ids}


def generate_video_ids_url(self, comma_separated_string: str) -> None:
    """
    The generate_video_ids_url function generates the video ids URL from a comma separated string.
    If no playlist title is given, it will generate the URL with no title.
    If there is a space in the playlist title, it will replace all spaces with underscores
    and add %20 for each space. Otherwise, if there are no spaces in the playlist title,
    it will add %20 after every comma.

    :param self: Used to Access the class variables.
    :param comma_separated_string:str: Used to Pass the comma separated string from the
    TextEdit_playlist_urls.
    :return: The url of the playlist.
    """
    if self.lineEdit_playlist_title.text() == "":
        video_ids_url = url.create_playlist_url(comma_separated_string, "", False)

    elif check_string.has_space_in_string(self.lineEdit_playlist_title.text()):
        title_no_spaces = replace_string.replace_space_in_string(
            self.lineEdit_playlist_title.text()
        )
        video_ids_url = url.create_playlist_url(
            comma_separated_string, title_no_spaces, True
        )
    else:
        video_ids_url = url.create_playlist_url(
            comma_separated_string, self.lineEdit_playlist_title.text(), True
        )
    playlist_url = generate_url.playlist_url(self, video_ids_url)
    if playlist_url != "":
        self.textEdit_playlist_generated_url.setText(playlist_url)
        self.textEdit_playlist_generated_url.setEnabled(True)
        self.pushButton_copy.setEnabled(True)
        self.actionCopy_URL.setEnabled(True)
        open_url.in_webbrowser(playlist_url)


def generate_playlist(self) -> None:
    """
    The generate_playlist function generates a playlist URL from the items in the playlist widget.
    The function also enables the copy button once a playlist has been generated.

    :param self: Used to Access the class attributes.
    :return: None.
    """
    if not is_playlist_widget_empty(self):
        playlist_widget = self.listWidget_playlist_items
        playlist_items = [
            playlist_widget.item(x).text() for x in range(playlist_widget.count())
        ]

        comma_separated_string = replace_string.create_comma_separated_string(
            playlist_items
        )
        generate_video_ids_url(self, comma_separated_string)
