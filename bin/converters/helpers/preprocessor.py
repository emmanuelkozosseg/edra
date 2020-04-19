from converters.features.chords import NoGuitarChords
from converters.features.verseorder import NoVerseOrders
import collections
import re


class SongPreprocessor:
    """Preprocesses a song's object."""

    _RE_LINE_SYMBOLS = re.compile(r" ?[|] ?")

    def __init__(self):
        # Set up default feature processors
        self._processors = {
            "chords": NoGuitarChords(),
            "order": NoVerseOrders(),
        }

    def set_required_features(self, *args):
        """Sets the feature processors needed by the converter.
        They override the default / previously assigned processors for their respective features
        (only one processor can be active for a feature at a time).

        :param args: list of required feature processors
        :return: None
        """
        for processor in args:
            self._processors[processor.get_feature()] = processor

    def preprocess(self, song_yaml,
                   soft_line_break_strategy=None,
                   hard_break_strategy=None):
        """
        Preprocesses the song YAML, performing common tasks.
        If options are omitted or passed as None, then they won't be performed.
        :param song_yaml: the song's object
        :param soft_line_break_strategy: 'break': breaks the lines on soft line breaks, 'ignore': ignores soft line breaks
        :param hard_break_strategy: 'convert': converts the hard break into a normal one
        :return:
        """
        for processor in self._processors.values():
            processor.process_song(song_yaml)
        for lang in song_yaml['lyrics']:
            for processor in self._processors.values():
                processor.process_lyrics(lang)
            for verse in lang['verses']:
                for processor in self._processors.values():
                    processor.process_verse(verse)
                if soft_line_break_strategy is not None:
                    self._process_soft_line_breaks(verse, soft_line_break_strategy)
                if hard_break_strategy is not None:
                    self._process_hard_breaks(verse, hard_break_strategy)

    def _process_soft_line_breaks(self, verse, mode):
        if mode == 'break':
            split_lines = (self._RE_LINE_SYMBOLS.split(l) if l is not None else [None] for l in verse['lines'])
            verse['lines'] = [l for split_line in split_lines for l in split_line]
        elif mode == 'ignore':
            for i, line in enumerate(verse['lines']):
                if line is None:
                    continue
                if isinstance(line, collections.Mapping):
                    for j, group_line in enumerate(line['lines']):
                        line['lines'][j] = self._RE_LINE_SYMBOLS.sub(' ', group_line)
                else:
                    verse['lines'][i] = self._RE_LINE_SYMBOLS.sub(' ', line)
        else:
            raise Exception("Unknown soft line break strategy '{}'. Possible values are: break, ignore".format(mode))

    @staticmethod
    def _process_hard_breaks(verse, mode):
        if mode == 'convert':
            for i, line in enumerate(verse['lines']):
                if line is None:
                    verse['lines'][i] = ''
        else:
            raise Exception("Unknown hard line break strategy '{}'. Possible value is: convert".format(mode))
