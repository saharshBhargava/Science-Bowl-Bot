import requests
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith('s.question'):
        global response
        response = await returnQuestion(message)

    if message.content.startswith(str(response["question"]["tossup_answer"][0])):
        await message.channel.send("That is correct!")
        response = await returnQuestion(message)

    if message.content.startswith('s.answer'):
        await message.channel.send(response["question"]["tossup_answer"])
        response = await returnQuestion(message)
        
async def returnQuestion(message):
    url = "https://scibowldb.com/api/questions/random"
    response = requests.get(url).json()
    embedVar = discord.Embed(
        title=response['question']['tossup_format'], description=response['question']['category'], color=discord.Colour.random())
    embedVar.add_field(
        name="Question", value=response['question']['tossup_question'], inline=True)

    await message.channel.send(embed=embedVar)
    print(response['question']['tossup_answer'])
    return response


client.run('token')
