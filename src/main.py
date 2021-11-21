# Run this command to activate the environment, from PowerShell:
#  PS C:\>  .venv\Scripts\Activate.ps1
# or from CMD
#  C:\>  .venv\Scripts\activate.bat
#
# Run this command to install all the packages required:
#   PS C:\> pip install -r requirements.txt
import os
os.add_dll_directory(os.getcwd())

import time
import vlc

html = urllib.request.urlopen('https://www.youtube.com/playlist?list=PLxws1M2-zjAPNbXeJrH_TTstwSQdm9KZ4')
video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())

album = []
for i in video_ids:
    if i not in album: album.append(i)

for i,song in enumerate(album):
    album[i] = 'https://www.youtube.com/watch?v=' + song

for song in album:
    media = pafy.new(song)
    best = media.getbestaudio()
    audio = vlc.MediaPlayer(best.url)
    print(media.title)
    audio.play()
    time.sleep(media._length)
