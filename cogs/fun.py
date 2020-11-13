import os
from os import sendfile
import random
from random import choice
import discord
from discord.channel import VoiceChannel
from discord.ext.commands.errors import MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands, tasks
import pyfiglet

class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client
        print("Fun is loaded")

    @commands.command(name="tg",brief="TheFantasio974 <3",description="TheFantasio974 <3",help="")
    async def tg(self,ctx):
        await ctx.author.send("```TG```\n"+"https://www.youtube.com/watch?v=CQZtyO0Usxw&ab_channel=L%C3%89GENDARY")


    @commands.command(name='swag',brief="Renvoie un lien vers le vrai Swagg",description="Renvoie un lien vers le vrai Swagg",help="")
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

    @commands.command(name="8ball",aliases=["8"],brief="Répond à une question en oui ou non",description="Répond à une question en oui ou non",help="8ball ou 8 + votre question")
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
        await ctx.send("https://www.youtube.com/watch?v=AMShoQ_qdc0&ab_channel=%EC%BF%A0%EC%82%BCkusam")
        
    @commands.command(name="ascii",brief="Renvoie votre message sous forme d'ascii",description="Renvoie votre message sous forme d'ascii",help="ascii + votre message")
    async def ascii(self,ctx, *,msg):
        await ctx.channel.send(f'```{pyfiglet.figlet_format(msg)}```')

    #La commande de chachawx, je ne suis pas responsable
    @commands.command(name="cuisine",hidden=True)
    async def cuisine(self,ctx):
        if(ctx.author.id == 221341133719076865):
            await ctx.send("Ta place est a la cuisine pd",tts=True)
        else:
            await ctx.send("chachawx only grrrrrr !")
    @commands.command(name="louix",hidden=True)
    async def louix(self,ctx):
        if(ctx.author.id == 221341133719076865):
            await ctx.send("Louix grosse merde",tts=True)
        else:
            await ctx.send("chachawx only grrrrrr !")

def setup(client):
    client.add_cog(Fun(client))