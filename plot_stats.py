import sys
import os
import re
from utils import *
# from extract_positions import extract_game_info
import pickle
import numpy as np
import matplotlib.pyplot as plt

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

# print(stat)

names=[]
nums=[]
ylabel=[]
points_played=[]
points_present=[]
sets=[]
starting_sets=[]
for player in stat.player:
    # print(player)
    # nums = ','.join([f"{x}" for x in player.numbers])
    # points_played_per_num=[]
    points_played.append([])
    points_present.append([])
    starting_sets.append([])

    unique_nums=list(set(player.numbers))
    # ylabel=f"{player.name} ("+','.join([f"{x}" for x in unique_nums])+")"
    names.append(player.name)
    nums.append(unique_nums)
    # print(ylabel)
    for number in unique_nums:
        # print(number)
        # print([x for x in player.points_played])
        points_played[-1].append(sum([player.points_played[i] for i in range(len(player.points_played)) if player.numbers[i]==number]))
        points_present[-1].append(sum([player.points_present[i] for i in range(len(player.points_present)) if player.numbers[i]==number]))
        starting_sets[-1].append(sum([player.starting_sets[i] for i in range(len(player.starting_sets)) if player.numbers[i]==number]))

    # sort numbers according to largest contribution of points_present
    ind = np.argsort(points_present[-1])[::-1]
    points_played[-1]  = [points_played[-1][i] for i in ind]
    points_present[-1] = [points_present[-1][i] for i in ind]
    starting_sets[-1]  = [starting_sets[-1][i] for i in ind]
    nums[-1] = [nums[-1][i] for i in ind]
    ylabel.append(player.name+" ("+",".join([f"{x}" for x in nums[-1]])+")")


fig1,ax1=plt.subplots()
yy=np.arange(len(points_played))
height=0.25
ax1.grid()
ax1.set_axisbelow(True)
for iplayer in range(len(stat.player)):
    points_played_left=0
    points_present_left=0
    starting_sets_left=0
    # color=np.array([[0,0,1.0], [0,1.0,0], [1.0,0,0]])
    color=np.array([[114,147,203],
                    [225,151, 76],
                    [132,166, 91]], dtype=np.float64)
    for inum in range(len(nums[iplayer])):
        h1=ax1.barh(yy[iplayer]+height, points_played[iplayer][inum]/stat.total_points , height=height, left=points_played_left , label='points played' , color=color[0]/255)
        h2=ax1.barh(yy[iplayer]       , points_present[iplayer][inum]/stat.total_points, height=height, left=points_present_left, label='points present', color=color[1]/255)
        h3=ax1.barh(yy[iplayer]-height, starting_sets[iplayer][inum]/stat.total_sets   , height=height, left=starting_sets_left , label='starting sets' , color=color[2]/255)
        points_played_left+=points_played[iplayer][inum]/stat.total_points
        points_present_left+=points_present[iplayer][inum]/stat.total_points
        starting_sets_left+=starting_sets[iplayer][inum]/stat.total_sets
        color*=0.66

ax1.set_yticks(yy, ylabel)
ax1.set_xlim([0,1])
xticks=ax1.get_xticks()
ax1.set_xticks(xticks, ["{x:.0f} %".format(x=100*x) for x in xticks])
fig1.subplots_adjust(left=0.2)
fig1.legend([h1._label,h2._label,h3._label])
# plt.show()
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
