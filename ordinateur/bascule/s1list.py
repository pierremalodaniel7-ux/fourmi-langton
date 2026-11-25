#!/usr/bin/env python3
"""s1list.py d2.json → cyclesS1.json : états S1 « CHANGÉE », période ≤ 600, zone ≤ 7×7, restreints aux cases de la zone,
dédoublonnés par orbite ; chaque entrée garde la liste des S0 (orbite d'origine ic) qui y mènent."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bascule import orbite, situ_piece
from moteur2 import charge
vus={}
for l in open(sys.argv[1]):
    d=json.loads(l)
    if d['classe']!='CHANGÉE' or 'zone' not in d or d['p1']>600: continue
    z=d['zone']
    if z[2]-z[0]>6 or z[3]-z[1]>6: continue
    r,a,c=d['S1'].split('|')
    cells=[tuple(map(int,x.split(','))) for x in c.split(';') if x]
    cells=[(x,y) for x,y in cells if z[0]<=x<=z[2] and z[1]<=y<=z[3]]
    A=[tuple(map(int,x.split(','))) for x in a.split(';')]
    sit=situ_piece(A,cells); key=orbite(A,cells,d['p1'])
    if key not in vus: vus[key]={'situation':sit,'periode':d['p1'],'depuis':[]}
    vus[key]['depuis'].append(d['id']+d['sortie'])
out=sorted(vus.values(),key=lambda e:e['periode'])
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cyclesS1.json'),'w'))
print(len(out),'orbites S1 ;',sum(len(e['depuis']) for e in out),'cas')
