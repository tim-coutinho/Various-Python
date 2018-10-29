from contextlib import contextmanager

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError


@contextmanager
def open_audio(song):
    """Automatically save audio file once done editing."""
    try:
        audio = EasyID3(song)
        yield audio
    except ID3NoHeaderError:
        yield
    else:
        audio.save()
