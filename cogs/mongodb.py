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

class mongodb(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Find user in the database
    @commands.command()
    async def find(self, ctx, member: discord.Member):
        results = collection.find({"_id": member.id}) 

        for result in results:
            await ctx.send(result)
    
    # Add user to the database
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, member: discord.Member):
        try:
            post = {"_id": member.id, "name": member.name, "message_count": 0}
            results = collection.insert_one(post)
            await ctx.send(f"{member._user} has been added to the database")
            print(f"{member._user} has been added to the database")
        except Exception as e:
            await ctx.send(f"{member._user} is already in the database")
    
    # Add everyone on the server to the database
    @commands.command()
    @commands.is_owner()
    async def addeveryone(self, ctx):
        server_members = ctx.guild.members
        
        for member in server_members:
            try:
                post = {"_id": member.id, "name": member.name, "message_count": 0}
                results = collection.insert_one(post)
                print(f"{member._user} has been added to the database")
            except Exception as e:
                print(f"{member._user} is already in the database")
    
    # Delete user from the database
    @commands.command(aliases=["remove"])
    @commands.is_owner()
    async def delete(self, ctx, member: discord.Member):
        try:
            post = {"_id": member.id, "name": member.name, "message_count": 0}
            results = collection.delete_one(post)
            await ctx.send(f"{member._user} has been removed from the database")
            print(f"{member._user} has been removed from the database")
        except Exception as e:
            await ctx.send("This user is not in the database")

def setup(client):
    client.add_cog(mongodb(client))
    print("MongoDB.py loaded")