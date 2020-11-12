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

load_dotenv()
DEFAULT_CHANNEL = os.getenv('DEFAULT_CHANNEL')

class Wisdom(commands.Cog):
    def __init__(self,client):
        self.client = client   
        self.dictionnary = None
        self.cycle = None
        print("wisdom is loaded")
    
    @commands.Cog.listener()
    async def on_ready(self): 
        self.channel = self.client.get_channel(int(DEFAULT_CHANNEL))
        filename = './assets/mots.txt'
        with open(filename) as file_object:
	        self.dictionnary = file_object.readlines()

        #Loops handling
        self.regenerateCycle.start()
        self.autoWisdom.start()
    
    def randomChoice(self):
            return random.choice(self.dictionnary).rstrip()
    
    @commands.command(name="random")
    async def random(self,ctx):
        await ctx.send(self.randomChoice())
    
    def patternGenerator(self):
        pattern = []
        pattern.append(f"J'ai fais un {self.randomChoice()}, c'etait {self.randomChoice()}...")
        pattern.append(f"@everyone Vous êtes tellement {self.randomChoice()} !")
        pattern.append(f"J'adore {self.randomChoice()}")
        pattern.append(f"Les LGBT font trop de {self.randomChoice()}")
        pattern.append(f"Je pense que François Hollande est {self.randomChoice()}")
        pattern.append(f"Dans l'ombre, j'irais chercher vos {self.randomChoice()} :blush:")
        pattern.append(f"J'ai envie de {self.randomChoice()}...")
        pattern.append(f"Savez-vous que les femmes sont {self.randomChoice()}, c'est pour ça qu'elles {self.randomChoice()} :joy:")
        pattern.append(f"Ma vie est trop {self.randomChoice()} :cry:")
        pattern.append(f"J'ai envie d'une Benson pour oublier les {self.randomChoice()}...")
        pattern.append(f"J'aimerais errer dans Cobbleland comme un {self.randomChoice()}")
        pattern.append(f"Personellement je préfère les {self.randomChoice()} à {self.randomChoice()} :man_shrugging:")
        pattern.append(f"Je me méfie des {self.randomChoice()}")
        pattern.append(f"Arretez de {self.randomChoice()}, je suis un shy boy :point_right: :point_left: ")
        pattern.append(f"Ton père est un voleur, il a volé toute les {self.randomChoice()} du monde pour les mettre dans tes {self.randomChoice()} :relieved:")
        pattern.append(f"Pourquoi les {self.randomChoice()} sont {self.randomChoice()} ? Parce qu'ils {self.randomChoice()} ! xD")
        pattern.append(f"Si j'etais président, j'instaurerais la {self.randomChoice()}")
        pattern.append(f"T'as un {self.randomChoice()} dans ton mirroir")
        pattern.append(f"Les {self.randomChoice()} ? Je déteste ça.")
        pattern.append(f"{self.randomChoice()} est la définition de sagesse, selon moi")
        pattern.append(f"Le quinquennat de Marine Lepen serait quelque chose de {self.randomChoice()} !")
        pattern.append(f"Je préconise d'utiliser des {self.randomChoice()} plutôt que des {self.randomChoice()}")
        pattern.append(f"Imagine tu {self.randomChoice()} des {self.randomChoice()} xD :rofl:")
        pattern.append(f"Et si le monde n'était qu'un {self.randomChoice()} {self.randomChoice()}:open_mouth:")
        pattern.append(f"Les {self.randomChoice()} {self.randomChoice()} à {self.randomChoice()} c'est lamentable !")
        pattern.append(f"Mon fils est devenu {self.randomChoice()}")
        pattern.append(f"Les handicapés c'est vraiment {self.randomChoice()}")
        pattern.append(f"C'est moi ou les migrants sont un peu {self.randomChoice()}:thinking:")
        pattern.append(f"J'ai beau avancer mon existence me ramène toujours à {self.randomChoice()}... :confused:")
        pattern.append(f"Femme qui {self.randomChoice()}, femme a moitié dans ton {self.randomChoice()} :smirk:")
       
        return pattern

    @commands.command(name="wisdom")
    async def wisdom(self,ctx):
        pattern = self.patternGenerator()
        await ctx.send(f"{random.choice(pattern)}\n")

    @commands.command(name="horoscope")
    async def horoscope(self,ctx):
          pattern = []
          pattern.append(f"Aujourd'hui {ctx.author.mention} va {self.randomChoice()}")
          pattern.append(f"{ctx.author.mention} est très {self.randomChoice()} en ce moment")
          await ctx.send(f"{random.choice(pattern)}\n")

    # LOOPS

    @tasks.loop(minutes=15)
    async def autoWisdom(self):
        await self.channel.send(next(self.cycle))
        
    @tasks.loop(seconds=27000)
    async def regenerateCycle(self):
        self.cycle = self.patternGenerator()
        self.cycle = random.sample(self.cycle,len(self.cycle))
        self.cycle = cycle(self.cycle)
     
def setup(client):
    client.add_cog(Wisdom(client))