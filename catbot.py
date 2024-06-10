import discord
import random
import asyncio
import ffmpeg
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)


voiceClient = None
left = False

@bot.event
async def on_ready():
    global voiceClient
    print(f'We have logged in as {bot.user}')
    await asyncio.sleep(3)
    while True:
        if not left:
            channel = getRandomChannel(bot.get_all_channels())
            if voiceClient is None and not channel is None:
                voiceClient = await channel.connect()
            elif not voiceClient is None and not channel is None:
                await voiceClient.move_to(channel)
        await asyncio.sleep(random.randint(10,300))

@bot.command(name='catleave', description='Disconnects the cat')
async def catleave(ctx):
    global voiceClient
    global left
    await ctx.message.delete()
    left = True
    if not voiceClient is None:
        await voiceClient.disconnect()
        voiceClient = None

@bot.command(name='catjoin', description='Allows the cat into the server')
async def catjoin(ctx):
    global left
    await ctx.message.delete()
    left = False

@bot.command(name='meow', description='Pets the command')
async def meow(ctx):
    global voiceClient
    await ctx.message.delete()
    if voiceClient is None or not voiceClient.is_playing():
        voiceClient.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="micah_meow.mp3"))


def getRandomChannel(channels):
    voiceChannels = []
    for channel in channels:
        if isinstance(channel, discord.VoiceChannel) and ((channel.user_limit < 1) or (len(channel.members) + 1 < channel.user_limit)):
            voiceChannels.append(channel)
    index = random.randint(0, len(voiceChannels) - 1)
    if len(voiceChannels) > 0:
        return voiceChannels[index]
    return None


def catbot():
    discord_key = os.environ.get('DISCORD_API_KEY')
    if discord_key is not None:
        bot.run(discord_key)
    else:
        print("DISCORD_API_KEY not set. exiting.")
