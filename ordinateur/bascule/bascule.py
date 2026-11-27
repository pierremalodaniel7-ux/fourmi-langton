#!/usr/bin/env python3
"""bascule.py : pour une situation « germe + pièce » (pièce près de l'origine), après un tir :
 - état résiduel S1 = cases et fourmis dans la boîte BP (la fourmi gomme et le germe exclus) ;
 - S1 seul est-il un cycle (src/fourmi, CYCLE exact) ? même orbite que S0 ?
 - 2e tir : germe neuf, même voie, sur S1 (décalages de temps s = 0..k−1 : S1 avancé de s pas) → fenêtre effacée ?
Fonctions utilisées par recherche.py ; tout calcul de vérité passe par src/fourmi."""
import subprocess, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
E=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../src/fourmi')
BP=(-15,-15,22,22); FEN='35,-75,75,-35'; TMP=f'/tmp/claude-0/bp{os.getpid()}.dump'
G=[(0,1),(1,2),(2,3),(2,2),(2,1),(2,0),(3,0),(3,-1),(2,-2),(1,-2),(-2,-1)]
def dans(x,y,b=BP): return b[0]<=x<=b[2] and b[1]<=y<=b[3]
def tir(sit,T):
    """lance src/fourmi -retour, renvoie (ligne de sortie, fourmis finales, cases finales)"""
    if os.path.exists(TMP): os.remove(TMP)
    out=subprocess.run([E,'-T',str(T),'-retour','-boite',FEN,'-dump',TMP,sit],capture_output=True,text=True).stdout.strip()
    d=open(TMP).read().strip().split('|')
    ants=[tuple(map(int,a.split(','))) for a in d[-2].split(';') if a]
    cells={tuple(map(int,c.split(',')[:2])) for c in d[-1].split(';') if c}
    return out,ants,cells
def fenetre_propre(out): return ' dans=0 ' in ' '+out.split('|',3)[3]
def residu(ants,cells,eraser=None):
    """S1 : (fourmis dans BP sauf la gomme, cases dans BP) ; parties = fourmis hors BP (gomme comprise)"""
    A=[a for i,a in enumerate(ants) if dans(a[0],a[1])]; C=sorted(c for c in cells if dans(*c))
    return A,C,len(ants)-len(A)
def situ_piece(A,C): return 'RL|'+';'.join(f'{x},{y},{d}' for x,y,d in A)+'|'+';'.join(f'{x},{y}' for x,y in C)
def cycle(A,C,T=400000):
    if not A: return 'vide'
    o=subprocess.run([E,'-T',str(T),situ_piece(A,C)],capture_output=True,text=True).stdout.strip().split('|')
    return f'CYCLE {o[5]}' if o[3]=='CYCLE' else o[3]+' '+o[4]+' '+o[6][:60]
def orbite(A,C,p,pos=False):
    """forme canonique de l'orbite (toutes phases ; cases restreintes à celles que les fourmis visitent pendant la période ;
    à translation près, ou en place si pos=True) pour comparer S0 et S1"""
    turn,ants,noir=charge(situ_piece(A,C)); vis=set(); hist=[]
    for t in range(p):
        for a in ants: vis.add((a[0],a[1]))
        hist.append(([tuple(a) for a in ants],set(noir))); pas(turn,ants,noir,range(len(ants)))
    orb=[]
    for an,no in hist:
        no={c for c in no if c in vis}
        mx,my=(0,0) if pos else (min(x for x,y in vis),min(y for x,y in vis))
        orb.append((tuple(sorted((a[0]-mx,a[1]-my,a[2]) for a in an)),tuple(sorted((x-mx,y-my) for x,y in no))))
    return min(orb)
def avance(A,C,s):
    turn,ants,noir=charge(situ_piece(A,C)); 
    for _ in range(s): pas(turn,ants,noir,range(len(ants)))
    return [tuple(a) for a in ants],sorted(noir)
def germe_sit(gx,gy,A,C):
    cases=[(x+gx,y+gy) for x,y in G]+list(C)
    return f'RL|{gx},{gy},B;'+';'.join(f'{x},{y},{d}' for x,y,d in A)+'|'+';'.join(f'{x},{y}' for x,y in cases)
