import discord
from discord.ext import commands
import commands.stream.twitch_stream as twitch

#A cog is kinda like a commands module for discord
class twitch_cog(commands.Cog):
    #region docstring
    """
    A Discord bot cog to add minor Twitch integration

    Commands
    --------
    stream:
        takes in a Twitch streamer username, returns an embed of their status
    """
    #endregion

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def stream(self, ctx, arg):
        #get the stream information from the appropriate function
        streamEmbedDict = twitch.get_stream(arg)
    
        #if the stream is live then use its data to update the embed
        #if a stream isn't live this data doesn't exist
        if streamEmbedDict['live'] == True:
            embed=discord.Embed(
                title="**" + streamEmbedDict['name'] + "** is Live with " + str(streamEmbedDict['viewers']) + " viewers!", 
                url="https://www.twitch.tv/" + arg, 
                description=streamEmbedDict['stream_title'], 
                color=0x6441a4)

            embed.set_author(name="🔴LIVE🔴")
            embed.add_field(name="Playing", value=streamEmbedDict['game'])

            sizedThumbnail = streamEmbedDict['thumbnail'].replace("{width}","1280")
            sizedThumbnail = sizedThumbnail.replace("{height}","720")
            embed.set_image(url=sizedThumbnail)

        #A default embed for when they're offline
        else:
            embed=discord.Embed(
                title="**" + streamEmbedDict['name'] + "** is Offline", 
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
    bot.add_cog(twitch_cog(bot))