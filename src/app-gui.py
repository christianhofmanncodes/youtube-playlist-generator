import sys
from PyQt6 import QtWidgets, uic


app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("src/ui/youtube-playlist-generator/form.ui")
window.show()

app.exec()
