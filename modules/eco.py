import discord
from discord.ext import commands, tasks
import json
import random
from discord.utils import get
import asyncio

# eco = {
#     1234: {
#         "bal": 10,
#         "cando": []
#     }
#
# }

outputs = []

leaderboard = []


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=10.0)
    async def update_leaderboard(self):
        with open('economy.json', 'r') as f:
            eco = json.load(f)
        server = get(self.client.guilds, id=693507386060701766)
        for member in server.members:
            in_leaderboard = False
            for user in leaderboard:
                if str(member.id) == user[1]:
                    in_leaderboard = True
            if not in_leaderboard:
                if not member.bot:
                    leaderboard.append([eco[str(member.id)]["bal"], str(member.id)])
        leaderboard.sort(reverse=True)

    @commands.Cog.listener()
    async def on_ready(self):
        with open('economy.json', 'r') as f:
            eco = json.load(f)
        with open('levels.json', 'r') as f:
            xp = json.load(f)

        for guild in self.client.guilds:
            for member in guild.members:
                if str(member.id) not in eco:
                    eco[str(member.id)] = dict()

                    eco[str(member.id)]["bal"] = 0

                    try:
                        exp = xp[str(member.id)]
                    except KeyError:
                        exp = 0
                    eco[str(member.id)]["last_xp"] = exp

                    if str(member.id) not in xp:
                        xp[str(member.id)] = 1
                    role = discord.utils.get(member.guild.roles, id=842711655150518273)
                    if role not in member.roles:
                        await member.add_roles(role)

        with open('economy.json', 'w') as f:
            json.dump(eco, f, indent=4)
        with open('levels.json', 'w') as f:
            json.dump(xp, f, indent=4)
        self.update_leaderboard.start()

    @commands.command(aliases=['wor', 'wrok', 'wok', 'rwok', 'praca', 'pracuj', 'crime'])
    async def work(self, ctx):
        with open('levels.json', 'r') as f:
            xp = json.load(f)
        with open('economy.json', 'r') as f:
            eco = json.load(f)
        if str(ctx.author.id) not in eco:
            eco[str(ctx.author.id)] = dict()
            eco[str(ctx.author.id)]["bal"] = 0
            eco[str(ctx.author.id)]["last_xp"] = xp[str(ctx.author.id)]
        else:
            wait = xp[str(ctx.author.id)] - eco[str(ctx.author.id)]["last_xp"]
            print(wait)
            if wait >= 10:
                income = random.randint(50, 600)
                eco[str(ctx.author.id)]["bal"] += income
                embed = discord.Embed(title="Praca",
                                      description=f"Pracujesz {int(income / 30.5)} godzin zarabiając {income}$.",
                                      color=0x33e170)
                eco[str(ctx.author.id)]["last_xp"] = xp[str(ctx.author.id)]
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Nie możesz pracować.",
                                      description=f"Wyślij jeszcze {10 - wait} wiadomości, (nie spam plz)\n żeby móc jeszcze "
                                                  f"raz pracować.",
                                      color=0xf41a3b)
                await ctx.send(embed=embed)

        with open('economy.json', 'w') as f:
            json.dump(eco, f, indent=4)

    @commands.command()
    async def bal(self, ctx, ping: discord.Member):
        with open('economy.json', 'r') as f:
            eco = json.load(f)
        print(str(ping.id) in eco)
        print(leaderboard)

        if str(ping.id) in eco:
            for i in range(len(leaderboard)):
                item = leaderboard[i]
                if item[1] == str(ping.id):
                    leaderboard_place = i + 1
            moni = eco[str(ping.id)]["bal"]
            embed = discord.Embed(
                title=ping.display_name,
                description=f"Ma  {moni}$. Miejsce na top - {str(leaderboard_place)}",
                color=0xfff70f
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["baltop", "toplist", "bals"])
    async def top(self, ctx):

        if len(leaderboard) >= 5:
            embed = discord.Embed(title="Top 5", description="Najbogatszych Epic Gamerów :sunglasses: ", color=0x6ee62d)
            for i in range(5):
                user = leaderboard[i]
                user_obj = await self.client.fetch_user(user[1])

                embed.add_field(name=f"{i + 1}. {user_obj.display_name}", value=f"{user[0]}", inline=False)
        else:
            embed = discord.Embed(title=f"Top {len(leaderboard)}", description="Najbogatszych Epic Gamerów :sunglasses: ", color=0x6ee62d)
            for i in range(len(leaderboard)):
                user = leaderboard[i]
                user_obj = await self.client.fetch_user(user[1])

                embed.add_field(name=f"{i + 1}. {user_obj.display_name}", value=f"{user[0]}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["rockpaperscissors", "papierkamien", "papierkamień", "papierkamieńnożyce", "rps", "pkn"])
    async def rock(self, ctx):
        with open('economy.json', 'r') as f:
            eco = json.load(f)
        await ctx.send("O ile chcesz się założyć?")
        msg = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
        try:
            money = int(msg.content.lower())
        except ValueError:
            await ctx.send("Nieprawidłowy argument. Użyj liczby.")
            return
        if eco[str(ctx.author.id)]["bal"] < money:
            await ctx.send("Nie masz tyle pieniędzy!")
            return

        await ctx.send("Ok! Co wybierasz? 1 - Papier, 2 - Kamień, 3- Nożyce")
        msg = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
        if not msg.content == "1" and not msg.content == "2" and not msg.content == "3":
            await ctx.send("Nieprawidłowy argument. Użyj '1', '2', lub '3'!")
            return
        player_choice = int(msg.content)
        bot_choice = random.randint(1, 3)
        eco[str(ctx.author.id)]["bal"] -= money
        waitforit = discord.Embed(title="Papier, kamień, nożyce", description="...", color=0x2780ce)

        integer_player = player_choice
        integer_bot = bot_choice

        if player_choice == 1:
            player_choice = ":newspaper:"
        elif player_choice == 2:
            player_choice = ":rock:"
        elif player_choice == 2:
            player_choice = ":scissors:"

        if bot_choice == 1:
            bot_choice = ":newspaper:"
        elif bot_choice == 2:
            bot_choice = ":rock:"
        elif bot_choice == 3:
            bot_choice = ":scissors:"

        print(bot_choice, player_choice, bot_choice == 3 and player_choice == 2)
        if (integer_bot == 1 and integer_player == 3) or (integer_bot == 2 and integer_player == 1) or (
                integer_bot == 3 and integer_player == 2):
            output = discord.Embed(title="Wygrana!", description=f"GG! Zarabiasz {money * 2}!", color=0x2780ce)
            output.add_field(name="Ty", value=player_choice, inline=True)
            output.add_field(name="Bot", value=bot_choice, inline=True)
        else:
            output = discord.Embed(title="Przegrana", description="Rip. :slight_frown: ", color=0xe21212)
            output.add_field(name="Ty", value=player_choice, inline=True)
            output.add_field(name="Bot", value=bot_choice, inline=True)
        to_edit = await ctx.send(embed=waitforit)
        await asyncio.sleep(1)
        await to_edit.edit(embed=output)


def setup(client):
    client.add_cog(Economy(client))
