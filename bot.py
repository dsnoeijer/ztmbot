import os
import json
import asyncio
import requests
import discord
from time import time

client = discord.Client()
token = os.environ.get('BOT_TOKEN')
question_token = os.environ.get('BOT_QUESTIONS')
score_update = os.environ.get('BOT_SCORE_UPDATE')
prefix = "/question"


def update_score(user, points):

    url = score_update
    new_score = {'name': user, 'points': points}
    x = requests.post(url, data=new_score)

    return


def get_question(*args):

    qs = ''
    answer = []

    response = requests.get(question_token)
    json_data = json.loads(response.text)
    cat = json_data[0]['cat'] + "\n"
    qs += "Question: \n"
    qs += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
        answer.append(item['answer'])

    points = json_data[0]['points']

    return(qs, cat, answer, points)


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith(prefix):
        args = message.content[10:].strip().split(' ')

        if len(message.content) > 9:
            num_questions = int(args[0])
        else:
            num_questions = 1

        i = 0
        while i < num_questions:
            question, cat, answer, points = get_question()

            # Add colors
            start_time = time()
            embed = discord.Embed(title=cat, description=question, color=0xff0000)
            await message.channel.send(embed=embed)

            def check(m):
                return m.author == message.author

            try:
                guess = await client.wait_for('message', check=check, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send("Sorry, time's up!")

            if guess.content in answer:
                end_time = time()
                total_time = end_time - start_time
                user = guess.author
                update_score(user, points)
                head, sep, tail = str(message.author).partition('#')

                embed = discord.Embed(
                    title=f"Correct, {head}!",
                    description=f"The answer was {answer[0]}. You answered in {total_time} seconds and earned {points} point. Next question in 15 seconds.")
                await message.channel.send(embed=embed)
                # await message.channel.send(str(head) + " has answered correctly: " + "\"" + answer[0] +
                #                            "\"and earned " + str(points) + " points!")
                time.sleep(15)

            i += 1

client.run(token)
