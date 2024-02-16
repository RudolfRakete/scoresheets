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
    name_str = list_saved_team_names()
    # print(file_list)
    raise Exception(f"No team name given. Found statistics files for the following teams:\n {name_str}\nCall as\npython3 plot_stats.py <team_name>")

team_name=sys.argv[1]
# team_name='SVP'

stat=load_stat_file(team_name)

# print(stat)

if not os.path.isdir('./figures'):
    os.mkdir('./figures/')

# sort players according to the smallest number in numbers list (officials go last)
smallest_num=[]
for player in stat.player:
    if any(isinstance(x, int) for x in player.numbers):
        smallest_num.append(min([x for x in player.numbers if isinstance(x,int)]))
    else:
        smallest_num.append(9999)
ind = np.argsort(smallest_num)
stat.player=[stat.player[i] for i in ind]

################################################################################
# loop through players and gather statistics                                   #
################################################################################
names=[]
nums=[]
ylabel=[]
#
points_involved=[]
points_present=[]
points_won=[]
points_lost=[]
#
sets=[]
sets_started=[]
sets_present=[]
sets_involved=[]
sets_won=[]
sets_lost=[]
#
matches_present=[]
matches_started=[]
matches_involved=[]
for player in stat.player:
    # print(player)
    points_involved.append([])
    points_present.append([])
    points_won.append([])
    points_lost.append([])
    #
    sets_started.append([])
    sets_present.append([])
    sets_involved.append([])
    sets_won.append([])
    sets_lost.append([])
    #
    matches_started.append([])
    matches_present.append([])
    matches_involved.append([])


    unique_nums=list(set(player.numbers))
    # ylabel=f"{player.name} ("+','.join([f"{x}" for x in unique_nums])+")"
    names.append(player.name)
    nums.append(unique_nums)
    # print(ylabel)
    for number in unique_nums:
        # statistics on points
        points_present[-1].append(sum([player.points_present[i] for i in range(len(player.points_present)) if player.numbers[i]==number]))
        points_involved[-1].append(sum([player.points_involved[i] for i in range(len(player.points_involved)) if player.numbers[i]==number]))
        points_won[-1].append(sum([player.points_won[i] for i in range(len(player.points_won)) if player.numbers[i]==number]))
        points_lost[-1].append(sum([player.points_lost[i] for i in range(len(player.points_lost)) if player.numbers[i]==number]))
        # statistics on sets
        sets_present[-1].append(sum([player.sets_present[i] for i in range(len(player.sets_present)) if player.numbers[i]==number]))
        sets_involved[-1].append(sum([player.sets_involved[i] for i in range(len(player.sets_involved)) if player.numbers[i]==number]))
        sets_started[-1].append(sum([player.sets_started[i] for i in range(len(player.sets_started)) if player.numbers[i]==number]))
        sets_won[-1].append(sum([player.sets_won[i] for i in range(len(player.sets_won)) if player.numbers[i]==number]))
        sets_lost[-1].append(sum([player.sets_lost[i] for i in range(len(player.sets_lost)) if player.numbers[i]==number]))
        # statistics on matches
        matches_present[-1].append(len([player.matches_present[i] for i in range(len(player.matches_present)) if player.numbers[i]==number]))
        matches_involved[-1].append(sum([player.matches_involved[i] for i in range(len(player.matches_involved)) if player.numbers[i]==number]))
        matches_started[-1].append(sum([player.matches_started[i] for i in range(len(player.matches_started)) if player.numbers[i]==number]))

    # sort numbers according to largest contribution of points_present
    ind = np.argsort(points_present[-1])[::-1]
    nums[-1]             = [nums[-1][i] for i in ind]
    #
    points_involved[-1]    = [points_involved[-1][i] for i in ind]
    points_present[-1]   = [points_present[-1][i] for i in ind]
    points_won[-1]       = [points_won[-1][i] for i in ind]
    points_lost[-1]      = [points_lost[-1][i] for i in ind]
    #
    sets_started[-1]     = [sets_started[-1][i] for i in ind]
    sets_present[-1]     = [sets_present[-1][i] for i in ind]
    sets_involved[-1]    = [sets_involved[-1][i] for i in ind]
    sets_won[-1]         = [sets_won[-1][i] for i in ind]
    sets_lost[-1]        = [sets_lost[-1][i] for i in ind]
    # 
    matches_started[-1]  = [matches_started[-1][i] for i in ind]
    matches_present[-1]  = [matches_present[-1][i] for i in ind]
    matches_involved[-1] = [matches_involved[-1][i] for i in ind]
    ylabel.append(player.name+" ("+",".join([f"{x}" for x in nums[-1]])+")")

print(matches_present)
# print(ylabel)
# print(matches_started)

