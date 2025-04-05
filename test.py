from PyQt5 import QtWidgets, QtCore
from GUI import Ui_MainWindow
import connect
import socket

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.counter = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_counter) #chaque 250ms lancer la requete de réponse
        self.timer.start(250)

    def update_counter(self):
        self.ui.ChatDisplay.append(f"Compteur : {self.counter}") #imprimer sur la box la variable de réponse
        self.counter += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
