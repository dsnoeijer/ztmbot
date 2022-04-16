import os
from time import time, sleep
from typing import Type
from decimal import Decimal
import datetime
import json
import asyncio
import requests
import discord


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


def get_question():

    qs = ''
    answer = []

    response = requests.get(question_token)
    json_data = json.loads(response.text)
    cat = json_data[0]['cat'] + "\n"
    qs += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
        answer.append(item['answer'])

    return(qs, cat, answer)


@client.event
async def on_message(message: Type[discord.message.Message]) -> None:
    print(type(message))

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
            question, cat, answer = get_question()

            # Add colors
            start_time = time()
            embed = discord.Embed(title=f"Question {i + 1} of {num_questions}", color=0xff0000)
            embed.add_field(name="Category", value=cat, inline=False)
            embed.add_field(name="Question", value=question, inline=False)
            embed.set_footer(text="ZTM Bot - work in progress")
            embed.timestamp = datetime.datetime.now()
            await message.channel.send(embed=embed)

            def check(m):
                return m.author == message.author

            try:
                guess = await client.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                return await message.channel.send("Sorry, time's up!")

            if guess.content in answer:
                end_time = time()
                total_time = round(Decimal(end_time - start_time), 2)

                if total_time <= 20:
                    points = 4
                elif total_time > 20 and total_time <= 40:
                    points = 2
                else:
                    points = 1

                user = guess.author
                update_score(user, points)
                head, sep, tail = str(message.author).partition('#')

                if i == num_questions - 1:
                    embed = discord.Embed(
                        title=f"Correct, {head}!",
                        description=f"The answer was **{answer[0]}**. You answered in {total_time} seconds and earned {points} point.\nRound has finished!")
                    await message.channel.send(embed=embed)

                else:
                    embed = discord.Embed(
                        title=f"Correct, {head}!",
                        description=f"The answer was **{answer[0]}**. You answered in {total_time} seconds and earned {points} point.\n Next question in 15 seconds.")
                    await message.channel.send(embed=embed)
                    sleep(15)

            i += 1

client.run(token)
