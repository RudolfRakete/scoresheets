import re
import copy
import global_positions as coords
from utils import *


def extract_player_info(pdffile,AorB):
    setlist=[]

    # extract information from score sheet
    for iset in range(4):
        # read final results
        scoreA_str=pdf2str(pdffile, coords.set[iset].final_scoreA)
        scoreB_str=pdf2str(pdffile, coords.set[iset].final_scoreB)

        # check if set was played
        if scoreA_str=="":
            continue
        scoreA=int(scoreA_str)
        scoreB=int(scoreB_str)

        # initialize current set
        current_set=set()
        current_set.num=iset+1
        current_set.players=[None]*6
        current_set.switches=[]
        print(f"Reading into for set {iset+1}")

        if AorB=='A':
            current_set.final_score = [scoreA,scoreB]
        elif AorB=='B':
            current_set.final_score = [scoreB,scoreA]

        # read starting player information and raw switch data
        if AorB=='A':
            pos = coords.set[iset].startingA
        elif AorB=='B':
            pos = coords.set[iset].startingB

        for ipos in range(6):
            # starting players
            current_player = int(pdf2str(pdffile, pos[ipos]))
            current_set.players[ipos] = current_player

            # switch info
            sw_pos = copy.copy(pos[ipos])
            sw_pos.x+=1
            sw_pos.W-=2
            sw_pos.y+=11.25 # one cell down
            sw_player_str = pdf2str(pdffile, sw_pos)
            sw_pos.y+=11.25
            sw1_score_str = pdf2str(pdffile, sw_pos)
            sw_pos.y+=11.25
            sw2_score_str = pdf2str(pdffile, sw_pos)

            # regular switch
            if sw1_score_str != "":
                sw_player=int(sw_player_str)
                sw1_score = list(map(int, re.findall(r'\d+', sw1_score_str)))
                current_switch=switch(playerin=sw_player,playerout=current_player,score=sw1_score)
                current_set.switches.append(current_switch)

            # switch back
            if sw2_score_str != "":
                sw_player=int(sw_player_str)
                sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                current_switch=switch(playerin=current_player,playerout=sw_player,score=sw2_score)
                current_set.switches.append(current_switch)


        print(current_set)


        # add set to setlist
        setlist.append(current_set)

    return setlist
