import os
import hashlib
from datetime import datetime
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from bidi import algorithm as bidialg
import arabic_reshaper
import matplotlib.pyplot as plt
import pandas as pd

from result import MyResultWindow

NUM_OF_WORDS = 20


def plot_text(text, file_path, font_name):
    plt.text(
        0.5,
        0.5,
        text,
        family=[font_name],
        fontsize=34,
        weight='black',
        horizontalalignment='center', verticalalignment='center')
    plt.axis('off')
    plt.savefig(file_path)
    plt.close()
    plt.cla()


class MyMainWindow(QMainWindow):
    def __init__(self, name: str, language: str):
        super(MyMainWindow, self).__init__()
        self.name = name
        self.language = language
        self.data_df = None
        self.result_df = None
        self.current_index = -1
        self.result_folder = ""
        self.initUI()

    def initUI(self) -> None:
        self.prepare_data()
        self.stimulies = self._get_stimuli()
        self.stimuli = next(self.stimulies)

        self.resize(900, 600)
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        #  Define styles
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(20)
        font.setItalic(True)

        self.imageLabel = QtWidgets.QLabel(self.centralWidget)
        self.imageLabel.setGeometry(QtCore.QRect(180, 70, 471, 191))
        self.imageLabel.setText("")
        self.imageLabel.setPixmap(
            QtGui.QPixmap(f"{self.get_result_folder()}/images/{self.stimuli['hash']}.svg"))
        self.imageLabel.setObjectName("imageLabel")
        
        self.real = QtWidgets.QPushButton(self.centralWidget)
        self.real.setGeometry(QtCore.QRect(670, 430, 101, 71))
        self.real.setFont(font)
        self.real.setStyleSheet("color: rgb(32, 74, 135);")
        self.real.setObjectName("real")
        self.real.setText("Real")
        self.real.clicked.connect(partial(self.process_action, "real"))
        
        
        self.fake = QtWidgets.QPushButton(self.centralWidget)
        self.fake.setGeometry(QtCore.QRect(30, 450, 101, 71))
        self.fake.setFont(font)
        self.fake.setAutoFillBackground(False)
        self.fake.setStyleSheet("color: rgb(32, 74, 135);")
        self.fake.setObjectName("fake")
        self.fake.setText("Fake")
        self.fake.clicked.connect(partial(self.process_action, "fake"))
        
        self.tips = QtWidgets.QLabel(self.centralWidget)
        self.tips.setGeometry(QtCore.QRect(90, 340, 720, 91))
        self.tips.setFont(font)
        self.tips.setStyleSheet("color: rgb(32, 74, 135);")
        self.tips.setAlignment(QtCore.Qt.AlignCenter)
        self.tips.setObjectName("tips")
        self.tips.setText(
            f"Hello, {self.name} please choose real or fake word.\n You can "
            f"do it with buttons or with keys \"r\" or \"f\""
        )
        
        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setGeometry(QtCore.QRect(190, 450, 451, 23))
        self.progressBar.setStyleSheet("color: rgb(32, 74, 135);")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.setCentralWidget(self.centralWidget)

    def keyPressEvent(self, event):
        if event.key() == 82:
            self.process_action("real")
        if event.key() == 70:
            self.process_action("fake")

    def process_action(self, answer) -> None:
        result = 1 if answer == "real" else 0
        self.result_df.loc[self.current_index, "real_answer"] = result
        try:
            self.stimuli = next(self.stimulies)
        except StopIteration:
            self._close()
        self.imageLabel.setPixmap(QtGui.QPixmap(
            f"{self.get_result_folder()}/images/{self.stimuli['hash']}.svg"
        ))


    def prepare_data(self) -> None:
        self.data_df = pd.read_csv(f"data/{self.language}.csv")
        self.data_df = self.data_df.sample(NUM_OF_WORDS, ignore_index=True, replace=False)
        self.result_df = pd.DataFrame(
            columns=(
                "hash", "stimuli", "correct_answer", "real_answer", "language"
            )
        )
        if self.language in ['ar', 'fa', 'ug', 'ur']:
            font_name = 'Noto Sans Arabic'
        elif self.language == "got":
            font_name = 'Noto Sans Gothic'
        elif self.language in ['he', 'yi']:
            font_name = 'Noto Sans Hebrew'
        elif self.language in ['hi', 'mr', 'sa']:
            font_name = 'Noto Sans Devanagari'
        elif self.language in ["hy", "hyw"]:
            font_name = 'Noto Sans Armenian'
        elif self.language == 'ja':
            font_name = 'Noto Sans JP'
        elif self.language == 'ko':
            font_name = 'Noto Sans KR Black'
        elif self.language == 'ta':
            font_name = 'Noto Sans Tamil'
        elif self.language == 'te':
            font_name = 'Noto Sans Telugu'
        elif self.language == 'zh':
            font_name = 'Noto Sans SC Black'
        else:
            font_name = 'Inter'

        for _, row in self.data_df.iterrows():
            text = row.stimulus

            # hash the text to get a unique filename
            hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            res = {
                "hash": hash,
                "stimuli": text,
                "correct_answer": 1 if row.correct_answer == "correct" else 0,
                "real_answer": -1,  # to make sure that it has been answered in future
                "language": self.language
            }
            self.result_df = self.result_df._append(
                res,
                ignore_index=True
            )
            img_dir = f'{self.get_result_folder()}/images'
            os.makedirs(img_dir, exist_ok=True)
            img_name = f'{img_dir}/{hash}.svg'
            if self.language == 'ar':
                text = arabic_reshaper.reshape(text)
            plot_text(bidialg.get_display(text), img_name, font_name)

    def get_result_folder(self) -> str:
        if not self.result_folder:
            self.result_folder = (
                f"results/{self.name}-{datetime.now().isoformat()}"
            )
        return self.result_folder

    def _get_stimuli(self):
        for index, raw in self.result_df.iterrows():
            self.current_index = index
            if self.current_index > 0:
                percent = int(self.current_index / NUM_OF_WORDS * 100)
                self.progressBar.setProperty("value", percent)
            yield raw

    def save_results(self) -> None:
        self.result_df.to_csv(
            f"{self.get_result_folder()}/data.csv", index=False
        )

    def _close(self) -> None:
        self.save_results()
        self.result_window = MyResultWindow(
            name=self.name,
            result=self.prepared_results
        )
        self.result_window.show()
        self.close()

    @property
    def prepared_results(self) -> dict:
        self.result_df["is_right"] = (
            self.result_df["correct_answer"] == self.result_df["real_answer"]
        ).astype(int)
        incorrect_data = self.result_df[self.result_df["correct_answer"] == 0]
        correct_data = self.result_df[self.result_df["correct_answer"] == 1]
        result = {
            "total": round((self.result_df["is_right"] == 1).sum() / len(self.result_df), 2),
            "correct": round((correct_data["is_right"] == 1).sum() / len(correct_data), 2),
            "incorrect": round((incorrect_data["is_right"] == 1).sum() / len(incorrect_data), 2),
        }
        return result
