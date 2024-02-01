from utils import *
from extract_positions import extract_game_info
from game_statistics import match2stat
import pickle
import glob

path='./scoresheets/SVP/'
# team_name=''
# team_name_regex=''
scoresheets=glob.glob('/'.join([path,'*.pdf']))
# print(scoresheets)

# scoresheets=['2074.pdf', '2071.pdf', '2025.pdf']
# scoresheets=['./scoresheets/2021.pdf']
# scoresheets=['./scoresheets/2074.pdf']


stat = statistics()
for imatch in range(len(scoresheets)):
    # print(f"Reading {scoresheets[imatch]}")
    match=extract_game_info(scoresheets[imatch])


    match_stat=match2stat(match)
    # print('match_stat:', match_stat)

    stat+=match_stat
    # print('stat after addition:',stat)


print(stat)

with open('stats.dat', 'wb') as f:
    pickle.dump([stat], f)


