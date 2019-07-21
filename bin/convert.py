#!/usr/bin/env python3
import argparse
import os
import ruamel.yaml

from converters.opensong import OpenSongConverter
from converters.json import JsonConverter
from converters.openlyrics import OpenLyricsConverter
from converters.diatar import DiatarConverter
from converters.emmasongs import EmmaSongsConverter
from converters.pdf import PdfConverter

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

    _enable_converter(OpenSongConverter, subparsers)
    _enable_converter(JsonConverter, subparsers)
    _enable_converter(OpenLyricsConverter, subparsers)
    _enable_converter(DiatarConverter, subparsers)
    _enable_converter(EmmaSongsConverter, subparsers)
    _enable_converter(PdfConverter, subparsers)

    return argparser.parse_args()


def _enable_converter(converter_class, subparsers):
    subparser = converter_class.create_argparser(subparsers)
    subparser.add_argument("--from-dir", required=True, help="directory where the Emmet.yaml files reside")
    subparser.set_defaults(converter=converter_class)


if __name__ == "__main__":
    main()
