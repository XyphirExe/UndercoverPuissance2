import discord
from discord.ext import commands
import asyncio
import random
import os
import time
from time import sleep
import pickle


client = commands.Bot(command_prefix="U^", case_insensitive=True)

TOKEN = "" # Insérer TOKEN ici!

guild_uc2 = None
category = None


@client.event
async def on_ready():
    print('Bot is ready.')
    print('As : ' + str(client.user.name))
    print('ID : ' + str(client.user.id))
    client.load_extension('Undercover')


@client.command()
@commands.is_owner()
async def load(ctx):
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("Undercover^2"))
    client.load_extension('Undercover')


@client.command()
@commands.is_owner()
async def stop(ctx):
    await client.close()
    print("Bot closed")


@client.command()
@commands.is_owner()
async def unload(ctx):
    client.unload_extension('Undercover')
    await client.change_presence(status=discord.Status.invisible, activity=discord.CustomActivity("Hors ligne"))


@client.command()
@commands.is_owner()
async def reload(ctx):
    client.reload_extension('Undercover')


@client.command()
@commands.is_owner()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

client.run(TOKEN)
