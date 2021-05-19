import discord
from discord.ext import commands


class Welcome(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("WelcomeMSG loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = self.client.get_channel(842458870383247388)
        embed = discord.Embed(title=f"Witaj", description=f"{member.mention}, na Epickim serwerze discord!", color=0x30fdef)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/83/6a/f9/836af91dfffa72c8dc0153e0c3ed2f76.png")

        await channel.send(embed=embed)


def setup(client):
    client.add_cog(Welcome(client))
