import discord
import asyncio

with open("token.txt",'r') as f:
    TOKEN = f.readline().strip()

with open("channel.txt",'r') as f:
    CHANNEL_ID = f.readline().strip()

REMINDER_INTERVAL = 20

client = discord.Client()

async def posture_check():
    await client.wait_until_ready()
    channel = client.get_channel(int(CHANNEL_ID))
    while not client.is_closed():
        await channel.send("Hello friends, time to check your posture!")
        await asyncio.sleep(REMINDER_INTERVAL)

@client.event
async def on_message(message):
    global REMINDER_INTERVAL
    if message.author == client.user:
        return
    channel = message.channel
    if message.content.startswith('!'):
        if message.content == "!hi" or message.content == "!hello":
            await channel.send("Hello %s!"%message.author.name)
        elif message.content.startswith('!interval'):
            try:
                REMINDER_INTERVAL = int(message.content.split(' ')[1])
                if REMINDER_INTERVAL != 1:
                    await channel.send("The interval is now set as '%i' seconds."%REMINDER_INTERVAL)
                else:
                    await channel.send("The interval is now set as 1 second.")
            except:
                await channel.send("I don't recognise that as a number :(")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(posture_check())
client.run(TOKEN)
