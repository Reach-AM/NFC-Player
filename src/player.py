import pafy
import random
import re
import urllib.request
import vlc

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel

class Player:
    tracks = []
    playlist = []
    label = None
    player = None
    current = None
    no = 0

    def __init__(self, url, label):
            self.label = label
            html = urllib.request.urlopen(url)
            video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())

            links = []
            for i,link in enumerate(video_ids):
                if link not in links:
                    song = []

                    media = pafy.new('https://www.youtube.com/watch?v=' + link)
                    best = media.getbestaudio()

                    song = {
                        'number': i,
                        'title': media.title,
                        'url': best.url,
                        'length': media._length
                    }
                    links.append(link)
                    self.tracks.append(song)
            del links

            self.playlist = self.tracks[:]
            self.current = QTimer()
            self.current.timeout.connect(lambda: self.playNext())
            self.playSong()
            #if shuffle: random.shuffle(self.playlist)


    def playPause(self):
        if self.player.is_playing():
            self.player.pause()
            self.current.stop()
        else:
            self.player.play()
            remaining = self.playlist[self.no]['length'] * 1000 - self.player.get_time() + 1000
            self.current.start(remaining)

    def playNext(self, auto = True):
        self.no += 1
        self.current.stop()
        if self.no < len(self.playlist):
            self.player.stop()
            self.playSong()
        else: self.no -+ 1

    def playSong(self):
        num = self.no
        self.label.setText(self.playlist[num]['title'])
        self.player = vlc.MediaPlayer(self.playlist [num]['url'])
        if self.no == num:
            self.player.play()
            self.current.start((self.playlist[num]['length']+1)*1000)
            self.current.singleShot(5000, lambda: self.vlc_success_check(num))

    def playBack(self):
        time = self.player.get_time()/1000
        if time < 5: self.no -= 1
        if self.no < 0: self.no = 0
        self.player.stop()
        self.current.stop()
        self.playSong()

    def vlc_success_check(self, num):
        if not self.player.is_playing() and self.no == num:
            self.current.stop()
            self.player = vlc.MediaPlayer(self.playlist [num]['url'])
            self.player.play()
            self.current.start((self.playlist[self.no]['length']+1)*1000)
            self.current.singleShot(5000, lambda: self.vlc_success_check(num))
