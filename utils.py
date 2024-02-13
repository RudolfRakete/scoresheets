import os
import re
import datetime
from dataclasses import dataclass, field

# @dataclass
# class team_info:
    # scoresheet_path:str='.'
    # team_name:str=''
    # team_name_regex:str=''

@dataclass
class coord:
    x:float=None
    y:float=None

@dataclass
class pdf_box:
    x:float=None
    y:float=None
    W:float=None
    H:float=None

@dataclass
class set_coords:
    startingA:     list[pdf_box] = field(default=list)
    # switchA:       list[pdf_box] = field(default=list)
    # switch_scoreA: list[pdf_box] = field(default=list)
    final_scoreA:  pdf_box = None
    rotationA: pdf_box = None
    startingB:     list[pdf_box] = field(default=list)
    # switchB:       list[pdf_box] = field(default=list)
    # switch_scoreB: list[pdf_box] = field(default=list)
    final_scoreB:  pdf_box = None
    rotationB: pdf_box = None

@dataclass
class tiebreak_coords:
    name_left:pdf_box=None
    name_middle:pdf_box=None
    name_right:pdf_box=None
    final_score_left:pdf_box=None
    final_score_middle:pdf_box=None 
    final_score_right:pdf_box=None


@dataclass
class VBsubstitution:
    playerout:int=None
    playerin:int=None
    score:list[int]=field(default=list)
    backsubstitution:int=None

    def __str__(self):
        if self.backsubstitution:
            return f"Substitution: {self.playerin} <- {self.playerout} at {self.score[0]}:{self.score[1]}"
        else:
            return f"Substitution: {self.playerout} -> {self.playerin} at {self.score[0]}:{self.score[1]}"

@dataclass
class player:
    name:str=''
    number:int=None
    is_libero:int=0

@dataclass
class VBset:
    num:int=None
    final_score:list[int]=field(default=list)
    starting:list[int]=field(default=list)
    players:list[int]=field(default=list)
    substitutions:list[VBsubstitution]=field(default=list)
    rotation:list[int]=field(default_factory=lambda: [])
    opp_rotation:list[int]=field(default_factory=lambda: [])

    def __str__(self):
        strout = f"Set {self.num}.\n"
        strout+=f"Final score {self.final_score}\n"
        strout+=f"Starting players: {self.starting}\n"
        strout+=f"Participating players: {self.players}\n"
        strout+=f"Rotation information: {self.rotation}\n                      {self.opp_rotation}\n"
        strout+=f"Substitutions:\n"
        for i in range(len(self.substitutions)):
            strout+=f"{self.substitutions[i]}\n"
        return strout

@dataclass
class VBmatch:
    opponent:str=''
    id:int=None
    date:datetime.date=None
    # n_players:int=None
    players:list[player]=field(default_factory=lambda: [])
    liberos:list[player]=field(default_factory=lambda: [])
    officials:list[player]=field(default_factory=lambda: [])
    # player_numbers:list[int]=field(default=list)
    # player_names:list[str]=field(default=list)
    # points_involved:list[int]=field(default=list)
    setlist:list[VBset]=field(default_factory=lambda: [])

    def num2player(self, num):
        player = [x for x in self.players if x.number==num]
        if not player:
            raise Exception(f"Player with number {num} not in player list:\n {self.players}")
        return player[0]

    def name2player(self, name):
        player = [x for x in self.players if x.name==name]
        if not player:
            raise Exception(f"Player with name {name} not in player list:\n {self.players}")
        return player[0]





def pdf2str(pdffile,pdf_box):
    options = '-x {x:d} -y {y:d} -W {W:d} -H {H:d}'.format(x=int(pdf_box.x), y=int(pdf_box.y), W=int(pdf_box.W), H=int(pdf_box.H))
    ex_call=' '.join(['pdftotext', options, pdffile, '-'])
    ret=os.popen(ex_call).read()
    ret = ret.strip()
    return ret

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

        if (self.name!=other.name):
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
                if len(other.dates)>=i+1:            self.dates[ind_match]            += other.dates[i]
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

        # print(f"Result: {self}\n\n")






@dataclass
class statistics:
    # class to store statistics of several matches
    # includes:
    # * list of match ids
    # * list of player statistics
    # * total number of points played across all matches
    # * total number of sets played across all matches
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
            if name==p.name:
                return p
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
            


def rot_raw2list(raw):
    rot = re.findall(r'╳|\d+', raw)
    # filter out ╳ and replace with -1 for now
    rot = [int(x) if x.isnumeric() else -1 for x in rot]
    # rot = [int(x.replace('╳','0')) for x in rot]
    rot.sort()
    return rot
