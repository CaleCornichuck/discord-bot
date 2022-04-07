# bot.py
import os

import discord
#import dotenv to access discord token
from dotenv import load_dotenv
#import discord commands for bots
from discord.ext import commands
#import twitter api code
import tapi

#access discord token and server name
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Create bot with '&' prefix
bot = commands.Bot(command_prefix='&')

#create client and allow it to print member names
#intents = discord.Intents.default()
#intents.members = True

#client = discord.Client(intents=intents)

#when client connects
#@client.event
#async def on_ready():
#    for guild in client.guilds:
#        if guild.name == GUILD:
#            break
#
#    print(
#        f'{client.user} is connected to the following guild:\n'
#        f'{guild.name}(id: {guild.id})'
#    )
#
#    members = '\n - '.join([member.name for member in guild.members])
#    print(f'Guild Members:\n - {members}')

#bot listens for message
@bot.command(name='twt')
async def tweets(ctx, user_name):
    if ctx.author == bot.user:
        return

    #Import and use searchTweets function from Twitter API code
    tweets = tapi.searchTweets(user_name)

    #Cycle through tweets and embed them for Discord bot to send
    if len(tweets) > 0:
        for x in tweets:
            #Create embed
            em = discord.Embed(title=x['text'], color=0xDEADBF)
            #Set the author to twitter user name
            em.set_author(name='@' + x['name'], icon_url=x['pp'])
            #If the tweet has a url to an image, set that using the embed function
            if any('url' in keys for keys in x):
                em.set_image(url=x['url'])
                #Send message
                await ctx.send(embed = em)
            else:
                #Send message
                await ctx.send(embed = em)
    #Print message if no tweets are found
    else:
        await ctx.send('No matching tweets found.')

#Simple command, prints out 'ohhhhh myyyyy goddddddd' when called
@bot.command(name='omg')
async def omg(ctx):
    response = 'ohhhhh myyyyy goddddddd'
    await ctx.send(response)

#Start bot
bot.run(TOKEN)