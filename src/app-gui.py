import sys
from PyQt6 import QtWidgets, uic


app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("src/gui/form.ui")
window.show()

app.exec()
