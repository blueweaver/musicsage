#!/usr/bin/env python3.9
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import discord
import json
from cherrypicker import CherryPicker
import pandas as pd
from discord.ext import commands
# The following code is used from the article on how to link the spotipy module to the spotify api
# https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b
cid = '**********'
secret = '******'
scope = "playlist-modify-public"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
token = util.prompt_for_user_token("******",scope,client_id=cid,client_secret=secret, redirect_uri="http://localhost/")
#sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
sp = spotipy.Spotify(auth=token)

TOKEN = '*************'
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
client = commands.Bot(command_prefix='!', help_command = help_command)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#track query examples
@client.command()
async def who(ctx, message):
    if ctx.author == client.user:
        return
    print(message)
    query = 'track: ' + message
    res = sp.search(q=query, limit=1, type='track')
    if(len(res["tracks"]["items"]) == 0):
        info = "Sorry! I cannot find what you are looking for. please try again."
        await ctx.channel.send(info)
        return
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
    info += "\n" + dfTrack['album.images'][0][1]['url']
    await ctx.channel.send(info)

@client.command()
async def explicit(ctx, message):
    if ctx.author == client.user:
        return
    print(message)
    query = 'track: ' + message
    res = sp.search(q=query, limit=1, type='track')
    if(len(res["tracks"]["items"]) == 0):
        info = "Sorry! I cannot find what you are looking for. please try again."
        await ctx.channel.send(info)
        return
    dfArtist = pd.json_normalize(res["tracks"]["items"][0]["artists"])
    dfTrack = pd.json_normalize(res["tracks"]["items"][0])
    dfTrack.info()
    info = "The song " + dfTrack['name'][0] + " by the "
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
    if(dfTrack['explicit'].bool() == False):
        info += " is not explicit"
    else:
        info += " is explicit"
    info += "\n" + dfTrack['album.images'][0][1]['url']
    await ctx.channel.send(info)
    
@client.command()
async def album(ctx, message):
    if ctx.author == client.user:
        return
    print(message)
    query = 'track: ' + message
    res = sp.search(q=query, limit=1, type='track')
    if(len(res["tracks"]["items"]) == 0):
        info = "Sorry! I cannot find what you are looking for. please try again."
        await ctx.channel.send(info)
        return
    dfArtist = pd.json_normalize(res["tracks"]["items"][0]["artists"])
    dfTrack = pd.json_normalize(res["tracks"]["items"][0])
    dfTrack.info()
    info = "The song " + dfTrack['name'][0] + " by the "
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
    info += " is on the album " + dfTrack['album.name'].values[0]
    info += "\n" + dfTrack['album.images'][0][1]['url']
    await ctx.channel.send(info)

#compare 2 songs
@client.command()
async def morePop(ctx, song1, song2):
    if ctx.author == client.user:
        return
    print("song1: " + song1)
    print("song2: " + song2)
    query1 = 'track: ' + song1
    query2 = 'track: ' + song2
    res1 = sp.search(q=query1, limit=1, type='track')
    res2 = sp.search(q=query2, limit=1, type='track')
    info = ""
    if(len(res1['tracks']['items']) == 0 or len(res2['tracks']['items']) == 0):
        info = "Sorry! I cannot find one of the songs that you are looking for. please try again."
        await ctx.channel.send(info)
        return
    dfTrack1 = pd.json_normalize(res1['tracks']['items'][0])
    dfTrack2 = pd.json_normalize(res2['tracks']['items'][0])
    dfTrack1.info()
    print("1: " + str(dfTrack1['popularity'][0]))
    print("2: " + str(dfTrack2['popularity'][0]))
    if(dfTrack1['popularity'][0] > dfTrack2['popularity'][0]):
        info += dfTrack1['name'][0] + " is more popular than " + dfTrack2['name'][0]
    elif(dfTrack1['popularity'][0] < dfTrack2['popularity'][0]):
        info += dfTrack2['name'][0] + " is more popular than " + dfTrack1['name'][0]
    else:
        info += "WOW! " + dfTrack1['name'][0] + " and " + dfTrack2['name'][0] + " are equally popular!"
    await ctx.channel.send(info)

#artist query examples
@client.command()
async def popularSongs(ctx, message):
    if ctx.author == client.user:
        return
    print(message)
    query = 'artist: ' + message
    res = sp.search(q=query, type='artist')
    if(len(res['artists']['items']) == 0):
        info = "Sorry! I cannot find what you are looking for. please try again."
        await ctx.channel.send(info)
        return
    topSongs = sp.artist_top_tracks(res['artists']['items'][0]['id'], country='US')
    dfTrack = pd.json_normalize(topSongs['tracks'])
    dfTrack.info()

    info = "Here are the top 10 songs by " + dfTrack['artists'][0][0]['name'] + ":\n"
    for i in range(len(dfTrack['name'])):
        info += "    " + str(i+1) + ". " + dfTrack['name'][i] + "\n"
    await ctx.channel.send(info)

@client.command()
async def listGenres(ctx):
    if ctx.author == client.user:
        return
    res = sp.recommendation_genre_seeds()
    info = "Here is a list of Genres that I know: \n"
    for i in range(len(res["genres"])):
        info += "   * " + res["genres"][i] + "  "
        if((i+1) % 4 == 0):
            info += "\n"
    await ctx.channel.send(info)

@client.command()
async def makeRec(ctx, first, second, third, spotID):
    if ctx.author == client.user:
        return
    query = "artist: " + first
    band = sp.search(q=query, type='artist')
    if(len(band['artists']['items']) == 0):
        info = "Sorry! I cannot find the band that you are looking for. please try again."
        await ctx.channel.send(info)
        return
    query2 = "track: " + third
    song = sp.search(q=query2, limit=1, type='track')
    if(len(song['tracks']['items']) == 0):
        info = "Sorry! I cannot find the song that you are looking for. please try again."
        await ctx.channel.send(info)
        return
    res = sp.recommendations(seed_artists=[band['artists']['items'][0]['id']], seed_genres=[second], seed_tracks=[song['tracks']['items'][0]['id']], limit=10, country='US')
    info = "Here is a playlist that I made based on your request: \n"
    dfTrack = pd.json_normalize(res['tracks'])
    dfTrack.info()
    playList = sp.user_playlist_create(spotID, "MusicSage", public=True, collaborative=False, description="Playlist generated by your music requests")
    for i in range(len(dfTrack['name'])):
        info += "* " + dfTrack['name'][i] + " by " + dfTrack['artists'][i][0]['name'] + "\n"
        info += "Preview: " + str(dfTrack['preview_url'][i]) + "\n\n"
        sp.playlist_add_items(playList['id'], [dfTrack['id'][i]], position=None)
    await ctx.channel.send(info)
client.run(TOKEN)