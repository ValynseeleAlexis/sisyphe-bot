import os
from os import sendfile
import random
from random import choice
import discord
from discord import guild
from discord.channel import VoiceChannel
from discord.ext.commands import bot
from discord.ext.commands.errors import ChannelNotFound, MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands, tasks
import pyfiglet
from itertools import cycle

load_dotenv()
DEFAULT_CHANNEL = os.getenv('DEFAULT_CHANNEL')
GUILD = os.getenv('DISCORD_GUILD')

class Audio(commands.Cog):
    def __init__(self,client):
        self.client = client
        print("Audio is loaded")

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.client.guilds, name=GUILD)
        self.channel = self.client.get_channel(int(DEFAULT_CHANNEL))
       # self.follow.start()
               
    @commands.command(name="join")
    async def join(self,ctx):
        channel = ctx.author.voice.channel
        vc = ctx.author.guild.voice_client
        if channel and vc:
              # Move to new channel if bot was connected to a previous one
                await vc.move_to(channel)
        elif channel:
            # If bot was not connected, connect it
            vc = await channel.connect()
        
    @commands.command(name="leave")
    async def leave(self,ctx):
        vc = ctx.author.guild.voice_client
        if vc:
            await vc.disconnect()
        else:
            await ctx.send("Sisyphe n'est pas connecté")

    @commands.command(name="play")
    async def play(self,ctx,*args):
        if args:
            nowPlaying = args[0]
        else:
            nowPlaying = "./assets/testing.opus"

        #Handling connection
        channel = ctx.author.voice.channel
        vc = ctx.author.guild.voice_client
        if channel and vc:
            # Move to new channel if bot was connected to a previous one
                await vc.move_to(channel)  
        elif channel:
            # If bot was not connected, connect it
               vc = await channel.connect()
        #handling playing audio
        if vc:
            if args:
                vc.play(discord.FFmpegPCMAudio(nowPlaying), after=lambda e: print('done', e))
            else:
                vc.play(discord.FFmpegPCMAudio(nowPlaying), after=lambda e: print('done', e))
            await ctx.send(f"Je joue maintenant {nowPlaying} :musical_note:")

    @commands.command(name="pause")
    async def pause(self,ctx):
        vc = ctx.author.guild.voice_client
        if vc:
            vc.pause()
            await ctx.send("Je mets en pause votre musique :musical_note: ")
        else:
            await ctx.send("Sisyphe n'est pas connecté")

    @commands.command(name="resume")
    async def resume(self,ctx):
        vc = ctx.author.guild.voice_client
        if vc:
            vc.resume()
            await ctx.send("Je reprends la lecture :musical_note: ")
        else:
            await ctx.send("Sisyphe n'est pas connecté")

    @commands.command(name="stop")
    async def stop(self,ctx):
        vc = ctx.author.guild.voice_client
        if vc:
            await ctx.send("J'arrete votre lecture :musical_note: ")
            vc.stop()
        else:
            await ctx.send("Sisyphe n'est pas connecté")

    @commands.command(name="isPlaying")
    async def isPlaying(self,ctx):
        vc = ctx.author.guild.voice_client
        if vc:
            if vc.is_playing():
                await ctx.send("Je suis actuellement entrain de jouer de la musique :musical_note:")
        else:
            await ctx.send("Sisyphe n'est pas connecté")

    @commands.command(name="chacha",hidden="true")
    async def chacha(self,ctx):
        await ctx.message.delete()
        await self.play(ctx,"./assets/chacha.mp3")
        

    # LOOP
    @tasks.loop(seconds=1)
    async def follow(self):
        master = self.guild.get_member(106726951737118720)
        if(master):
            channel = master.voice.channel
            vc = self.guild.voice_client

            if channel and vc:
              # Move to new channel if bot was connected to a previous one
                await vc.move_to(channel)
            else:
            # If bot was not connected, connect it
                await channel.connect()
            if not channel and vc: # Disconnect if member has left
                await vc.disconnect()

def setup(client):
    client.add_cog(Audio(client))