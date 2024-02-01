import sys
import os
import re
from utils import *
# from extract_positions import extract_game_info
import pickle
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv)==1:
    file_list = os.listdir('./files/')
    name_list=[]
    print(file_list)
    for file in file_list:
        reg = re.search('statistics_(.*).dat', file)
        if reg:
            name_list.append(reg.group(1))

    name_str=', '.join(name_list)

    # print(file_list)
    raise Exception(f"No team name given. Found statistics files for the following teams:\n {name_str}\nCall as\npython3 plot_stats.py <team_name>")

team_name=sys.argv[1]
# team_name='SVP'

fname=f"./files/statistics_{team_name}.dat"
if not os.path.isfile(fname):
    raise Exception('Could not find file with game statistice call main.py with the correct team names set.')
with open(fname, 'rb') as f:
    stat = pickle.load(f)[0]

# print(stat)

names=[]
points_played=[]
points_present=[]
sets=[]
starting_sets=[]
for player in stat.player:
    # print(player)
    names.append(player.name)
    points_played.append(sum(player.points_played)/stat.total_points)
    points_present.append(sum(player.points_present)/stat.total_points)
    # sets.append(len(player.points_present)/stat.total_sets)
    starting_sets.append(sum(player.starting_sets)/stat.total_sets)



fig1,ax1=plt.subplots()
xx=np.arange(len(points_played))
width=0.25
ax1.grid()
ax1.set_axisbelow(True)
ax1.bar(xx-width, points_played , width=width, label='points played')
ax1.bar(xx      , points_present, width=width, label='points present')
ax1.bar(xx+width, starting_sets , width=width, label='starting sets')
ax1.set_xticks(xx, names)
ax1.set_ylim([0,1])
yticks=ax1.get_yticks()
ax1.set_yticks(yticks, ["{y:.0f} %".format(y=100*y) for y in yticks])
ax1.tick_params(axis='x', rotation=90)
fig1.subplots_adjust(bottom=0.2)
fig1.legend()
plt.show()
fig1.savefig(f"figures/{team_name}_proportions.png")
