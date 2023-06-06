"""module dialogs.search_dialog"""

import logging
import sys

from PyQt5 import uic
from PyQt5.QtCore import QLocale, QTranslator, Qt
from PyQt5.QtGui import QFont, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QTableWidgetItem,
)
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import requests

from dialogs.builtin_dialogs import show_warning_dialog
from playlist import video_info
from playlist.video_info import (
    get_more_search_results,
    get_video_info,
    return_video_ids_from_search_object,
)
from settings.operations import get_settings
from settings.settings import APP_ICON, SETTING_FILE_LOCATION
from strings import replace_string
from time_and_date import convert_date, convert_time

app = QApplication(sys.argv)
app_context = ApplicationContext()


class SearchDialog(QDialog):
    """
    Class for the search results dialog with all its components and functions.
    """

    def __init__(self, app_context, parent=None) -> None:
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
            app_context.get_resource("forms/search_dialog.ui"),
            self,
        )
        self.setWindowIcon(QIcon(app_context.get_resource(APP_ICON)))
        self.setFont(QFont("Roboto"))

        self.translate_ui()
        self.translate_search_results_dialog()

        self.search_results = []
        self.search_object = {}

        self.buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)

        self.lineEdit_search_field.textChanged.connect(self.act_search_field_change)
        self.toolButton_load_more_search_results.clicked.connect(
            lambda: self.button_load_more_search_results_clicked(self.search_object)
        )
        self.lineEdit_search_field.returnPressed.connect(self.search_videos)
        self.pushButton_search.clicked.connect(self.search_videos)

    def fill_out_info(self, search_results) -> None:
        """
        The fill_out_info function fills out the information of a video in the GUI.
        It takes as input a dictionary containing all of the information about that video,
        and then fills out each label with that information.

        :param self: Used to Access the class attributes.
        :param search_results: Used to Pass the search results list to the function.
        :return: None.
        """
        video_ids_list = return_video_ids_from_search_object(search_results)

        self.tableWidget_search_results.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
        )

        for row_index, video_id in enumerate(video_ids_list):
            video_info_dict = get_video_info(video_id)

            self.tableWidget_search_results.insertRow(row_index)
            self.tableWidget_search_results.setItem(
                row_index, 0, QTableWidgetItem(str(video_info_dict["title"]))
            )
            self.tableWidget_search_results.setItem(
                row_index, 1, QTableWidgetItem(str(video_info_dict["author"]))
            )
            self.tableWidget_search_results.setItem(
                row_index, 2, QTableWidgetItem(str(video_info_dict["channel_id"]))
            )
            self.tableWidget_search_results.setItem(
                row_index, 3, QTableWidgetItem(str(video_info_dict["channel_url"]))
            )
            self.tableWidget_search_results.setItem(
                row_index, 4, QTableWidgetItem(str(video_info_dict["thumbnail_url"]))
            )
            self.tableWidget_search_results.setItem(
                row_index, 5, QTableWidgetItem(str(video_info_dict["description"]))
            )
            self.tableWidget_search_results.setItem(
                row_index, 6, QTableWidgetItem(str(video_info_dict["keywords"]))
            )
            self.tableWidget_search_results.setItem(
                row_index,
                7,
                QTableWidgetItem(
                    str(
                        convert_time.convert_hours_minutes_seconds(
                            video_info_dict["length"]
                        )
                    )
                ),
            )
            self.tableWidget_search_results.setItem(
                row_index,
                8,
                QTableWidgetItem(
                    str(convert_date.format_date(video_info_dict["publish_date"]))
                ),
            )
            self.tableWidget_search_results.setItem(
                row_index, 9, QTableWidgetItem(str(video_info_dict["rating"]))
            )
            self.tableWidget_search_results.setItem(
                row_index,
                10,
                QTableWidgetItem(
                    str(replace_string.format_int_with_commas(video_info_dict["views"]))
                ),
            )
            self.tableWidget_search_results.setItem(
                row_index, 11, QTableWidgetItem(str(video_id))
            )
            item = self.tableWidget_search_results.item(row_index, 0)
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
            )
            item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidget_search_results.resizeColumnsToContents()

        self.lbl_result_count.setText(f"{len(video_ids_list)} videos found")

    def search_videos(self) -> None:
        """
        The search_videos function is called when the user clicks on the search button.
        It takes in a string from the lineEdit_search_field and passes it to video_info.py's
        search_for_videos function, which returns a tuple of two objects:
        (a Search object, and a list of Video objects).
        The first element is stored as self.searchObject,
        while each element in the second is appended to self.videoList.

        :param self: Used to Access the class attributes and methods.
        :return: Search_object and search_results.
        """
        text = self.lineEdit_search_field.text()
        if text != "":
            search_object, search_results = video_info.search_for_videos(text)
            self.search_results = search_results
            self.search_object = search_object
            self.fill_out_info(search_results)
        else:
            search_object, search_results = None, None

    def button_load_more_search_results_clicked(self, search_object) -> None:
        """
        The button_load_more_search_results_clicked function is called
        when the user clicks on the "Load More" button.
        It calls get_more_search_results to retrieve more search results
        from the API, and then fills out those results in the GUI.

        :param self: Used to Refer to the object that is calling the function.
        :param search_object: Used to Get the next page of search results.
        :return: None.
        """
        search_results = get_more_search_results(search_object)
        if search_results is not None:
            self.fill_out_info(search_results)
        else:
            show_warning_dialog(
                self, "No more search results", "There are no more search results!"
            )

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

        if url.lower().startswith("https"):
            response = requests.get(url, verify=True, timeout=1000)
            logging.debug(response.status_code)
            data = response.content

            img = QImage()
            img.loadFromData(data)
            self.lbl_thumbnail.setPixmap(QPixmap(img))
        else:
            raise ValueError from None

    def translate_search_results_dialog(self) -> None:
        """
        The translate_video_info_dialog function is used to translate the SearchDialog.

        :param self: Used to Access the attributes and methods of the class.
        :return: None.
        """
        self.setWindowTitle(
            app.translate("SearchDialog", "Search"),
        )

    def translate_ui(self):
        """Translates the UI based on language settings"""
        self.trans = QTranslator(self)

        settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)

        if settings_dict["general"][0]["programLanguage"] == "English":
            logging.info("Program language is English.")

        elif settings_dict["general"][0]["programLanguage"] == "Deutsch":
            data = app_context.get_resource("forms/translations/de/SearchDialog.qm")
            german = QLocale(QLocale.Language.German, QLocale.Country.Germany)
            self.trans.load(german, data)
            app.instance().installTranslator(self.trans)

        elif settings_dict["general"][0]["programLanguage"] == "Español":
            data = app_context.get_resource("forms/translations/es-ES/SearchDialog.qm")
            spanish = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)
            self.trans.load(spanish, data)
            app.instance().installTranslator(self.trans)

        elif settings_dict["general"][0]["programLanguage"] == "Polski":
            data = app_context.get_resource("forms/translations/pl/SearchDialog.qm")
            polish = QLocale(QLocale.Language.Polish, QLocale.Country.Poland)
            self.trans.load(polish, data)
            app.instance().installTranslator(self.trans)

    def act_search_field_change(self):
        """
        The act_search_field_change function enables the search button
        if there is text in the search field.
        If there is no text, it disables the button.

        :param self: Used to Represent the instance of the class.
        :return: A boolean value.
        """
        if self.lineEdit_search_field.text():
            self.pushButton_search.setEnabled(True)
        else:
            self.pushButton_search.setEnabled(False)
