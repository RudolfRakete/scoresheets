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
class substitution:
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
class set:
    num:int=None
    final_score:list[int]=field(default=list)
    starting:list[int]=field(default=list)
    players:list[int]=field(default=list)
    substitutions:list[substitution]=field(default=list)

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
class match:
    opponent:str=''
    n_players:int=None
    player_numbers:list[int]=field(default=list)
    player_names:list[str]=field(default=list)
    # points_played:list[int]=field(default=list)
    setlist:list[set]=field(default=list)


def pdf2str(pdffile,pdf_box):
    options = '-x {x:d} -y {y:d} -W {W:d} -H {H:d}'.format(x=int(pdf_box.x), y=int(pdf_box.y), W=int(pdf_box.W), H=int(pdf_box.H))
    ex_call=' '.join(['pdftotext', options, pdffile, '-'])
    ret=os.popen(ex_call).read()
    ret = ret.strip()
    return ret

@dataclass
class match_statistics:
    player_numbers:list[int]=field(default=list)
    player_names:list[int]=field(default=list)
    points_played:list[int]=field(default=list)
    starting_sets:list[int]=field(default=list)
    total_points:int=None
