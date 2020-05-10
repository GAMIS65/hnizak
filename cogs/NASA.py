import os
import discord
import requests
import json
import dotenv
import datetime
from dotenv import load_dotenv
from discord.ext import commands

TOKEN = os.getenv('NASA_TOKEN')    # NASA TOKEN


class NASA(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Astronomy Picture of the Day
    @commands.command(aliases=["apod", "Apod"])
    async def APOD(self, ctx, args):

        APOD = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={TOKEN}&date={args}")    # API URL
        data_json = APOD.json()    # data from the API URL to json

        image_title = data_json.get('title')    # get image title
        image_url = data_json.get('url')    # get image url
        image_photographer = data_json.get('copyright')    # get name of the photographer

        # Embed
        embed = discord.Embed(colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())   # embed colour and timestamp

        embed.set_author(name="Astronomy Picture of the Day")
        embed.set_image(url=image_url)
        embed.add_field(name="Title:", value=image_title, inline=False)
        embed.add_field(name="Photographer:", value=image_photographer, inline=False)

        await ctx.send(embed=embed)

    # Picture from the Mars rover
    @commands.command()
    async def rover(self, ctx, *args):
        
        parameters = list(args)    # URL parameters

        rover = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{parameters[0]}/photos?earth_date={parameters[1]}&api_key={TOKEN}")    # API URL
        data_json = rover.json()    # data from the API URL to json

        rover_image = data_json['photos'][3]['img_src']
        rover_sol = data_json['photos'][3]['sol']

        # Embed
        embed = discord.Embed(colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())   # embed colour and timestamp

        embed.set_author(name="Mars Rover Photos")
        embed.set_image(url=rover_image)
        embed.add_field(name="Sol:", value=rover_sol, inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(NASA(client))
    print("NASA.py loaded")
