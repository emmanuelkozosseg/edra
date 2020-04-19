class FeatureProcessor:
    """Common parent of an Emmet.yaml feature processor, which can enable/disable/enhance an Emmet.yaml feature."""

    def __init__(self, feature):
        self._feature = feature

    def get_feature(self):
        """Returns the feature's standard name. Used to identify feature processors that belong to the same feature.

        :return: the feature's standard name
        """
        return self._feature

    def process_song(self, song):
        """Processes a song on the song's level.

        :param song: the song's object
        :return: None
        """
        pass

    def process_lyrics(self, lyrics):
        """Processes a single 'lyrics' object of a song.

        :param lyrics: the 'lyrics' node
        :return: None
        """
        pass

    def process_verse(self, verse):
        """Processes a single 'verse' object of a song.

        :param verse: the 'verse' object
        :return: None
        """
        pass
