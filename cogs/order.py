import discord
import random
import datetime
from discord.ext import commands, tasks
from itertools import cycle
from random import randrange

now = datetime.datetime.now()
text1 = now.strftime("%D, %H:%M:%S")

class order(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Latency
    @commands.command()
    async def latency(self, ctx):
        await ctx.send(f"{round(self.client.latency * 1000)}ms")

    # Ask
    @commands.command()
    async def ask(self, ctx):
        responses = ["Yes",
                     "No", ]
        await ctx.send(f"{random.choice(responses)}")

    # Clear
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    # Uptime
    @commands.command()
    async def uptime(self, ctx):
        await ctx.send(f"The bot is UP since {text1}")

    # Kick
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    # Ban
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for {reason}")

    # Unban
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return

    # PP
    @commands.command()
    async def pp(self, ctx):
        await ctx.send(f"Your pp is {randrange(25)}cm long")

def setup(client):
    client.add_cog(order(client))
    print("Order.py loaded")