"""
Module containing the logic for the draft logic
"""
import logging
import random

from draft.card_pool import CardPool
from draft.player import BotPlayer, TermPlayer, DiscordPlayer
from draft.booster import Booster

class DraftTable():
    def __init__(self, draft_table_id="", player_count = -1, draft_pool = "default", allow_bots = False):
        self.draft_table_id = draft_table_id
        self.player_count = player_count
        self.draft_pool = draft_pool

        self.players = []
        self.boosters = []
        self.stage_boosters = []
        self.booster_size = -1
        self.allow_bots = allow_bots

        self.has_picked = None
        self.turn = -1
        self.direction = 0

        self.draft_stage = 0
        self.main_channel = None
        self.start_message = None

        logging.info("Table initialized!")

    async def update_start_message(self):
        msg_str = "# Game name: {0} - Player count: {1}/{2}\n".format(self.draft_table_id, len(self.get_players()), self.player_count)
        for i in range(self.player_count):
            plr_name = ""
            plr_id = -1

            try:
                plr_name = self.get_players()[i].name

                for i in range(len(self.players)):
                    if plr_name == self.players[i].name:
                        plr_id = i
                        break
            except:
                pass

            msg_str += "**{0}**. {1}".format(i+1, plr_name.capitalize())

            if self.draft_stage != 0 and plr_id != -1:
                if self.has_picked[plr_id]:
                    msg_str += " has picked!"
                else:
                    msg_str += " is picking..."

            msg_str += "\n"

        await self.start_message.edit(msg_str)

    def set_main_channel(self, main_channel):
        self.main_channel = main_channel

    def can_start_draft(self):
        return len(self.players) == self.player_count or self.allow_bots

    def get_players(self):
        pl = []
        for p in self.players:
            if isinstance(p, DiscordPlayer):
                pl.append(p)
        return pl

    def join_player(self, player_name, term_player=False, author=None):
        if player_name in [player.name for player in self.players]:
            raise Exception("Player {0} already in the table!".format(player_name))

        if len(self.players) == self.player_count:
            raise Exception("Table already full!")

        if self.draft_stage != 0:
            raise Exception("Cannot join players after draft has started!")

        if term_player:
            player = TermPlayer(player_name)
        else:
            player = DiscordPlayer(player_name, author=author, dt=self)

        self.players.append(player)
        logging.info("Added player {0}".format(player_name))

    def add_bot(self, bot_name):
        if bot_name in [player.name for player in self.players]:
            raise Exception("Bot {0} already in the table!".format(player_name))

        if len(self.players) == self.player_count:
            raise Exception("Table already full!")

        if self.draft_stage != 0:
            raise Exception("Cannot join players after draft has started!")

        bot = BotPlayer(bot_name)
        self.players.append(bot)
        logging.info("Added bot {0}".format(bot_name))

    def remove_player(self, player_name):
        if player_name not in [p.name for p in self.players]:
            raise Exception("Player {0} not in the draft table".format(player_name))

        if self.draft_stage != 0:
            raise Exception("Cannot remove players after draft has started!")

        for i in range(len(self.players)):
            if self.players[i].name == player_name:
                self.players.pop(i)
                break

        logging.info("Removed player {0}".format(player_name))

    def create_boosters(self):
        if self.boosters:
            raise Exception("Boosters are not empty!")

        card_pool = CardPool()

        for p in self.players:
            for i in range(3): # Amount of turns
                booster = Booster()

                booster.add_card(card_pool.pull_cmd())
                booster.add_card(card_pool.pull_tcs())
                booster.add_card(card_pool.pull_cu())
                booster.add_card(card_pool.pull_ncu())
                booster.add_card(card_pool.pull_att())
                for i in range(2): # Add two random cards
                    match random.randint(1,4):
                        case 1:
                            booster.add_card(card_pool.pull_cu())
                        case 2:
                            booster.add_card(card_pool.pull_cu())
                        case 3:
                            booster.add_card(card_pool.pull_ncu())
                        case 4:
                            booster.add_card(card_pool.pull_att())

                self.boosters.append(booster)
                logging.info("Created booster:")
                logging.info(booster)
                logging.info("-----")
        self.booster_size = len(self.boosters[0].get_cards())

    async def start_draft(self):
        if len(self.players) != self.player_count and not self.allow_bots:
            raise Exception("Table not full!")

        bot_count = 0
        while len(self.players) != self.player_count:
            bot_name = "Bot " + str(bot_count + 1)
            self.add_bot(bot_name)
            bot_count += 1

        logging.info("Starting draft")
        self.create_boosters()

        random.shuffle(self.players)
        logging.info("Shuffled player seats")

        self.draft_stage = 1

        for i in range(self.player_count):
            self.stage_boosters.append(self.boosters.pop(0))

        self.turn = 0
        self.direction = 1

        # Give options
        await self.draft_turn()

    async def trigger_next_round(self):
        if not (False in self.has_picked):
            if self.booster_size == self.turn+1:
                if self.draft_stage == 3:
                    await self.end_draft()
                else:
                    self.stage_boosters.clear()
                    for i in range(self.player_count):
                        self.stage_boosters.append(self.boosters.pop(0))
                    logging.info("Allocating new boosters")

                    self.draft_stage += 1
                    self.turn = 0
                    self.direction = -1 * self.direction
                    await self.draft_turn()
            else:
                self.turn += 1
                await self.draft_turn()

        await self.update_start_message()

    async def draft_turn(self):
        print("Starting Round {0} - Turn {1}".format(self.draft_stage, self.turn+1))
        self.has_picked = [False]*self.player_count

        for i in range(self.player_count):
            answer = await self.players[i].make_choice(self.stage_boosters[(i+self.turn*self.direction) % self.player_count], self.draft_stage, self.turn+1)
            if answer:
                self.has_picked[i] = True

        await self.trigger_next_round()

    async def pick_card_for_player(self, player_name, card):
        player_id = -1

        for i in range(len(self.players)):
            if player_name == self.players[i].name:
                player_id = i
                break

        if player_id == -1:
            raise Exception("You are not part of the draft!")

        if self.has_picked[player_id]:
            raise Exception("You have already picked a card!")

        b = self.stage_boosters[(i+self.turn*self.direction) % self.player_count]

        if card-1 < 0 or card > len(b.get_cards()):
            raise Exception("Card id out of range: {0}".format(card))

        await self.players[player_id].remove_buttons()

        self.players[player_id].choose_card(b.pick_card(card-1))
        self.has_picked[player_id] = True
        await self.trigger_next_round()

    async def end_draft(self):
        msg = "# Draft has ended!\nHere are the drafted pools of the players!"
        if self.main_channel is None:
            print(msg[2:])
        else:
            await self.main_channel.send(msg)

        for player in self.players:
            await player.trigger_end_message(self.main_channel)

    async def show_player_cards(self, player_name, condensed):
        player_id = -1

        for i in range(len(self.players)):
            if player_name == self.players[i].name:
                player_id = i
                break

        if player_id == -1:
            raise Exception("You are not part of the draft!")

        await self.players[player_id].show_cards(condensed)

    def __str__(self):
        dt_str = "Draft: {0}\n".format(self.draft_table_id)
        dt_str += "Players:\n"

        for p in self.players:
            dt_str += str(p) + "\n"

        return dt_str
