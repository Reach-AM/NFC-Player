# Run this command to activate the environment, from PowerShell:
#  PS C:\>  .venv\Scripts\Activate.ps1
# or from CMD
#  C:\>  .venv\Scripts\activate.bat
import sys
import time

from player import *

from PyQt5.QtCore import QTimer
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
    #lTitle = None
    bBack = bPlayPause = bNext = None

    def __init__(self, playlist):
        super().__init__()
        lTitle = QLabel()
        self.player = Player(playlist, lTitle)

        self.setWindowTitle("Daft Punk")
        self.setFixedSize(500, 600)

        # Create layouts
        vlayout = QVBoxLayout()
        hlayout = QGridLayout()

        # Set image in label
        label = QLabel()
        pixmap = QPixmap('assets/img/dft.jpg')
        label.setPixmap(pixmap)

        # Set title label
        lTitle.setText(self.player.playlist[self.player.no]['title'])

        # Back button
        self.bBack = QPushButton("⏮️");
        self.bBack.setFont(QFont('Arial', 23))
        self.bBack.clicked.connect(self.back_pressed)

        # Play / Pause button
        self.bPlayPause = QPushButton("⏯");
        self.bPlayPause.setFont(QFont('Arial', 23))
        self.bPlayPause.clicked.connect(self.playpause_pressed)

        # Next button
        self.bNext = QPushButton("⏭️");
        self.bNext.setFont(QFont('Arial', 23))
        self.bNext.clicked.connect(self.next_pressed)

        # Add widgets to the hlayout
        hlayout.addWidget(self.bBack, 0, 0)
        hlayout.addWidget(self.bPlayPause, 0, 1)
        hlayout.addWidget(self.bNext, 0, 2)

        # Add widgets to the vlayout
        vlayout.addWidget(label)
        vlayout.addWidget(lTitle)
        vlayout.addLayout(hlayout)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window(playlist)
    window.show()
    sys.exit(app.exec_())

#album = Album(playlist)

#for song in Album.playlist:
#    audio = vlc.MediaPlayer(song['url'])
#    print(song['title'])
#    audio.play()
#    time.sleep(song['length'])
