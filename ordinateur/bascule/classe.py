#!/usr/bin/env python3
"""classe.py F.out : répartition des issues. RETOUR exact = fourmi 0 en R(départ) ; hors=0 : rien ne reste hors boîte."""
import sys, collections, re
C=collections.Counter(); ex=collections.defaultdict(list)
for l in open(sys.argv[1]):
    f=l.rstrip('\n').split('|'); m=re.search(r'dans=(\d+) hors=(\d+)',l); dans,hors=int(m.group(1)),int(m.group(2))
    iss=f[4]
    if iss=='RETOUR': k='RETOUR exact, pièce identique' if dans==0 and hors==0 else ('RETOUR exact, pièce CHANGÉE' if hors==0 else 'RETOUR, reste hors boîte')
    else:
        d=re.search(r'\|(\d+),(-?\d+),(-?\d+),(\d+) boite',l)
        k=f'{iss} P{d.group(1)} ({d.group(2)},{d.group(3)})' if d else iss
    C[k]+=1; ex[k].append(l)
for k,v in C.most_common(): print(f'{v:7d}  {k}')
if len(sys.argv)>2:
    for k in ex:
        if 'RETOUR' in k:
            for l in ex[k][:int(sys.argv[2])]: print(k,'::',l[:300])
