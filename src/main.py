# Run this command to activate the environment, from PowerShell:
#  PS C:\>  .venv\Scripts\Activate.ps1
# or from CMD
#  C:\>  .venv\Scripts\activate.bat
import sys
import time

from player import *

from PyQt5 import QtCore
from PyQt5 import QtGui
#from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

playlist = 'https://www.youtube.com/playlist?list=PLxws1M2-zjAPNbXeJrH_TTstwSQdm9KZ4'

class Window(QWidget):
    player = None
    bBack = bPlayPause = bNext = bShuffle = bRepeat = None

    def __init__(self, playlist):
        super().__init__()
        lTitle = QLabel()
        self.bPlayPause = QPushButton("⏸️");
        self.player = Player(playlist, lTitle, self.bPlayPause)

        self.setStyleSheet("background-color: rgb(23,23,23); color : rgb(232, 232, 232);")
        self.setWindowTitle("Daft Punk")
        self.setFixedSize(520, 700)

        # Create layouts
        vlayout = QVBoxLayout()
        hlayout = QGridLayout()
        hlayout2 = QGridLayout()

        # Set image in label
        label = QLabel()
        pixmap = QPixmap('assets/img/dft.jpg')
        label.setPixmap(pixmap)

        # Set labels
        lAlbum= QLabel('Daft Punk - Random Access Memories')
        lTitle.setText(self.player.playlist[self.player.no]['title'])
        lAlbum.setFont(QFont('Lato', 14))
        lAlbum.setAlignment(QtCore.Qt.AlignCenter)
        lTitle.setFont(QFont('Lato', 10))
        lTitle.setAlignment(QtCore.Qt.AlignCenter)

        # Back button
        self.bBack = QPushButton("⏮️");
        self.bBack.setFont(QFont('Lato', 23))
        self.bBack.clicked.connect(self.back_pressed)

        # Play / Pause button
        self.bPlayPause.setFont(QFont('Lato', 23))
        self.bPlayPause.clicked.connect(self.playpause_pressed)

        # Next button
        self.bNext = QPushButton("⏭️");
        self.bNext.setFont(QFont('Lato', 23))
        self.bNext.clicked.connect(self.next_pressed)

        # Shuffle button
        self.bShuffle = QPushButton("🔀");
        self.bShuffle.setFont(QFont('Lato', 20))
        self.bShuffle.clicked.connect(self.shuffle_pressed)

        # Repeat button
        self.bRepeat = QPushButton("🔁️");
        self.bRepeat.setFont(QFont('Lato', 20))
        self.bRepeat.clicked.connect(self.repeat_pressed)

        # Add widgets to the hlayout
        hlayout.addWidget(self.bBack, 0, 0)
        hlayout.addWidget(self.bPlayPause, 0, 1)
        hlayout.addWidget(self.bNext, 0, 2)

        # Add widgets to the hlayout2
        hlayout2.addWidget(self.bShuffle, 0, 0)
        hlayout2.addWidget(self.bRepeat, 0, 1)

        # Add widgets to the vlayout
        vlayout.addWidget(lAlbum)
        vlayout.addWidget(label)
        vlayout.addWidget(lTitle)
        vlayout.addLayout(hlayout)
        vlayout.addLayout(hlayout2)

        # Set the layout on the application's window
        self.setLayout(vlayout)

    def back_pressed(self):
        self.player.playBack()
        self.bBack.setEnabled(False)
        QTimer.singleShot(1000, lambda: self.bBack.setDisabled(False))

    def next_pressed(self):
        self.player.playNext(False)
        self.bNext.setEnabled(False)
        QTimer.singleShot(1000, lambda: self.bNext.setDisabled(False))

    def playpause_pressed(self):
        self.player.playPause()
        self.bPlayPause.setEnabled(False)
        QTimer.singleShot(1000, lambda: self.bPlayPause.setDisabled(False))

    def shuffle_pressed(self):
        self.player.shuffle()
        self.bShuffle.setEnabled(False)
        QTimer.singleShot(1000, lambda: self.bShuffle.setDisabled(False))

    def repeat_pressed(self):
        self.player.repeat()
        self.bRepeat.setEnabled(False)
        QTimer.singleShot(1000, lambda: self.bRepeat.setDisabled(False))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('assets/font/Lato.ttf')
    window = Window(playlist)
    window.show()
    sys.exit(app.exec_())
