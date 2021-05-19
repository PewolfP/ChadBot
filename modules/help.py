import discord
from discord.ext import commands
import time
import json


class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command()
    async def help(self, ctx):
        info =discord.Embed(title="Info", description="Każdą komendę należy pisać małymi literami.\nMają one też "
                                                      "ukryte alternatywy. (Znajdziesz je?)\n<> oznaczają "
                                                      "argumenty.", color=0xee82ee)

        msg1 = discord.Embed(title="Leveling", description="Każda oryginalna wiadomość to 1 exp.\n 50 exp to 1 level.\n Levelowanie jest wyłączone na #komendy.",
                             color=0x4b0082)
        msg2 = discord.Embed(title="Bal <ping>",
                             description="Sprawdza ile pieniędzy\n i które miejsce na top ma osoba.", color=0x0000ff)
        msg3 = discord.Embed(title="RPS", description="Rock Paper Scissors, ale możesz założyć się o cały swój majątek!", color=0x008000)
        msg4 = discord.Embed(title="Top", description="Zobacz kto ma najwyższy level na serwerze!", color=0xffff00)
        msg5 = discord.Embed(title="Work", description="Pracuj, zarabiając walutę. Aby pracować jeszcze raz, zdobądź 10 xp.", color=0xffa500)
        msg6 = discord.Embed(title="EXP <ping>", description="Sprawdź EXP i Level członka serwera.", color=0xff0000)

        to_send = [info, msg1, msg2, msg3, msg4, msg5, msg6]
        await ctx.send("Wysyłam ci informacje na priv.")
        for item in to_send:
            await ctx.author.send(embed=item)


def setup(client):
    client.add_cog(HelpCommand(client))
