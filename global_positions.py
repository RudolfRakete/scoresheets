from utils import *

title=pdf_box(300, 24, 300, 38)

teamlist_left=pdf_box(590, 296, 113, 255)
teamlist_right=pdf_box(706, 296, 113, 255)

# coordinates of team names (taken from player overview)
letter_left =pdf_box(590  , 296.16, 12, 14)
letter_right=pdf_box(705.6, 296.16, 12, 14)
team_left   =pdf_box(603  ,296.2  , 78, 12)
team_right  =pdf_box(718.5,296.2  , 78, 12)

n_players_left=pdf_box(682, 296.2, 21, 12)
n_players_right=pdf_box(797, 296.2, 21, 12)

# get coordinates of playerinfo
playerinfo_vstride=9.75
player_numbers_left  = pdf_box(591.15, 309.00, 10.5, 10)
player_names_left    = pdf_box(602.3 , 309.00, 90  , 10)
player_numbers_right = pdf_box(705.58, 311.91, 10.5, 10)
player_names_right   = pdf_box(716.8 , 311.91, 90  , 10)

# initialize class for pdf coordinates to read info
VBset=[]
tb=tiebreak_coords()
tb.starting_left=[pdf_box]*6
tb.starting_middle=[pdf_box]*6
tb.starting_right=[pdf_box]*6
for i in range(5):
    VBset.append(set_coords())
    VBset[i].startingA= [pdf_box()]*6
    VBset[i].startingB= [pdf_box()]*6


# final results coordinates
# set 1
VBset[0].final_scoreA=pdf_box(251,97 ,25,40)
VBset[0].final_scoreB=pdf_box(407,97 ,25,40)
# set 2
VBset[1].final_scoreA=pdf_box(738,97 ,25,40)
VBset[1].final_scoreB=pdf_box(582,97 ,25,40)
# set 3
VBset[2].final_scoreA=pdf_box(251,211,25,40)
VBset[2].final_scoreB=pdf_box(407,211,25,40)
# set 4
VBset[3].final_scoreA=pdf_box(738,211,25,40)
VBset[3].final_scoreB=pdf_box(582,211,25,40)
# set 4
tb.name_left          = pdf_box(165.8, 297, 84, 15)
tb.name_middle        = pdf_box(321.7, 297, 84, 15)
tb.name_right         = pdf_box(477.8, 297, 84, 15)
tb.final_score_left   = pdf_box(251.2, 325, 25, 40)
tb.final_score_middle = pdf_box(407.1, 325, 25, 40)
tb.final_score_right  = pdf_box(563.2, 325, 25, 40)


