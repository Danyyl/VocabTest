from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class MyResultWindow(QMainWindow):
    def __init__(self, name, result):
        super(MyResultWindow, self).__init__()
        self.name = name
        self.result = result
        self.initUI()

    def initUI(self) -> None:
        self.resize(900, 600)
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)

        self.resultLabel = QtWidgets.QLabel(self.centralWidget)
        self.resultLabel.setGeometry(QtCore.QRect(90, 50, 600, 400))
        self.resultLabel.setFont(font)
        self.resultLabel.setStyleSheet("color: rgb(32, 74, 135);")
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLabel.setObjectName("result")
        self.resultLabel.setText(f"Dear, {self.name}\nYour result - \n{self.format_result()}")

        self.setCentralWidget(self.centralWidget)

    def format_result(self) -> str:
        return (
            f"Score with real words - {self.result['correct'] * 100}%\n"
            f"Score with fake words - {self.result['incorrect'] * 100}%\n"
            f"Total score - {self.result['total'] * 100}%\n"
        )

