import os

class coord:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def __str__(self):
        return f"({self.x},{self.y})"

class pdf_box:
    def __init__(self, x, y, W, H):
        self.x=x
        self.y=y
        self.W=W
        self.H=H

    def __str__(self):
        return f"pdf box: ({self.x} {self.y} {self.W} {self.H})"


class set:
    def __init__(self, num=0, players=[None]*6, final_score=[None]*2):
        self.num=num
        self.players=players
        self.final_score=final_score

    def __str__(self):
        return f"Set number {self.num}."


def pdf2str(pdffile,pdf_box):
    options = '-x {x:d} -y {y:d} -W {W:d} -H {H:d}'.format(x=pdf_box.x, y=pdf_box.y, W=pdf_box.W, H=pdf_box.H)
    ex_call=' '.join(['pdftotext', options, pdffile, '-'])
    ret=os.popen(ex_call).read()
    ret = ret.strip()
    return ret
