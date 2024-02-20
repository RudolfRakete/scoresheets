# import re
import datetime
from difflib import SequenceMatcher
from dataclasses import dataclass, field
from extract_positions import extract_game_info
import config as cnfg

@dataclass
class player_statistics:
    # includes player name and the following lists
    # * player number (or code) for each match
    # * id of the match played
    # * points won in each match (not yet used)
    # * points lost in each match (not yet used)
    # * points played in each match
    # * number of the points present for each match
    # * number of sets the player was in the starting rotation for each match played
    # * number of sets won and lost where the player participated
    name:str=''
    numbers:list[int]=field(default_factory=lambda: []) # list to account for change of player number between matches
    # match info
    dates:list[datetime.date]  = field(default_factory = lambda: [])
    matches_present:list[int]  = field(default_factory = lambda: []) # contains match id
    matches_started:list[int]  = field(default_factory = lambda: []) # contains number of matches 
    matches_involved:list[int] = field(default_factory = lambda: []) # contains number of matches
    matches_won:list[int]      = field(default_factory = lambda: []) # contains number of matches
    matches_lost:list[int]     = field(default_factory = lambda: []) # contains number of matches
    # set info
    sets_present:list[int]  = field(default_factory = lambda: [])
    sets_started:list[int]  = field(default_factory = lambda: [])
    sets_involved:list[int] = field(default_factory = lambda: [])
    sets_won:list[int]      = field(default_factory = lambda: [])
    sets_lost:list[int]     = field(default_factory = lambda: [])
    # points info
    points_present:list[int]  = field(default_factory = lambda: [])
    points_involved:list[int] = field(default_factory = lambda: [])
    points_won:list[int]      = field(default_factory = lambda: [])
    points_lost:list[int]     = field(default_factory = lambda: [])

    def __add__(self, other):
        if not other.name:
            raise Exception(f"Can not add player statistics without name.")

        if not other.matches_present:
            raise Exception(f"Can not add player statistics without match id.\nself:\n{self}\nother:\n{other}")

        # if (self.name!=other.name):
        closeness=SequenceMatcher(None, self.name, other.name).ratio()
        if closeness<cnfg.name_closeness_threshold:
            raise Exception(f"Trying to add stats of {other.name} to stats of {self.name}")
        # print(f"Adding \n{other}\nto \n{self}")

        if other.numbers:
            self.numbers += other.numbers
            # get unique numbers
            # self.numbers = list(set(self.numbers))
        
        for i in range(len(other.matches_present)):
            # check if match is already present in self.matches_present
            match_id=other.matches_present[i]
            # if (self.matches_present) and (match_id in self.matches_present):
            if (match_id in self.matches_present):
                ind_match=self.matches_present.index(match_id)
                # check if items in list exist (may not exist when lazily adding player_statistics with only partially set stats)
                # if len(other.dates)>=i+1:            self.dates[ind_match]            += other.dates[i]
                #
                if len(other.matches_started)>=i+1:  self.matches_started[ind_match]  += other.matches_started[i]
                if len(other.matches_involved)>=i+1: self.matches_involved[ind_match] += other.matches_involved[i]
                if len(other.matches_won)>=i+1:      self.matches_won[ind_match]      += other.matches_won[i]
                if len(other.matches_lost)>=i+1:     self.matches_lost[ind_match]     += other.matches_lost[i]
                #
                if len(other.sets_present)>=i+1:     self.sets_present[ind_match]     += other.sets_present[i]
                if len(other.sets_started)>=i+1:     self.sets_started[ind_match]     += other.sets_started[i]
                if len(other.sets_involved)>=i+1:    self.sets_involved[ind_match]    += other.sets_involved[i]
                if len(other.sets_won)>=i+1:         self.sets_won[ind_match]         += other.sets_won[i]
                if len(other.sets_lost)>=i+1:        self.sets_lost[ind_match]        += other.sets_lost[i]
                #
                if len(other.points_present)>=i+1:   self.points_present[ind_match]   += other.points_present[i]
                if len(other.points_involved)>=i+1:  self.points_involved[ind_match]  += other.points_involved[i]
                if len(other.points_won)>=i+1:       self.points_won[ind_match]       += other.points_won[i]
                if len(other.points_lost)>=i+1:      self.points_lost[ind_match]      += other.points_lost[i]
            else:
                self.matches_present.append(other.matches_present[i])
                # check if items in list exist (may not exist when lazily adding player_statistics with only partially set stats)
                if len(other.dates)>=i+1:            self.dates.append(other.dates[i])
                else:                                self.dates.append(0)
                #                                    
                if len(other.matches_started)>=i+1:  self.matches_started.append(other.matches_started[i])  
                else:                                self.matches_started.append(0)
                if len(other.matches_involved)>=i+1: self.matches_involved.append(other.matches_involved[i])
                else:                                self.matches_involved.append(0)
                if len(other.matches_won)>=i+1:      self.matches_won.append(other.matches_won[i])          
                else:                                self.matches_won.append(0)
                if len(other.matches_lost)>=i+1:     self.matches_lost.append(other.matches_lost[i])        
                else:                                self.matches_lost.append(0)
                #                                    
                if len(other.sets_present)>=i+1:     self.sets_present.append(other.sets_present[i])        
                else:                                self.sets_present.append(0)
                if len(other.sets_started)>=i+1:     self.sets_started.append(other.sets_started[i])        
                else:                                self.sets_started.append(0)
                if len(other.sets_involved)>=i+1:    self.sets_involved.append(other.sets_involved[i])      
                else:                                self.sets_involved.append(0)
                if len(other.sets_won)>=i+1:         self.sets_won.append(other.sets_won[i])                
                else:                                self.sets_won.append(0)
                if len(other.sets_lost)>=i+1:        self.sets_lost.append(other.sets_lost[i])              
                else:                                self.sets_lost.append(0)
                #
                if len(other.points_involved)>=i+1:  self.points_involved.append(other.points_involved[i])  
                else:                                self.points_involved.append(0)
                if len(other.points_won)>=i+1:       self.points_won.append(other.points_won[i])            
                else:                                self.points_won.append(0)
                if len(other.points_lost)>=i+1:      self.points_lost.append(other.points_lost[i])          
                else:                                self.points_lost.append(0)
                if len(other.points_present)>=i+1:   self.points_present.append(other.points_present[i])    
                else:                                self.points_present.append(0)

        return self


    def __str__(self):
        str=f"Name: {self.name}\n"
        # str+=f"

        return str







