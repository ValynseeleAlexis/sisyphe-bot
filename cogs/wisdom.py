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
GUILD = os.getenv('DISCORD_GUILD')

class Wisdom(commands.Cog):
    def __init__(self,client):
        self.client = client   
        self.dictionnary = None
        self.cycle = None
        print("Wisdom is loaded")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.client.guilds, name=GUILD)
        self.channel = self.client.get_channel(int(DEFAULT_CHANNEL))
        filename = './assets/mots.txt'
        with open(filename) as file_object:
	        self.dictionnary = file_object.readlines()

        #Loops handling
        self.regenerateCycle.start()
        #self.autoWisdom.start()
    
    def randomChoice(self):
            return random.choice(self.dictionnary).rstrip()
    
    def patternGenerator(self):
        pattern = []
        # Number of patterns = 30
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

    @commands.command(name="random",brief="Genère un mot aléatoirement",description="Renvoie un mot aléatoirement en se servant du dicitonnaire interne de sisyphe")
    async def random(self,ctx):
        await ctx.send(self.randomChoice())

    @commands.command(name="wisdom",aliases=['w'],brief="Genère un message d'une grande sagesse (alias:w)",description="Genère un message à l'aide de modèles et du dictionnaire de sisyphe",help="Utilisez wisdom ou w pour demander à sisyphe de générer un message aléatoirement")
    async def wisdom(self,ctx):
        pattern = self.patternGenerator()
        await ctx.message.delete()
        await ctx.send(f"{random.choice(pattern)}\n")
       

    @commands.command(name="horoscope",aliases=['h'],brief="Prédit votre avenir ou celui de la personne mentionné (alias:h)",description="Genère un message aléatoire à l'aide de modèles et du dictionnaire de sisyphe",help="Utilisez horoscope ou h suivi de votre cible,sans cible vous serez choisi par défaut")
    async def horoscope(self,ctx,*target):
        localTarget = ''
        pattern = []
        await ctx.message.delete()
        if(target):
            for ar in target:
                localTarget += ar+' '
        else:
            localTarget = ctx.author.mention
        pattern.append(f"Aujourd'hui {localTarget} va {self.randomChoice()}")
        pattern.append(f"{localTarget} est très {self.randomChoice()} en ce moment")
        pattern.append(f"{localTarget} va mourir de {self.randomChoice()}")
        pattern.append(f"Aujourd'hui {localTarget} est {self.randomChoice()} et ses actions sont {self.randomChoice()}")
        pattern.append(f"{localTarget} un mot pour décrire votre situation amoureuse : {self.randomChoice()}")
        pattern.append(f"{localTarget} va rencontrer Yveline Bertaux ! :two_hearts:")
     
        await ctx.send(f"{random.choice(pattern)}\n")

    @commands.command(name="horoscope2",aliases=['h2'],brief="Prédit votre avenir en commun avec la personne mentionné (alias:h2)",description="Genère un message aléatoire à l'aide de modèles et du dictionnaire de sisyphe",help="Utilisez horoscope2 ou h2 suivi de votre cible,sans cible la seconde cible sera aléatoire")
    async def horoscopeEnsemble(self,ctx,*target):
        await ctx.message.delete()
        members = []
        pattern = []
        localTarget = None
        guild = ctx.author.guild

        for member in guild.members:
            members.append(member)
        localTarget = (random.choice(members)).mention
        
        if(target):
            localTarget = ''
            for ar in target:
                localTarget += ar+' '
                
        pattern.append(f"La relation entre {ctx.author.mention} et {localTarget} est {self.randomChoice()}")
        pattern.append(f"{ctx.author.mention} va {self.randomChoice()} {localTarget}")
        pattern.append(f"{ctx.author.mention} est mieux que {localTarget}")
        pattern.append(f"{ctx.author.mention} et {localTarget} tombent soudainement fan de {self.randomChoice()} {self.randomChoice()}")

        await ctx.send(f"{random.choice(pattern)}\n")
    # LOOP
    @tasks.loop(minutes=15)
    async def autoWisdom(self):
        await self.channel.send(next(self.cycle))
        
    @tasks.loop(minutes=450)
    async def regenerateCycle(self):
        self.cycle = self.patternGenerator()
        self.cycle = random.sample(self.cycle,len(self.cycle))
        self.cycle = cycle(self.cycle)
     
def setup(client):
    client.add_cog(Wisdom(client))
