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

# class coord:
    # def __init__(self, x, y):
        # self.x=x
        # self.y=y
    # def __str__(self):
        # return f"({self.x},{self.y})"

# class pdf_box:
    # def __init__(self, x, y, W, H):
        # self.x=x
        # self.y=y
        # self.W=W
        # self.H=H

    # def __str__(self):
        # return f"pdf box: ({self.x} {self.y} {self.W} {self.H})"

# class pdf_coords:
    # def __init__(self, set=[None]*5):
        # self.set=set

# class set_coords:
    # def __init__(self, num=None, startingA=[None]*6, switchA=[None]*6, switch_scoreA=[[None]*2]*6, final_scoreA=[None], startingB=[None]*6, switchB=[None]*6, switch_scoreB=[[None]*2]*6, final_scoreB=[None]):
        # self.num=num
        # self.startingA=startingA
        # self.switchA=switchA
        # self.switch_scoreA=switch_scoreA
        # self.final_scoreA=final_scoreA
        # self.startingB=startingB
        # self.switchB=switchB
        # self.switch_scoreB=switch_scoreB
        # self.final_scoreB=final_scoreB


@dataclass
class set:
    num:int=None
    final_score:list[int]=field(default=list)
    players:list[int]=field(default=list)
    switches:list[int]=field(default=list)
    # def __init__(self, num=0, final_score=[None]*2, players=[None]*6, switches=[]):
        # self.num=num
        # self.final_score=final_score
        # self.players=players
        # self.switches=switches

    def __str__(self):
        strout = f"Set {self.num}.\n"
        strout+=f"Final score {self.final_score}\n"
        strout+=f"Starting players: {self.players}\n"
        strout+=f"Switches:\n"
        for i in range(len(self.switches)):
            strout+=f"{self.switches[i]}\n"
        return strout

@dataclass
class switch:
    playerout:int=None
    playerin:int=None
    score:list[int]=field(default=list)
    # def __init__(self, playerout=None, playerin=None, score=[None]*2):
        # self.playerout=playerout
        # self.playerin=playerin
        # self.score=score

    def __str__(self):
        return f"Switch: {self.playerout} -> {self.playerin} at {self.score[0]}:{self.score[1]}"


def pdf2str(pdffile,pdf_box):
    options = '-x {x:d} -y {y:d} -W {W:d} -H {H:d}'.format(x=int(pdf_box.x), y=int(pdf_box.y), W=int(pdf_box.W), H=int(pdf_box.H))
    ex_call=' '.join(['pdftotext', options, pdffile, '-'])
    ret=os.popen(ex_call).read()
    ret = ret.strip()
    return ret


# def 