# starting position coordinates
# units in pt
linewidth = 0.75
pos_width  = (20.25+21)/2
pos_height = 10.5
# set 1 A
VBset[0].startingA[0]=pdf_box(123   ,96.7  ,pos_width,pos_height)
VBset[0].startingA[1]=pdf_box(144   ,96.7  ,pos_width,pos_height)
VBset[0].startingA[2]=pdf_box(165.7 ,96.7  ,pos_width,pos_height)
VBset[0].startingA[3]=pdf_box(186.7 ,96.7  ,pos_width,pos_height)
VBset[0].startingA[4]=pdf_box(208.45,96.7  ,pos_width,pos_height)
VBset[0].startingA[5]=pdf_box(229.45,96.7  ,pos_width,pos_height)
# set 1 B
VBset[0].startingB[0]=pdf_box(278.9 ,96.7  ,pos_width,pos_height)
VBset[0].startingB[1]=pdf_box(299.9 ,96.7  ,pos_width,pos_height)
VBset[0].startingB[2]=pdf_box(321.65,96.7  ,pos_width,pos_height)
VBset[0].startingB[3]=pdf_box(342.65,96.7  ,pos_width,pos_height)
VBset[0].startingB[4]=pdf_box(364.4 ,96.7  ,pos_width,pos_height)
VBset[0].startingB[5]=pdf_box(385.4 ,96.7  ,pos_width,pos_height)
# set 2 A
VBset[1].startingA[0]=pdf_box(608.8 ,96.7  ,pos_width,pos_height)
VBset[1].startingA[1]=pdf_box(630.5 ,96.7  ,pos_width,pos_height)
VBset[1].startingA[2]=pdf_box(652.3 ,96.7  ,pos_width,pos_height)
VBset[1].startingA[3]=pdf_box(673.3 ,96.7  ,pos_width,pos_height)
VBset[1].startingA[4]=pdf_box(695.05,96.7  ,pos_width,pos_height)
VBset[1].startingA[5]=pdf_box(716.05,96.7  ,pos_width,pos_height)
# set 2 B
VBset[1].startingB[0]=pdf_box(452.86,96.7  ,pos_width,pos_height)
VBset[1].startingB[1]=pdf_box(474.6 ,96.7  ,pos_width,pos_height)
VBset[1].startingB[2]=pdf_box(496.36,96.7  ,pos_width,pos_height)
VBset[1].startingB[3]=pdf_box(517.35,96.7  ,pos_width,pos_height)
VBset[1].startingB[4]=pdf_box(539.1 ,96.7  ,pos_width,pos_height)
VBset[1].startingB[5]=pdf_box(560.05,96.7  ,pos_width,pos_height)
# set 3 A
VBset[2].startingA[0]=pdf_box(123   ,210.67,pos_width,pos_height)
VBset[2].startingA[1]=pdf_box(144   ,210.67,pos_width,pos_height)
VBset[2].startingA[2]=pdf_box(165.7 ,210.67,pos_width,pos_height)
VBset[2].startingA[3]=pdf_box(186.7 ,210.67,pos_width,pos_height)
VBset[2].startingA[4]=pdf_box(208.45,210.67,pos_width,pos_height)
VBset[2].startingA[5]=pdf_box(229.45,210.67,pos_width,pos_height)
# set 3 B
VBset[2].startingB[0]=pdf_box(278.9 ,210.67,pos_width,pos_height)
VBset[2].startingB[1]=pdf_box(299.9 ,210.67,pos_width,pos_height)
VBset[2].startingB[2]=pdf_box(321.65,210.67,pos_width,pos_height)
VBset[2].startingB[3]=pdf_box(342.65,210.67,pos_width,pos_height)
VBset[2].startingB[4]=pdf_box(364.4 ,210.67,pos_width,pos_height)
VBset[2].startingB[5]=pdf_box(385.4 ,210.67,pos_width,pos_height)
# set 4 A
VBset[3].startingA[0]=pdf_box(608.8 ,210.67,pos_width,pos_height)
VBset[3].startingA[1]=pdf_box(630.5 ,210.67,pos_width,pos_height)
VBset[3].startingA[2]=pdf_box(652.3 ,210.67,pos_width,pos_height)
VBset[3].startingA[3]=pdf_box(673.3 ,210.67,pos_width,pos_height)
VBset[3].startingA[4]=pdf_box(695.05,210.67,pos_width,pos_height)
VBset[3].startingA[5]=pdf_box(716.05,210.67,pos_width,pos_height)
# set 4 B
VBset[3].startingB[0]=pdf_box(452.86,210.67,pos_width,pos_height)
VBset[3].startingB[1]=pdf_box(474.6 ,210.67,pos_width,pos_height)
VBset[3].startingB[2]=pdf_box(496.36,210.67,pos_width,pos_height)
VBset[3].startingB[3]=pdf_box(517.35,210.67,pos_width,pos_height)
VBset[3].startingB[4]=pdf_box(539.1 ,210.67,pos_width,pos_height)
VBset[3].startingB[5]=pdf_box(560.05,210.67,pos_width,pos_height)
# set 5
tb.starting_left[0]=pdf_box(123.1, 325, pos_width, pos_height)
tb.starting_left[1]=pdf_box(144  , 325, pos_width, pos_height)
tb.starting_left[2]=pdf_box(166  , 325, pos_width, pos_height)
tb.starting_left[3]=pdf_box(187  , 325, pos_width, pos_height)
tb.starting_left[4]=pdf_box(209  , 325, pos_width, pos_height)
tb.starting_left[5]=pdf_box(229.5, 325, pos_width, pos_height)

tb.starting_middle[0]=pdf_box(279.2, 325, pos_width, pos_height)
tb.starting_middle[1]=pdf_box(299.9, 325, pos_width, pos_height)
tb.starting_middle[2]=pdf_box(321.7, 325, pos_width, pos_height)
tb.starting_middle[3]=pdf_box(342.7, 325, pos_width, pos_height)
tb.starting_middle[4]=pdf_box(364.6, 325, pos_width, pos_height)
tb.starting_middle[5]=pdf_box(385.3, 325, pos_width, pos_height)

tb.starting_right[0]=pdf_box(435  , 325, pos_width, pos_height)
tb.starting_right[1]=pdf_box(456  , 325, pos_width, pos_height)
tb.starting_right[2]=pdf_box(477.6, 325, pos_width, pos_height)
tb.starting_right[3]=pdf_box(498.5, 325, pos_width, pos_height)
tb.starting_right[4]=pdf_box(520.4, 325, pos_width, pos_height)
tb.starting_right[5]=pdf_box(541.5, 325, pos_width, pos_height)

# starting position coordinates
# units in pt
linewidth = 0.75
pos_width  = (20.25+21)/2
pos_height = 10.5

# rotation information
# set 1
VBset[0].rotationA = pdf_box(122, 141, 126, 34)
VBset[0].rotationB = pdf_box(278, 141, 126, 34)
# set 2
VBset[1].rotationB = pdf_box(452, 141, 126, 34)
VBset[1].rotationA = pdf_box(608, 141, 126, 34)
# set 3
VBset[2].rotationA = pdf_box(122, 255, 126, 34)
VBset[2].rotationB = pdf_box(278, 255, 126, 34)
# set 4
VBset[3].rotationB = pdf_box(452, 255, 126, 34)
VBset[3].rotationA = pdf_box(608, 255, 126, 34)
# set 5
tb.rotation_left   = pdf_box(122, 369, 126, 34)
tb.rotation_middle = pdf_box(278, 369, 126, 34)
tb.rotation_right  = pdf_box(434, 369, 126, 34)
