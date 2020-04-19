from converters.features.base import FeatureProcessor
import logging
import re


"""
Processors for the verse order.
Read class names like: "I need [ClassName]"
By default, "I need NoVerseOrders"
"""


class NoVerseOrders(FeatureProcessor):
    """Removes existing verse orders from the song objects."""

    def __init__(self):
        super().__init__("order")

    def process_lyrics(self, lyrics):
        if 'order' in lyrics:
            del lyrics['order']


class ValidVerseOrdersForAllSongs(FeatureProcessor):
    """
    Verifies existing verse orders, and tries to auto-assign one if there isn't one.
    Issues a warning if auto-assignment fails. In this case, the order will be missing.
    """

    _VALID_VERSE_NAME_FOR_AUTO_ASSIGNMENT = re.compile(r"^v([0-9]+)$")

    def __init__(self):
        super().__init__("order")

    def process_lyrics(self, lyrics):
        if 'order' in lyrics:
            self._verify_order(lyrics)
        else:
            self._auto_assign_order(lyrics)

    @staticmethod
    def _verify_order(lyrics):
        verses_in_order = {v for v in lyrics['order']}
        verses_in_lyrics = {v['name'] for v in lyrics['verses']}
        if len(verses_in_order ^ verses_in_lyrics) != 0:
            raise Exception("Different verses are present in the order and the verse list.")

    def _auto_assign_order(self, lyrics):
        order = []
        chorus_seen = False
        for verse in lyrics['verses']:
            if verse['name'] == 'c':
                chorus_seen = True
                order.append(verse['name'])
            elif self._VALID_VERSE_NAME_FOR_AUTO_ASSIGNMENT.match(verse['name']):
                order.append(verse['name'])
                if chorus_seen:
                    order.append("c")
            else:
                logging.warning("Verse name '"+verse['name']+"' can't be used in auto-assignment. Not assigning an order.")
                return

        # If the assigned order is the same as the natural order (e.g. for a song without a chorus), then don't assign anything
        verses_in_order = [v['name'] for v in lyrics['verses']]
        if order == verses_in_order:
            return

        lyrics['order'] = order
