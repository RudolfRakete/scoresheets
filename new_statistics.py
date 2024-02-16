from utils import *
import shutil
import sys
from game_statistics import match2stat, statistics
import pickle
import glob

def get_help_str():
    str="Call as\nnew_statistics.py <team_name> <team_name_regex>\nExample: new_statistics.py BRV 'BERLIN RECYCLING|Berlin'\n"
    str+="\nteam_name can be anything.\n"
    str+="team_name_regex must match scoresheet header and team list header.\n"
    # print(str)
    return str

if len(sys.argv)==1:
    str="No arguments given.\n"
    print(str+get_help_str())
    exit()

if sys.argv[1]=='help':
    print(get_help_str())
    exit()

# Sanitize inputs                                                              #
if len(sys.argv)<3:
    str="No team name and regex given.\n"
    str+=get_help_str()
    raise Exception(str)

if len(sys.argv)>3:
    raise Exception(f"No team name and regex given.\nCall as\nnew_statistics.py <team_name> <team_name_regex>\nExample: new_statistics.py BRV 'BERLIN RECYCLING|Berlin'\n")


team_name=sys.argv[1]
team_name_regex=sys.argv[2]
path=f'./scoresheets/{team_name}/'
scoresheets=glob.glob('/'.join([path,'*.pdf']))
# scoresheets=glob.glob('/'.join([path,'2010.pdf']))


# Initialize statistics and add statistics from each scoresheet.
stat = statistics(team_name=team_name, team_name_regex=team_name_regex)
for fname in scoresheets:
    stat.add_scoresheet(fname)


# Save new statistics (copying old file to backup if found)
fname_stat=f"./files/statistics_{team_name}.dat"
fname_stat_backup=f"./files/statistics_{team_name}_backup.dat"
if os.path.isfile(fname_stat):
    shutil.copy(fname_stat, fname_stat_backup)
with open(fname_stat, 'wb') as f:
    pickle.dump([stat], f)
