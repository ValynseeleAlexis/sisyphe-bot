import os
from os import sendfile
import random
from random import choice
import discord
from discord.channel import VoiceChannel
from discord.ext.commands.errors import ChannelNotFound, MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands, tasks
import pyfiglet
from itertools import cycle
from discord.voice_client import VoiceClient
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

queue = []

class Audio(commands.Cog):
    def __init__(self,client):
        self.client = client
        print("Audio is loaded")

    async def makeConnection(self,ctx):
        voiceChannel = ctx.author.voice.channel
        vc = ctx.author.guild.voice_client
        if voiceChannel and vc:
              # Move to new channel if bot was connected to a previous one
                await vc.move_to(voiceChannel)
        elif voiceChannel:
            # If bot was not connected, connect it
            vc = await voiceChannel.connect()
         
        return vc

    async def getConnection(self,ctx):
        vc =  ctx.author.guild.voice_client
        if vc:
            return vc
        else:
            await ctx.send("Sisyphe n'est pas connecté")
         
    @commands.command(name="join")
    async def join(self,ctx):
        await self.makeConnection(ctx)
        
    @commands.command(name="leave")
    async def leave(self,ctx):
        vc = await self.getConnection(ctx)
        if vc:
            await vc.disconnect()
        

    @commands.command(name="play")
    async def play(self,ctx,url):
        #Making connection
        vc = await self.makeConnection(ctx)
        #handling playing audio
        async with ctx.typing():
            player = await YTDLSource.from_url(url,loop=self.client.loop)
            vc.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Now playing:** {}'.format(player.title))
      

    @commands.command(name="pause")
    async def pause(self,ctx):
        vc = await self.getConnection(ctx)
        if vc:
            vc.pause()
            await ctx.send("Je mets en pause votre musique :musical_note: ")
    
    @commands.command(name="resume")
    async def resume(self,ctx):
        vc = await self.getConnection(ctx)
        if vc:
            vc.resume()
            await ctx.send("Je reprends la lecture :musical_note: ")
       
    @commands.command(name="stop")
    async def stop(self,ctx):
        vc = await self.getConnection(ctx)
        if vc:
            await ctx.send("J'arrete votre lecture :musical_note: ")
            vc.stop()
        
    @commands.command(name="isPlaying")
    async def isPlaying(self,ctx):
        vc = await self.getConnection(ctx)
        if vc:
            if vc.is_playing():
                await ctx.send("Je suis actuellement entrain de jouer de la musique :musical_note:")

    # LOOP
    #Checking if sisyphe is playing music, if not launch a timeout
    @tasks.loop(seconds=10)
    async def notPlaying(self,ctx):
        print("Checking for music")
        vc = ctx.author.guild.voice_client
        if vc:
            if vc.is_playing() == False and self.timeout.is_running() == False:
                print("Starting timeout")
                self.timeout.start(ctx)
            elif vc.is_playing() and self.timeout.is_running():
                print("Stoppping timeout")
                self.timeout.stop()

     #Wait to timeout sisyphe
    @tasks.loop(minutes=1)
    async def timeout(self,ctx):
        vc = ctx.author.guild.voice_client
        if vc:
            if self.timeout.current_loop > 0 and vc.is_playing() == False:
                await vc.move_to(None)
                await ctx.send("Timeout")
                self.notPlaying.stop()
                self.timeout.stop()
    
def setup(client):
    client.add_cog(Audio(client))