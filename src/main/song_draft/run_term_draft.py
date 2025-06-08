"""
Simple environment for running drafts
"""
import logging
import asyncio

from draft.draft_table import DraftTable

logging.basicConfig(level = logging.INFO)

dt = DraftTable("test", 8, allow_bots = True)
dt.join_player("Me", term_player=True)
asyncio.run(dt.start_draft())

