import os
from os import sendfile
import random
from random import choice
import discord
from discord import activity
from discord.channel import VoiceChannel
from discord.ext import tasks
from discord.ext.commands.errors import CommandError, CommandNotFound, MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands
from itertools import cycle

load_dotenv('dotenv_path=../.env')
GUILD = os.getenv('DISCORD_GUILD')
DEFAULT_CHANNEL = os.getenv('DEFAULT_CHANNEL')

class Event(commands.Cog):

    def __init__(self,client):
        self.client = client
        # default guild specified in .env
        self.guild = None
        # default channel
        self.channel = None
        print("Event is loaded")

    # Connexion
    @commands.Cog.listener()
    async def on_ready(self):
        #Initializing attributs
        self.guild = discord.utils.get(self.client.guilds, name=GUILD)
        self.channel = self.client.get_channel(int(DEFAULT_CHANNEL))

        #Setting status
        await self.client.change_presence(status=discord.Status.online,activity=discord.Game('Must push rocks !'))

        print('###READY###\n'
        f'{self.client.user} is connected to the following guild:\n'
        f'{self.guild.name}(id: {self.guild.id})'
        )
        
    # Command error handling
    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Il me manque des paramètres OwO !") 
        if isinstance(error, CommandNotFound):
            await ctx.send("Commande inconnue ! Owo")

    # Member Update
    @commands.Cog.listener()
    async def on_member_update(self,before, after):
        if(before.nick != after.nick):
            if(after.nick):
                message = f'{before.mention} a changé de pseudo et a opté pour {after.nick}'
            else:
                message = f"{before.mention} n'as plus de pseudonyme"
            await self.channel.send(message)

    # LOOPS
  
def setup(client):
    client.add_cog(Event(client))
