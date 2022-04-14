import os
import json
import asyncio
import requests
import discord


client = discord.Client()


def update_score():

    url = "https://lit-ocean-06406.herokuapp.com/api/score/update/"
    new_score = {'name': 'dan', 'points': 10}
    x = requests.post(url, data=new_score)

    return


def get_question():

    qs = ''
    answer = []
    points = 0

    response = requests.get("https://lit-ocean-06406.herokuapp.com/api/random/")
    json_data = json.loads(response.text)
    cat = json_data[0]['cat'] + "\n"
    qs += "Question: \n"
    qs += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
        answer.append(item['answer'])

    points = json_data[0]['points']

    return(qs, cat, answer)


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('/question'):
        question, cat, answer, points = get_question()

        embed = discord.Embed(title=cat, description=question, color=0xff0000)
        await message.channel.send(embed=embed)

        def check(m):
            return m.author == message.author

        try:
            guess = await client.wait_for('message', check=check, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send("Sorry, time's up!")

        if guess.content in answer:
            user = guess.author
            update_score()
            head, sep, tail = str(message.author).partition('#')
            await message.channel.send(str(head) + " has answered correctly: " + "\"" + answer[0] +
                                       "\"and earned " + str(points) + " points!")

token = os.environ.get('BOT_TOKEN')
client.run(token)
