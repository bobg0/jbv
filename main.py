import discord
from discord.ext import commands
import os, asyncio

#import all of the cogs
from help_cog import help_cog
from music_cog import music_cog
from typing import Final
import os
import openai
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL  # Updated to use yt_dlp
from responses import get_response

# STEP 0: LOAD ENVIRONMENT VARIABLES
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_KEY')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

client: commands.Bot = commands.Bot(command_prefix='.', intents=intents)


# STEP 2: AI CHAT FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)
    await client.process_commands(message)


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

#remove the default help command so that we can write out own
bot.remove_command('help')

async def main():
    async with bot:
        await bot.add_cog(help_cog(bot))
        await bot.add_cog(music_cog(bot))
        await bot.start(TOKEN)

asyncio.run(main())