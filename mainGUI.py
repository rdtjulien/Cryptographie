from PyQt5 import QtWidgets, QtCore
from GUI import Ui_MainWindow
import socket
import sys
import time
import shift
import Vigenere
import connect
import send_message

M = b's'

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
        self.sock = sock

        self.socket_thread = SocketListener(sock)
        self.socket_thread.new_response.connect(self.afficher_reponse)
        self.ui.pushButton_7.clicked.connect(self.task_shift)
        self.ui.pushButton_6.clicked.connect(self.task_vigenere)
        self.ui.pushButton_5.clicked.connect(self.task_dh)
        self.ui.pushButton_4.clicked.connect(self.task_RSA_encode)
        self.ui.pushButton_3.clicked.connect(self.task_RSA_decode)

        self.socket_thread.start()

    def task_shift(self):
        try:
            TASK = "shift"
            TYPE = "encode"
            LENGTH = 10
            message = f"task {TASK} {TYPE} {LENGTH}"
            message_ints = send_message.message_to_int(message)
            encoded_message = send_message.encode_message(M, message_ints)

            #self.sock.sendall(encoded_message)

            shift.encode(self.sock, self.afficher_reponse, encoded_message)

        except Exception as e:
            print("Erreur dans shift encode :", e)

    def task_vigenere(self):
        try:
            TASK = "vigenere"
            TYPE = "encode"
            LENGTH = 10
            message = f"task {TASK} {TYPE} {LENGTH}"
            message_ints = send_message.message_to_int(message)
            encoded_message = send_message.encode_message(M, message_ints)

            #self.sock.sendall(encoded_message)

            Vigenere.encode(self.sock, self.afficher_reponse, encoded_message)

        except Exception as e:
            print("Erreur dans shift encode :", e)

    def task_RSA_encode(self):
        print()
    
    def task_RSA_decode(self):
        print()
    
    def task_dh(self):
        print()

    def task_hash_hash(self):
        print()
    
    def task_hash_verify(self):
        print()

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
