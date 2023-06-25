from enum import IntEnum

class Role(IntEnum):
    Controller = 1,
    Initiator = 2,
    Duelist = 3,
    Sentinel = 4

role_dict = {
    'Deadlock':Role.Sentinel
    'Gekko':Role.Initiator,
    'Fade':Role.Initiator,
    'Breach':Role.Initiator,
    'Raze':Role.Duelist,
    'Chamber':Role.Sentinel,
    'KAY/O':Role.Initiator,
    'Skye':Role.Initiator,
    'Cypher':Role.Sentinel,
    'Sova':Role.Initiator,
    'Killjoy':Role.Sentinel,
    'Harbor':Role.Controller,
    'Viper':Role.Controller,
    'Phoenix':Role.Duelist,
    'Astra':Role.Controller,
    'Brimstone':Role.Controller,
    'Neon':Role.Duelist,
    'Yoru':Role.Duelist,
    'Sage':Role.Sentinel,
    'Reyna':Role.Duelist,
    'Omen':Role.Controller,
    'Jett':Role.Duelist,
}

role_controller_list = []
for agent in role_dict:
    if role_dict[agent] == Role.Controller:
        role_controller_list.append(agent)

role_sentinel_list = []
for agent in role_dict:
    if role_dict[agent] == Role.Sentinel:
        role_sentinel_list.append(agent)

role_duelist_list = []
for agent in role_dict:
    if role_dict[agent] == Role.Duelist:
        role_duelist_list.append(agent)

role_initiator_list = []
for agent in role_dict:
    if role_dict[agent] == Role.Initiator:
        role_initiator_list.append(agent)

