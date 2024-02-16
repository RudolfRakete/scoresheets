import os
import re
import copy
import global_positions as coords
import numpy as np
import datetime
from utils import *


def extract_game_info(pdffile, team_name_regex):
    if not os.path.isfile(pdffile):
        raise Exception(f"Scoresheet not found. {pdffile}")
    current_match=VBmatch()
    current_match.setlist=[]
    current_match.players=[]
    # current_match.player_names=[]
    # current_match.player_numbers=[]

    # get match id
    title=pdf2str(pdffile, coords.title)
    # get team names and determine if tracked team is A or B
    reg=re.search(r'([AB]) (.*) vs\. (.*) ([AB])', title)
    if not reg:
        raise Exception(f"Could not determine teams and letters (A/B) from title: {title}")

    # print(reg.group(1))
    # print(reg.group(2))
    # print(reg.group(3))
    # print(reg.group(4))

    if re.search(team_name_regex, reg.group(2)):
        AorB=reg.group(1)
        current_match.opponent=reg.group(3)
    elif re.search(team_name_regex, reg.group(3)):
        AorB=reg.group(4)
        current_match.opponent=reg.group(2)
    else:
        raise Exception(f"Could not find \'{team_name_regex}\' in title: {title}")

    reg_id=re.search(r'Spiel (\d+)', title)
    if reg_id:
        current_match.id=int(reg_id.group(1))
    else:
        raise Exception(f"Could not extract match id from title: {title}")

    print(f"Reading scoresheet for match {current_match.id} against {current_match.opponent}")

    reg_date=re.search(r'(\d{2}).(\d{2}).(\d{4})', title)
    if reg_date:
        day=int(reg_date.group(1))
        month=int(reg_date.group(2))
        year=int(reg_date.group(3))
        current_match.date=datetime.date(day=day, month=month, year=year)
        # current_match.date=reg_date.group(1)
    else:
        raise Exception(f"Could not extract date from title: {title}")
    # print(current_match.date)

################################################################################
# read team list                                                               #
################################################################################
    teamlist_left=pdf2str(pdffile, coords.teamlist_left).split('\n')
    teamlist_right=pdf2str(pdffile, coords.teamlist_right).split('\n')
    team_header_left=teamlist_left[0]
    team_header_right=teamlist_right[0]

    if re.search(team_name_regex, team_header_left):
        teamlist=teamlist_left
    elif re.search(team_name_regex, team_header_right):
        teamlist=teamlist_right
    else:
        raise Exception(f"Could not find \'{team_name_regex}\' in teamlist header")

    is_libero=0
    player_name_list=[]
    for line in teamlist:
        # print('line:',line)
        reg_header=re.search('[AB] (.*)', line)
        if reg_header:
            # found header
            if reg_header.group(1)=='Libero':
                is_libero=1
            # elif reg_header.group(1)=='Offizielle':
            else:
                is_libero=0
        reg_player=re.search(r'(\d+) (.*)', line)
        if reg_player:
            # found player
            number = reg_player.group(1)
            name = reg_player.group(2)
            player_name_list.append(name)
            # remove special marks from player names (neede twice if both are present)
            name=re.sub('^[C|★] ', '', name)
            name=re.sub('^[C|★] ', '', name)
            if not is_libero:
                current_match.players.append(player(name=name, number=int(number)))
            else:
                lib_player = current_match.num2player(int(number))
                lib_player.is_libero=1
        reg_official=re.search('(T|CT|SC|P) (.*)', line)
        if reg_official:
            # found official
            official_type=reg_official.group(1)
            name=reg_official.group(2)
            # check if official is also player (if yes update number, if not append new player)
            if name in player_name_list:
                p=current_match.name2player(name)
                p.number=f"{p.number}+{official_type}"
            else:
                current_match.players.append(player(name=name, number=official_type))



