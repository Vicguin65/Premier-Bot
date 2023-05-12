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
    response = requests.get(f'{url}/val/content/v1/contents',
                            headers={'X-Riot-Token': riot_key}, params={'locale': 'en-US'})
    data = response.json()
    agent = random.choice(data['characters'])
    if role == None:
        while agent['name'] not in role_dict.keys():
            break
        await interaction.followup.send(agent['name'])
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
    


def generate_episode_list():
    response = requests.get(f'{url}/val/content/v1/contents',
                            headers={'X-Riot-Token': riot_key}, params={'locale': 'en-US'})
    if response.status_code != 200:
        print('ERROR: NOT 202 RESPONSE')
        return
    
    data = response.json()
    list_episodes = [{episode['name']: episode['id']}
                     for episode in data['acts'] if episode['type'] != 'act']
    list_choices = []
    for episode in list_episodes:
        list_choices.append(discord.app_commands.Choice(
            name=f'{list(episode.keys())[0]}', value=f'{episode[list(episode.keys())[0]]}'))
    return list_choices


def act_list():
    list_acts = []
    list_acts.append(discord.app_commands.Choice(
        name='ACT 1', value=1))
    list_acts.append(discord.app_commands.Choice(
        name='ACT 2', value=2))
    list_acts.append(discord.app_commands.Choice(
        name='ACT 3', value=3))
    return list_acts

@tree.command(name='act-info', description='Get data about a specific act')
@app_commands.describe(episode='Choose an act to get data from', acts='Which Act? (1-3)',index='What rank to start with?', players='How many players below the index? (Max of 200)')
@app_commands.choices(episode=generate_episode_list())
@app_commands.choices(acts=act_list())
async def act_info(interaction, episode: discord.app_commands.Choice[str], acts: discord.app_commands.Choice[int], index: int, players: int):
    await interaction.response.defer()

    response_acts = requests.get(f'{url}/val/content/v1/contents',
                            headers={'X-Riot-Token': riot_key}, params={'locale': 'en-US'})
    if response_acts.status_code != 200:
        await interaction.followup.send(f'ERROR: {response_acts.status_code} act not found')
        return

    data_acts = response_acts.json()['acts']
    act_id = ''
    for act in range(len(data_acts)):
        if data_acts[act]['name'] == episode.name:
            act_id = data_acts[act + acts.value]['id']
        else: 
            act +=4

    if act_id == '':
        print('ERROR: ACT NOT FOUND')
        await interaction.followup.send('ERROR: ACT NOT FOUND')
    if players > 200:
        players = 200
    if players <= 0:
        players = 1
    if index < 0:
        index = 0

    response = requests.get(f'{url}/val/ranked/v1/leaderboards/by-act/{act_id}',
                            headers={'X-Riot-Token': riot_key}, params={'size': players, 'startIndex': index})
    if response.status_code != 200:
        if response.status_code == 404:
            await interaction.followup.send('ERROR: Bad index or size')
        else:
            await interaction.followup.send(f'ERROR: {response.status_code}')
        return
    data = response.json()        

    message = f'You Chose {episode.name} {acts.name}\n\n'
    for player in data['players']:
        message += (f'Rank: {player["leaderboardRank"]}\nPlayer: {player["gameName"]}\nRating:{player["rankedRating"]}\nWins:{player["numberOfWins"]}\n\n')
        if len(message) > 2000:
            break

    await interaction.followup.send(message[:2000])


@client.event
async def on_ready():
    await tree.sync()

    print('Logged in as {0.user}'.format(client))

client.run(os.getenv('BOT_TOKEN'))
