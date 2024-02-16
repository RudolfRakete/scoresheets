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


def rot_raw2list(raw):
    rot = re.findall(r'╳|\d+', raw)
    # filter out ╳ and replace with -1 for now
    rot = [int(x) if x.isnumeric() else -1 for x in rot]
    # rot = [int(x.replace('╳','0')) for x in rot]
    rot.sort()
    return rot

def list_saved_team_names():
    file_list = os.listdir('./files/')
    name_list=[]
    print(file_list)
    for file in file_list:
        reg = re.search('statistics_(.*).dat', file)
        if reg:
            name_list.append(reg.group(1))

    name_str=', '.join(name_list)
    return name_str
