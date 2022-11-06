import discord
from discord import app_commands
from discord.ext import commands
from . import twitch_stream as twitch

#A cog is kinda like a commands module for discord
class TwitchCog(commands.Cog):
    """
    A Discord bot cog to add minor Twitch integration

    Commands
    --------
    stream:
        takes in a Twitch streamer username, returns an embed of their status
    """

    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name='stream',
        description='Get information from a twitch stream'
    )
    async def stream(self, interaction: discord.Interaction, streamer: str):
        #get the stream information from the appropriate function
        try:
            streamEmbedDict = twitch.get_stream(streamer)
        except:
            embed=discord.Embed(title="**Could not find streamer**")
            interaction.response.send_message(embed=embed)
            return
        
        #if the stream is live then use its data to update the embed
        #if a stream isn't live this data doesn't exist
        if streamEmbedDict['live'] == True:
            embed=discord.Embed(
                title="**" + streamEmbedDict['name'] + "** is Live with " + str(streamEmbedDict['viewers']) + " viewers!", 
                url="https://www.twitch.tv/" + streamer, 
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
                url="https://www.twitch.tv/" + streamer,  
                color=0x6441a4)
        embed.set_thumbnail(url=streamEmbedDict['pfp'])
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TwitchCog(bot))