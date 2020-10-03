import discord
from discord.ext import commands as com

def setup(client, settings):
        client.add_cog(commands(client, settings))

class commands(com.Cog):

    def __init__(self, client, settings):
        self.client = client
        self.settings = settings

    @com.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @com.command()
    async def new_game(self, ctx):
        embed = discord.Embed(title = "New Game", color=0x800040)
        embed.add_field(name="Players", value=[], inline=True)
