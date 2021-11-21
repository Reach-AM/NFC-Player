import re
import urllib.request
import pafy

def getAlbum(playlist):
    html = urllib.request.urlopen('https://www.youtube.com/playlist?list=PLxws1M2-zjAPNbXeJrH_TTstwSQdm9KZ4')
        html = urllib.request.urlopen(playlist)
    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())

    links = []
    for i in video_ids:
        if i not in links: links.append(i)

    for i,link in enumerate(links):
        links[i] = 'https://www.youtube.com/watch?v=' + link

    album = []
    for link in links:
        song = []
        media = pafy.new(link)
        best = media.getbestaudio()
        song.append(media.title)
        song.append(best.url)
        song.append(media._length)
        album.append(song) link

    return album
