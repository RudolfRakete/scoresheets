from utils import statistics, player_statistics

def match2stat(match):
    print(match)
    match_stat=statistics()

    # initialize player statistics for the match
    for p in match.players:
        player=player_statistics(name=p.name, numbers=[p.number])
        match_stat.player.append(player)

    points_in_match=0
    for set in match.setlist:
        points_in_set=sum(set.final_score)
        points_in_match+=points_in_set


        # add total points played in match to each player. subtract points if
        # player is substituted
        for player_num in set.starting:
            # get player name from number
            player=match.num2player(player_num)
            match_stat.add_player_stat(player_statistics(name=player.name, matches=[match.id], starting_sets=[1], points_played=[points_in_set]))

        # loop through substitutions and transfer points from players (out) to players (in)
        for subst in set.substitutions:
            points_played_at_subst=sum(subst.score)
            playerin=match.num2player(subst.playerin)
            playerout=match.num2player(subst.playerout)
            points_to_end_of_set=points_in_set-points_played_at_subst
            match_stat.add_player_stat(player_statistics(name=playerin.name, matches=[match.id], points_played=[points_to_end_of_set]))
            match_stat.add_player_stat(player_statistics(name=playerout.name, matches=[match.id], points_played=[-points_to_end_of_set]))

    match_stat.total_points=points_in_match
    match_stat.total_sets=len(match.setlist)

    for p in match.players:
        # add points present to all players in the match
        match_stat.add_player_stat(player_statistics(name=p.name, matches=[match.id], points_present=[points_in_match]))


    # print(match_stat)
    return match_stat

