#!/usr/bin/env python3
import argparse
import os
import ruamel.yaml

from converters.opensong import OpenSongConverter
from converters.json import JsonConverter
from converters.openlyrics import OpenLyricsConverter
from converters.diatar import DiatarConverter

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

    OpenSongConverter.add_argparser(subparsers)
    JsonConverter.add_argparser(subparsers)
    OpenLyricsConverter.add_argparser(subparsers)
    DiatarConverter.add_argparser(subparsers)

    return argparser.parse_args()


if __name__ == "__main__":
    main()
