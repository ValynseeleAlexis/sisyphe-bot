# sisyphe.py
import os
from os import name, sendfile
import random
from random import choice
import discord
from discord.channel import VoiceChannel
from discord.ext.commands.errors import MissingRequiredArgument, UserInputError
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents().all()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='.', intents=intents,
description="Bienvenue sur l'aide de Sisyphe\n")

# Uncomment when pushing to Heroku
@client.command(hidden=True)
async def host(ctx):
	#await ctx.send("Je suis host sur Heroku !")
	await ctx.send("Je suis host localement !")

@client.command(name="load",hidden=True)
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send("extension loaded succesfuly !")

@client.command(name="unload",hidden=True)
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send("extension unloaded succesfuly !")

@client.command(name="reload",hidden=True)
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')
	await ctx.send("extension reloaded succesfuly !")

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
