import discord
from discord.ext import commands
from discord.utils import get
import json
last_message = {}

level_req = {
    2: 776427071056379906,
    4: 697362598504562689,
    10: 697362598504562689

}

disabled_channels = [776732837084790794, 693882789568708648]


class Levels(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Levels loaded")





    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, id=842711655150518273)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):

        uid = str(message.author.id)
        if uid != str(self.client.user.id):

            with open('levels.json', 'r') as f:
                xp = json.load(f)

            if uid not in xp:
                xp[uid] = 0
            if message.channel.id not in disabled_channels:
                if str(message.author.id) not in last_message:
                    xp[uid] += 1
                    last_message[str(message.author.id)] = message.content
                elif last_message[str(message.author.id)] != message.content:
                    xp[uid] += 1
                exp = xp[uid]
                if exp % 50 == 0:
                    embed = discord.Embed(title="Level up!", description=f"Ale epicko, wbiłeś level {int(exp / 50)}",
                                          color=0x18f21f)
                    embed.add_field(name="\u200b", value=f"Wysłałeś już {exp} wiadomości!", inline=False)
                    embed.set_thumbnail(url=message.author.avatar_url)

                    await message.channel.send(embed=embed)
                    if exp / 50 in level_req:
                        role = discord.utils.get(message.author.guild.roles, id=level_req[exp / 50])
                        await message.author.add_roles(role)
                with open('levels.json', 'w') as f:
                    json.dump(xp, f, indent=4)

                last_message[str(message.author.id)] = message.content

    # @commands.command(name="exp")
    # async def exp(self, ctx, user: discord.User):
    #
    #     with open('levels.json', 'r') as f:
    #         xp = json.load(f)
    #     embed = discord.Embed(title=user.mention, description=f"Ma level {xp[user.id]}", color=0x18f2e3)
    #     await ctx.send(embed=embed)

    @commands.command()
    async def exp(self, ctx, user: discord.User):
        with open('levels.json', 'r') as f:
            xp = json.load(f)
        if str(user.id) in xp:
            if xp[str(user.id)] < 50:
                embed = discord.Embed(title=user.display_name, description=f"Ma  {xp[str(user.id)]} XP.",
                                      color=0x18f2e3)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=user.display_name,
                    description=f"Ma  {xp[str(user.id)]} XP i level {int(xp[str(user.id)] / 50)}",
                    color=0x18f2e3
                )
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Levels(client))
