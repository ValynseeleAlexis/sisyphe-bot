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
        print("Utilitaire is loaded")
    
    @commands.command(name='membres',brief="Renvoie la liste des membres du serveur courant",description="Renvoie la liste des membres du serveur courant",help="")
    async def membres(self,ctx):
        guild = ctx.author.guild
        await ctx.send(f"{ctx.author.mention} , voici la liste des membres de {guild.name}")
        for member in guild.members:
            response = '-{}\n'.format(member.name)
            await ctx.send(response)

    @commands.command(name='ping',brief="Renvoie le ping de Sisyphe",description="Renvoie le ping de Sisyphe",help="")
    async def ping(self,ctx):
        await ctx.send(f'Pong! ({round(self.client.latency * 1000)} ms)')

    @commands.command(name="mdr",brief="xD",description="xD",help="xD")
    async def mdr(self,ctx):
        # Handling chachawx
        if(ctx.author.id == 221341133719076865):
            await ctx.send("Miskine le reuf")
        else:
            guild = ctx.author.guild
            for vc in guild.voice_channels:
                for member in vc.members:
                    if(member.bot == False):
                        await member.move_to(None)
                        await ctx.send(f"{member.mention} xD")

    @commands.command(name="repete",aliases=["r"],brief="Demande a Sisyphe de lire votre message (alias:r)",description="Demande a Sisyphe de lire votre message en tts",help="repete ou r + votre message")
    async def repete(self,ctx, *,msg):
        await ctx.message.delete()
        await ctx.channel.send(f'{msg}',tts=True)

    @commands.command(name="purge",aliases=['p'],brief="Purge le channel courant du nombre messages précisés (alias:p)",description="Purge le channel courant du nombre messages précisés",help="clear ou c + nombre de messages")
    async def clear(self,ctx,amount: int):
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {len(deleted)} messages")

def setup(client):
    client.add_cog(Utilitaire(client))