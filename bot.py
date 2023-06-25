import os
import random

import discord
import requests
from discord import app_commands
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

from tools import (role_controller_list, role_dict, role_duelist_list,
                   role_initiator_list, role_sentinel_list, Role)

load_dotenv()
riot_key = os.getenv('RIOT_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
url = 'https://na.api.riotgames.com'


@tree.command(name='random-team-comp', description='Generate a random team comp')
async def team_comp(interaction):
    await interaction.response.defer()

    team = []
    team.append(random.choice(role_controller_list))
    team.append(random.choice(role_sentinel_list))
    team.append(random.choice(role_duelist_list))
    team.append(random.choice(role_initiator_list))
    random_agent = random.choice(list(role_dict.keys()))
    while random_agent in team:
        random_agent = random.choice(list(role_dict.keys()))
    team.append(random_agent)
    message = f'Your randomly generated team comp is:\n\nController: {team[0]}\nSentinel: {team[1]}\nDuelist: {team[2]}\nInitiator: {team[3]}\nRandom:{team[4]}'
    await interaction.followup.send(message)


@tree.command(name='random-agent', description='Generate a random agent')
@app_commands.describe(role='(Optional) Choose a role for the agent')
@app_commands.choices(role=[app_commands.Choice(name='controller',value=1),app_commands.Choice(name='initiator',value=2),app_commands.Choice(name='duelist',value=3),app_commands.Choice(name='sentinel',value=4)])
async def rand_agent(interaction, role: app_commands.Choice[int]=None):
    await interaction.response.defer()

    if role == None:
        agent = random.choice(list(role_dict.keys()))
        await interaction.followup.send(agent)

    else: 
        if role.value == 1:
            agent = random.choice(role_controller_list)
        elif role.value == 2:
            agent = random.choice(role_initiator_list)
        elif role.value == 3:
            agent = random.choice(role_duelist_list)
        elif role.value == 4:
            agent = random.choice(role_sentinel_list)
        else:
            await interaction.followup.send('ERROR NOT A CORRECT ROLE')
        await interaction.followup.send(agent)

@client.event
async def on_ready():
    await tree.sync()

    print('Logged in as {0.user}'.format(client))

client.run(os.getenv('BOT_TOKEN'))