plot_data=[points_present, points_involved, points_won, sets_started]
plot_norm=[stat.total_points, stat.total_points, stat.total_points, stat.total_sets]
# plot_label=['points involved', 'points won', 'points present', 'starting sets', 'sets won']
plot_label=['Punkte anwesend', 'Punkte gespielt', 'Punkte gewonnen', 'Startaufstellung']
n_data=len(plot_data)


################################################################################
# print and export table with player statistics                                #
################################################################################
fname_tex=f'files/table_{team_name}.tex'
n_matches=len(stat.matches)
# title='Statistics for {n_matches} matches from {first} to {last}.'.format(n_matches=n_matches, first=stat.first_date.strftime('%d.%m.%Y'), last=stat.last_date.strftime('%d.%m.%Y'))
title='Statistik für {n_matches} Spiele des {team_name} vom {first} bis {last}.'.format(n_matches=n_matches, team_name=team_name, first=stat.first_date.strftime('%d.%m.%Y'), last=stat.last_date.strftime('%d.%m.%Y'))
# points | starting sets | involved sets | matches
# percent of total and present for each
header1 =' '*20+'{points:20s} | {sets_started:20s} | {sets:20s} | {matches:20s}'.format(
    points='Punkte',
    sets_started='Sätze in Startaufstellung',
    sets='Sätze mit Beteiligung',
    matches='Spiele'
    )
header2='{name:20s} | {numbers:8s} | {presence_ratio:8s} | {p_involved:4s} | {p_involved_ratio1:8s} | {p_involved_ratio2:8s} | {s_involved:2s} | {s_involved_ratio1:8s} | {s_involved_ratio2:8s} | {s_started:2s} | {s_started_ratio1:8s} | {s_started_ratio2:8s} | {m_involved:2s} | {m_involved_ratio1:8s} | {m_involved_ratio2:8s} | {m_started:2s} | {m_started_ratio1:8s} | {m_started_ratio2:8s}'.format(
        name='Name',
        numbers='Nummern',
        presence_ratio='anw.',
        p_involved='gespielt',
        p_involved_ratio1='% ges.',
        p_involved_ratio2='% anw. (Spieler)',
        s_started='gestartet',
        s_started_ratio1='% ges.',
        s_started_ratio2='% anw. (Spieler)',
        s_involved='anw.',
        s_involved_ratio1='% ges.',
        s_involved_ratio2='% anw. (Spieler)',
        m_involved='beteiligt',
        m_involved_ratio1='% ges.',
        m_involved_ratio2='% anw. (Spieler)',
        m_started='gestartet',
        m_started_ratio1='% ges.',
        m_started_ratio2='% anw. (Spieler)',
        )
tex_header1='&& \\multicolumn{4}{|c|}{Punkte} & \\multicolumn{6}{|c|}{Sätze} & \\multicolumn{3}{|c|}{Spiele}\\\\\n'
tex_header2=header2.replace('|','&')
tex_header2=tex_header2.replace('%','\\%')
print(title)
print(header1)
print(header2)
# print(tex_header)

tex_table=''
for iplayer in range(len(stat.player)):
    p_present=sum(points_present[iplayer])
    p_present_as_player=sum([points_present[iplayer][i] for i in range(len(points_present[iplayer])) if type(nums[iplayer][i])==int])
    p_involved=sum(points_involved[iplayer])
    p_won=sum(points_won[iplayer])
    p_lost=sum(points_lost[iplayer])
    # 
    s_present=sum(sets_present[iplayer])
    s_present_as_player=sum([sets_present[iplayer][i] for i in range(len(sets_present[iplayer])) if type(nums[iplayer][i])==int])
    s_involved=sum(sets_involved[iplayer])
    s_started=sum(sets_started[iplayer])
    # 
    # print(matches_present[iplayer])
    m_present=sum(matches_present[iplayer])
    m_present_as_player=sum([matches_present[iplayer][i] for i in range(len(matches_present[iplayer])) if type(nums[iplayer][i])==int])
    m_involved=sum(matches_involved[iplayer])
    m_started=sum(matches_started[iplayer])
    #
    # safely convert ratios to strings avoiding div by 0
    p_involved_ratio2_str = "{:3.0f}".format(p_involved/p_present_as_player*100) if p_present_as_player>0 else ''
    s_involved_ratio2_str = "{:3.0f}".format(s_involved/s_present_as_player*100) if s_present_as_player>0 else ''
    s_started_ratio2_str  = "{:3.0f}".format(s_started /s_present_as_player*100) if s_present_as_player>0 else ''
    line='{name:20s} | {numbers:8s} | {presence_ratio:3.0f}% | {p_involved:4d} | {p_involved_ratio1:3.0f}% | {p_involved_ratio2:s}% | {s_involved:2d} | {s_involved_ratio1:3.0f}% | {s_involved_ratio2:s}% | {s_started:2d} | {s_started_ratio1:3.0f}% | {s_started_ratio2:s}% | {m_involved:2d} | {m_involved_ratio1:3.0f}% | {m_involved_ratio2:3.0f}% | {m_started:2d} | {m_started_ratio1:3.0f}% | {m_started_ratio2:3.0f}%'.format(
        name=stat.player[iplayer].name,
        numbers=','.join([f"{x}" for x in set(stat.player[iplayer].numbers)]),
        #
        presence_ratio=p_present/stat.total_points*100,
        p_involved=p_involved,
        p_involved_ratio1=p_involved/stat.total_points*100,
        p_involved_ratio2=p_involved_ratio2_str,
        #
        s_involved=s_involved,
        s_involved_ratio1=s_involved/stat.total_sets*100,
        s_involved_ratio2=s_involved_ratio2_str,
        #
        s_started=s_started,
        s_started_ratio1=s_started/stat.total_sets*100,
        s_started_ratio2=s_started_ratio2_str,
        #
        m_involved=m_involved,
        m_involved_ratio1=m_involved/stat.total_matches*100,
        m_involved_ratio2=m_involved/m_present*100,
        #
        m_started=m_started,
        m_started_ratio1=m_started/stat.total_matches*100,
        m_started_ratio2=m_started/m_present*100,
        )
    tex_line=line.replace('|','&')
    tex_line=tex_line.replace('%','\\%')
    tex_line+='\\\\\n'
    tex_table+=tex_line
    print(line)
    # print(tex_line)


