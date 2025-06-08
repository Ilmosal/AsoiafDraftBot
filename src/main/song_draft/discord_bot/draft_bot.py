"""
This file contains the logic for the discord bot
"""
import logging

import discord
from discord.ext import commands

class DraftBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ongoing_draft = None
        self.test_var = 1234


