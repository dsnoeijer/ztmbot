import discord
import requests
import json
import asyncio


client = discord.Client()


def get_question():

    qs = ''
    answer = []
    response = requests.get("https://quiet-mesa-21253.herokuapp.com/api/random/")
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
        await message.channel.send(question)

        def check(m):
            return m.author == message.author

        try:
            guess = await client.wait_for('message', check=check, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send("Sorry, time's up!")

        if guess.content in answer:
            head, sep, tail = str(message.author).partition('#')
            await message.channel.send(str(head) + " has answered correctly: " + "\"" + answer[0] + "\"")


client.run('OTYzMDg4OTI2MDk1MDQ4NzI2.YlRAdQ.3ajFQsyEOvX7bLCxBHdcwSBkEDg')
