"""
File containing definition of player things
"""

from draft.card import Card

import discord

import random
import logging
import aiohttp
import io

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

    async def make_choice(self, booster):
        raise Exception("Do not use the Player stub!")

    async def trigger_end_message(self):
        raise Exception("Do not use the Player stub!")

class BotPlayer(Player):
    """
    Class for a dummy bot player that makes random choices
    """
    async def make_choice(self, booster):
        """
        Make a random choice
        """
        card_i = random.randint(0, len(booster.get_cards())-1)
        self.choose_card(booster.pick_card(card_i))

        return True

    async def trigger_end_message(self):
        pass

class TermPlayer(Player):
    """
    Player playing through terminal for testing purposes
    """
    async def make_choice(self, booster):
        incorrect_answer = True

        print("Make a choice!")
        print(booster)

        prompt = int(input())

        self.choose_card(booster.pick_card(prompt))
        return True

    async def trigger_end_message(self):
        print(player)

class DiscordPlayer(Player):
    """
    PLayer playing through discord.
    """
    def __init__(self, name, author):
        self.author = author
        super().__init__(name)
        self.thread = None

    def set_thread(self, thread):
        self.thread = thread

    def get_author(self):
        return self.author

    async def show_cards(self, condensed):
        await self.thread.send("Picked cards:")
        c_type_dict = {
            'cmd': 'Commanders',
            'tc': 'Tactics Cards',
            'cu': 'Combat Unis',
            'ncu': 'Non-Combat Units',
            'att': 'Attachments'
        }

        for card_type in Card.card_types:
            msg = "{0}".format(c_type_dict[card_type])
            await self.thread.send(msg)

            for card in self.choices:
                if card.card_type == card_type:
                    msg = ""
                    if condensed:
                        msg += card.card_str
                    else:
                        for ci in card.card_ids:
                            my_url = "https://asoiaf-stats.com/images/2025/{0}.jpg".format(ci.strip())
                            msg += "[{0}]({1}) ".format(card.card_str, my_url)

                    await self.thread.send(msg)



    async def trigger_end_message(self):
        await self.thread.send("Picked cards:")
        c_type_dict = {
            'cmd': 'Commanders',
            'tc': 'Tactics Cards',
            'cu': 'Combat Unis',
            'ncu': 'Non-Combat Units',
            'att': 'Attachments'
        }

        for card_type in Card.card_types:
            msg = "{0}".format(c_type_dict[card_type])
            await self.thread.send(msg)

            for card in self.choices:
                if card.card_type == card_type:
                    msg = ""
                    for ci in card.card_ids:
                        my_url = "https://asoiaf-stats.com/images/2025/{0}.jpg".format(ci.strip())
                        msg += "[{0}]({1}) ".format(card.card_str, my_url)

                    await self.thread.send(msg)

    async def make_choice(self, booster):
        choice_message = "Pick one option\n"
        await self.thread.send(choice_message)

        for card_i in range(len(booster.get_cards())):
            choice_message = "Card {0}\n".format(card_i+1)
            for card in booster.get_cards()[card_i].card_ids:
                my_url = "https://asoiaf-stats.com/images/2025/{0}.jpg".format(card.strip())
                choice_message += "[{0}]({1}) ".format(card, my_url)
            await self.thread.send(choice_message)

#            for comp in booster.get_cards()[card_i].card_ids:
#                my_url = "https://asoiaf-stats.com/images/2025/{0}.jpg".format(comp.strip())
#                async with aiohttp.ClientSession() as session:
#                    async with session.get(my_url) as resp:
#                        data = io.BytesIO(await resp.read())
#                        await self.thread.send(file=discord.File(data, '{0}.jpg'.format(comp.strip())))

