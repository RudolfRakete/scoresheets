from utils import *
import re
import sys
import shutil
from game_statistics import match2stat, statistics
import pickle
import glob

# Sanitize inputs                                                              #
if len(sys.argv)==1:
    name_str = list_saved_team_names()
    raise Exception(f"No team name and scoresheet file given. Found statistics files for the following teams:\n {name_str}\nCall as\npython3 plot_stats.py <team_name> <path/to/scoresheet.pdf>")

if len(sys.argv)==2:
    reg = re.search('.*\.pdf$', sys.argv[1])
    if reg:
        name_str = list_saved_team_names()
        raise Exception(f"No team name given. Found statistics files for the following teams:\n {name_str}\nCall as\npython3 plot_stats.py <team_name> <path/to/scoresheet.pdf>")
    else:
        raise Exception(f"No score sheet file given. \nCall as\npython3 plot_stats.py <team_name> <path/to/scoresheet.pdf>")
        

if len(sys.argv)>3:
    raise Exception(f"Too many arguments given.\nCall as\npython3 plot_stats.py <team_name> <path/to/scoresheet.pdf>")


team_name=sys.argv[1]
fname_scoresheet=sys.argv[2]


# Load current statistics for team                                             #
fname_stat=f"./files/statistics_{team_name}.dat"
fname_stat_backup=f"./files/statistics_{team_name}_backup.dat"
if not os.path.isfile(fname_stat):
    raise Exception('Could not find file {fname_stat} with game statistics. Call new_statistics.py.')
shutil.copy(fname_stat, fname_stat_backup)
with open(fname_stat, 'rb') as f:
    # copy old file as backup
    stat = pickle.load(f)[0]


# Extract and add statistics from scoresheet                                   #
stat.add_scoresheet(fname_scoresheet)


# Save new statistics                                                          #
with open(f"./files/statistics_{team_name}.dat", 'wb') as f:
    pickle.dump([stat], f)
