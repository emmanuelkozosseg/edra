import errno
import os
import re
from xml.etree import ElementTree

from converters.base import AbstractConverter


class OpenSongConverter(AbstractConverter):
    _RE_SONG_NUMBER = re.compile(r'^([a-z]?)([0-9]+)[a-z]*$', re.IGNORECASE)

    def __init__(self, args):
        super().__init__()
        self._from_dir = args.from_dir
        self._out_dir = args.to_dir
        self._books = None

    @staticmethod
    def create_argparser(subparsers):
        parser_opensong = subparsers.add_parser("opensong", help="Converts to OpenSong format.")
        parser_opensong.add_argument("--to-dir", required=True, help="directory of target files; will be deleted if exists")
        return parser_opensong

    def setup(self):
        self._create_out_dir(self._out_dir)

        books = self.read_books(self._from_dir)
        self._books = {b['id']: b for b in books}

    def convert(self, song_yaml, filepath):
        if not song_yaml['books']:
            raise Exception("No books are specified in song '{}'.".format(filepath))

        self._preprocessor.preprocess(song_yaml, flatten=True, soft_line_break_strategy='break')

        for book in song_yaml['books']:
            # Continue if this is just a "marker book"
            if 'lang' not in book:
                continue

            # Look for the language of this book
            lang_yaml = self._get_lyrics_from_yaml(song_yaml, book['lang'])
            if lang_yaml is None:
                raise Exception("Book {} in song '{}' uses undefined language {}.".format(book['id'], filepath, book['lang']))

            # Convert lang
            song_xml = self._lang_to_osxml(lang_yaml, book['number'])

            song_xml_filename = self._pad_song_number_for_filename(book['number']) + " " + lang_yaml['title'].replace(".", "") + ".xml"

            song_xml_dirpath = os.path.join(self._out_dir, self._books[book['id']]['name'])
            self._mkdirs_ignore_if_exists(song_xml_dirpath)

            song_xml.write(os.path.join(song_xml_dirpath, song_xml_filename), encoding='utf-8')

    def _lang_to_osxml(self, lang_yaml, song_no):
        os_song = ElementTree.Element('song')

        os_title = ElementTree.SubElement(os_song, 'title')
        os_title.text = lang_yaml['title']

        os_hymn_number = ElementTree.SubElement(os_song, 'hymn_number')
        os_hymn_number.text = song_no

        os_lyrics = ElementTree.SubElement(os_song, 'lyrics')
        os_lyrics.text = self._assemble_os_lyrics(lang_yaml['verses'])

        self._add_empty_elements(os_song, ['author', 'copyright', 'presentation', 'ccli', 'key', 'aka', 'key_line', 'ccli',
                                           'user1', 'user2', 'user3', 'theme', 'linked_songs', 'tempo', 'time_sig'])
        ElementTree.SubElement(os_song, 'capo', {'print': 'false'})
        ElementTree.SubElement(os_song, 'backgrounds', {'resize': 'screen', 'keep_aspect': 'false', 'link': 'false', 'background_as_text': 'false'})

        return ElementTree.ElementTree(os_song)

    @staticmethod
    def _assemble_os_lyrics(verses_yaml):
        os_lyrics_lines = []
        for verse_yaml in verses_yaml:
            # Empty line between verses
            if os_lyrics_lines:
                os_lyrics_lines.append("")

            os_lyrics_lines.append('[' + verse_yaml['name'].upper() + ']')
            for i, line in enumerate(verse_yaml['lines']):
                if line is None:  # Hard break -- separate slide
                    os_lyrics_lines.append(' ||')
                elif line == "" and i != 0:  # Soft break -- empty line
                    os_lyrics_lines[-1] = os_lyrics_lines[-1] + " |"
                else:
                    os_lyrics_lines.append(' '+line)

        return "\n".join(os_lyrics_lines)

    @staticmethod
    def _add_empty_elements(parent, element_names):
        for name in element_names:
            ElementTree.SubElement(parent, name)

    def _pad_song_number_for_filename(self, song_no):
        m = self._RE_SONG_NUMBER.match(song_no)
        if not m:
            raise Exception("Unsupported song number: {}".format(song_no))
        prefix, number = m.groups()
        if not prefix and len(number) < 3:
            number = "0" * (3-len(number)) + number
        if prefix and len(number) < 2:
            number = "0" * (2-len(number)) + number
        return prefix + number
    
    @staticmethod
    def _mkdirs_ignore_if_exists(dirpath):
        try:
            os.makedirs(dirpath)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise