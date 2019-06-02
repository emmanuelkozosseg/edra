import collections
import json
import logging
import ruamel.yaml

from converters.base import AbstractConverter


class JsonConverter(AbstractConverter):
    def __init__(self, args):
        super().__init__()
        self._from_dir = args.from_dir
        self._to_file = args.to
        self._songs = []

    @staticmethod
    def add_argparser(subparsers):
        parser_json = subparsers.add_parser("json", help="Converts to JSON format.")
        parser_json.add_argument("--from-dir", required=True, help="directory where the Emmet.yaml files reside")
        parser_json.add_argument("--to", required=True, help="target file")
        parser_json.set_defaults(converter=JsonConverter)

    def convert(self, song_yaml, filepath):
        self._preprocessor.preprocess(song_yaml, flatten=True, soft_line_break_strategy='ignore')

        self._songs.append(song_yaml)

    def finish(self):
        books_yaml = self.read_books(self._from_dir)

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
