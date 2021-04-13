# bot.py
# Made by Eduardo Migueis
# 19167
import os
import random
import requests
import json
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='cat', brief='Picks a game from Steam for you. Args= [game_1], [game_2], ...', description='You can use the command without any arguments and get a random game from Steam. And you can put a list of games ([game_1], [game_2], ...) for the cat to pick one.')
async def cat(ctx, *arg):
    if len(arg) == 0:
        json_game = get_random_game()
        response = get_prefix(ctx.author) + str(json_game['name'])
        await ctx.send(response)
        embed = discord.Embed()
        embed.description = "Checkout this game [on Steam](https://store.steampowered.com/app/"+str(
            json_game['appid'])+"/)."
        await ctx.send(embed=embed)
    else:
        arg = list(arg)
        arg = ' '.join(arg).split(',')
        response = get_prefix(ctx.author) + '**'+random.choice(arg)+'**'
        await ctx.send(response)


def get_prefix(author):
    aut = '<@'+str(author.id)+'>'
    cat_prefixes = [
        'Meow, '+aut+' should play: ',
        'Well '+aut+', if you feel like having some fun: ',
        'Cats are connoisseurs of comfort. '+aut+', lay back and play: ',
        'I had you at meow, right? '+aut+' should play: ',
        'Want a great recommendation, '+aut+'? Here you go! ',
        'I am a gamer cat! '+aut+'. Play:'
    ]
    return random.choice(cat_prefixes)


def get_random_game():
    response = requests.get(
        "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json")
    return response.json()['applist']['apps'][random.randint(0, 1000)]


@bot.command(name='disclaimer', brief='A disclaimer about the bot.')
async def disclaimer(ctx, *arg):
    response = "Because this bot uses the Steam API with no restrictions to the content provided by Steam, the bot can recommend inappropriate content."
    await ctx.send(response)

bot.run(TOKEN)
