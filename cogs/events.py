import discord
import pymongo
import os
import dotenv
from pymongo import MongoClient
from discord.ext import commands

connection_string = os.getenv('MongoDB')

cluster = MongoClient(connection_string)
db = cluster["discord"]
collection = db["test"]

class events(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server.")
        try:
            post = {"_id": member.id, "name": member.name, "message_count": 0}
            results = collection.insert_one(post)
            print(f"{member._user} has been added to the database")
        except Exception as e:
            print(f"{member._user} is already in the database")

    # Leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server.")

    # Count messages
    @commands.Cog.listener()
    async def on_message(self, message):
        collection.find_one_and_update({"_id": message.author.id}, {"$inc":{"message_count": 1}})

    # Errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("This command doesn't exist or is currently disabled.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument.")


def setup(client):
    client.add_cog(events(client))
    print("Events.py loaded")