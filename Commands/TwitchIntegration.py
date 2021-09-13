import requests #funny library to work with APIs weeeee
import json     #This sucks and I don't understand it
import os       #getting info from .env again
import discord
from discord.ext import commands

def get_stream(streamer):
    #all these credentials should be in a secure file before hosting
    Client_ID = os.getenv('TwitchClientID')         #application id on twitch's website
    Client_Secret = os.getenv('TwitchClientSecret') #secret credential that might reset in however many days idk
    
    #request for an authenticator key for this session and converting it to an access token
    Auth = requests.post("https://id.twitch.tv/oauth2/token", {'client_id': Client_ID, 'client_secret': Client_Secret, 'grant_type': "client_credentials"})
    AuthJson = json.loads(Auth.text)
    AccessToken = "Bearer " + AuthJson['access_token']

    #combining the auth key and client id to get the stream information
    HEAD = {"Authorization": AccessToken, 
            "Client-Id": Client_ID}

    streamURL = "https://api.twitch.tv/helix/streams?user_login=" + streamer #streamer api link 
    #get the data on a specific stream from the api and convert it to json
    stream = requests.get(url = streamURL, headers = HEAD)
    streamData = json.loads(stream.text)

    #twitch return go [first object item (an array called data)][object 2 index within array][object 2 item]
    #get streamer's user profile
    streamerURL = "https://api.twitch.tv/helix/users?login=" + streamer
    streamUserProfile = requests.get(url = streamerURL, headers = HEAD)
    userProfileData = json.loads(streamUserProfile.text)
    
    
    
    #check if the streamer is live based on whether the data object exists
    # If so we grab a bunch of other data such as viewer count and format it as json for ease of use later
    streamInfo = {}
    if streamData['data'] != []:
        try: 
            #shortening the reference to stream/streamer data
            streamDataParsed = streamData['data'][0]
            userDataParsed = userProfileData['data'][0]
            streamInfo = {
                'live': True, 
                'name': userDataParsed['display_name'], 
                'pfp': userDataParsed['profile_image_url'], 
                'viewers': streamDataParsed['viewer_count'], 
                'stream_title': streamDataParsed['title'],
                'game': streamDataParsed['game_name'], 
                'thumbnail': str(streamDataParsed['thumbnail_url'])
                }
            
        except Exception as e:
           return e
    else:
        streamInfo = {
                'live': False, 
                'name': userProfileData['data'][0]['display_name'], 
                'pfp': userProfileData['data'][0]['profile_image_url'], 
                }
    return streamInfo

#A cog is kinda like a commands module for discord
class TwitchDiscordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def stream(self, ctx, arg):
        #get the stream information from the appropriate function
        streamEmbedDict = get_stream(arg)
    
        #if the stream is live then use its data to update the embed
        #if a stream isn't live this data doesn't exist
        if streamEmbedDict['live'] == True:
            embed=discord.Embed(title="**" + streamEmbedDict['name'] + "** is Live with " + str(streamEmbedDict['viewers']) + " viewers!", 
                                url="https://www.twitch.tv/" + arg, 
                                description=streamEmbedDict['stream_title'], 
                                color=0x6441a4)

            embed.set_author(name="🔴LIVE🔴")
            embed.set_thumbnail(url=streamEmbedDict['pfp'])
            embed.add_field(name="Playing", value=streamEmbedDict['game'])

            sizedThumbnail = streamEmbedDict['thumbnail'].replace("{width}","1280")
            sizedThumbnail = sizedThumbnail.replace("{height}","720")
            embed.set_image(url=sizedThumbnail)

            await ctx.channel.send(embed=embed)
        #A default embed for when they're offline
        else:
            embed=discord.Embed(title="**" + streamEmbedDict['name'] + "** is Offline", 
                                url="https://www.twitch.tv/" + arg,  
                                color=0x6441a4)
            embed.set_thumbnail(url=streamEmbedDict['pfp'])

            await ctx.channel.send(embed=embed)
    
    @stream.error
    async def stream_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("$stream (streamer name)")
        elif isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title="**Could not find streamer**")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Unexpected error: " + str(error))
        print("", str(ctx.message.jump_url), str(error), sep="\n")

def setup(bot):
    bot.add_cog(TwitchDiscordCog(bot))