################################################################################
# extract information from score sheet                                         #
################################################################################
    for iset in range(4):
        # read final results
        scoreA_str=pdf2str(pdffile, coords.VBset[iset].final_scoreA)
        scoreB_str=pdf2str(pdffile, coords.VBset[iset].final_scoreB)

        # check if set was played
        if scoreA_str=="":
            continue
        # check if any sanction points are marked below final score (looking at you, Kai!!! -.-)
        scoreA_str = scoreA_str.split('\n')[0]
        scoreB_str = scoreB_str.split('\n')[0]
        scoreA=int(scoreA_str)
        scoreB=int(scoreB_str)

        # initialize current set
        current_set=VBset()
        current_set.num=iset+1
        current_set.starting=[None]*6
        current_set.players=[]
        current_set.substitutions=[]
        print(f"Reading info for set {iset+1}")

        if AorB=='A':
            current_set.final_score = [scoreA,scoreB]
        elif AorB=='B':
            current_set.final_score = [scoreB,scoreA]

        # read starting player information and raw substitution data
        if AorB=='A':
            pos = coords.VBset[iset].startingA
        elif AorB=='B':
            pos = coords.VBset[iset].startingB

        for ipos in range(6):
            # starting players
            current_player = int(pdf2str(pdffile, pos[ipos]))
            current_set.starting[ipos] = current_player
            current_set.players.append(current_player)

            # substitution info
            sw_pos = copy.copy(pos[ipos])
            sw_pos.x+=1
            sw_pos.W-=2
            sw_pos.y+=11.25 # one cell down
            sw_player_str = pdf2str(pdffile, sw_pos)
            sw_pos.y+=11.25
            sw1_score_str = pdf2str(pdffile, sw_pos)
            sw_pos.y+=11.25
            sw2_score_str = pdf2str(pdffile, sw_pos)

            # regular substitution
            if sw1_score_str != "":
                sw_player=int(sw_player_str)
                sw1_score = list(map(int, re.findall(r'\d+', sw1_score_str)))
                current_subst=VBsubstitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                current_set.players.append(sw_player)
                current_set.substitutions.append(current_subst)

            # back substitution
            if sw2_score_str != "":
                sw_player=int(sw_player_str)
                sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                current_subst=VBsubstitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
                current_set.substitutions.append(current_subst)

        # read rotation information
        rot_strA=pdf2str(pdffile, coords.VBset[iset].rotationA)
        rot_strB=pdf2str(pdffile, coords.VBset[iset].rotationB)
        if AorB=='A':
            current_set.rotation=rot_raw2list(rot_strA)
            current_set.opp_rotation=rot_raw2list(rot_strB)
        elif AorB=='B':
            current_set.rotation=rot_raw2list(rot_strB)
            current_set.opp_rotation=rot_raw2list(rot_strA)

        # print(current_set)


        # add set to setlist
        current_match.setlist.append(current_set)

    # extract tiebreak information if neccessary
    tb_name_left=pdf2str(pdffile, coords.tb.name_left)
    tb_name_middle=pdf2str(pdffile, coords.tb.name_middle)
    tb_name_right=pdf2str(pdffile, coords.tb.name_right)

    # print(tb_name_left)
    # print(tb_name_middle)
    # print(tb_name_right)

    tb_sides_switched=False
    if tb_name_right!='':
        tb_sides_switched=True

    
    # check if tiebreak is recorded
    reg1=re.search(team_name_regex, tb_name_left)
    reg2=re.search(team_name_regex, tb_name_middle)
    # if tb_name_left!='':
    if reg1 or reg2:
        current_set=VBset()
        current_set.num=5
        current_set.starting=[None]*6
        current_set.players=[]
        current_set.substitutions=[]
        print("Reading info for set 5 (tiebreak)")

        final_score_left_str   = pdf2str(pdffile, coords.tb.final_score_left)
        final_score_middle_str = pdf2str(pdffile, coords.tb.final_score_middle)
        final_score_right_str  = pdf2str(pdffile, coords.tb.final_score_right)

        # print(final_score_left_str)
        # print(final_score_middle_str)
        # print(final_score_right_str)

        final_score_left=int(final_score_left_str)
        final_score_middle=int(final_score_middle_str)
        final_score_right=int(final_score_right_str)

        rot_str_left   = pdf2str(pdffile, coords.tb.rotation_left)
        rot_str_middle = pdf2str(pdffile, coords.tb.rotation_middle)
        rot_str_right  = pdf2str(pdffile, coords.tb.rotation_right)

        rot_left_only = rot_raw2list(rot_str_left)
        rot_middle = rot_raw2list(rot_str_middle)
        rot_right = rot_raw2list(rot_str_right)

        # combine left and right rotation lists and remove duplicates
        rot_left = list(set(rot_left_only+rot_right))
        rot_left.sort()

        # print(rot_left)
        # print(rot_middle)

        # check if tracked team is on the outside
        if re.search(team_name_regex, tb_name_left):
            # print('tracked team is on the left of tiebreak')
            # read starting player info
            for ipos in range(6):
                current_player=int(pdf2str(pdffile, coords.tb.starting_left[ipos]))
                current_set.starting[ipos]=current_player
                current_set.players.append(current_player)

                # read substitutions (left side)
                sw_pos = copy.copy(coords.tb.starting_left[ipos])
                sw_pos.x+=1
                sw_pos.W-=2
                sw_pos.y+=11.25 # one cell down
                sw_player_str = pdf2str(pdffile, sw_pos)
                sw_pos.y+=11.25
                sw1_score_str = pdf2str(pdffile, sw_pos)
                sw_pos.y+=11.25
                sw2_score_str = pdf2str(pdffile, sw_pos)

                # regular substitution
                if sw1_score_str != "":
                    sw_player=int(sw_player_str)
                    sw1_score = list(map(int, re.findall(r'\d+', sw1_score_str)))
                    current_subst=VBsubstitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                    current_set.players.append(sw_player)
                    current_set.substitutions.append(current_subst)

                # back substitution
                if sw2_score_str != "":
                    sw_player=int(sw_player_str)
                    sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                    current_subst=VBsubstitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
                    current_set.substitutions.append(current_subst)

                # read substitutions (right side)
                sw_pos = copy.copy(coords.tb.starting_right[ipos])
                sw_pos.x+=1
                sw_pos.W-=2
                sw_pos.y+=11.25 # one cell down
                sw_player_str = pdf2str(pdffile, sw_pos)
                sw_pos.y+=11.25
                sw1_score_str = pdf2str(pdffile, sw_pos)
                sw_pos.y+=11.25
                sw2_score_str = pdf2str(pdffile, sw_pos)

                # regular substitution
                if sw1_score_str != "":
                    sw_player=int(sw_player_str)
                    sw1_score = list(map(int, re.findall(r'\d+', sw1_score_str)))
                    current_subst=VBsubstitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                    current_set.players.append(sw_player)
                    current_set.substitutions.append(current_subst)

                # back substitution
                if sw2_score_str != "":
                    sw_player=int(sw_player_str)
                    sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                    current_subst=VBsubstitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
                    current_set.substitutions.append(current_subst)


            current_set.rotation=rot_left
            current_set.opp_rotation=rot_middle
            
            # read final score info
            if tb_sides_switched:
                current_set.final_score=[final_score_right,final_score_middle]
            else:
                current_set.final_score=[final_score_left,final_score_middle]
        # team is in the middle
        # else:
        elif re.search(team_name_regex, tb_name_middle):
            # print('UNTESTED CODE!!')
            # print('tracked team is in the middle of tiebreak')
            # read starting player info
            for ipos in range(6):
                current_player=int(pdf2str(pdffile, coords.tb.starting_middle[ipos]))
                current_set.starting[ipos]=current_player
                current_set.players.append(current_player)

                # read substitutions (left side)
                sw_pos = copy.copy(coords.tb.starting_middle[ipos])
                sw_pos.x+=1
                sw_pos.W-=2
                sw_pos.y+=11.25 # one cell down
                sw_player_str = pdf2str(pdffile, sw_pos)
                sw_pos.y+=11.25
                sw1_score_str = pdf2str(pdffile, sw_pos)
                sw_pos.y+=11.25
                sw2_score_str = pdf2str(pdffile, sw_pos)

                # regular substitution
                if sw1_score_str != "":
                    sw_player=int(sw_player_str)
                    sw1_score = list(map(int, re.findall(r'\d+', sw1_score_str)))
                    current_subst=VBsubstitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                    current_set.players.append(sw_player)
                    current_set.substitutions.append(current_subst)

                # back substitution
                if sw2_score_str != "":
                    sw_player=int(sw_player_str)
                    sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                    current_subst=VBsubstitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
                    current_set.substitutions.append(current_subst)


            current_set.rotation=rot_middle
            current_set.opp_rotation=rot_left

            if tb_sides_switched:
                current_set.final_score=[final_score_middle,final_score_right]
            else:
                current_set.final_score=[final_score_middle,final_score_left]
        else:
            raise Exception('Could not find {team_name_regex} in header for tiebreak: {tb_name_left},{tb_name_middle}')


        current_match.setlist.append(current_set)

        

    return current_match
