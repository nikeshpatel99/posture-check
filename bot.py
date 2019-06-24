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
    # TODO - get rid of True
    while True:
        await channel.send("Hello friends, time to check your posture!")
        # TODO - make REMINDER_INTERVAL user defined
        await asyncio.sleep(REMINDER_INTERVAL)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(posture_check())
client.run(TOKEN)
