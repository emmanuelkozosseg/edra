from converters.features.base import FeatureProcessor
import collections
import re


"""
Processors for guitar chord related Emmet.yaml constructs (chords, repeat groups and chord anchors).
Read class names like: "I need [ClassName]"
By default, "I need NoGuitarChords"
"""


class GuitarChordsWithAllFeatures(FeatureProcessor):
    """Keeps everything as is."""
    def __init__(self):
        super().__init__("chords")


class GuitarChordsWithoutPositioning(FeatureProcessor):
    """Removes chord anchors from the lyrics, thus losing the ability to position the chords within the lines."""

    _RE_CHORD_ANCHORS = re.compile(r"\^")
    _RE_MULTIPLE_SPACES = re.compile(r" {2,}")

    def __init__(self):
        super().__init__("chords")

    def process_verse(self, verse):
        self._remove_chord_anchors(verse)

    def _remove_chord_anchors(self, verse):
        for i, line in enumerate(verse['lines']):
            if line is None:
                continue
            verse['lines'][i] = self._RE_MULTIPLE_SPACES.sub(" ", self._RE_CHORD_ANCHORS.sub("", line)).strip()


class NoGuitarChords(GuitarChordsWithoutPositioning):
    """Removes chord anchors, repeat groups and guitar chords (as without repeat groups, they are unusable)."""

    def process_song(self, song):
        if 'chords' in song:
            del song['chords']

    def process_verse(self, verse):
        self._flatten_verse(verse)
        self._remove_chord_anchors(verse)

    @staticmethod
    def _flatten_verse(verse):
        # Skip if there are no blocks
        if next((line for line in verse['lines'] if isinstance(line, collections.Mapping)), None) is None:
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
