import sys
import os
import re
from utils import *
# from extract_positions import extract_game_info
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps

interactive=False

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

print(stat)

# sort players according to the smallest number in numbers list (officials go last)
smallest_num=[]
for player in stat.player:
    if any(isinstance(x, int) for x in player.numbers):
        smallest_num.append(min([x for x in player.numbers if isinstance(x,int)]))
    else:
        smallest_num.append(9999)

ind = np.argsort(smallest_num)

stat.player=[stat.player[i] for i in ind]

names=[]
nums=[]
ylabel=[]
points_won=[]
points_lost=[]
points_played=[]
points_present=[]
sets=[]
starting_sets=[]
sets_won=[]
sets_lost=[]
for player in stat.player:
    # print(player)
    # nums = ','.join([f"{x}" for x in player.numbers])
    # points_played_per_num=[]
    points_won.append([])
    points_lost.append([])
    points_played.append([])
    points_present.append([])
    starting_sets.append([])
    sets_won.append([])
    sets_lost.append([])

    unique_nums=list(set(player.numbers))
    # ylabel=f"{player.name} ("+','.join([f"{x}" for x in unique_nums])+")"
    names.append(player.name)
    nums.append(unique_nums)
    # print(ylabel)
    for number in unique_nums:
        # print(number)
        # print([x for x in player.points_played])
        points_won[-1].append(sum([player.points_won[i] for i in range(len(player.points_won)) if player.numbers[i]==number]))
        points_lost[-1].append(sum([player.points_lost[i] for i in range(len(player.points_lost)) if player.numbers[i]==number]))
        points_played[-1].append(sum([player.points_played[i] for i in range(len(player.points_played)) if player.numbers[i]==number]))
        points_present[-1].append(sum([player.points_present[i] for i in range(len(player.points_present)) if player.numbers[i]==number]))
        starting_sets[-1].append(sum([player.starting_sets[i] for i in range(len(player.starting_sets)) if player.numbers[i]==number]))
        sets_won[-1].append(sum([player.sets_won[i] for i in range(len(player.sets_won)) if player.numbers[i]==number]))
        sets_lost[-1].append(sum([player.sets_lost[i] for i in range(len(player.sets_lost)) if player.numbers[i]==number]))

    # sort numbers according to largest contribution of points_present
    ind = np.argsort(points_present[-1])[::-1]
    points_won[-1]     = [points_won[-1][i] for i in ind]
    points_lost[-1]    = [points_lost[-1][i] for i in ind]
    points_played[-1]  = [points_played[-1][i] for i in ind]
    points_present[-1] = [points_present[-1][i] for i in ind]
    starting_sets[-1]  = [starting_sets[-1][i] for i in ind]
    sets_won[-1]       = [sets_won[-1][i] for i in ind]
    sets_lost[-1]      = [sets_lost[-1][i] for i in ind]
    nums[-1]           = [nums[-1][i] for i in ind]
    ylabel.append(player.name+" ("+",".join([f"{x}" for x in nums[-1]])+")")

plot_data=[points_present, points_played, points_won, starting_sets]
plot_norm=[stat.total_points, stat.total_points, stat.total_points, stat.total_sets]
# plot_label=['points played', 'points won', 'points present', 'starting sets', 'sets won']
plot_label=['Punkte anwesend', 'Punkte gespielt', 'Punkte gewonnen', 'Startaufstellung']
n_data=len(plot_data)


################################################################################
# print and export table with player statistics                                #
################################################################################
fid = open(f'files/table_{team_name}_raw.tex', 'w')
n_matches=len(stat.matches)
title=f'Statistics for {n_matches} matches from {stat.first_date} to {stat.last_date}.'
header='{name:20s} | {numbers:8s} | {p_present:6s} ({p_present_ratio:3s}) | {p_played:6s} ({p_played_ratio1:4s},{p_played_ratio2:4s}) | {p_won:4s} | {p_lost:4s} | {p_ratio_str:s}'.format(
    # name='Name',
    # numbers='Numbers',
    # p_present='present',
    # p_present_ratio='%',
    # p_played='played',
    # p_played_ratio1='own',
    # p_played_ratio2='tot',
    # p_won='won',
    # p_lost='lost',
    # p_ratio_str='ratio'
    name='Name',
    numbers='Nummern',
    p_present='anwesend',
    p_present_ratio='%',
    p_played='gespielt',
    p_played_ratio1='anw',
    p_played_ratio2='tot',
    p_won='gew',
    p_lost='verl',
    p_ratio_str='Quote'
    )
