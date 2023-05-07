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

@tree.command(name="random-team-comp", description="Generate a random team comp")
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

@tree.command(name="random-controller", description="Generate a random controller")
async def rand_controller(interaction):
    await interaction.response.defer()
    response = requests.get(f'{url}/val/content/v1/contents',
                            headers={"X-Riot-Token": riot_key}, params={"locale": "en-US"})
    data = response.json()
    agent = random.choice(data['characters'])
    while agent['name'] == 'Null UI Data!' or role_dict[agent['name']] != Role.Controller:
        agent = random.choice(data['characters'])
    
    await interaction.followup.send(agent['name'])

@tree.command(name="random-sentinel", description="Generate a random sentinel")
async def rand_sentinel(interaction):
    await interaction.response.defer()
    response = requests.get(f'{url}/val/content/v1/contents',
                            headers={"X-Riot-Token": riot_key}, params={"locale": "en-US"})
    data = response.json()
    agent = random.choice(data['characters'])
    while agent['name'] == 'Null UI Data!' or role_dict[agent['name']] != Role.Sentinel:
        agent = random.choice(data['characters'])
    
    await interaction.followup.send(agent['name'])

@tree.command(name="random-duelist", description="Generate a random duelist")
async def rand_duelist(interaction):
    await interaction.response.defer()
    response = requests.get(f'{url}/val/content/v1/contents',
                            headers={"X-Riot-Token": riot_key}, params={"locale": "en-US"})
    data = response.json()
    agent = random.choice(data['characters'])
    while agent['name'] == 'Null UI Data!' or role_dict[agent['name']] != Role.Duelist:
        agent = random.choice(data['characters'])
    
    await interaction.followup.send(agent['name'])

@tree.command(name="random-initiator", description="Generate a random initiator")
async def rand_initiator(interaction):
    await interaction.response.defer()
    response = requests.get(f'{url}/val/content/v1/contents',
                            headers={"X-Riot-Token": riot_key}, params={"locale": "en-US"})
    data = response.json()
    agent = random.choice(data['characters'])
    while agent['name'] == 'Null UI Data!' or role_dict[agent['name']] != Role.Initiator:
        agent = random.choice(data['characters'])
    
    await interaction.followup.send(agent['name'])

@tree.command(name="random-agent", description="Generate a random agent")
async def rand_agent(interaction):
    await interaction.response.defer()
    response = requests.get(f'{url}/val/content/v1/contents',
                            headers={"X-Riot-Token": riot_key}, params={"locale": "en-US"})
    data = response.json()
    agent = random.choice(data['characters'])
    while agent['name'] == 'Null UI Data!':
        agent = random.choice(data['characters'])
    
    await interaction.followup.send(agent['name'])

@client.event
async def on_ready():
    await tree.sync()

    print('Logged in as {0.user}'.format(client))

client.run(os.getenv('BOT_TOKEN'))
