#!/usr/bin/env python3.9
import discord
import json
from cherrypicker import CherryPicker
import pandas as pd
from discord.ext import commands
import musicbrainzngs

TOKEN = '*************'
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
    musicbrainzngs.set_useragent("musicSage", "1.0", "https://github.com/blueweaver/musicsage")
    musicbrainzngs.set_format(fmt='json')
    print(message)
    res = musicbrainzngs.search_recordings(message, limit=1, strict=True)
    picker = CherryPicker(res)
    flat = picker['recordings'].flatten().get()
    df = pd.DataFrame(flat)
    info = "Artist: "
    info += str(df['artist-credit_0_name'].values[0])
    await ctx.channel.send(info)
client.run(TOKEN)