tex_header=header.replace('|','&')
tex_header=tex_header.replace('(','& (')
tex_header=tex_header.replace('%','\\%')
fid.write(tex_header+'\\\\\n')
print(title)
print(header)
# print(tex_header)

for iplayer in range(len(stat.player)):
    p_won=sum(points_won[iplayer])
    p_lost=sum(points_lost[iplayer])
    p_played=sum(points_played[iplayer])
    p_present=sum(points_present[iplayer])
    p_ratio_str="{p_ratio:.2f}".format(p_ratio=p_won/p_lost) if p_lost>0 else ''
    if p_won+p_lost!=p_played: raise Exception(f'Failed consistency check for {stat.player[iplayer].name}: {p_won}+{p_lost}!={p_played}')
    line='{name:20s} | {numbers:8s} | {p_present:6d} ({p_present_ratio:3.0f}%) | {p_played:6d} ({p_played_ratio1:3.0f}%,{p_played_ratio2:3.0f}%) | {p_won:4d} | {p_lost:4d} | {p_ratio_str:s}'.format(
        name=stat.player[iplayer].name,
        numbers=','.join([f"{x}" for x in set(stat.player[iplayer].numbers)]),
        p_present=p_present,
        p_present_ratio=p_present/stat.total_points*100,
        p_played=p_played,
        p_played_ratio1=p_played/p_present*100,
        p_played_ratio2=p_played/stat.total_points*100,
        p_won=p_won,
        p_lost=p_lost,
        p_ratio_str=p_ratio_str
        )
    tex_line=line.replace('|','&')
    tex_line=tex_line.replace('(','& (')
    tex_line=tex_line.replace('%','\\%')
    tex_line+='\\\\\n'
    fid.write(tex_line)
    print(line)
    # print(tex_line)

fid.close()


################################################################################
# Plot bar chart                                                               #
################################################################################

# Cmap=plt.get_cmap("Pastel1")
Cmap=plt.get_cmap("Dark2")

# print(color)
dimming=2/3

# color=np.array([[0,0,1.0], [0,1.0,0], [1.0,0,0]])
# color=np.array([[114,147,203],
                # [225,151, 76],
                # [132,166, 91]], dtype=np.float64)

fig1,ax1=plt.subplots()
# yy=np.arange(len(points_played))
yy=np.arange(len(points_played),0,-1)
height=1/(n_data+1)
ax1.grid()
ax1.set_axisbelow(True)
for iplayer in range(len(stat.player)):
    points_played_left=0
    points_present_left=0
    starting_sets_left=0
    left=[0]*n_data
    for inum in range(len(nums[iplayer])):
        offset=(n_data-1)/2
        for idata in range(n_data):
            # print(Cmap(idata))
            color=[dimming**inum*x for x in Cmap(idata)[0:3]]
            # print(color)
            ax1.barh(yy[iplayer]+offset*height, plot_data[idata][iplayer][inum]/plot_norm[idata], height=height, left=left[idata], label=plot_label[idata], color=color)
            left[idata]+=plot_data[idata][iplayer][inum]/plot_norm[idata]
            offset-=1
        # h1=ax1.barh(yy[iplayer]+height, points_played[iplayer][inum]/stat.total_points , height=height, left=points_played_left , label='points played' , color=color[0]/255)
        # h2=ax1.barh(yy[iplayer]       , points_present[iplayer][inum]/stat.total_points, height=height, left=points_present_left, label='points present', color=color[1]/255)
        # h3=ax1.barh(yy[iplayer]-height, starting_sets[iplayer][inum]/stat.total_sets   , height=height, left=starting_sets_left , label='starting sets' , color=color[2]/255)
        # points_played_left+=points_played[iplayer][inum]/stat.total_points
        # points_present_left+=points_present[iplayer][inum]/stat.total_points
        # starting_sets_left+=starting_sets[iplayer][inum]/stat.total_sets
        # color*=0.66

