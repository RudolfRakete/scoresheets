from utils import *
# final results coordinates
finalA=[]
finalB=[]
# set 1
finalA.append(pdf_box(251,97,25,45))
finalB.append(pdf_box(407,97,25,45))
# set 2
finalA.append(pdf_box(738,97,25,45))
finalB.append(pdf_box(582,97,25,45))
# set 3
finalA.append(pdf_box(251,211,25,45))
finalB.append(pdf_box(407,211,25,45))
# set 4
finalA.append(pdf_box(738,211,25,45))
finalB.append(pdf_box(582,211,25,45))
# set 5
# finalA.append(pdf_box(738,97,25,45))
# finalB.append(pdf_box(582,97,25,45))


# starting position coordinates
# units in pt
linewidth = 1
pos_width  = 20
pos_height = 10
startA=[]
startB=[]
# set 1
startA.append(coord(123,97))
startB.append(coord(279,97))
# set 2
startA.append(coord(609,97))
startB.append(coord(453,97))
# set 3
startA.append(coord(123,211))
startB.append(coord(279,211))
# set 4
startA.append(coord(609,211))
startB.append(coord(453,211))
# set 5
# startA.append(coord(609,211))
# startB.append(coord(453,211))


def get_starting_coords(AorB, iset):
    if AorB=='A':
        start_coord=startA[iset]
    elif AorB=='B':
        start_coord=startB[iset]

    pos=[]
    for i in range(6):
        pos.append(pdf_box(start_coord.x+i*(pos_width+linewidth),start_coord.y,pos_width,pos_height))
    
    return pos

