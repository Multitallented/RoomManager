import discord
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

voiceClient = None
hiddenMemberCount = 0

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_member_join(member):
    print(f'New member joined')
    if (member.voice and member.voice.channel):
        room = member.voice.channel.name
        print(f'voice channel found {room}')
        if (not hasRole(member.roles, room)):
            print(f'role added {room}')
            role = discord.utils.get(member.guild.roles, name=room)
            await member.add_roles()

async def hasRole(roles, role):
    for x in range(roles):
        if (x.name == role):
            return True
        pass
    return False

def anyChannelHasHiddenMembers(channels, role):
    memberCount = 0
    for channel in channels:
        permissions = channel.permissions_for(role)
        if isinstance(channel, discord.VoiceChannel) and getChannelMemberCount(channel.members) > 0 and not permissions.view_channel:
            memberCount = memberCount + getChannelMemberCount(channel.members)
    return memberCount

def getChannelMemberCount(members):
    for member in members:
        if (member.name == 'Cat'):
            return len(members) - 1
    return len(members)

@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user:
        return
    global voiceClient
    global hiddenMemberCount
    everyoneRole = member.guild.default_role
    newHiddenMemberCount = anyChannelHasHiddenMembers(client.get_all_channels(), everyoneRole)

    if after.channel and (not before.channel or before.channel != after.channel):
        channel = after.channel.name
        role = discord.utils.get(member.guild.roles, name=channel)
        if role:
            await member.add_roles(role)
    if before.channel and (not after.channel or after.channel != before.channel):
        channel = before.channel.name
        role = discord.utils.get(member.guild.roles, name=channel)
        if role:
            await member.remove_roles(role)

    isBeforeChannelHidden = False
    if before.channel and not after.channel:
        permissionsBefore = before.channel.permissions_for(everyoneRole)
        isBeforeChannelHidden = not permissionsBefore.view_channel

    if voiceClient is None and newHiddenMemberCount > 0:
        frontPorch = discord.utils.get(member.guild.voice_channels, name='Front Porch')
        voiceClient = await frontPorch.connect()
    elif voiceClient and (hiddenMemberCount < 1 or (isBeforeChannelHidden and hiddenMemberCount < 2)):
        await voiceClient.disconnect()
        voiceClient = None
    if voiceClient and hiddenMemberCount != newHiddenMemberCount and newHiddenMemberCount > 0:
        hiddenMemberCount = newHiddenMemberCount
        newName = f'{hiddenMemberCount} people in hidden rooms'
        await voiceClient.guild.me.edit(nick=newName)
    else:
        hiddenMemberCount = newHiddenMemberCount

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!opensesame'):
        channel = discord.utils.get(message.author.guild.voice_channels, name='Library')
        memLen = len(channel.members)
        if (memLen > 0) and message.author.voice.channel and message.author.voice.channel.name == 'Library':
            secretRoom = discord.utils.get(message.author.guild.voice_channels, name='Solarium')
            await message.author.move_to(secretRoom)
        await message.delete()

    if message.content.startswith('!joinme'):
        role = discord.utils.get(message.author.guild.roles, name='Private Room Access')
        if role and role not in message.author.roles:
            await message.author.add_roles(role)
        channel = discord.utils.get(message.author.guild.voice_channels, name='Hallway')
        length = len(channel.members)
        if (length > 0) and message.author.voice.channel and message.author.voice.channel.category.name == 'Private Rooms':
            move = channel.members[0]
            destination = message.author.voice.channel
            await move.move_to(destination)
        await message.delete()


discord_key = os.environ.get('DISCORD_API_KEY')
if discord_key is not None:
    client.run(discord_key)
else:
    print("DISCORD_API_KEY not set. exiting.")
