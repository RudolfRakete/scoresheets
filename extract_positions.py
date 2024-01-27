import os
import subprocess
import global_positions as pdfpos
from utils import *

# path='/home/ben/Nextcloud/documents/Volleyball/SVP/'
pdffile='2074.pdf'
AorB='A'

setlist=[]

for iset in range(4):
    current_set=set(num=iset+1)
    print(current_set)

    # read final results
    scoreA=int(pdf2str(pdffile, pdfpos.finalA[iset]))
    scoreB=int(pdf2str(pdffile, pdfpos.finalB[iset]))
    if AorB=='A':
        current_set.final_score = [scoreA,scoreB]
    elif AorB=='B':
        current_set.final_score = [scoreB,scoreA]

    print(current_set.final_score)

    # read starting player information
    pos=pdfpos.get_starting_coords(AorB, iset)
    for ipos in range(6):
        current_set.players[ipos] = int(pdf2str(pdffile, pos[ipos]))

    print(current_set.players)
    setlist.append(current_set)

