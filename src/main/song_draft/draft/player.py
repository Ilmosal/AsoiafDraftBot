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
                    plr_str += card.get_card_string() + "\n"

        return plr_str

    async def make_choice(self, booster, round_n, turn_n):
        raise Exception("Do not use the Player stub!")

    async def trigger_end_message(self, main = None):
        raise Exception("Do not use the Player stub!")

class BotPlayer(Player):
    """
    Class for a dummy bot player that makes random choices
    """
    async def make_choice(self, booster, round_n, turn_n):
        """
        Make a random choice
        """
        card_i = random.randint(0, len(booster.get_cards())-1)
        self.choose_card(booster.pick_card(card_i))

        return True

    async def trigger_end_message(self, main = None):
        pass

class TermPlayer(Player):
    """
    Player playing through terminal for testing purposes
    """
    async def make_choice(self, booster, round_n, turn_n):
        incorrect_answer = True

        print("# Round {0} - Pick {1} - {2} cards this pick\n".format(round_n, turn_n, 8-turn_n))
        print(booster)

        prompt = int(input())

        self.choose_card(booster.pick_card(prompt))
        return True

    async def trigger_end_message(self, main = None):
        print(self)

class PickButton(discord.ui.View):
    def __init__(self, player, card_id, dt):
        self.player = player
        self.card_id = card_id
        super().__init__()
        self.dt = dt

    @discord.ui.button(label="Pick Card", style=discord.ButtonStyle.primary, row=0)
    async def button_callback(self, button, interaction):
        await interaction.response.defer()
        await self.dt.pick_card_for_player(self.player.name, self.card_id+1)

class ShowPlayerButton(discord.ui.View):
    def __init__(self, player):
        self.player = player
        super().__init__()

    @discord.ui.button(label="Show Cards", style=discord.ButtonStyle.success, row=0)
    async def button_callback(self, button, interaction):
        await interaction.response.defer()
        await self.player.show_cards(condensed=True)

class DiscordPlayer(Player):
    """
    PLayer playing through discord.
    """
    def __init__(self, name, author, dt):
        self.author = author
        super().__init__(name)
        self.thread = None
        self.dt = dt
        self.choices = []
        self.button_choices = []

    def set_thread(self, thread):
        self.thread = thread

    def get_author(self):
        return self.author

    async def remove_buttons(self):
        for c_msg, choice in self.button_choices:
            await choice.edit(view=None)

    async def show_cards(self, condensed):
        msg = "# Picked cards:\n"
        c_type_dict = {
            'cmd': 'Commanders',
            'tc': 'Tactics Cards',
            'cu': 'Combat Unis',
            'ncu': 'Non-Combat Units',
            'att': 'Attachments'
        }

        if condensed:
            for card_type in Card.card_types:
                msg += "__**{0}**__:\n".format(c_type_dict[card_type])

                for card in self.choices:
                    if card.card_type == card_type:
                        msg += " - " + card.get_card_string(with_link = False) + "\n"
            await self.thread.send(msg)
        else:
            await self.thread.send(msg)
            for card_type in Card.card_types:
                msg = "__**{0}**__:".format(c_type_dict[card_type])
                await self.thread.send(msg)

                for card in self.choices:
                    if card.card_type == card_type:
                        await self.thread.send(card.get_card_string(with_link = True))

    async def trigger_end_message(self, main = None):
        msg = "# {0} Cards\n".format(self.name)

        c_type_dict = {
            'cmd': 'Commanders',
            'tc': 'Tactics Cards',
            'cu': 'Combat Unis',
            'ncu': 'Non-Combat Units',
            'att': 'Attachments'
        }

        for card_type in Card.card_types:
            msg += "__**{0}**__:\n".format(c_type_dict[card_type])

            for card in self.choices:
                if card.card_type == card_type:
                    msg += " - " + card.get_card_string(with_link = False) + "\n"

        await main.send(msg)

    async def make_choice(self, booster, round_n, turn_n):
        choice_message = "# Round {0} - Pick {1} - {2} cards this pick\n".format(round_n, turn_n, 8-turn_n)
        await self.thread.send(choice_message)
        self.button_choices.clear()

        for card_i in range(len(booster.get_cards())):
            choice_message = "__**Card {0}**__\n".format(card_i+1)
            choice_message += booster.get_cards()[card_i].get_card_string(with_link=True)
            self.button_choices.append([choice_message, await self.thread.send(choice_message, view=PickButton(player=self, card_id=card_i, dt=self.dt))])

        await self.thread.send("Show picked cards", view=ShowPlayerButton(player=self))
