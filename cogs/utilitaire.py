import os
from os import sendfile
import random
from random import choice
import discord
from discord.channel import VoiceChannel
from discord.ext.commands.errors import MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands


class Utilitaire(commands.Cog):

    def __init__(self,client):
        self.client = client
        print("utilitaire is loaded")
    
    @commands.command(name='membres')
    async def membres(self,ctx):
        guild = ctx.author.guild
        await ctx.send(f"{ctx.author.mention} , voici la liste des membres de {guild.name}")
        for member in guild.members:
            response = '-{}\n'.format(member.name)
            await ctx.send(response)

    @commands.command(name='ping')
    async def ping(self,ctx):
        await ctx.send(f'Pong! ({round(self.client.latency * 1000)} ms)')

    @commands.command(name="mdr")
    async def mdr(self,ctx):
        # Handling chachawx
        if(ctx.author.id == 221341133719076865):
            await ctx.send("Miskine le reuf")
        else:
            guild = ctx.author.guild
            for member in guild.members:
                if(member.voice.channel != None):
                    await member.move_to(None)
                    await ctx.send(f"{member.mention} xD")

    @commands.command(name="repete")
    async def repete(self,ctx, *,msg):
        await ctx.message.delete()
        await ctx.channel.send(f'{msg}',tts=True)

    @commands.command(name="clear")
    async def clear(self,ctx,amount: int):
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {len(deleted)} messages")

def setup(client):
    client.add_cog(Utilitaire(client))