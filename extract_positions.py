import re
import copy
import global_positions as coords
from utils import *


def extract_game_info(pdffile):
    current_match=match()
    current_match.setlist=[]
    current_match.player_names=[]
    current_match.player_numbers=[]

    # get team names and determine if SVP is A or B
    letter_left=pdf2str(pdffile, coords.letter_left)
    letter_right=pdf2str(pdffile, coords.letter_right)
    if (letter_left=='') or (letter_right==''):
        raise Exception('Could not read team letters (A/B) from player list.')
    # print(letter_left)
    # print(letter_right)
    name_left=pdf2str(pdffile, coords.team_left)
    name_right=pdf2str(pdffile, coords.team_right)
    # print(nameA, nameB)

    if re.match('Preu[ss|ß]en Berlin', name_left):
        AorB=letter_left
        LorR='L'
        current_match.opponent=name_right
    elif re.match('Preu[ss|ß]en Berlin', name_right):
        AorB=letter_right
        LorR='R'
        current_match.opponent=name_left
    else:
        raise Exception('Could not determine if SVP is team A or B.')
    # print(AorB)
    print(current_match.opponent)

    # get number of players
    if LorR=='L':
        n_players_str=pdf2str(pdffile,coords.n_players_left)
        coord_player_num=copy.copy(coords.player_numbers_left)
        coord_player_name=copy.copy(coords.player_names_left)
    else:
        n_players_str=pdf2str(pdffile,coords.n_players_right)
        coord_player_num=copy.copy(coords.player_numbers_right)
        coord_player_name=copy.copy(coords.player_names_right)

    current_match.n_players = int(re.findall('\d+', n_players_str)[0])

    # if AorB=='A':
        # current_match.n_players=n_playersA
        # coord_player_num=coords.player_numbersA
        # coord_player_name=coords.player_namesA
    # else:
        # current_match.n_players=n_playersB
        # coord_player_num=coords.player_numbersB
        # coord_player_name=coords.player_namesB

    # get player numbers and names
    for iplayer in range(current_match.n_players):
        # print(iplayer)
        number=pdf2str(pdffile, coord_player_num)
        name=pdf2str(pdffile, coord_player_name)
        # print(iplayer)
        # print(coord_player_num)
        # print(coord_player_name)
        # print(number,name)
        if (number=='') or (name==''):
            raise Exception(f"Could not read all players from playerinfo.\nSuccessfully read:{current_match.player_names}.")
        current_match.player_numbers.append(int(number))
        name=re.sub('^[C|★] ', '', name)
        current_match.player_names.append(name)
        # print(number, name)
        coord_player_num.y+=coords.playerinfo_vstride
        coord_player_name.y+=coords.playerinfo_vstride




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
            pos = coords.set[iset].startingA
        elif AorB=='B':
            pos = coords.set[iset].startingB

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
                current_subst=substitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                current_set.players.append(sw_player)
                current_set.substitutions.append(current_subst)

            # back substitution
            if sw2_score_str != "":
                sw_player=int(sw_player_str)
                sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                current_subst=substitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
                current_set.substitutions.append(current_subst)


        print(current_set)


        # add set to setlist
        current_match.setlist.append(current_set)

    # extract tiebreak information if neccessary
    tb_name_left=pdf2str(pdffile, coords.tb.name_left)
    tb_name_middle=pdf2str(pdffile, coords.tb.name_middle)
    tb_name_right=pdf2str(pdffile, coords.tb.name_right)

    print(tb_name_left)
    print(tb_name_middle)
    print(tb_name_right)

    tb_sides_switched=False
    if tb_name_right!='':
        tb_sides_switched=True

    
    # check if tiebreak is recorded
    if tb_name_left!='':
        current_set=set()
        current_set.num=5
        current_set.starting=[None]*6
        current_set.players=[]
        current_set.substitutions=[]
        print("Reading info for set 5 (tiebreak)")

        final_score_left=int(pdf2str(pdffile, coords.tb.final_score_left))
        final_score_middle=int(pdf2str(pdffile, coords.tb.final_score_middle))
        final_score_right=int(pdf2str(pdffile, coords.tb.final_score_right))

        # print(final_score_left)
        # print(final_score_middle)
        # print(final_score_right)
        # check if SVP is on the outside
        if re.match('.*Preu[ss|ß]en Berlin.*', tb_name_left):
            print('SVP is on the left')
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
                    current_subst=substitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                    current_set.players.append(sw_player)
                    current_set.substitutions.append(current_subst)

                # back substitution
                if sw2_score_str != "":
                    sw_player=int(sw_player_str)
                    sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                    current_subst=substitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
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
                    current_subst=substitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                    current_set.players.append(sw_player)
                    current_set.substitutions.append(current_subst)

                # back substitution
                if sw2_score_str != "":
                    sw_player=int(sw_player_str)
                    sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                    current_subst=substitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
                    current_set.substitutions.append(current_subst)


            
            # read final score info
            if tb_sides_switched:
                current_set.final_score=[final_score_right,final_score_middle]
            else:
                current_set.final_score=[final_score_left,final_score_middle]
        # SVP is in the middle
        else:
            print('SVP is in the middle')
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
                    current_subst=substitution(playerin=sw_player,playerout=current_player,score=sw1_score, backsubstitution=0)
                    current_set.players.append(sw_player)
                    current_set.substitutions.append(current_subst)

                # back substitution
                if sw2_score_str != "":
                    sw_player=int(sw_player_str)
                    sw2_score = list(map(int, re.findall(r'\d+', sw2_score_str)))
                    current_subst=substitution(playerin=current_player,playerout=sw_player,score=sw2_score, backsubstitution=1)
                    current_set.substitutions.append(current_subst)

            if tb_sides_switched:
                current_set.final_score=[final_score_middle,final_score_right]
            else:
                current_set.final_score=[final_score_middle,final_score_left]

        print(current_set)

        current_match.setlist.append(current_set)

        

    return current_match
