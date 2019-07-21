import collections
import re


class SongPreprocessor:
    _RE_LINE_SYMBOLS = re.compile(r" ?[|] ?")

    def preprocess(self, song_yaml,
                   flatten=False,
                   soft_line_break_strategy=None,
                   hard_break_strategy=None):
        """
        Preprocesses the song YAML, performing common tasks.
        If options are omitted or passed as None, then they won't be performed.
        :param song_yaml: the song's object
        :param flatten: if True, then repeat groups will be flattened and chords will be removed
        :param soft_line_break_strategy: 'break': breaks the lines on soft line breaks, 'ignore': ignores soft line breaks
        :param hard_break_strategy: 'convert': converts the hard break into a normal one
        :return:
        """
        for lang in song_yaml['lyrics']:
            for verse in lang['verses']:
                if flatten:
                    self._flatten_verse(verse)
                if soft_line_break_strategy is not None:
                    self._process_soft_line_breaks(verse, soft_line_break_strategy)
                if hard_break_strategy is not None:
                    self._process_hard_breaks(verse, hard_break_strategy)

        del song_yaml['chords']

    @staticmethod
    def _flatten_verse(verse):
        # Skip if there are no blocks
        if next((l for l in verse['lines'] if isinstance(l, collections.Mapping)), None) is None:
            return

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

    def _process_soft_line_breaks(self, verse, mode):
        if mode == 'break':
            split_lines = (self._RE_LINE_SYMBOLS.split(l) for l in verse['lines'] if l is not None)
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
