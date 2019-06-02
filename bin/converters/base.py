from abc import abstractmethod
import collections
import logging
import os
import re
import ruamel.yaml
import shutil
from converters.helpers.preprocessor import SongPreprocessor


class AbstractConverter:
    _RE_LINE_SYMBOLS = re.compile(r" ?[|] ?")

    def __init__(self):
        self._preprocessor = SongPreprocessor()

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
    