from PyQt5 import QtWidgets
import sys
from mainGUI import MainApp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
