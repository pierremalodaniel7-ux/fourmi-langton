#!/usr/bin/env python3
"""lignes.py chaine.json : pour chaque préfixe pair (2, 4, … impulsions), cases noires restantes sur la ligne a
(bande |x+y − voie| ≤ 12, entre la pièce (x > 15) et la source la plus lointaine (moins 15)), au pas T + 20 000. src/fourmi."""
import sys, json
from lib import *
H=json.load(open(sys.argv[1]))
for h in H:
    m=h['impulsions']; r,A,C=parse(h['situation']); src=A[0]; lane=A[m-1][0]+A[m-1][1]
    (o,an,ce),=lot([h['situation']],h['T']+20000,'lg')
    n=sum(1 for x,y in ce if abs(x+y-lane)<=12 and 15<x<src[0]-15)
    print(f'{m} impulsions : {n} cases noires sur la ligne (jusqu\'à x = {src[0]-15})')
