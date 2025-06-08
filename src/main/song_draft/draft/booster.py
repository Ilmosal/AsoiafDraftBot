"""
File for booster related logic
"""

from draft.card import Card

class Booster():
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def pick_card(self, card_id):
        return self.cards.pop(card_id)

    def get_cards(self):
        return self.cards

    def __str__(self):
        booster_str = "Booster\n-------\n"

        for card_i in range(len(self.cards)):
            booster_str += "Card " + str(card_i) +" - "+ str(self.cards[card_i]) + "\n"

        return booster_str
