import discord
from discord.ext import commands
import time
import json

# eco = {
#     1234: {
#         "bal": 10,
#         "time": [14, 15, 56]
#     }
#
# }



class Author(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Author  loaded")

    @commands.command()
    async def block(self, ctx, time : int):
        if ctx.author.id == 295918758780862465:
            time.sleep(time)
    @commands.command()
    async def emoji_test(self, ctx):
        await ctx.send("<:ChadDog:842454518817095781>")

def setup(client):
    client.add_cog(Author(client))
