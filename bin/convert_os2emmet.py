#!/usr/bin/python3
import argparse
from xml.etree import ElementTree
import os
import ruamel.yaml
from ruamel.yaml import YAML
import re
from collections import OrderedDict


_RE_WHITESPACE = re.compile(r"\s")
_RE_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9-]")
_RE_SONG_NO_FORMATTER = re.compile(r"^([A-Z]*)0*([0-9]+)$")


def main():
    parser = argparse.ArgumentParser(description="Converts OpenSong lyrics to Emmet's format.")
    parser.add_argument("--from-dir", required=True, help="Directory where the OpenSong files reside.")
    parser.add_argument("--to-dir", required=True, help="Directory where the Emmet format songs should be placed.")
    args = parser.parse_args()

    yaml = YAML()
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)

    for opensong_file in (f for f in os.listdir(args.from_dir) if f.endswith(".xml")):
        # Read XML
        os_xml = ElementTree.parse(os.path.join(args.from_dir, opensong_file)).getroot()
        song_title = os_xml.find("title").text.strip()
        lyrics = os_xml.find("lyrics").text
        song_no = os_xml.find("hymn_number").text
        if song_no is not None:
            song_no = song_no.strip()
            song_no = _RE_SONG_NO_FORMATTER.sub(r"\1\2", song_no)

        # Generate filename
        song_filename = song_title.lower()
        song_filename = _RE_WHITESPACE.sub("-", song_filename)
        song_filename = song_filename.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ö", "o") \
            .replace("ő", "o").replace("ú", "u").replace("ü", "u").replace("ű", "u")
        song_filename = _RE_NON_ALPHANUMERIC.sub("", song_filename)
        if song_no is not None:
            song_filename = song_no + "-" + song_filename
            # TODO: pad with zeroes
        song_filename += ".yaml"

        # Parse lyrics
        song_verses = []
        current_verse = None
        for lyric_line in lyrics.split("\n"):
            lyric_line = lyric_line.strip()
            if not lyric_line:
                continue

            if lyric_line.startswith("["):
                current_verse = _create_verse(lyric_line[1:-1].lower(), song_verses)
            elif lyric_line.startswith("||"):
                current_verse["lines"].append(None)
            else:
                if current_verse is None:
                    current_verse = _create_verse("v1", song_verses)
                current_verse["lines"].append(lyric_line)

        # Create and write yaml
        lang_obj = ruamel.yaml.comments.CommentedMap(OrderedDict())
        lang_obj['lang'] = "hu"
        lang_obj['title'] = song_title
        lang_obj['verses'] = song_verses

        song_yaml = ruamel.yaml.comments.CommentedMap(OrderedDict())
        song_yaml["books"] = []
        if song_no is not None:
            song_book = ruamel.yaml.comments.CommentedMap(OrderedDict())
            song_book['id'] = 'emmet'
            song_book['number'] = song_no
            song_yaml["books"].append(song_book)
        song_yaml["lyrics"] = [lang_obj]

        with open(os.path.join(args.to_dir, song_filename), "w") as f:
            print("Writing file: "+song_filename)
            yaml.dump(song_yaml, stream=f)

    print("Done.")


def _create_verse(name, verse_list):
    current_verse = ruamel.yaml.comments.CommentedMap(OrderedDict())
    current_verse["name"] = name
    current_verse["lines"] = []
    verse_list.append(current_verse)
    return current_verse


if __name__ == '__main__':
    main()
