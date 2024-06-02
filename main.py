# bot.py
import os

import discord
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

intent = discord.Intents.default()
intent.messages = True
intent.guild_messages = True
intent.guilds = True
intent.message_content = True
client = discord.Client(intents=intent)
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="Only output your response as \"complaint\" or \"normal\". You are programmed to determine if a statement is a complaint or not a complaint it must not blindly react to any negative words. It must have a context and subject. For example: input: \"man this task is so hard\" output: \"complaint\". input: \"the sun is so shiny today\" output: \"normal\". input: \"cocaine\" output: \"normal\". input: \"suck\" output: \"normal\", input: \"lol you suck\" output: \"normal\"",
)

chat_session = model.start_chat()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'{client.user} is connected to the following guilds:')
    for guild in client.guilds:
        print(f'name: {guild.name}, id: {guild.id}')

@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return
    else:
        print(f"message received: {message.content}")
        response = chat_session.send_message(message.content).text.strip()
        print(response)
        if "complaint" in response.lower():
            print("it is a complaint")
            await message.reply("womp womp")

client.run(TOKEN)