#!/usr/bin/env python3.9
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import discord
import json
from cherrypicker import CherryPicker
import pandas as pd
from discord.ext import commands
# The following code is used from the article on how to link the spotipy module to the spotify api
# https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b
cid = '*******'
secret = '********'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

TOKEN = '*******'
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
client = commands.Bot(command_prefix='!', help_command = help_command)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def who(ctx, message):
    if ctx.author == client.user:
        return
    print(message)
    query = 'track: ' + message
    res = sp.search(q=query, limit=1, type='track')
    df = pd.json_normalize(res["tracks"]["items"][0]["artists"][0])
    df.info()
    print(df['name'].values[0])
    info = "Artist: "
    info += str(df['name'].values[0])
    await ctx.channel.send(info)
client.run(TOKEN)