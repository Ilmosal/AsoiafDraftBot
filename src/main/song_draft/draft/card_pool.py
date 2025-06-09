"""
Class for containing and asking for the card pool of the draft
"""

from draft.card import Card

import csv
import random

class CardPool():
    def __init__(self, card_pool="default"):
        self.card_pool = card_pool
        self.rares = []
        self.tcs = []
        self.ncus = []
        self.cus = []
        self.cmds = []
        self.atts = []

        pool_data = []

        with open("draft_data.csv", 'r') as draft_data_file:
            reader = csv.reader(draft_data_file, delimiter=",")
            for row in reader:
                pool_data.append(list(row))

        row_len = len(pool_data)

        # create tactics cards
        for r in range(row_len):
            card_str = pool_data[r][0].split('/')
            if card_str[0] == '':
                continue

            card_ids = pool_data[r][1].split('/')
            card_costs = pool_data[r][2].split('/')
            new_card = Card(card_str, card_ids, card_costs, card_type="tc")
            self.tcs.append(new_card)

        # create rares
        for r in range(row_len):
            card_str = pool_data[r][3].split('/')
            if card_str[0] == '':
                continue

            card_ids = pool_data[r][4].split('/')
            card_costs = pool_data[r][5].split('/')
            card_t = ""
            match r % 3:
                case 0:
                    card_t = "cu"
                case 1:
                    card_t = "ncu"
                case 2:
                    card_t = "cmd"

            new_card = Card(card_str, card_ids, card_costs, card_type=card_t)
            self.rares.append(new_card)

        # create combat units
        for r in range(row_len):
            card_str = pool_data[r][6].split('/')
            if card_str[0] == '':
                continue

            card_ids = pool_data[r][7].split('/')
            card_costs = pool_data[r][8].split('/')
            new_card = Card(card_str, card_ids, card_costs, card_type="cu")
            self.cus.append(new_card)

        # create NCUS
        for r in range(row_len):
            card_str = pool_data[r][9].split('/')
            if card_str[0] == '':
                continue

            card_ids = pool_data[r][10].split('/')
            card_costs = pool_data[r][11].split('/')
            new_card = Card(card_str, card_ids, card_costs, card_type="ncu")
            self.ncus.append(new_card)

        # create attachments
        for r in range(row_len):
            card_str = pool_data[r][12].split('/')
            if card_str[0] == '':
                continue

            card_ids = pool_data[r][13].split('/')
            card_costs = pool_data[r][14].split('/')
            new_card = Card(card_str, card_ids, card_costs, card_type="att")
            self.atts.append(new_card)

        # create commanders
        for r in range(row_len):
            card_str = pool_data[r][15].split('/')
            if card_str[0] == '':
                continue

            card_ids = pool_data[r][16].split('/')
            card_costs = pool_data[r][17].split('/')
            new_card = Card(card_str, card_ids, card_costs, card_type="cmd")
            self.cmds.append(new_card)


    def get_rares(self):
        return self.rares

    def get_cmds(self):
        return self.cmds

    def get_tcs(self):
        return self.tcs

    def get_ncus(self):
        return self.ncus

    def get_cus(self):
        return self.cus

    def get_atts(self):
        return self.atts

    def pull_rare(self):
        if len(self.rares) == 0:
            raise Exception("No rares to pull from!")

        return self.rares.pop(random.randint(0, len(self.rares)-1))

    def pull_cmd(self):
        if len(self.cmds) == 0:
            raise Exception("No commanders to pull from!")

        return self.cmds.pop(random.randint(0, len(self.cmds)-1))

    def pull_tcs(self):
        if len(self.tcs) == 0:
            raise Exception("No tactics cards to pull from!")

        return self.tcs.pop(random.randint(0, len(self.tcs)-1))

    def pull_ncu(self):
        if len(self.ncus) == 0:
            raise Exception("No NCUs to pull from!")

        return self.ncus.pop(random.randint(0, len(self.ncus)-1))

    def pull_cu(self):
        if len(self.cus) == 0:
            raise Exception("No combat units to pull from!")

        return self.cus.pop(random.randint(0, len(self.cus)-1))

    def pull_att(self):
        if len(self.atts) == 0:
            raise Exception("No attachments to pull from!")

        return self.atts.pop(random.randint(0, len(self.atts)-1))
