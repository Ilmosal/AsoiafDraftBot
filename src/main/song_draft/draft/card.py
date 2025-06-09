"""
Main class for the relevant features of a card
"""

class Card():
    card_types = ["cmd", "tc", "cu", "ncu", "att"]
    def __init__(self, card_str = [], card_ids=[], costs=[], card_type = None):
        self.card_str = card_str
        self.card_ids = card_ids
        self.card_costs = costs

        if card_type not in self.card_types:
            raise Exception("Faulty card type! {0} not in {1}".format(self.card_types, card_type))

        self.card_type = card_type

    def __str__(self):
        return self.get_card_string()

    def get_component_ids(self):
        return self.card_ids

    def get_card_string(self, with_link=False):
        ret_str = ""
        for i in range(len(self.card_str)):
            c_str = self.card_str[i]
            if self.card_costs[i].strip() != "-":
                c_str += " - {0} pt".format(self.card_costs[i].strip())

            if with_link:
                c_str = "[{0}](https://asoiaf-stats.com/images/2025/{1}.jpg)".format(c_str, self.card_ids[i].strip())

            ret_str += c_str

            if i+1 != len(self.card_str):
                ret_str += ", "

        return ret_str