with open('files/tex_wrapper.tex', 'r') as f:
    tex_wrapper = f.read()
# print(tex_wrapper)
tex_wrapper=tex_wrapper.replace('TITLE', title)
tex_wrapper=tex_wrapper.replace('TABLE', tex_table)

with open(fname_tex, 'w') as f:
    f.write(tex_wrapper)

try:
    os.popen(f'pdflatex -output-directory=./files/ {fname_tex}')
except:
    print('Could not compile statistics table to pdf. Skipping.')
    # ret=os.popen(ex_call).read()


################################################################################
# Plot bar chart                                                               #
################################################################################

# Cmap=plt.get_cmap("Pastel1")
Cmap=plt.get_cmap("Dark2")

# print(color)
dimming=2/3

fig1,ax1=plt.subplots()
# yy=np.arange(len(points_involved))
yy=np.arange(len(points_involved),0,-1)
height=1/(n_data+1)
ax1.grid()
ax1.set_axisbelow(True)
for iplayer in range(len(stat.player)):
    points_involved_left=0
    points_present_left=0
    sets_started_left=0
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

ax1.set_yticks(yy, ylabel)
ax1.set_xlim([0,1])
xticks=ax1.get_xticks()
ax1.set_xticks(xticks, ["{x:.0f} %".format(x=100*x) for x in xticks])
fig1.subplots_adjust(left=0.25)
# fig1.legend([h1._label,h2._label,h3._label])
fig1.legend(plot_label)
fig1.suptitle(title)
plt.show()
fig1.savefig(f"figures/{team_name}_proportions.png")



if interactive:
    import plotly.express as px
    import plotly.graph_objects as go
    fig2=go.Figure()
    # px.bar(x=[0.0,1.0], y=[1.3, 2.4])
    # fig2.add_trace(go.Bar(x=[0.0,1.0], y=[1.3, 2.4]))
    for iplayer in range(len(stat.player)):
        # print(yy[iplayer], points_involved[iplayer])
        points_involved_left=0
        points_present_left=0
        sets_started_left=0
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
            hover1=f"{names[iplayer]} ({nums[iplayer][inum]}): {points_involved[iplayer][inum]}/{stat.total_points}"
            hover2=f"{names[iplayer]} ({nums[iplayer][inum]}): {points_present[iplayer][inum]}/{stat.total_points}"
            hover3=f"{names[iplayer]} ({nums[iplayer][inum]}): {sets_started[iplayer][inum]}/{stat.total_sets}"
            bar1=go.Bar(y=[yy[iplayer]+height],
                 x=[points_involved[iplayer][inum]/stat.total_points],
                 width=height,
                 base=points_involved_left,
                 orientation='h',
                 marker=marker1,
                 legendgroup='points involved',
                 name='points involved',
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
                 x=[sets_started[iplayer][inum]/stat.total_sets],
                 width=height,
                 base=sets_started_left,
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

            points_involved_left+=points_involved[iplayer][inum]/stat.total_points
            points_present_left+=points_present[iplayer][inum]/stat.total_points
            sets_started_left+=sets_started[iplayer][inum]/stat.total_sets
            color*=0.66
        # px.bar(y=[yy[iplayer]], x=points_involved[iplayer], barmode='group')
        # fig2.add_trace(go.Bar(y=[yy[iplayer]]*len(points_involved[iplayer]), x=points_involved[iplayer], offset=

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
