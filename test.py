from PyQt5 import QtWidgets, QtCore
from GUI import Ui_MainWindow
import socket
import sys
import time

class SocketListener(QtCore.QThread):
    new_response = QtCore.pyqtSignal(str)

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.running = True

    def run(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    continue
                reponse = data.decode('utf-8', errors='ignore').strip().replace('\x00', '')
                if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
                    reponse = reponse[5:]
                self.new_response.emit(reponse)
            except Exception as e:
                print("Erreur de réception :", e)
            time.sleep(0.25)

    def stop(self):
        self.running = False
        self.wait()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self, sock):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.socket_thread = SocketListener(sock)
        self.socket_thread.new_response.connect(self.afficher_reponse)
        self.socket_thread.start()

    def afficher_reponse(self, message):
        self.ui.ChatDisplay.append(f"Réponse serveur : {message}")

    def closeEvent(self, event):
        self.socket_thread.stop()
        event.accept()

PORT = 6000
ADDRESS = 'vlbelintrocrypto.hevs.ch'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((ADDRESS, PORT))
    print("Connecté au serveur")
except Exception as e:
    print("Connexion échouée :", e)
    sys.exit(1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp(sock)
    window.show()
    sys.exit(app.exec_())
