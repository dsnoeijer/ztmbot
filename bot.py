import os
from time import time, sleep
from typing import Type, Tuple
from decimal import Decimal
import datetime
import json
import asyncio
import requests
import discord


CLIENT = discord.Client()
TOKEN = os.environ.get('BOT_TOKEN')
QUESTION_TOKEN = os.environ.get('BOT_QUESTIONS')
SCORE_UPDATE = os.environ.get('BOT_SCORE_UPDATE')
PREFIX = "/question"


def update_score(user, points):
    url = SCORE_UPDATE
    new_score = {'name': user, 'points': points}
    requests.post(url, data=new_score)

    return


def get_question():

    question = ''
    answer = []

    response = requests.get(QUESTION_TOKEN)
    json_data = json.loads(response.text)
    cat = json_data[0]['cat'] + "\n"
    question += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
        answer.append(item['answer'])

    return(question, cat, answer)


@CLIENT.event
async def on_message(message):

    if message.author == CLIENT.user:
        return

    if message.content.startswith(PREFIX):
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

            def check(message):
                return message.author

            try:
                guess = await CLIENT.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                return await message.channel.send("Sorry, time's up!")

            if guess.content in answer:
                end_time = time()
                total_time = round(Decimal(end_time - start_time), 2)

                if total_time <= 20:
                    points = 4
                elif total_time <= 40:
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

CLIENT.run(TOKEN)
