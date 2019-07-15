import discord
import asyncio

with open("token.txt",'r') as f:
    TOKEN = f.readline().strip()

DEFAULT_REMINDER_INTERVAL = 20

current_jobs = {}

client = discord.Client()

async def posture_check_channel(channel):
    await client.wait_until_ready()
    while not client.is_closed() and channel.id in current_jobs:
        await channel.send("Hello friends, time to check your posture!")
        await asyncio.sleep(current_jobs[channel.id])

async def posture_check_user(user):
    while user.status != discord.Status.offline and user.id in current_jobs:
        await user.send("Hello " + user.name + "! It's time to check your posture")

        await asyncio.sleep(current_jobs[user.id])
        
@client.event
async def on_message(message):
    global REMINDER_INTERVAL
    if message.author == client.user:
        return
    channel = message.channel
    if message.content.startswith('!'):
        if message.content == "!hi" or message.content == "!hello":
            await channel.send("Hello %s!"%message.author.name)
        elif message.content == "!help":
            msg = "!setchannel :  add a channel to receive reminders\n!releasechannel : remove channel from receiving list\n!letsgetpersonal : subscribe to pm reminders\n!unsubscribe : unsubscribe from pm reminders\n!interval 30 : set the reminder interval to 30s (hint: you can change the 30)"
            await channel.send(msg)
        elif message.content == "!setchannel":
            if channel.id in current_jobs:
                await channel.send("You already have reminders set for this channel!")
            else:
                current_jobs[channel.id] = DEFAULT_REMINDER_INTERVAL
                client.loop.create_task(posture_check_channel(channel))
        elif message.content == "!releasechannel":
            if channel.id in current_jobs:
                del current_jobs[channel.id]
                await channel.send("No more posture checks for this channel.")
            else:
                await channel.send("You aren't receiving reminders on this channel!")
        elif message.content == "!letsgetpersonal":
            if message.author.id in current_jobs:
                await message.author.send("You already receive personal reminders!")
            else:
                current_jobs[message.author.id] = DEFAULT_REMINDER_INTERVAL
                client.loop.create_task(posture_check_user(message.author))
        elif message.content == "!unsubscribe":
            if message.author.id in current_jobs:
                del current_jobs[message.author.id]
                await message.author.send("You have successfully unsubscribed.")
            else:
                await message.author.send("You can't unsubscribe if you haven't subscribed!")
        elif message.content.startswith('!interval'):
            try:
                REMINDER_INTERVAL = int(message.content.split(' ')[1])
                if REMINDER_INTERVAL < 1:
                    raise ValueError()
                if message.channel.type == discord.ChannelType.text:
                    current_jobs[channel.id] = REMINDER_INTERVAL
                else:
                    current_jobs[message.author.id] = REMINDER_INTERVAL
                if REMINDER_INTERVAL != 1:
                    await channel.send("The interval is now set as '%i' seconds."%REMINDER_INTERVAL)
                else:
                    await channel.send("The interval is now set as 1 second.")
            except:
                await channel.send("I don't recognise that as a number :(")
        else:
            await channel.send("I don't recognise that command :(")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
client.run(TOKEN)
