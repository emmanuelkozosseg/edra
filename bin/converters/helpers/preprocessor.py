import collections
import re


class SongPreprocessor:
    _RE_LINE_SYMBOLS = re.compile(r" ?[|] ?")

    def preprocess(self, song_yaml, flatten=False, soft_line_break_strategy=None):
        for lang in song_yaml['lyrics']:
            for verse in lang['verses']:
                if flatten:
                    self._flatten_verse(verse)
                if soft_line_break_strategy is not None:
                    self._process_soft_line_breaks(verse, soft_line_break_strategy)

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
                verse['lines'][i] = self._RE_LINE_SYMBOLS.sub(' ', line)
        else:
            raise Exception("Unknown soft line break strategy '{}'. Possible values are: break, ignore".format(mode))
