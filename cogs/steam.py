import discord
import requests
import json
import datetime
import os
import pymongo
from pymongo import MongoClient
from discord.ext import commands, tasks

steam_api_key = os.getenv('steam_api_key')

connection_string = os.getenv('MongoDB')

cluster = MongoClient(connection_string)
db = cluster["discord"]
collection = db["steam"]


class steam(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.day_counter.start()
        self.ban_checker.start()

    @tasks.loop(seconds=1.0)
    async def day_counter(self):
        now = datetime.datetime.now()
        text1 = now.strftime("%H:%M:%S")
        if text1 == "00:00:00":
            collection.update_many({}, {"$inc":{"days": 1}})
            if collection.find({"days": {"$gt" : 30}}):
                collection.delete_many({"days": {"$gt" : 30}})
        else:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass
        else:
            message_id = payload.message_id
            results = collection.find({})
            for result in results:
                if message_id == result['message_id']:
                    collection.find_one_and_update({"message_id": result["message_id"]}, {"$addToSet": {"tracked_by": payload.member.id}})
                else:
                    pass

    @tasks.loop(hours=6.0)
    async def ban_checker(self):
        await self.client.wait_until_ready()
        results = collection.find({})
        for result in results:
            user_data = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steam_api_key}&steamids={result['_id']}")
            data_json = user_data.json()

            player_bans = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steam_api_key}&steamids={result['_id']}")
            player_bans_json = player_bans.json()

            try:
                VACBanned = player_bans_json['players'][0]['VACBanned']
                NumberOfGameBans = player_bans_json['players'][0]['NumberOfGameBans']
                DaysSinceLastBan = player_bans_json['players'][0]['DaysSinceLastBan']

                update = collection.find_one_and_update({'_id': result['_id']}, {"$set": {
                "VACBanned": VACBanned,
                "NumberOfGameBans": NumberOfGameBans,
                "DaysSinceLastBan": DaysSinceLastBan,
                }})

                if (VACBanned or NumberOfGameBans > 0 and DaysSinceLastBan < 3):
                    update = collection.delete_one({'_id': result['_id']})
                    for user_id in result['tracked_by']:
                        user = self.client.get_user(user_id) 
                        embed=discord.Embed(title="Profile", url=f"https://steamcommunity.com/profiles/{result['_id']}", color=0xff0000)
                        embed.add_field(name=f"{result['personaname']} was banned", value=f"VAC Banned: {VACBanned}", inline=True)
                        embed.add_field(name="\u200b", value=f"Number of game bans: {NumberOfGameBans}", inline=True)
                        await user.send(embed=embed)
                else:
                    pass
            except Exception as e:
                print(e)
            
    @ban_checker.before_loop
    async def before_ban_checker(self):
        print('waiting...')
        await self.client.wait_until_ready()

    @commands.command()
    async def track(self, ctx, *args):
        async def get_data(self, steam_id):
            user_data = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steam_api_key}&steamids={steam_id}")
            data_json = user_data.json()

            player_bans = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steam_api_key}&steamids={steam_id}")
            player_bans_json = player_bans.json()
            global post
            try:
                post = {
                "_id": steam_id,
                "personaname": data_json['response']['players'][0]['personaname'],
                "VACBanned": player_bans_json['players'][0]['VACBanned'],
                "NumberOfGameBans": player_bans_json['players'][0]['NumberOfGameBans'],
                "DaysSinceLastBan": player_bans_json['players'][0]['DaysSinceLastBan'],
                "days": 0,
                "tracked_by": [ctx.message.author.id],
                "message_id": ctx.message.id
                }
                return post
            except Exception as e:
                await ctx.send(f"An error occured. This means this user is already being tracked or doesn't exist.")

        if (args[0] == "vanity"):
            try:
                vanity = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={steam_api_key}&vanityurl={args[1]}")
                data_json = vanity.json()

                steam_id = data_json['response']["steamid"]

                await get_data(self, steam_id)
                results = collection.insert_one(post)
                await ctx.send("This user is now being tracked. React to your message to get a notification")
                await ctx.message.add_reaction("🔔")
            except Exception as e:
                await ctx.send("Make sure you entered everything correctly")
        elif (args[0] == "id"):
            try:
                steam_id = args[1]

                await get_data(self, steam_id)
                results = collection.insert_one(post)
                await ctx.send("This user is now being tracked. React to your message to get a notification")
                await ctx.message.add_reaction("🔔")
            except Exception as e:
                await ctx.send("Make sure you entered everything correctly")
        else:
            await ctx.send("Make sure you entered everything correctly")
        

def setup(client):
    client.add_cog(steam(client))
    print("Steam.py loaded")