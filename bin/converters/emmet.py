import collections
import json
import logging
import ruamel.yaml

from converters.base import AbstractConverter
from converters.features.verseorder import ValidVerseOrdersForAllSongs


class EmmetJsonConverter(AbstractConverter):
    def __init__(self, args):
        super().__init__()
        self._preprocessor.set_required_features(ValidVerseOrdersForAllSongs())
        self._from_dir = args.from_dir
        self._to_file = args.to
        self._verbose = args.verbose
        self._songs = []

    @staticmethod
    def create_argparser(subparsers):
        parser_json = subparsers.add_parser("emmet-json", help="Converts to JSON format for use in Emmet.")
        parser_json.add_argument("--to", required=True, help="target file")
        parser_json.add_argument("-v", "--verbose", action="store_true", help="verbose mode")
        return parser_json

    def convert(self, song_yaml, filepath):
        if self._verbose:
            logging.info("Processing {}...".format(filepath))

        self._preprocessor.preprocess(song_yaml, soft_line_break_strategy='ignore')

        self._songs.append(song_yaml)

    def finish(self):
        books_yaml = self.read_books(self._from_dir)

        logging.info("Writing to '{}'...".format(self._to_file))
        with open(self._to_file, "wt") as f:
            f.write(EmmetJsonConverter.YamlJsonEncoder(separators=(',', ':')).encode({
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
