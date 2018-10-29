#!/usr/bin/env python3
from argparse import ArgumentParser
from os import listdir
from os.path import join
from time import time

from youtube_dl import YoutubeDL

from lib import open_audio


def get_args():
    parser = ArgumentParser()
    parser.add_argument('--album',
                        help='Album the songs belong to')
    parser.add_argument('--artist',
                        help='Artist of the songs')
    parser.add_argument('-g', '--genre',
                        help='Genre of the songs')
    parser.add_argument('-p', '--playlist',
                        dest='noplaylist',
                        action='store_false',
                        help='Download all songs in a playlist link')
    parser.add_argument('-y', '--year',
                        help='Year the songs were made')
    parser.add_argument('videos',
                        nargs='+',
                        help='Youtube links to the songs')
    return parser.parse_args()


def main():
    args = get_args()
    dir = join('/mnt/c/Users/t/Downloads/songs', args.album or str(int(time())))

    options = {
        'format': 'bestaudio/best',
        'noplaylist': args.noplaylist,
        'outtmpl': join(dir, '%(playlist_index)s.%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0'
        }],
        'youtube_include_dash_manifest': False
    }

    videos = args.videos
    with YoutubeDL(options) as ydl:
        ydl.download(videos)

    for song in listdir(dir):
        with open_audio(join(dir, song)) as audio:
            audio['album'] = [args.album]
            audio['artist'] = [args.artist]
            audio['albumartist'] = [args.artist]
            audio['date'] = [args.year]
            audio['genre'] = [args.genre]
            audio['title'] = [song.split('.', 1)[1].rsplit('.', 1)[0]]
            if not args.noplaylist:
                audio['tracknumber'] = [song.split('.', 1)[0]]


if __name__ == '__main__':
    main()
