from utils import match_statistics

def player_statistics(match):
    stat=match_statistics()
    stat.player_numbers=match.player_numbers
    stat.player_names=match.player_names
    stat.points_played=[0]*len(match.player_numbers)
    stat.starting_sets=[0]*len(match.player_numbers)

    # print(stat)
    # print(stat.player_numbers.index(13))
    # print(stat.player_names[stat.player_numbers.index(13)])

    points_in_match=0
    for set in match.setlist:
        points_in_set=sum(set.final_score)
        points_in_match+=points_in_set
        # print(points_in_set)


        # add total points played in match to each player. subtract points if
        # player is substituted
        for player in set.starting:
            ind_player=stat.player_numbers.index(player)
            stat.starting_sets[ind_player]+=1
            stat.points_played[ind_player]+=points_in_set

        # loop through substitutions and transfer points from players (out) to players (in)
        for subst in set.substitutions:
            points_played_at_subst=sum(subst.score)
            ind_playerout=stat.player_numbers.index(subst.playerout)
            ind_playerin=stat.player_numbers.index(subst.playerin)
            stat.points_played[ind_playerout]-=points_in_set-points_played_at_subst
            stat.points_played[ind_playerin ]+=points_in_set-points_played_at_subst

    stat.total_points=points_in_match

    print(stat)

