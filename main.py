from utils import *
# from extract_positions import extract_game_info
from game_statistics import match2stat, statistics
import pickle
import glob

team_name='SVP'
team_name_regex='Preußen Berlin'
path=f'./scoresheets/{team_name}/'
# scoresheets=glob.glob('/'.join([path,'*.pdf']))
# scoresheets=glob.glob('/'.join([path,'2010.pdf']))
scoresheets=glob.glob('/'.join([path,'202*.pdf']))

# team_name='BVV'
# team_name_regex='Berliner VV'
# path=f'./scoresheets/{team_name}/'
# scoresheets=glob.glob('/'.join([path,'*.pdf']))

# path='./scoresheets/BRV/'
# team_name='BRV'
# team_name_regex='BERLIN RECYCLING|Berlin'
# scoresheets=glob.glob('/'.join([path,'*.pdf']))

# scoresheets=['2074.pdf', '2071.pdf', '2025.pdf']
# scoresheets=['./scoresheets/SVP/2025.pdf']
# scoresheets=['./scoresheets/2074.pdf']


stat = statistics(team_name=team_name, team_name_regex=team_name_regex)
for imatch in range(len(scoresheets)):
    # print(f"Reading {scoresheets[imatch]}")
    # match=extract_game_info(scoresheets[imatch],team_name_regex)


    # print(match)
    # match_stat=match2stat(match)
    # print('match_stat:', match_stat)

    # stat+=match_stat

    stat=stat.add_scoresheet(scoresheets[imatch])
    # print('stat after addition:',stat)


print(stat)

with open(f"./files/statistics_{team_name}.dat", 'wb') as f:
    pickle.dump([stat], f)


