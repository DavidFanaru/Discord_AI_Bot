from dotenv import load_dotenv
import discord
import os
from ..chatgpt_ai.openai import chatgpt_response, check_for_offensive_content, chatgpt_translate, chatgpt_quiz
import asyncio

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz_in_progress = False
        self.i = 0
        
    async def on_ready(self):
        print("Successfully logged in as: ", self.user)

    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, user_message = None, None

        is_offensive = check_for_offensive_content(message.content)

        if is_offensive:
            await message.author.add_roles(discord.utils.get(message.guild.roles, name="Muted"))
            await message.channel.send(f"{message.author.mention}, you've been muted for using offensive language.")

            await asyncio.sleep(120)
            await message.author.remove_roles(discord.utils.get(message.guild.roles, name="Muted"))
            await message.channel.send(f"{message.author.mention}, your mute has been lifted after 2 minutes.")

        for text in ['!ask', '!translate', '!quiz']:
            if message.content.startswith(text):
                command = message.content.split(' ')[0]
                user_message = message.content.replace(text, '')

        if command == '!ask':
            bot_response = chatgpt_response(prompt=user_message)
            await message.channel.send(f"Answer: {bot_response}")

        if command == '!translate':
            language = user_message.split(' ')[1]
            text = user_message.replace(language, '')
            bot_response = chatgpt_translate(text, language)
            await message.channel.send(f"Translate text: \n{bot_response}")

        if command == '!quiz':
            topic = user_message.split(' ')[1]
            print(topic)
            bot_response = chatgpt_quiz(topic)
            self.correct_answer = bot_response.split(': ')[-1]
            print(self.correct_answer)
            quiz_question = bot_response[:-len(self.correct_answer)]
            print(quiz_question)
            await message.channel.send(f"You have to answer this question:\n{quiz_question}")
            self.quiz_in_progress = True
            self.i = 0

        # Check if a quiz is in progress and if the message is from the same user
        if self.quiz_in_progress == True:
            if self.i == 1:
                user_answer = message.content.strip().lower()
                if user_answer == self.correct_answer[0].lower():
                    await message.channel.send("Congratulations! That's the correct answer.")
                else:
                    await message.channel.send(f"Sorry, that's incorrect. The correct answer is: {self.correct_answer}")
                self.quiz_in_progress = False
            self.i = 1


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
