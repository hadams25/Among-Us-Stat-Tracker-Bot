import discord
from discord.ext import commands as com

def setup(client):
        client.add_cog(commands(client))

class commands(com.Cog):

    def __init__(self, client):
        self.client = client

    @com.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @com.command()
    async def new_game(self, ctx):
        embed = discord.Embed(title = "New Game", color=0x800040)
        embed.add_field(name="Players", value=[], inline=True)
