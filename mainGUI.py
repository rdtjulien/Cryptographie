from PyQt5 import QtWidgets, QtCore
from GUI import Ui_MainWindow
import socket
import sys
import time
import shift
import Vigenere
import connect
import send_message
import rsa
import dh
import hash

M = b's'

class SocketListener(QtCore.QThread):
    new_response = QtCore.pyqtSignal(str)

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.running = True

#timer chat a revoir

    #def run(self):
    #    while self.running:
    #        try:
    #            data = self.sock.recv(1024)
    #            if not data:
    #                continue
    #            reponse = data.decode('utf-8', errors='ignore').strip().replace('\x00', '')
    #            if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
    #                reponse = reponse[5:]
    #            self.new_response.emit(reponse)
    #        except Exception as e:
    #            print("Erreur de réception :", e)
    #        time.sleep(0.25)

    def stop(self):
        self.running = False
        self.wait()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self, sock):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sock = sock

        self.socket_thread = SocketListener(sock)
        self.socket_thread.new_response.connect(self.afficher_reponse)

        self.ui.pushButton_7.clicked.connect(lambda: self.run_task("task shift encode 10", shift.encode))
        self.ui.pushButton_6.clicked.connect(lambda: self.run_task("task vigenere encode 10", Vigenere.encode))
        self.ui.pushButton_5.clicked.connect(lambda: self.run_task("task DifHel", dh.decrypt))
        self.ui.pushButton_4.clicked.connect(lambda: self.run_task("task RSA encode 10", rsa.encrypt))
        self.ui.pushButton_3.clicked.connect(lambda: self.run_task("task RSA decode 10", rsa.decrypt))
        self.ui.pushButton_8.clicked.connect(lambda: self.run_task("task hash hash", hash.encrypt))
        self.ui.pushButton_9.clicked.connect(lambda: self.run_task("task hash hash", hash.encrypt))  # changer 

        self.ui.pushButton_10.clicked.connect(self.clear_chat)

        self.socket_thread.start()

    def clear_chat(self):
        self.ui.ChatDisplay.clear()

    def afficher_reponse(self, message):
        self.last_response = message
        self.ui.ChatDisplay.append(f"Réponse serveur : {message}")

    def reponse(self):
        data = sock.recv(1024)
        reponse = data.decode('utf-8', errors='ignore').strip().replace('\x00', '')

        if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
            reponse = reponse[5:]

        print(f"Réponse serveur : {reponse}")
        self.last_response = reponse
        self.ui.ChatDisplay.append(f"Réponse serveur : {reponse}")
        return reponse

    def get_last_response(self):
        return self.last_response

    def run_task(self, message: str, handler_func):
        try:
            message_ints = send_message.message_to_int(message)
            encoded_message = send_message.encode_message(M, message_ints)
            handler_func(self.sock, self.reponse, encoded_message)
        except Exception as e:
            print(f"Erreur dans la tâche '{message}': {e}")

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