@dataclass
class statistics:
    # class to store statistics of several matches
    # includes:
    # * list of match ids
    # * list of player statistics
    # * total number of points played across all matches
    # * total number of sets played across all matches
    team_name:str=''
    team_name_regex:str=''
    first_date:datetime.date=datetime.date(day=1,month=1,year=datetime.MAXYEAR)
    last_date:datetime.date=datetime.date(day=1,month=1,year=datetime.MINYEAR)
    matches:list[int]=field(default_factory=lambda: [])
    player:list[player_statistics]=field(default_factory=lambda: [])
    total_points:int=0 
    total_points_won:int=0
    total_points_lost:int=0
    total_sets:int=0
    total_sets_won:int=0
    total_sets_lost:int=0
    total_matches:int=0

    def get_player_stat(self, name):
        # returns or creates a new player_statistics class and appends to list
        for p in self.player:
            closeness=SequenceMatcher(None, name, p.name).ratio()
            if closeness>cnfg.name_closeness_threshold:
                # print(f"Found incomplete name match: {p.name} | {name} | {closeness}")
                return p
            # if name==p.name:
                # return p
        new_player=player_statistics()
        new_player.name=name
        self.player.append(new_player)
        return self.player[-1]

    def add_player_stat(self, player_stat):
        # ALWAYS USE THIS FUNCTION WHEN ADDING PLAYER STATISTICS. THE __add__ FUNCTION OF player_statistics ENSURES CORRECT ADDITION WITH INCOMPLETE player_statistics.
        # adds player_statistics to list
        # creates new entry if player name is not found
        player=self.get_player_stat(player_stat.name)
        player+=player_stat

    def __add__(self, other):
        if self.first_date>other.first_date:
            self.first_date=other.first_date
        if self.last_date<other.last_date:
            self.last_date=other.last_date
        # print(f"Adding\n{other}\nto\n{self}")
        self.matches+=other.matches
        self.total_points+=other.total_points
        self.total_points_won+=other.total_points_won
        self.total_points_lost+=other.total_points_lost
        self.total_sets+=other.total_sets
        self.total_sets_won+=other.total_sets_won
        self.total_sets_lost+=other.total_sets_lost
        self.total_matches+=other.total_matches
        
        # add player statistics
        for player_stat2 in other.player:
            player_stat1 = self.get_player_stat(player_stat2.name)
            player_stat1 += player_stat2

        # print(f"Result:\n{self}")
        return self

    def add_scoresheet(self, file):
        game_info=extract_game_info(file, self.team_name_regex)
        new_stats=match2stat(game_info)
        return self+new_stats
            


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

