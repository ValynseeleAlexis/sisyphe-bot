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
    async def play(self,ctx,*args):
        file = ""
        name = ""
        if args:
            if (args[0] == "chacha"):
                file = "assets/chacha.mp3"
                name = "On ne négocie pas avec les terroristes"
            if (args[0] == "tg"):
                file = "assets/tg.mp3"
                name = "TheFantasio974 :heart:"         
        else:
            file = "assets/testing.opus"
            name = "[PLAY LIST] 피곤한데 잠이 안와 , 그래서 틀어봤어 Lofi Music"

        #Making connection
        vc = await self.makeConnection(ctx)
        #handling playing audio
        if vc and file:
            vc.play(discord.FFmpegPCMAudio(file), after=lambda e: print('done', e))
            await ctx.send(f"Je joue maintenant {name} :musical_note:")
        else:
            await ctx.send("Erreur argument inconnu")

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