from dotenv import load_dotenv
import discord
import os
from ..chatgpt_ai.openai import chatgpt_response, check_for_offensive_content
import asyncio

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print("Successfully logged in as: ", self.user)

    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, user_message = None, None

        # Check for offensive content using OpenAI
        is_offensive = check_for_offensive_content(message.content)

        if is_offensive:
        # Mute the user
            await message.author.add_roles(discord.utils.get(message.guild.roles, name="Muted"))
            await message.channel.send(f"{message.author.mention}, you've been muted for using offensive language.")

            await asyncio.sleep(120)
            await message.author.remove_roles(discord.utils.get(message.guild.roles, name="Muted"))
            await message.channel.send(f"{message.author.mention}, your mute has been lifted after 2 minutes.")



        for text in ['/ai','/bot','/chatgpt']:
            if message.content.startswith(text):
                command = message.content.split(' ')[0]
                user_message = message.content.replace(text, '')
                print(command, user_message)

        if command == '/ai' or command == '/bot' or command == '/chatgpt':
            bot_response = chatgpt_response(prompt = user_message)
            await message.channel.send(f"Answer: {bot_response}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)