import discord
from discord.ext import commands


from music_cog import music_cog

Bot = commands.Bot(command_prefix='/')

Bot.add_cog(music_cog(Bot))

@Bot.command()
async def scrie(ctx, *args):
        m_args = " ".join(args)
        await ctx.send(m_args)

@Bot.listen()
async def on_message(message):
    if message.author == Bot.user:
        return
    
    if message.content.startswith('$salut'):
       await message.channel.send('hey, boss!')

'''@Bot.event
async def on_message(message):
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await Bot.wait_for('message', check=check)
        await channel.send('Hello {.author} on channel {.channel}!'.format(msg, msg))'''

token = ""
with open("token") as file:
    token = file.read()


Bot.run(token)
