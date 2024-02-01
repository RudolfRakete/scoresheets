import os
from dataclasses import dataclass, field

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
    startingB:     list[pdf_box] = field(default=list)
    # switchB:       list[pdf_box] = field(default=list)
    # switch_scoreB: list[pdf_box] = field(default=list)
    final_scoreB:  pdf_box = None

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

    def __str__(self):
        strout = f"Set {self.num}.\n"
        strout+=f"Final score {self.final_score}\n"
        strout+=f"Starting players: {self.starting}\n"
        strout+=f"Participating players: {self.players}\n"
        strout+=f"Substitutions:\n"
        for i in range(len(self.substitutions)):
            strout+=f"{self.substitutions[i]}\n"
        return strout

@dataclass
class VBmatch:
    opponent:str=''
    id:int=None
    # n_players:int=None
    players:list[player]=field(default_factory=lambda: [])
    liberos:list[player]=field(default_factory=lambda: [])
    officials:list[player]=field(default_factory=lambda: [])
    # player_numbers:list[int]=field(default=list)
    # player_names:list[str]=field(default=list)
    # points_played:list[int]=field(default=list)
    setlist:list[set]=field(default_factory=lambda: [])

    def num2player(self, num):
        player = [x for x in self.players if x.number==num]
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
    # * number of the matches played
    # * points played in each match
    # * number of sets the player was in the starting rotation for each match played
    # * number of the points present for each match
    name:str=''
    numbers:list[int]=field(default_factory=lambda: []) # list to account for change of player number between matches
    matches:list[str]=field(default_factory=lambda: [])
    points_played:list[int]=field(default_factory=lambda: [])
    starting_sets:list[int]=field(default_factory=lambda: [])
    points_present:list[int]=field(default_factory=lambda: [])

    def __add__(self, other):
        if (self.name!=other.name):
            raise Exception(f"Trying to add stats of {other.name} to stats of {self.name}")
        # print(f"Adding \n{other}\nto \n{self}")

        if other.numbers:
            self.numbers += other.numbers
            # get unique numbers
            self.numbers = list(set(self.numbers))
        
        for i in range(len(other.matches)):
            match_id=other.matches[i]
            # if (self.matches) and (match_id in self.matches):
            if (match_id in self.matches):
                ind_match=self.matches.index(match_id)
                # check if items in list exist (may not exist when lazily adding player_statistics with only partially set stats)
                if len(other.points_played)>=i+1:
                    self.points_played[ind_match] += other.points_played[i]
                if len(other.points_present)>=i+1:
                    self.points_present[ind_match] += other.points_present[i]
                if len(other.starting_sets)>=i+1:
                    self.starting_sets[ind_match] += other.starting_sets[i]
            else:
                self.matches.append(other.matches[i])
                # check if items in list exist (may not exist when lazily adding player_statistics with only partially set stats)
                if len(other.points_played)>=i+1:
                    self.points_played.append(other.points_played[i])
                else: 
                    self.points_played.append(0)
                if len(other.points_present)>=i+1:
                    self.points_present.append(other.points_present[i])
                else:
                    self.points_present.append(0)
                if len(other.starting_sets)>=i+1:
                    self.starting_sets.append(other.starting_sets[i])
                else:
                    self.starting_sets.append(0)

        return self

        # print(f"Result: {self}\n\n")






@dataclass
class statistics:
    # class to store statistics of several matches
    # includes:
    # * list of player statistics
    # * total number of points played across all matches
    # * total number of sets played across all matches
    player:list[player_statistics]=field(default_factory=lambda: [])
    total_points:int=0
    total_sets:int=0

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
        # adds player_statistics to list
        # creates new entry if player name is not found
        player=self.get_player_stat(player_stat.name)
        player+=player_stat

    def __add__(self, other):
        # print(f"Adding\n{other}\nto\n{self}")
        self.total_points+=other.total_points
        self.total_sets+=other.total_sets
        
        # add player statistics
        for player_stat2 in other.player:
            player_stat1 = self.get_player_stat(player_stat2.name)
            player_stat1 += player_stat2

        # print(f"Result:\n{self}")
        return self
            

