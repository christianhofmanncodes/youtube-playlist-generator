"""module playlist.playlist"""

import logging
import random

from strings import check_string, replace_string
from url import generate_url, open_url, url
from dialogs import dialogs


def shuffle(self) -> None:
    """Shuffle playlist with random.shuffle()."""
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
    """Return number of items in playlist as int."""
    playlist = self.listWidget_playlist_items
    return len([playlist.item(x) for x in range(playlist.count())])


def playlist_widget_has_x_or_more_items(self, number: int) -> bool:
    """Return True if one ore more items in playlist."""
    return number_of_playlist_items(self) >= number


def is_playlist_widget_empty(self) -> bool:
    """Return True if no items in the playlist."""
    return number_of_playlist_items(self) == 0


def make_item_editable(self) -> None:
    """Make item in playlist editable."""
    index = self.listWidget_playlist_items.currentIndex()
    if index.isValid():
        item = self.listWidget_playlist_items.itemFromIndex(index)
        if not item.isSelected():
            item.setSelected(True)
        self.listWidget_playlist_items.edit(index)


def output_list_from_playlist_ids(self) -> list:
    """Return playlist items as a list."""
    playlist = self.listWidget_playlist_items
    return [playlist.item(x).text() for x in range(playlist.count())]


def remove_duplicates_from_playlist(self) -> None:
    """If playlist contains duplicated items remove them from the list."""
    logging.debug("Remove duplicates from playlist:")
    dialogs.show_info_dialog(self, "Success!", "Any duplicates have been deleted.")
    playlist = output_list_from_playlist_ids(self)
    logging.debug(playlist)

    playlist_without_duplicates = list(dict.fromkeys(playlist))

    ytplaylist_dict = generate_dict_from_fields(
        self.lineEdit_playlist_title.text(),
        playlist_without_duplicates,
    )

    self.listWidget_playlist_items.clear()
    import_from_dict(self, ytplaylist_dict)

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
    """Get content from dict and load it into the fields in the application."""
    playlist_title = ytplaylist_dict["playlistTitle"]
    playlist_ids = ytplaylist_dict["playlistIDs"]

    self.lineEdit_playlist_title.setText(playlist_title)
    logging.debug(playlist_ids)
    self.listWidget_playlist_items.addItems(playlist_ids)


def check_if_items_in_playlist(self) -> bool:
    """Returns True if more than one item in playlist."""
    number_of_items = self.listWidget_playlist_items.count()
    logging.debug("Playlist items count: %s", number_of_items)
    return number_of_items >= 1


def generate_dict_from_fields(playlist_title: str, playlist_ids: list) -> dict:
    """Return playlist items and title as dict."""
    return {"playlistTitle": playlist_title, "playlistIDs": playlist_ids}


def generate_video_ids_url(self, comma_separated_string: str) -> None:
    """Generate the video ids URL from a comma separated string."""
    if self.lineEdit_playlist_title.text() == "":
        video_ids_url = url.create_playlist_url(comma_separated_string, "", False)

    elif check_string.has_space_in_string(self.lineEdit_playlist_title.text()):
        title_no_spaces = strings.replace_string.replace_space_in_string(
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
    """Generate playlist URL and enable copy button."""
    if not is_playlist_widget_empty(self):
        playlist_widget = self.listWidget_playlist_items
        playlist_items = [
            playlist_widget.item(x).text() for x in range(playlist_widget.count())
        ]

        comma_separated_string = replace_string.create_comma_separated_string(
            playlist_items
        )
        generate_video_ids_url(self, comma_separated_string)
