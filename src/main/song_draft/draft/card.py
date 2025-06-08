"""
Main class for the relevant features of a card
"""


class Card():
    card_types = ["cmd", "tc", "cu", "ncu", "att"]
    def __init__(self, card_str = "default card", card_ids=[], costs=[], card_type = None):

        self.card_str = card_str
        self.card_ids = card_ids
        self.costs = costs

        if card_type not in self.card_types:
            raise Exception("Faulty card type! {0} not in {1}".format(self.card_types, card_type))

        self.card_type = card_type

    def __str__(self):
        return "{0} - {1} - {2}".format(self.card_str, self.card_ids, self.costs)

    def get_component_ids(self):
        return self.card_ids
