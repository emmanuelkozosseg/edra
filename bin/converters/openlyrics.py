import os
import time
from xml.etree import ElementTree

from converters.base import AbstractConverter


class OpenLyricsConverter(AbstractConverter):
    def __init__(self, args):
        super().__init__()
        self._from_dir = args.from_dir
        self._out_dir = args.to_dir

    @staticmethod
    def create_argparser(subparsers):
        parser_openlyrics = subparsers.add_parser("openlyrics", help="Converts to OpenLyrics format.")
        parser_openlyrics.add_argument("--to-dir", required=True, help="directory of target files; will be deleted if exists")
        return parser_openlyrics

    def setup(self):
        super()._create_out_dir(self._out_dir)
        ElementTree.register_namespace('', "http://openlyrics.info/namespace/2009/song")

    def convert(self, song_yaml, filepath):
        self._preprocessor.preprocess(song_yaml, flatten=True, soft_line_break_strategy='ignore')

        # Look up primary language
        emm_hu_book = next((b for b in song_yaml['books'] if b['id'] == 'emm_hu'), None)
        if emm_hu_book is None:
            return

        # Look up lyrics for primary language
        song_lyrics = next(l for l in song_yaml['lyrics'] if l['lang'] == emm_hu_book['lang'])

        # Assemble XML
        ol_song = ElementTree.Element('song', attrib={
            'version': '0.8',
            'createdIn': 'Emmet.yaml Converter',
            'modifiedIn': 'Emmet.yaml Converter',
            'modifiedDate': time.strftime("%Y-%m-%dT%H:%M:%S%z")
        })

        ol_properties = ElementTree.SubElement(ol_song, 'properties')
        ol_titles = ElementTree.SubElement(ol_properties, 'titles')
        ol_title = ElementTree.SubElement(ol_titles, 'title')
        ol_title.text = song_lyrics['title']
        ol_songbooks = ElementTree.SubElement(ol_properties, 'songbooks')
        ol_songbook = ElementTree.SubElement(ol_songbooks, 'songbook', attrib={
            'name': 'Jézus él!', 'entry': emm_hu_book['number']
        })

        ol_lyrics = ElementTree.SubElement(ol_song, 'lyrics')
        for verse in song_lyrics['verses']:
            verse_parts = self._split_verse_on_hard_breaks(verse['lines'])

            for i, verse_part in enumerate(verse_parts):
                verse_suffix = '' if len(verse_parts) == 1 else '-' + str(i+1)

                ol_verse = ElementTree.SubElement(ol_lyrics, 'verse', attrib={
                    'name': verse['name'] + verse_suffix
                })
                ol_lines = ElementTree.SubElement(ol_verse, 'lines')
                is_first = True
                for line in verse_part:
                    line = self._clean_verse_line(line)
                    if is_first:
                        ol_lines.text = line
                        is_first = False
                    else:
                        ElementTree.SubElement(ol_lines, 'br').tail = "\n"+line

        # Write XML
        ol_tree = ElementTree.ElementTree(ol_song)
        filename = "{song_no}-{lang}-{title}.xml".format(
            song_no=emm_hu_book['number'], lang=emm_hu_book['lang'], title=song_lyrics['title']
        )
        ol_tree.write(os.path.join(self._out_dir, filename), encoding='utf-8')
