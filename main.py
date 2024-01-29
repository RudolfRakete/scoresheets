from extract_positions import extract_game_info
from game_statistics import player_statistics

scoresheets=['2074.pdf', '2071.pdf', '2025.pdf']

for imatch in range(len(scoresheets)):
    print(f"Reading {scoresheets[imatch]}")
    match=extract_game_info(scoresheets[imatch])


    player_statistics(match)
