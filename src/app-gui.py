import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QApplication,
    QWidget,
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

    def addButtonPressed(self):
        self.textEdit_url_id.setText("Button 'Add' clicked!")

    def copyButtonPressed(self):
        self.textEdit_playlist_generated_url.setText("Button 'Copy' clicked!")


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_red.xml")
    window = Ui()
    window.show()  # show window
    sys.exit(app.exec())

    # app = QtWidgets.QApplication(sys.argv)
    # window = uic.loadUi("src/gui/form.ui")
    # apply_stylesheet(app, theme="dark_red.xml")
    # window.show()

    # app.exec()


if __name__ == "__main__":
    main()
