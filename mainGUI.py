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
import protocol

M = b's'
T = b't'

class SocketListener(QtCore.QThread):
    new_response = QtCore.pyqtSignal(str)
    new_response_bytes = QtCore.pyqtSignal(bytes)

    def __init__(self, sock, is_on_task_tab_callback):
        super().__init__()
        self.sock = sock
        self.running = True
        self.is_on_task_tab = is_on_task_tab_callback

    def run(self):
        while self.running:
            try:
                if self.is_on_task_tab():
                    time.sleep(0.05)
                else:
                    data = self.sock.recv(1024)
                    if not data:
                        continue
                    self.new_response_bytes.emit(data)
                    reponse = data.decode('utf-8', errors='ignore').strip().replace('\x00', '')
                    if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
                        reponse = reponse[5:]
                    self.new_response.emit(reponse)
                time.sleep(0.25)
            except Exception as e:
                print("Erreur de réception :", e)

    def stop(self):
        self.running = False


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sock = sock

        self.on_task_tab = False
        self.ui.tabtool_encoding.currentChanged.connect(self.on_tab_changed)

        self.ui.pushButton_normal.clicked.connect(self.envoyer_normal)
        self.ui.pushButton_shift_key.clicked.connect(self.envoyer_key_shift)
        self.ui.pushButton_shift.clicked.connect(self.envoyer_shift)
        self.ui.pushButton_vigenere_key.clicked.connect(self.envoyer_vigenere_key)
        self.ui.pushButton_vigenere.clicked.connect(self.envoyer_vigenere)
        self.ui.pushButton_port.clicked.connect(self.connect_to_server)

        self.vigenere_key = None

        self.ui.pushButton_shift_task.clicked.connect(lambda: self.run_task("task shift encode 10", shift.encode))
        self.ui.pushButton_vigenere_task.clicked.connect(lambda: self.run_task("task vigenere encode 10", Vigenere.encode))
        self.ui.pushButton_dh_task.clicked.connect(lambda: self.run_task("task DifHel", dh.decrypt))
        self.ui.pushButton_RSA_encode_task.clicked.connect(lambda: self.run_task("task RSA encode 10", rsa.encrypt))
        self.ui.pushButton_RSA_decode_task.clicked.connect(lambda: self.run_task("task RSA decode 10", rsa.decrypt))
        self.ui.pushButton_hash_hash_task.clicked.connect(lambda: self.run_task("task hash hash", hash.encrypt))
        self.ui.pushButton_hash_verify_task.clicked.connect(lambda: self.run_task("task hash hash", hash.encrypt))
        self.ui.pushButton_clear.clicked.connect(self.clear_chat_display)
        self.ui.pushButton_clear_2.clicked.connect(self.clear_chat_display)

    def on_tab_changed(self, index):
        tab_name = self.ui.tabtool_encoding.tabText(index)
        print(f"Onglet actuel : {tab_name}")
        self.on_task_tab = (tab_name == "Task")


    def clear_chat_display(self):
        self.ui.ChatDisplay.clear()

    def afficher_reponse_chat_display(self, message):
        self.last_response = message
        current_widget = self.ui.tabtool_encoding.currentWidget()
        if current_widget == self.ui.tab_normal:
            try:
                self.ui.ChatDisplay.append(f"[Normal] {self.last_response}")
            except Exception as e:
                print(f"Erreur send normal : {e}")
        elif current_widget == self.ui.tab_shift:
            try:
                shift_value = self.ui.lcdNumber_3.value()
                decoded_ints = shift.trans_shift_bytes(self.last_response_bytes, int(-shift_value))
                decoded_ints = send_message.byte_message(decoded_ints)
                message_str = send_message.byte_to_string(decoded_ints)
                safe_message = message_str.encode('utf-8').decode('utf-8')
                self.ui.ChatDisplay.append(f"[Shift] {safe_message}")
            except Exception as e:
                print(f"Erreur déchiffrage shift : {e}")
                self.ui.ChatDisplay.append(f"[Shift][Erreur] {message}")
        elif current_widget == self.ui.tab_vigenere:
            try:
                message = Vigenere.decrypt_vigenere(self.last_response_bytes, self.vigenere_key)
                message = send_message.byte_message(message)
                message = send_message.byte_to_string(message)
                self.ui.ChatDisplay.append(f"[Vigenere] {message}")
            except Exception as e:
                print(f"Erreur déchiffrage Vigenere : {e}")
                self.ui.ChatDisplay.append(f"[Vigenere][Erreur] {message}")
        else:
            self.ui.ChatDisplay.append(f"[Normal] {message}")

    def afficher_reponse_task(self, message):
        self.last_response = message
        self.ui.chatTask.append(f"Réponse serveur : {message}")

    def reponse(self):
        data = self.sock.recv(1024)
        reponse = data.decode('utf-8', errors='ignore').strip().replace('\x00', '')
        if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
            reponse = reponse[5:]
        print(f"Réponse serveur : {reponse}")
        self.last_response = reponse
        self.ui.chatTask.append(f"Réponse serveur : {reponse}")
        return reponse

    def get_last_response(self):
        return self.last_response
    
    def store_last_response_bytes(self, message_bytes):
        self.last_response_bytes = message_bytes[6:]


    def run_task(self, message: str, handler_func):
        try:
            self.ui.chatTask.clear()
            message_ints = protocol.str_to_int_list(message)
            encoded_message = protocol.wrap_message(message_ints,M)
            handler_func(self.sock, encoded_message, self.reponse)
        except Exception as e:
            print(f"Erreur dans la tâche '{message}': {e}")

    def envoyer_normal(self):
        texte = self.ui.plainTextEdit_normal.toPlainText().strip()
        print(texte)
        if not texte:
            return
        try:
            self.ui.plainTextEdit_normal.clear()
            message_ints = protocol.str_to_int_list(texte)
            encoded_message = protocol.wrap_message(message_ints,T)
            self.sock.sendall(encoded_message)
        except Exception as e:
            print(f"Erreur lors de l'envoi du texte: {e}")

    def envoyer_key_shift(self):
        key = self.ui.plainTextEdit_shift_key.toPlainText().strip()
        if not key:
            return
        try:
            self.ui.plainTextEdit_shift_key.clear()
            value = int(key)
            self.ui.lcdNumber_3.display(value)
        except Exception as e:
            print(f"Erreur nbre")


    def envoyer_shift(self):
        texte = self.ui.plainTextEdit_shift.toPlainText().strip()
        if not texte:
            return
        try:
            self.ui.plainTextEdit_shift.clear()
            shift_value = self.ui.lcdNumber_3.value()
            message = shift.trans_shift(str(texte), int(shift_value))
            encoded_message = send_message.encode_message(T, message)
            self.sock.sendall(encoded_message)
        except Exception as e:
            print(f"Erreur lors de l'envoi du texte shift : {e}")

    def envoyer_vigenere_key(self):
        key = self.ui.plainTextEdit_vigenere_key.toPlainText().strip()
        if not key:
            return
        try:
            self.ui.plainTextEdit_vigenere_key.clear()
            self.ui.textBrowser_vigenere_key.clear()
            self.ui.textBrowser_vigenere_key.append(f"Clé: {key}")
            self.vigenere_key = key
        except Exception as e:
            print(f"Erreur lors de l'envoi de la clé vigenere: {e}")

    def envoyer_vigenere(self):
        texte = self.ui.plainTextEdit_vigenere.toPlainText().strip()
        key = self.vigenere_key
        if not texte:
            return
        try:
            self.ui.plainTextEdit_vigenere.clear()
            key = Vigenere.generate_key(texte, key)
            message = Vigenere.encrypt_vigenere(texte, key)
            encoded_message = send_message.encode_message(T, message)
            self.sock.sendall(encoded_message)
        except Exception as e:
            print(f"Erreur lors de l'envoi du texte vigenere: {e}")

    def connect_to_server(self):
        port = self.ui.textEdit_port.toPlainText().strip()

        try:
            port = int(port)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ADDRESS, port))
            self.ui.ChatDisplay.append(f"Connecté")

            self.socket_thread = SocketListener(self.sock, lambda: self.on_task_tab)
            self.socket_thread.new_response.connect(self.afficher_reponse_chat_display)
            self.socket_thread.new_response_bytes.connect(self.store_last_response_bytes)
            self.socket_thread.start()
        except Exception as e:
            self.ui.ChatDisplay.append(f"[Erreur] Connexion échouée : {e}")


    def closeEvent(self, event):
        self.socket_thread.stop()
        event.accept()

ADDRESS = 'vlbelintrocrypto.hevs.ch'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp(sock)
    window.show()
    sys.exit(app.exec_())