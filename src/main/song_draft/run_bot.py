import discord
import logging

from draft.draft_table import DraftTable
import utils

with open('discord_token', 'r') as token_file:
    token = token_file.readline()

bot = discord.Bot()
bot.ongoing_draft = None
bot.ongoing_draft_category = None
bot.ongoing_draft_channel = None
bot.ongoing_draft_player_threads = None
bot.ongoing_draft_start_message = None

@bot.slash_command()
async def create_draft(ctx, game_name : str, player_count : int, allow_bots : bool = False):
    msg = ""

    if bot.ongoing_draft is None:
        try:
            bot.ongoing_draft = DraftTable(draft_table_id = game_name, player_count = player_count, allow_bots = allow_bots)
            msg += "Game created"
        except Exception as e:
            msg += "Issue with creating a game! Error: {0}".format(e)
    else:
        msg += "There is already a game going on!"

    await ctx.respond(msg)
    bot.ongoing_draft_category = await ctx.guild.create_category_channel("{0}_draft".format(game_name))
    bot.ongoing_draft_channel = await ctx.guild.create_text_channel('main', category = bot.ongoing_draft_category)
    bot.ongoing_draft_start_message = await bot.ongoing_draft_channel.send(utils.table_status(bot.ongoing_draft))
    bot.ongoing_draft.set_main_channel(bot.ongoing_draft_channel)

@bot.slash_command()
async def join(ctx):
    msg = ""
    try:
        bot.ongoing_draft.join_player(ctx.author.name, author=ctx.author)
        msg += "{0} joined game succesfully!".format(ctx.author.name)
    except Exception as e:
        msg += "Issue with joining game: {0}".format(e)

    await ctx.respond(msg)
    await bot.ongoing_draft_start_message.edit(utils.table_status(bot.ongoing_draft))

@bot.slash_command()
async def remove(ctx, name : str):
    msg = ""
    try:
        bot.ongoing_draft.remove_player(name)
        msg += "{0} removed from game succesfully!".format(name)
    except Exception as e:
        msg += "Issue with removing a player from game: {0}".format(e)

    await ctx.respond(msg)
    await bot.ongoing_draft_start_message.edit(utils.table_status(bot.ongoing_draft))

@bot.slash_command()
async def show_draft(ctx):
    msg = ""
    if bot.ongoing_draft is None:
        msg += "No ongoing draft!"
    else:
        msg += str(utils.table_status(bot.ongoing_draft))

    await ctx.respond(msg)

@bot.slash_command()
async def start_draft(ctx):
    if bot.ongoing_draft is None:
        return await ctx.respond("No draft to start!")
    if not bot.ongoing_draft.can_start_draft():
        return await ctx.respond("Cannot start draft! Not enough players.")

    bot.ongoing_draft_player_threads = {}

    await ctx.respond("Starting Draft...")
    for p in bot.ongoing_draft.get_players():
        player_thread_name = p.name + "_draft"
        player_thread = await bot.ongoing_draft_channel.create_thread(name=player_thread_name)
        await player_thread.add_user(p.author)
        bot.ongoing_draft_player_threads[p.name] = player_thread
        p.set_thread(player_thread)

    await bot.ongoing_draft.start_draft()

@bot.slash_command()
async def show_cards(ctx, condensed: bool = True):
    await ctx.interaction.response.defer()
    try:
        await bot.ongoing_draft.show_player_cards(player_name = ctx.author.name, condensed = condensed)
        ctx.respond("Cards shown!")
    except Exception as e:
        await ctx.respond("Something went wrong with the command: {0}".format(e))

@bot.slash_command()
async def clear_game(ctx):
    await ctx.respond("Clearing game!")
    if bot.ongoing_draft_channel is None:
        await ctx.respond("There are no active games!")
    else:
        if bot.ongoing_draft_player_threads is not None:
            for t in bot.ongoing_draft_player_threads.values():
                await t.delete()

        await bot.ongoing_draft_channel.delete()
        await bot.ongoing_draft_category.delete()

        bot.ongoing_draft = None
        bot.ongoing_draft_category = None
        bot.ongoing_draft_channel = None
        bot.ongoing_draft_player_threads = None
        bot.ongoing_draft_start_message = None

@bot.slash_command()
async def pick_card(ctx, card: int):
    await ctx.interaction.response.defer()
    try:
        await bot.ongoing_draft.pick_card_for_player(ctx.author.name, card)
        await ctx.respond("Card picked!")
    except Exception as e:
        await ctx.respond("Something went wrong with the pick: {0}".format(e))

bot.run(token)
