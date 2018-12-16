#!/usr/bin/env python3
import argparse
import errno
from xml.etree import ElementTree
import os
import ruamel.yaml
import json
import collections
import shutil
import re
import logging
logging.basicConfig(format="[%(asctime)s|%(levelname)s] %(message)s", level=logging.DEBUG)


def main():
    args = _parse_args()
    converter = args.converter(args)

    converter.setup()
    yaml = ruamel.yaml.YAML()
    logging.info("Processing files...")
    for root, _, files in os.walk(args.from_dir):
        for yaml_file in files:
            if not yaml_file.endswith('.yaml') or yaml_file.startswith('_'):
                continue
            yaml_file_path = os.path.join(root, yaml_file)
            with open(yaml_file_path, "rt") as f:
                song_yaml = yaml.load(f)
            converter.convert(song_yaml, filepath=yaml_file_path)
    converter.finish()

    logging.info("--- Completed. ---")


def _parse_args():
    argparser = argparse.ArgumentParser(description="Converts Emmet.yaml songs to other formats.")
    subparsers = argparser.add_subparsers()

    parser_opensong = subparsers.add_parser("opensong", help="Converts to OpenSong format.")
    parser_opensong.add_argument("--from-dir", required=True, help="directory where the Emmet.yaml files reside")
    parser_opensong.add_argument("--to-dir", required=True, help="directory of target files; will be deleted if exists")
    parser_opensong.set_defaults(converter=OpenSongConverter)

    parser_json = subparsers.add_parser("json", help="Converts to JSON format.")
    parser_json.add_argument("--from-dir", required=True, help="directory where the Emmet.yaml files reside")
    parser_json.add_argument("--to", required=True, help="target file")
    parser_json.set_defaults(converter=JsonConverter)

    return argparser.parse_args()


class AbstractConverter:
    def setup(self):
        pass

    def convert(self, song_yaml, filepath):
        pass

    def finish(self):
        pass


class OpenSongConverter(AbstractConverter):
    _RE_SONG_NUMBER = re.compile(r'^([a-z]?)([0-9]+)$', re.IGNORECASE)

    def __init__(self, args):
        self._out_dir = args.to_dir

    def setup(self):
        if os.path.exists(self._out_dir):
            logging.info("The '{}' directory exists, removing...".format(self._out_dir))
            shutil.rmtree(self._out_dir)
        logging.info("Creating directory '{}'...".format(self._out_dir))
        os.mkdir(self._out_dir)

    def convert(self, song_yaml, filepath):
        if not song_yaml['books']:
            raise Exception("No books are specified in song '{}'.".format(filepath))

        for book in song_yaml['books']:
            # Look for the language of this book
            lang_yaml = next((l for l in song_yaml['lyrics'] if l['lang'] == book['lang']), None)
            if lang_yaml is None:
                raise Exception("Book {} in song '{}' uses undefined language {}.".format(book['id'], filepath, book['lang']))

            # Convert lang
            song_xml = self._lang_to_osxml(lang_yaml, book['number'])

            song_xml_filename = self._pad_song_number_for_filename(book['number']) + " " + lang_yaml['title'].replace(".", "") + ".xml"

            song_xml_dirpath = os.path.join(self._out_dir, book['id'])
            self._mkdirs_ignore_if_exists(song_xml_dirpath)

            song_xml.write(os.path.join(song_xml_dirpath, song_xml_filename), encoding='utf-8')

        return

        main_book = next((b for b in song_yaml['books'] if b['id'] == 'emmet'), None)
        if main_book is None:
            main_book = song_yaml['books'][0]

        for lang_yaml in song_yaml['lyrics']:
            lang = lang_yaml['lang']

            song_xml = self._lang_to_osxml(lang_yaml, main_book['number'])

            song_xml_filename = self._pad_song_number_for_filename(main_book['number']) + " " + lang_yaml['title'].replace(".", "") + ".xml"

            song_xml_dirpath = os.path.join(self._out_dir, main_book['id'], lang)
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
                if line is None:
                    os_lyrics_lines.append(' ||')
                elif line == "" and i != 0:
                    os_lyrics_lines[-1] = os_lyrics_lines[-1] + " |"
                else:
                    os_lyrics_lines.append(' ' + line)

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


class JsonConverter(AbstractConverter):
    def __init__(self, args):
        self._from_dir = args.from_dir
        self._to_file = args.to
        self._songs = []

    def convert(self, song_yaml, filepath):
        self._songs.append(song_yaml)

    def finish(self):
        logging.info("Reading _books.yaml...")
        with open(os.path.join(self._from_dir, "_books.yaml"), "rt") as f:
            books_yaml = ruamel.yaml.YAML().load(f)

        logging.info("Writing to '{}'...".format(self._to_file))
        with open(self._to_file, "wt") as f:
            f.write(JsonConverter.YamlJsonEncoder(separators=(',', ':')).encode({
                "books": books_yaml,
                "songs": self._songs
            }))

    class YamlJsonEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ruamel.yaml.comments.CommentedSeq):
                return list(o)
            if isinstance(o, ruamel.yaml.comments.CommentedMap):
                d = collections.OrderedDict()
                for k, v in o.items():
                    d[k] = v
                return d
            super().default(o)


if __name__ == "__main__":
    main()
