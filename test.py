<<<<<<< HEAD
=======
from PyQt5 import QtWidgets, QtCore
from GUI import Ui_MainWindow
import connect
import socket
import send_message
import shift
import time
import Vigenere
import rsa

# Partie connection serveur
PORT = 6000
ADDRESS = 'vlbelintrocrypto.hevs.ch'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ADDRESS, PORT))
    print("Connected")
except Exception as e:
    print("Cannot connect to the server")


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.counter = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(connect.reponse()) #chaque 250ms lancer la requete de réponse
        self.timer.start(250)

    def update_counter(self):
        self.ui.ChatDisplay.append(f"Compteur : {connect.reponse}") #imprimer sur la box la variable de réponse
        self.counter += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
>>>>>>> 2db07dd56caf78cc8c3be64984e787b991733bbe