ax1.set_yticks(yy, ylabel)
ax1.set_xlim([0,1])
xticks=ax1.get_xticks()
ax1.set_xticks(xticks, ["{x:.0f} %".format(x=100*x) for x in xticks])
fig1.subplots_adjust(left=0.2)
# fig1.legend([h1._label,h2._label,h3._label])
fig1.legend(plot_label)
plt.show()
fig1.savefig(f"figures/{team_name}_proportions.png")



if interactive:
    import plotly.express as px
    import plotly.graph_objects as go
    fig2=go.Figure()
    # px.bar(x=[0.0,1.0], y=[1.3, 2.4])
    # fig2.add_trace(go.Bar(x=[0.0,1.0], y=[1.3, 2.4]))
    for iplayer in range(len(stat.player)):
        # print(yy[iplayer], points_played[iplayer])
        points_played_left=0
        points_present_left=0
        starting_sets_left=0
        # color=np.array([[0,0,1.0], [0,1.0,0], [1.0,0,0]])
        color=np.array([[114,147,203],
                        [225,151, 76],
                        [132,166, 91]], dtype=np.float64)
        for inum in range(len(nums[iplayer])):
            col1='rgb('+','.join(["{}".format(int(x)) for x in color[0]])+')'
            col2='rgb('+','.join(["{}".format(int(x)) for x in color[1]])+')'
            col3='rgb('+','.join(["{}".format(int(x)) for x in color[2]])+')'
            # print(col)
            marker1=go.bar.Marker(color=col1)
            marker2=go.bar.Marker(color=col2)
            marker3=go.bar.Marker(color=col3)
            # hoverlabel1=go.bar.Hoverlabel(bgcolor='#ffffff')
            # hoverlabel1=go.bar.Hoverlabel()
            hover1=f"{names[iplayer]} ({nums[iplayer][inum]}): {points_played[iplayer][inum]}/{stat.total_points}"
            hover2=f"{names[iplayer]} ({nums[iplayer][inum]}): {points_present[iplayer][inum]}/{stat.total_points}"
            hover3=f"{names[iplayer]} ({nums[iplayer][inum]}): {starting_sets[iplayer][inum]}/{stat.total_sets}"
            bar1=go.Bar(y=[yy[iplayer]+height],
                 x=[points_played[iplayer][inum]/stat.total_points],
                 width=height,
                 base=points_played_left,
                 orientation='h',
                 marker=marker1,
                 legendgroup='points played',
                 name='points played',
                 hoverinfo="text",
                 hovertext=hover1
                        )
            bar2=go.Bar(y=[yy[iplayer]       ],
                 x=[points_present[iplayer][inum]/stat.total_points],
                 width=height,
                 base=points_present_left,
                 orientation='h',
                 marker=marker2,
                 legendgroup='points present',
                 name='points present',
                 hoverinfo="text",
                 hovertext=hover2
                        )
            bar3=go.Bar(y=[yy[iplayer]-height],
                 x=[starting_sets[iplayer][inum]/stat.total_sets],
                 width=height,
                 base=starting_sets_left,
                 orientation='h',
                 marker=marker3,
                 legendgroup='starting sets',
                 name='starting sets',
                 hoverinfo="text",
                 hovertext=hover3
                        )
            if (iplayer>0 or inum>0):
                bar1.showlegend=False
                bar2.showlegend=False
                bar3.showlegend=False
            fig2.add_trace(bar1)
            fig2.add_trace(bar2)
            fig2.add_trace(bar3)

            points_played_left+=points_played[iplayer][inum]/stat.total_points
            points_present_left+=points_present[iplayer][inum]/stat.total_points
            starting_sets_left+=starting_sets[iplayer][inum]/stat.total_sets
            color*=0.66
        # px.bar(y=[yy[iplayer]], x=points_played[iplayer], barmode='group')
        # fig2.add_trace(go.Bar(y=[yy[iplayer]]*len(points_played[iplayer]), x=points_played[iplayer], offset=

    fig2.update_layout(
            yaxis=dict(
                tickmode='array',
                tickvals=yy,
                ticktext=ylabel
                ),
            xaxis_tickformat='.0%'
            # xaxis=dict(tickformat='.0f%')
            )
    # fig2.update_layout(xaxis=dict(tickformat='.2f%'))
    # fig2.update_layout(xaxis_tickformat = '.0%')
    fig2.show()
