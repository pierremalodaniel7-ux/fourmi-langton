#!/usr/bin/env python3
"""palindrome.py honnetes.json i : bascule honnête (1 paire ON/OFF). Au pas t* du RETOUR exact : où sont les cases qui diffèrent
du départ ? la pièce est-elle à la phase de la pièce seule au pas t*, ou à une autre phase (décalage) ? src/fourmi + moteur2."""
import sys, json
from lib import *
H=json.load(open(sys.argv[1])); hb=H[int(sys.argv[2])]
if 'S1F' in os.environ: pass
b=Bascule(hb); sit=hb['situation']; r,A,C=parse(sit)
(o,an,ce),=lot([sit],hb['T'],'pa','-retour'); f=o.split('|'); ts=int(f[5]); print('RETOUR' if f[3]=='RETOUR' else f[3],'t* =',ts,f[6][:40])
ini=set(C); d=ce^ini; g1,g2=A[1][:2],A[0][:2]
near=lambda p,q,k=12:abs(p[0]-q[0])<k and abs(p[1]-q[1])<k
print('cases ≠ départ :',len(d),'; près source 1 :',sum(near(c,g1) for c in d),'; près source 2 :',sum(near(c,g2) for c in d),'; près pièce :',sum(near(c,(2,2)) for c in d))
# phase de la pièce
turn,a2,n2=charge(situ(A[2:],C[11:-11])); hist=[]
for t in range(ts+1):
    hist.append(tuple(tuple(x) for x in a2)); pas(turn,a2,n2,range(len(a2)))
P=tuple(tuple(x) for x in an[2:]); p=b.p0
k=[t for t in range(p) if hist[t]==P]
print('pièce au pas t* = pièce seule au pas', k, '(mod période', p, ') ; t* mod p =', ts%p, '→ décalage de phase', [(ts-x)%p for x in k])
a3,n3=py_final(sit,ts); print('moteur2 :','identique' if a3==an and n3==ce else 'DIFFÉRENT')
