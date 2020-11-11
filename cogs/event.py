import os
from os import sendfile
import random
from random import choice
import discord
from discord.channel import VoiceChannel
from discord.ext.commands.errors import CommandError, CommandNotFound, MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('dotenv_path=../.env')
GUILD = os.getenv('DISCORD_GUILD')

class Event(commands.Cog):

    def __init__(self,client):
        self.client = client
    
    # Connexion
    @commands.Cog.listener()
    async def on_ready(self):
	    guild = discord.utils.get(self.client.guilds, name=GUILD)
	    print(
	    f'{self.client.user} is connected to the following guild:\n'
	    f'{guild.name}(id: {guild.id})'
	    )

    # Command error handling
    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Il me manque un paramètre OwO !") 
        if isinstance(error, CommandNotFound):
            await ctx.send("Commande inconnue ! Owo")

    # Member Update
    @commands.Cog.listener()
    async def on_member_update(self,before, after):
	    channel = self.client.get_channel(775826986886627348)
	    if(before.nick != after.nick):
		    if(after.nick):
			    message = f'{before.mention} a changé de pseudo et a opté pour {after.nick}'
		    else:
			    message = f"{before.mention} n'as plus de pseudonyme"
		    await channel.send(message)



def setup(client):
    client.add_cog(Event(client))