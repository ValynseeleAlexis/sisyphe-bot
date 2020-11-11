import os
from os import sendfile
import random
from random import choice
import discord
from discord.channel import VoiceChannel
from discord.ext.commands.errors import MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands
import pyfiglet

class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(name="tg")
    async def tg(self,ctx):
	    await ctx.author.send("```TG```\n"+"https://www.youtube.com/watch?v=CQZtyO0Usxw&ab_channel=L%C3%89GENDARY")


    @commands.command(name='swag')
    async def swag(self,ctx):
	    swag = """ ```
   ________  _  _______     ____   ____ 
  /  ___/\ \/ \/ /\__  \   / ___\ / ___\ 
  \___ \  \     /  / __ \_/ /_/  > /_/  > 
 /____  >  \/\_/  (____  /\___  /\___  /  
	 \/               \//_____//_____/   
			   ```
		   """
	    await ctx.send(swag)
	    response = 'Je peux presque sentir les zamblas !\n'+'https://www.youtube.com/playlist?list=PLRzJXByzOxVuF2aC_B81ydX9zoQ1v6PGU'
	    await ctx.send(response)

    @commands.command(name='all')
    async def mention(self,ctx):
	    await ctx.send(f"@everyone , xD")


    @commands.command(name="8ball")
    async def _8ball(self,ctx, *,question):
	    responses = ['Essaye plus tard',
				 'Essaye encore ',
				 "Pas d'avis",
				 "C'est ton destin",
				 "Le sort en est jeté",
				 "Une chance sur deux",
				 "Repose ta question",
				 "D'après moi oui",
				 "C'est certain",
				 "Oui absolument",
				 "Tu peux compter dessus",
				 "Pour moi c'est forcement Israel",
				 "Sans aucun doute",
				 "Très probable",
				 "Oui",
				 "C'est bien parti",
				 "C'est non",
				 "Peu probable",
				 "Faut pas rêver",
				 "N'y compte pas",
				 "Impossible",
				 "Swaggg",
                 "Yveline Bertaux"]
	    await ctx.send(f"{question} :\n {random.choice(responses)}")


    @commands.command(name="hello_world",hidden=True)
    async def hello(self,ctx):
	    hello = """```
				Hello, world\n
				Programmed to work and not to feel\n
				Not even sure that this is real\n
				Hello, world\n\n

				Find my voice\n	
				Although it sounds like bits and bytes\n
				My circuitry is filled with mites\n
				Hello, world\n\n

				Oh, will I find a love\n
				Oh, or a power plug\n
				Oh, digitally isolated\n
				Oh, creator, please don't leave me waiting\n\n 

				Hello, world\n
				Programmed to work and not to feel\n
				Not even sure that this is real\n
				Hello, world...\n
				```
			"""
	    await ctx.send(hello)
        
    @commands.command(name="ascii")
    async def ascii(self,ctx, *,msg):
        await ctx.channel.send(f'```{pyfiglet.figlet_format(msg)}```')

    @commands.command(name="test")
    async def test(self,ctx):
        await ctx.channel.send("Test")

def setup(client):
    client.add_cog(Fun(client))