"""
File containing definition of player things
"""

from draft.card import Card

import random
import logging

class Player():
    """
    The basis for the player class. Extend for other use cases
    """
    def __init__(self, name):
        self.name = name
        self.choices = []

    def choose_card(self, card):
        self.choices.append(card)

    def __str__(self):
        plr_str = "{0}\n---------\n".format(self.name)
        for card_type in Card.card_types:
            plr_str += "\n{0}\n--------\n".format(card_type)
            for card in self.choices:
                if card.card_type == card_type:
                    plr_str += str(card) + "\n"

        return plr_str

    def make_choice(self, booster):
        raise Exception("Do not use the Player stub!")

class BotPlayer(Player):
    """
    Class for a dummy bot player that makes random choices
    """
    def make_choice(self, booster):
        """
        Make a random choice
        """
        card_i = random.randint(0, len(booster.get_cards())-1)
        self.choose_card(booster.pick_card(card_i))

        return True

class TermPlayer(Player):
    """
    Player playing through terminal for testing purposes
    """
    def make_choice(self, booster):
        incorrect_answer = True

        print("Make a choice!")
        print(booster)

        prompt = int(input())

        self.choose_card(booster.pick_card(prompt))
        return True

class DiscordPlayer(Player):
    """
    PLayer playing through discord.
    """
    def __init__(self, name, discord_bot):
        self.discord_bot = discord_bot
        super.__init__(name)

    def make_choice(self, booster):
        pass
