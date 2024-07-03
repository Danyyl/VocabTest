import re
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from main import MyMainWindow


class MyWelcomeWindow(QMainWindow):
    def __init__(self):
        super(MyWelcomeWindow, self).__init__()
        self.initUI()

    def initUI(self) -> None:
        self.resize(900, 600)
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        #  Define styles
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(20)
        font.setItalic(True)

        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(230, 220, 271, 51))
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("color: rgb(32, 74, 135);")
        self.comboBox.setObjectName("comboBox")
        items = self.get_languages()
        self.comboBox.addItems(items)
        self.comboBox.setCurrentText(items[0])

        self.mainText = QtWidgets.QLabel(self.centralWidget)
        self.mainText.setGeometry(QtCore.QRect(90, 40, 600, 181))
        self.mainText.setFont(font)
        self.mainText.setStyleSheet("color: rgb(32, 74, 135);")
        self.mainText.setAlignment(QtCore.Qt.AlignCenter)
        self.mainText.setObjectName("mainText")
        self.mainText.setText("Please enter your name and pick language\n and start test after")

        self.mainButton = QtWidgets.QPushButton(self.centralWidget)
        self.mainButton.setGeometry(QtCore.QRect(300, 410, 201, 61))
        self.mainButton.setFont(font)
        self.mainButton.setStyleSheet("color: rgb(32, 74, 135);")
        self.mainButton.setObjectName("mainButton")
        self.mainButton.clicked.connect(self.click_main_button)
        self.mainButton.setText("Start")

        self.userName = QtWidgets.QTextEdit(self.centralWidget)
        self.userName.setGeometry(QtCore.QRect(230, 280, 351, 70))
        self.userName.setFont(font)
        self.userName.setStyleSheet("color: rgb(32, 74, 135);")
        self.userName.setObjectName("userName")

        self.setCentralWidget(self.centralWidget)

    def click_main_button(self) -> None:
        if not self.userName.toPlainText():
            self.mainText.setText(
                "You did not enter your name!\nPlease enter your name"
            )
        else:
            self.main_window = MyMainWindow(
                name=self.userName.toPlainText(),
                language=self.comboBox.currentText()
            )
            self.main_window.show()
            self.close()

    def get_languages(self) -> list:
        result = []
        template = re.compile(r'(.+)\.csv')
        for file in os.listdir("data"):
            m = template.match(file)
            if m:
                result.append(m.group(1))
        return result
