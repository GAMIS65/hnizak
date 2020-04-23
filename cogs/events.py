import discord
from discord.ext import commands

class events(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server.")

    # Leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server.")

    # Errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("This command doesn't exist or is currently disabled. If you need help contact GAMIS65.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command. If you need help contact server admin.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument. If you need help contact GAMIS65.")


def setup(client):
    client.add_cog(events(client))
    print("Events.py loaded")