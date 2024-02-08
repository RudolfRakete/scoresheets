from utils import statistics, player_statistics

def match2stat(match):
    # print(match)
    match_stat=statistics(matches=[match.id])

    # initialize player statistics for the match
    for p in match.players:
        player=player_statistics(name=p.name, matches=[match.id], numbers=[p.number], dates=[match.date])
        match_stat.first_date=match.date
        match_stat.last_date=match.date
        # match_stat.player.append(player)
        match_stat.add_player_stat(player)


    points_in_match=0
    sets_won=0
    sets_lost=0
    for set in match.setlist:
        points_in_set=sum(set.final_score)
        points_in_match+=points_in_set

        if set.final_score[0]>set.final_score[1]:
            current_set_won=True
            sets_won+=1
        else:
            current_set_won=False
            sets_lost+=1
        # add to won and lost sets to all participating players
        for player_num in set.players:
            player=match.num2player(player_num)
            if current_set_won:
                match_stat.add_player_stat(player_statistics(name=player.name, matches=[match.id], sets_won=[1]))
            else:
                match_stat.add_player_stat(player_statistics(name=player.name, matches=[match.id], sets_lost=[1]))


        # add total points played in match to each player. subtract points if
        # player is substituted
        for player_num in set.starting:
            # get player name from number
            player=match.num2player(player_num)
            match_stat.add_player_stat(player_statistics(name=player.name, matches=[match.id], starting_sets=[1], points_played=[points_in_set], points_won=[set.final_score[0]], points_lost=[set.final_score[1]]))

        # loop through substitutions and transfer points from players (out) to players (in)
        for subst in set.substitutions:
            points_played_at_subst=sum(subst.score)
            points_won_at_subst=subst.score[0]
            points_lost_at_subst=subst.score[1]
            playerin=match.num2player(subst.playerin)
            playerout=match.num2player(subst.playerout)
            points_to_end_of_set=points_in_set-points_played_at_subst
            points_won_to_end=set.final_score[0]-points_won_at_subst
            points_lost_to_end=set.final_score[1]-points_lost_at_subst
            match_stat.add_player_stat(player_statistics(name=playerin.name, matches=[match.id], points_played=[points_to_end_of_set], points_won=[points_won_to_end], points_lost=[points_lost_to_end]))
            match_stat.add_player_stat(player_statistics(name=playerout.name, matches=[match.id], points_played=[-points_to_end_of_set], points_won=[-points_won_to_end], points_lost=[-points_lost_to_end]))

    match_stat.total_points=points_in_match
    match_stat.total_sets_won=sets_won
    match_stat.total_sets_lost=sets_lost
    match_stat.total_sets=len(match.setlist)

    for p in match.players:
        # add points present to all players in the match
        match_stat.add_player_stat(player_statistics(name=p.name, matches=[match.id], points_present=[points_in_match]))
        if sets_won>sets_lost:
            match_stat.add_player_stat(player_statistics(name=p.name, matches=[match.id], matches_won=[1]))
        else:
            match_stat.add_player_stat(player_statistics(name=p.name, matches=[match.id], matches_lost=[1]))


    # print(match_stat)
    return match_stat

