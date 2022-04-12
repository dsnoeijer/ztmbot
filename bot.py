import os
import json
import asyncio
import requests
import discord


client = discord.Client()


def get_question():

    qs = ''
    answer = []
    response = requests.get("https://lit-ocean-06406.herokuapp.com/api/random/")
    json_data = json.loads(response.text)
    qs += "Question: \n"
    qs += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
        answer.append(item['answer'])

    return(qs, answer)


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('/question'):
        question, answer = get_question()

        embed = discord.Embed(title="Question:", description=question, color=0xff0000)
        await message.channel.send(embed=embed)
        # await message.channel.send(question)

        def check(m):
            return m.author == message.author

        try:
            guess = await client.wait_for('message', check=check, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send("Sorry, time's up!")

        if guess.content in answer:
            head, sep, tail = str(message.author).partition('#')
            await message.channel.send(str(head) +
                                       " has answered correctly: " + "\"" + answer[0] + "\"")

token = os.environ.get('BOT_TOKEN')
client.run(token)
