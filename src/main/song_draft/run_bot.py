import discord
import logging

from draft.draft_table import DraftTable
import utils

with open('../../../discord_token', 'r') as token_file:
    token = token_file.readline()

bot = discord.Bot()
bot.ongoing_draft = None
bot.ongoing_draft_category = None
bot.ongoing_draft_channel = None
bot.ongoing_draft_player_threads = None
bot.ongoing_draft_players = None

@bot.slash_command()
async def create_draft(ctx, game_name : str, player_count : int, allow_bots : bool = False):
    msg = ""

    if bot.ongoing_draft is None:
        try:
            bot.ongoing_draft = DraftTable(draft_table_id = game_name, player_count = player_count, allow_bots = allow_bots)
            msg += "Game started"
        except Exception as e:
            msg += "Issue with creating a game! Error: {0}".format(e)
    else:
        msg += "There is already a game going on!"

    await ctx.respond(msg)
    bot.ongoing_draft_category = await ctx.guild.create_category_channel("{0}_draft".format(game_name))
    bot.ongoing_draft_channel = await ctx.guild.create_text_channel('main', category = bot.ongoing_draft_category)

@bot.slash_command()
async def join(ctx):
    msg = ""
    try:
        bot.ongoing_draft.join_player(ctx.author.name, author=ctx.author)
        msg += "{0} joined game succesfully!".format(ctx.author.name)
    except Exception as e:
        msg += "Issue with joining game: {0}".format(e)

    await ctx.respond(msg)

@bot.slash_command()
async def remove(ctx, name : str):
    msg = ""
    try:
        bot.ongoing_draft.remove_player(name)
        msg += "{0} removed from game succesfully!".format(name)
    except Exception as e:
        msg += "Issue with removing a player from game: {0}".format(e)

    await ctx.respond(msg)

@bot.slash_command()
async def show_draft(ctx):
    msg = ""
    if bot.ongoing_draft is None:
        msg += "No ongoing draft!"
    else:
        msg += str(utils.game_status_str(bot.ongoing_draft))

    await ctx.respond(msg)

@bot.slash_command()
async def start_draft(ctx):
    bot.ongoing_draft_player_threads = {}

    for p in bot.ongoing_draft.get_players():
        player_thread_name = p.name + "_draft"
        player_thread = await bot.ongoing_draft_channel.create_thread(name=player_thread_name)
        await player_thread.add_user(p.author)
        bot.ongoing_draft_player_threads[p.name] = player_thread
        p.set_thread(player_thread)

    await bot.ongoing_draft.start_draft()

@bot.slash_command()
async def show_cards(ctx, condensed: bool = True):
    try:
        await bot.ongoing_draft.show_player_cards(player_name = ctx.author.name, condensed = condensed)
    except Exception as e:
        await ctx.respond("Something went wrong with the command: {0}".format(e))

@bot.slash_command()
async def clear_game(ctx):
    bot.ongoing_draft = None

@bot.slash_command()
async def pick_card(ctx, card: int):
    try:
        await bot.ongoing_draft.pick_card_for_player(ctx.author.name, card)
    except Exception as e:
        await ctx.respond("Something went wrong with the pick: {0}".format(e))

bot.run(token)
