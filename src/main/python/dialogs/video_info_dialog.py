"""dialogs.video_info_dialog module"""

import sys
import urllib

from PyQt6 import uic
from PyQt6.QtGui import QFont, QIcon, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QDialog
from fbs_runtime.application_context.PyQt6 import ApplicationContext

from settings.settings import APP_ICON


app = QApplication(sys.argv)
app_context = ApplicationContext()


class VideoInfoDialog(QDialog):
    """
    Class for the settings dialog with all its components and functions.
    """

    def __init__(self, app, app_context, video_information, parent=None) -> None:
        """
        The __init__ function is called automatically every time
        the class is being used to create a new object.
        The first argument of every class method, including init,
        is always a reference to the current instance of the class.
        By convention, this argument is always named self.
        In init __self__ refers to the newly created object; in other
        class methods, it refers to the instance whose method was called.

        :param self: Used to Access the attributes and methods of the class.
        :param parent=None: Used to Ensure that the dialog box does not close when it is launched.
        :return: None.
        """

        super().__init__(parent)
        uic.loadUi(
            app_context.get_resource("forms/video_info_dialog.ui"),
            self,
        )
        self.setWindowIcon(QIcon(app_context.get_resource(APP_ICON)))
        self.setFont(QFont("Roboto"))

        self.translate_video_info_dialog()
        self.fill_out_info(video_information)

    def fill_out_info(self, video_information) -> None:
        """
        The fill_out_info function fills out the information of a video in the GUI.
        It takes as input a dictionary containing all of the information about that video,
        and then fills out each label with that information.

        :param self: Used to Access the class attributes.
        :param video_information: Used to Pass the video information dictionary to the function.
        :return: None.
        """
        self.load_thumbnail(video_information)
        self.lbl_length.setText(str(video_information["length"]))
        self.lbl_title.setText(video_information["title"])
        self.lbl_publish_date.setText(str(video_information["publish_date"]))
        self.lbl_author.setText(video_information["author"])
        self.textBrowser_description.setText(video_information["description"])
        self.lbl_keywords.setText(str(video_information["keywords"]))

    def load_thumbnail(self, video_information) -> None:
        """
        The load_thumbnail function loads the thumbnail image for a video.
        It takes in a dictionary containing the thumbnail url,
        and uses that to load the thumbnail image.

        :param self: Used to Access variables that belongs to the class.
        :param video_information: Used to Get the thumbnail url from the video_information dict.
        :return: None.
        """
        url = video_information["thumbnail_url"]

        with urllib.request.urlopen(url) as response:
            data = response.read()

        img = QImage()
        img.loadFromData(data)
        self.lbl_thumbnail.setPixmap(QPixmap(img))

    def translate_video_info_dialog(self) -> None:
        """
        The translate_video_info_dialog function is used to translate the VideoInfoDialog.

        :param self: Used to Access the attributes and methods of the class.
        :return: None.
        """
        self.setWindowTitle(
            app.translate("VideoInfoDialog", "Video information"),
        )
