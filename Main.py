
import discord                      #boy I wonder what this is
from discord.ext import commands    #commands module of the discord api
import TwitchIntegration            #Twitch API file
import os                           #open .env files
from dotenv import load_dotenv

streamer = "shahzam"

#creating a bot instance, the connection to discord
bot = commands.Bot(command_prefix="$")

load_dotenv()

#@bot.event is used to register an event
@bot.event
#on_ready is called when the bot is ready to be used (good for initialization)
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
#defines a command
async def stream(ctx, arg):
    #get the stream information from the Twitch API file
    streamEmbedDict = TwitchIntegration.get_stream(arg)
    
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
async def stream_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("$stream (streamer name)")
    elif isinstance(error, commands.CommandInvokeError):
        embed=discord.Embed(title="**Could not find streamer**")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Unexpected error: " + str(error))
    print("", str(ctx.message.jump_url), str(error), sep="\n")


bot.run(os.getenv('DiscordToken'))