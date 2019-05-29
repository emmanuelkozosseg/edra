from abc import abstractmethod
import collections
import logging
import os
import re
import ruamel.yaml
import shutil


class AbstractConverter:
    _RE_LINE_SYMBOLS = re.compile(r" ?[|] ?")

    def setup(self):
        pass

    @abstractmethod
    def convert(self, song_yaml, filepath):
        pass

    def finish(self):
        pass

    @staticmethod
    def read_books(song_dir):
        logging.info("Reading _books.yaml...")
        with open(os.path.join(song_dir, "_books.yaml"), "rt") as f:
            books_yaml = ruamel.yaml.YAML().load(f)
        return books_yaml

    @staticmethod
    def _create_out_dir(out_dir):
        if os.path.exists(out_dir):
            logging.info("The '{}' directory exists, removing...".format(out_dir))
            shutil.rmtree(out_dir)
        logging.info("Creating directory '{}'...".format(out_dir))
        os.mkdir(out_dir)

    @staticmethod
    def _flatten(song_yaml):
        """
        Flattens the song lyrics (flattens groups and removes guitar chords).
        :param song_yaml:
        :return:
        """
        for lang in song_yaml['lyrics']:
            for verse in lang['verses']:
                # Skip if there are no blocks
                if next((l for l in verse['lines'] if isinstance(l, collections.Mapping)), None) is None:
                    continue

                # Copy to new array
                new_lines = []
                for line in verse['lines']:
                    if isinstance(line, collections.Mapping):
                        group_lines = line['lines']
                        group_lines[0] = '/: ' + group_lines[0]
                        group_lines[-1] += ' :/'
                        new_lines.extend(group_lines)
                    else:
                        new_lines.append(line)
                verse['lines'] = new_lines
        del song_yaml['chords']

    @staticmethod
    def _clean_verse_line(line):
        return AbstractConverter._RE_LINE_SYMBOLS.sub(" ", line)

    @staticmethod
    def _split_verse_on_hard_breaks(lines):
        result = []
        first_unprocessed = 0
        for i in range(len(lines)):
            if lines[i] is None:
                result.append(lines[first_unprocessed:i])
                first_unprocessed = i+1
        if first_unprocessed == 0:
            result.append(lines)
        else:
            result.append(lines[first_unprocessed:])
        return result
    