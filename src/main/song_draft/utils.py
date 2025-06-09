"""
Utils for the discord bot
"""
from draft.draft_table import DraftTable

def table_status(draft_table):
    sts_str = "# Game name: {0} - Player count: {1}/{2}\n".format(draft_table.draft_table_id, len(draft_table.get_players()), draft_table.player_count)
    for i in range(draft_table.player_count):
        plr_name = ""
        try:
            plr_name = draft_table.get_players()[i].name
        except:
            pass

        sts_str += "**{0}**: {1}\n".format(i+1, plr_name)

    return sts_str

