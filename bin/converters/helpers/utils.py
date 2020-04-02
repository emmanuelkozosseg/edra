import re

_RE_SONG_NUMBER = re.compile(r'^([a-z]?)([0-9]+)[a-z]*$', re.IGNORECASE)


def pad_song_number(song_no):
    m = _RE_SONG_NUMBER.match(song_no)
    if not m:
        raise Exception("Unsupported song number: {}".format(song_no))
    prefix, number = m.groups()
    if not prefix and len(number) < 3:
        number = "0" * (3 - len(number)) + number
    if prefix and len(number) < 2:
        number = "0" * (2 - len(number)) + number
    return prefix + number
