from utils import statistics, player_statistics

def match2stat(match):
    # print(match)
    match_stat=statistics(matches=[match.id], total_matches=1)

    # initialize player statistics for the match
    for p in match.players:
        player=player_statistics(name=p.name, matches_present=[match.id], numbers=[p.number], dates=[match.date])
        match_stat.first_date=match.date
        match_stat.last_date=match.date
        # match_stat.player.append(player)
        match_stat.add_player_stat(player)


    points_in_match=0
    sets_won=0
    sets_lost=0
    players_involved=[]
    for current_set in match.setlist:
        points_in_set=sum(current_set.final_score)
        points_in_match+=points_in_set

        if current_set.final_score[0]>current_set.final_score[1]:
            current_set_won=True
            sets_won+=1
        else:
            current_set_won=False
            sets_lost+=1
        for player_num in current_set.players:
            player=match.num2player(player_num)
            players_involved.append(player)
            match_stat.add_player_stat(player_statistics(name=player.name, matches_present=[match.id], sets_involved=[1]))
            # add to won and lost sets to all participating players
            if current_set_won:
                match_stat.add_player_stat(player_statistics(name=player.name, matches_present=[match.id], sets_won=[1]))
            else:
                match_stat.add_player_stat(player_statistics(name=player.name, matches_present=[match.id], sets_lost=[1]))


        # add total points played in match to each player. subtract points if
        # player is substituted
        for player_num in current_set.starting:
            # get player name from number
            player=match.num2player(player_num)
            match_stat.add_player_stat(player_statistics(name=player.name, matches_present=[match.id], sets_started=[1], points_involved=[points_in_set], points_won=[current_set.final_score[0]], points_lost=[current_set.final_score[1]]))
            # add match starting players to statistics
            if current_set.num==1:
                match_stat.add_player_stat(player_statistics(name=player.name, matches_present=[match.id], matches_started=[1]))

        # loop through substitutions and transfer points from players (out) to players (in)
        for subst in current_set.substitutions:
            points_involved_at_subst=sum(subst.score)
            points_won_at_subst=subst.score[0]
            points_lost_at_subst=subst.score[1]
            playerin=match.num2player(subst.playerin)
            playerout=match.num2player(subst.playerout)
            points_to_end_of_set=points_in_set-points_involved_at_subst
            points_won_to_end=current_set.final_score[0]-points_won_at_subst
            points_lost_to_end=current_set.final_score[1]-points_lost_at_subst
            match_stat.add_player_stat(player_statistics(name=playerin.name, matches_present=[match.id], points_involved=[points_to_end_of_set], points_won=[points_won_to_end], points_lost=[points_lost_to_end]))
            match_stat.add_player_stat(player_statistics(name=playerout.name, matches_present=[match.id], points_involved=[-points_to_end_of_set], points_won=[-points_won_to_end], points_lost=[-points_lost_to_end]))

    match_stat.total_points=points_in_match
    match_stat.total_sets_won=sets_won
    match_stat.total_sets_lost=sets_lost
    match_stat.total_sets=len(match.setlist)

    for p in match.players:
        # add (points & sets) present to all players in the match
        match_stat.add_player_stat(player_statistics(name=p.name, matches_present=[match.id], points_present=[points_in_match]))
        match_stat.add_player_stat(player_statistics(name=p.name, matches_present=[match.id], sets_present=[len(match.setlist)]))

        if p in players_involved:
            match_stat.add_player_stat(player_statistics(name=p.name, matches_present=[match.id], matches_involved=[1]))

        if sets_won>sets_lost:
            match_stat.add_player_stat(player_statistics(name=p.name, matches_present=[match.id], matches_won=[1]))
        else:
            match_stat.add_player_stat(player_statistics(name=p.name, matches_present=[match.id], matches_lost=[1]))


    # print(match_stat)
    return match_stat

