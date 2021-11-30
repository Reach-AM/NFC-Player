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
    label = playbutton = None
    player = None
    current = None
    no = 0
    shff = rept = False

    def __init__(self, url, label, playbutton):
            self.label = label
            self.playbutton = playbutton
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
                        'title': media.title.split(' - ')[1].split(' (')[0],
                        'url': best.url,
                        'length': media._length,
                        'og': 'https://www.youtube.com/watch?v=' + link
                    }
                    links.append(link)
                    self.tracks.append(song)
            del links

            self.playlist = self.tracks[:]
            self.current = QTimer()
            self.current.timeout.connect(lambda: self.playNext())
            self.playSong()
            #if shuffle: random.shuffle(self.playlist)

    def __str__(self):
        str = '['
        for i, song in enumerate(self.playlist):
            if i < len(self.playlist)-1:
                str += song['title'] + ', '
            else:
                str += song['title'] + ']'
        return str

    def playPause(self):
        if self.player.is_playing():
            self.player.pause()
            self.current.stop()
            self.playbutton.setText("▶")
        else:
            self.player.play()
            remaining = self.playlist[self.no]['length'] * 1000 - self.player.get_time() + 1000
            self.current.start(remaining)
            self.playbutton.setText("⏸")

    def playNext(self, auto = True):
        self.no += 1
        self.current.stop()
        if self.no < len(self.playlist):
            self.player.stop()
            self.playSong()
        else:
            self.no = 0
            self.player.stop()
            if self.rept: self.playSong()
            else:
                self.playSong(False)
                self.playbutton.setText("▶️")

    def playSong(self, play = True):
        num = self.no
        self.label.setText(self.playlist[num]['title'])
        self.player = vlc.MediaPlayer(self.playlist [num]['url'])
        if self.no == num and play:
            self.player.play()
            self.current.start((self.playlist[num]['length']+1)*1000)
            self.playbutton.setText("⏸")
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
            self.playlist[num]['url'] = pafy.new(self.playlist[num]['og']).getbestaudio().url
            self.player = vlc.MediaPlayer(self.playlist[num]['url'])
            self.player.play()
            self.current.start((self.playlist[self.no]['length']+1)*1000)
            self.current.singleShot(5000, lambda: self.vlc_success_check(num))

    def shuffle(self):
        if not self.shff:
            nowp = self.playlist.pop(self.no)
            random.shuffle(self.playlist)
            self.playlist.insert(0,nowp)
            self.no = 0
            self.shff = True
        else:
            self.no = self.playlist[self.no]['number']
            self.playlist = self.tracks[:]
            self.shff = False

    def repeat(self):
        if self.rept: self.rept = False
        else: self.rept = True
