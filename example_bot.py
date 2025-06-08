import discord

token = None

with open('discord_token', 'r') as token_file:
    token = token_file.readline()

bot = discord.Bot()

class MyView(discord.ui.View):
    @discord.ui.button(label='click me!', style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.send_message('You clicked the button')

@bot.slash_command()
async def button(ctx):
    await ctx.respond("This is a button!", view=MyView())

bot.run(token)
