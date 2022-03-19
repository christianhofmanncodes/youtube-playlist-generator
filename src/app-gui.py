import sys
from PyQt6 import uic
from PyQt6.QtGui import QClipboard
from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QApplication,
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
)
from qt_material import apply_stylesheet


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("src/gui/form.ui", self)
        self.pushButton_add.clicked.connect(self.addButtonPressed)
        self.pushButton_copy.clicked.connect(self.copyButtonPressed)
        self.pushButton_import.clicked.connect(self.importButtonPressed)
        self.pushButton_export.clicked.connect(self.exportButtonPressed)
        self.pushButton_generate.clicked.connect(self.generateButtonPressed)
        self.pushButton_delete_item.clicked.connect(self.deleteItemButtonClicked)
        self.pushButton_clear_playlist.clicked.connect(self.clearPlaylistButtonClicked)

    def addButtonPressed(self):
        text = self.textEdit_url_id.toPlainText()
        if text != "":
            self.listWidget_playlist_items.addItem(str(text))
            self.textEdit_url_id.clear()

    def clearPlaylistButtonClicked(self):
        self.listWidget_playlist_items.clear()

    def deleteItemButtonClicked(self):
        listItems = self.listWidget_playlist_items.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.listWidget_playlist_items.takeItem(
                self.listWidget_playlist_items.row(item)
            )

    def copyButtonPressed(self):
        # self.textEdit_playlist_generated_url.setText("Test")
        text = self.textEdit_playlist_generated_url.toPlainText()
        QApplication.clipboard().setText(text)

    def importButtonPressed(self):
        import_dlg = QFileDialog(self)
        import_dlg.setWindowTitle("Please import your playlist-file")
        import_dlg.exec()

    def exportButtonPressed(self):
        export_dlg = QFileDialog(self)
        export_dlg.setWindowTitle(
            "Please define a location to export your playlist-file"
        )
        export_dlg.exec()

    def generateButtonPressed(self):
        self.textEdit_playlist_generated_url.setText("Button 'Generate' clicked!")


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_red.xml")
    window = Ui()
    window.show()  # show window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
