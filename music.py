#!/usr/bin/env python3.9
from matplotlib import artist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import discord
import json
from cherrypicker import CherryPicker
import pandas as pd
from discord.ext import commands
# The following code is used from the article on how to link the spotipy module to the spotify api
# https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b
cid = '********'
secret = '********'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

TOKEN = '********'
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
    dfArtist = pd.json_normalize(res["tracks"]["items"][0]["artists"])
    dfTrack = pd.json_normalize(res["tracks"]["items"][0])
    dfArtist.info()
    info = "The song " + dfTrack['name'][0] + " is by the "
    if(dfArtist['name'].size == 2):
        info += "artists " + dfArtist['name'].values[0] + " and " + dfArtist['name'].values[1]
    elif(dfArtist['name'].size > 1):
        info += "artists "
        for i in range(dfArtist['name'].size):
            if(i != dfArtist['name'].size-1):
                info += dfArtist['name'].values[i] + ", "
            else:
                info += "and " + dfArtist['name'].values[i]
    else:
        info += "artist " + dfArtist['name'].values[0]
    await ctx.channel.send(info)
client.run(TOKEN)