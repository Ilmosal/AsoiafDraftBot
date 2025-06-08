"""
Module containing the logic for the draft logic
"""
import logging
import random

from draft.card_pool import CardPool
from draft.player import BotPlayer, TermPlayer
from draft.booster import Booster

class DraftTable():
    def __init__(self, draft_table_id="", player_count = -1, draft_pool = "default", allow_bots = False):
        self.draft_table_id = draft_table_id
        self.player_count = player_count
        self.draft_pool = draft_pool

        self.players = []
        self.boosters = []
        self.stage_boosters = []
        self.booster_size = 11
        self.allow_bots = allow_bots

        self.has_picked = None

        self.draft_stage = 0

        logging.info("Table initialized!")

    def join_player(self, player_name, term_player=False):
        if player_name in [player.name for player in self.players]:
            raise Exception("Player {0} already in the table!".format(player_name))

        if len(self.players) == self.player_count:
            raise Exception("Table already full!")

        if self.draft_stage != 0:
            raise Exception("Cannot join players after draft has started!")

        player = TermPlayer(player_name)
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
        if player_name not in self.players.keys():
            raise Exception("Player {0} not in the draft table".format(player_name))

        if draft_stage != 0:
            raise Exception("Cannot remove players after draft has started!")

        for i in range(len(self.players)):
            if self.players[i].name == player_name:
                self.players.pop(i)
                break

        self.players.pop(player_name)
        logging.info("Removed player {0}".format(player_name))

    def create_boosters(self):
        if self.boosters:
            raise Exception("Boosters are not empty!")

        card_pool = CardPool()

        for p in self.players:
            for i in range(2):
                booster = Booster()
                booster.add_card(card_pool.pull_rare())
                booster.add_card(card_pool.pull_tcs())
                booster.add_card(card_pool.pull_tcs())
                booster.add_card(card_pool.pull_cu())
                booster.add_card(card_pool.pull_cu())
                booster.add_card(card_pool.pull_cu())
                booster.add_card(card_pool.pull_ncu())
                booster.add_card(card_pool.pull_ncu())
                booster.add_card(card_pool.pull_att())
                booster.add_card(card_pool.pull_att())
                booster.add_card(card_pool.pull_cmd())

                self.boosters.append(booster)
                logging.info("Created booster:")
                logging.info(booster)
                logging.info("-----")

    def start_draft(self):
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

        # Give options
        self.draft_turn(turn = 0, direction=1)

    def draft_turn(self, turn, direction):
        logging.info("Starting Round {0} - Turn {1}".format(self.draft_stage, turn+1))
        self.has_picked = [False]*self.player_count

        for i in range(self.player_count):
            answer = self.players[i].make_choice(self.stage_boosters[(i+turn*direction) % self.player_count])
            if answer:
                self.has_picked[i] = True

        if not (False in self.has_picked):
            if self.booster_size == turn+1:
                if self.draft_stage == 2:
                    self.end_draft()
                else:
                    self.stage_boosters.clear()
                    for i in range(self.player_count):
                        self.stage_boosters.append(self.boosters.pop(0))
                    logging.info("Allocating new boosters")

                    self.draft_stage = 2
                    self.draft_turn(turn=0, direction=-1*direction)
            else:
                self.draft_turn(turn+1, direction)

    def end_draft(self):
        logging.info("Draft ended")
        logging.info("------")

        for player in self.players:
            logging.info(str(player))
            logging.info("------")

    def __str__(self):
        dt_str = "Draft: {0}\n".format(self.draft_table_id)
        dt_str += "Players:\n"

        for p in self.players:
            dt_str += str(p) + "\n"

        return dt_str
