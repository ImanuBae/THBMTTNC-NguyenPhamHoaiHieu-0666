# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

UI_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(UI_DIR, '..'))

sys.path = [
    path for path in sys.path
    if os.path.abspath(path or os.getcwd()) != UI_DIR
]
sys.path.insert(0, PROJECT_DIR)

from cipher.ecc import ECCCipher


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.ecc_cipher = ECCCipher()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(545, 395)
        MainWindow.setMinimumSize(QtCore.QSize(545, 395))

        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(130, 15, 170, 45))
        title_font = QtGui.QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_font.setWeight(75)
        self.title_label.setFont(title_font)
        self.title_label.setObjectName("title_label")

        self.btn_generate = QtWidgets.QPushButton(self.centralwidget)
        self.btn_generate.setGeometry(QtCore.QRect(315, 22, 110, 27))
        self.btn_generate.setObjectName("btn_generate")

        self.information_label = QtWidgets.QLabel(self.centralwidget)
        self.information_label.setGeometry(QtCore.QRect(22, 90, 90, 25))
        self.information_label.setObjectName("information_label")

        self.information_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.information_text.setGeometry(QtCore.QRect(120, 70, 400, 85))
        self.information_text.setObjectName("information_text")

        self.signature_label = QtWidgets.QLabel(self.centralwidget)
        self.signature_label.setGeometry(QtCore.QRect(22, 190, 90, 25))
        self.signature_label.setObjectName("signature_label")

        self.signature_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.signature_text.setGeometry(QtCore.QRect(120, 170, 400, 85))
        self.signature_text.setObjectName("signature_text")

        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setGeometry(QtCore.QRect(182, 305, 88, 28))
        self.btn_sign.setObjectName("btn_sign")

        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setGeometry(QtCore.QRect(376, 305, 88, 28))
        self.btn_verify.setObjectName("btn_verify")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connect_events()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ECC Cipher"))
        self.title_label.setText(_translate("MainWindow", "ECC CIPHER"))
        self.btn_generate.setText(_translate("MainWindow", "Generate Keys"))
        self.information_label.setText(_translate("MainWindow", "Information:"))
        self.signature_label.setText(_translate("MainWindow", "Signature:"))
        self.btn_sign.setText(_translate("MainWindow", "Sign"))
        self.btn_verify.setText(_translate("MainWindow", "Verify"))

    def connect_events(self):
        self.btn_generate.clicked.connect(self.generate_keys)
        self.btn_sign.clicked.connect(self.sign_message)
        self.btn_verify.clicked.connect(self.verify_signature)

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(None, "ECC Error", message)

    def generate_keys(self):
        self.ecc_cipher.generate_keys()
        self.information_text.setPlainText("ECC keys generated successfully")

    def sign_message(self):
        message = self.information_text.toPlainText()
        if not message:
            self.show_error("Please enter information.")
            return

        try:
            private_key, _ = self.ecc_cipher.load_keys()
            signature = self.ecc_cipher.sign(message, private_key)
        except FileNotFoundError:
            self.show_error("Please generate keys first.")
            return
        except Exception as error:
            self.show_error(str(error))
            return

        self.signature_text.setPlainText(signature.hex())

    def verify_signature(self):
        message = self.information_text.toPlainText()
        signature_hex = self.signature_text.toPlainText().strip()
        if not message or not signature_hex:
            self.show_error("Please enter information and signature.")
            return

        try:
            signature = bytes.fromhex(signature_hex)
            _, public_key = self.ecc_cipher.load_keys()
        except ValueError:
            self.show_error("Signature must be a hex string.")
            return
        except FileNotFoundError:
            self.show_error("Please generate keys first.")
            return
        except Exception as error:
            self.show_error(str(error))
            return

        if self.ecc_cipher.verify(message, signature, public_key):
            self.information_text.setPlainText(message + "\n\nSignature is valid")
        else:
            self.information_text.setPlainText(message + "\n\nSignature is invalid")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
