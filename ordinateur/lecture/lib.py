"""lib.py : outils communs de la nuit 26/11 (lecture de la bascule T). Calcul de vérité : src/fourmi ; contrôle : moteur2.py."""
import json, os, subprocess, sys
D=os.path.dirname(os.path.abspath(__file__)); B=os.path.join(D,'../bascule')
sys.path.insert(0,B)
from moteur2 import charge, pas
E=os.path.join(D,'../../src/fourmi'); TMPD=os.environ.get('TMPD','/tmp/claude-0'); os.makedirs(TMPD,exist_ok=True)
G=[(0,1),(1,2),(2,3),(2,2),(2,1),(2,0),(3,0),(3,-1),(2,-2),(1,-2),(-2,-1)]   # germe R-20 (fourmi en (0,0) cap B)
C2=json.load(open(os.path.join(B,'cycles2.json')))
S1C=json.load(open(os.path.join(B,os.environ.get('S1F','cyclesS1.json'))))
def situ(A,C,r='RL'): return r+'|'+';'.join(f'{x},{y},{d}' for x,y,d in A)+'|'+';'.join(f'{x},{y}' for x,y in C)
def parse(sit):
    r,a,c=(sit.split('|')+['',''])[:3]
    A=[tuple(int(v) if v.lstrip('-').isdigit() else 'HDBG'.index(v) for v in t.split(',')) for t in a.split(';') if t]
    C=[tuple(map(int,t.split(',')[:2])) for t in c.split(';') if t and (len(t.split(','))<3 or int(t.split(',')[2])%2)]
    return r,A,C
def piece0(ic,s=0):
    c=C2[ic]; turn,ants,noir=charge(c['situation']); p=c['periode']; vis=set(); et=None
    for t in range(p):
        if t==s: et=([tuple(a) for a in ants],sorted(noir))
        for a in ants: vis.add((a[0],a[1]))
        pas(turn,ants,noir,range(len(ants)))
    mx=min(x for x,y in vis); my=min(y for x,y in vis)
    return [(x-mx,y-my,d) for x,y,d in et[0]],[(x-mx,y-my) for x,y in et[1]],p
def orbite(sit,p):
    """ensemble des états (fourmis, cases noires visitées) de l'orbite, en place ; et cases visitées"""
    turn,an,no=charge(sit); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],set(no))); pas(turn,an,no,range(len(an)))
    return {(tuple(a),frozenset(c for c in no if c in vis)) for a,no in L}, vis
class Bascule:
    """bascule : S0 = cycles2[ic] phase s (repère du tir 1), S1 = cyclesS1_c2[i1] (même repère)"""
    def __init__(s,h,S1L=None):
        ic,ph=h['hit']['S0'][:2]; s.ic=ic; A0,C0,p0=piece0(ic,ph); s.A0,s.C0,s.p0=A0,C0,p0
        s.O0,s.V0=orbite(situ(A0,C0),p0); e=(S1L or S1C)[h['hit']['S1']]; s.O1,s.V1=orbite(e['situation'],e['periode']); s.npc=len(A0)
        s.situation=h['situation']; s.T=h['T']
    def etat(s,an,ce):
        P=tuple(tuple(a) for a in an[-s.npc:])
        if (P,frozenset(x for x in ce if x in s.V0)) in s.O0: return 'S0'
        if (P,frozenset(x for x in ce if x in s.V1)) in s.O1: return 'S1'
        return '…'
def lot(sits,T,tag='lot',opts=''):
    """src/fourmi -lot -dump : renvoie [(ligne de sortie, fourmis finales, cases noires finales)]"""
    f=os.path.join(TMPD,f'{tag}{os.getpid()}')
    open(f+'.txt','w').write('\n'.join(sits)+'\n')
    if os.path.exists(f+'.dump'): os.remove(f+'.dump')
    out=subprocess.run(f"{E} -T {T} {opts} -dump {f}.dump -lot < {f}.txt",shell=True,capture_output=True,text=True).stdout.splitlines()
    R=[]
    for o,l in zip(out,open(f+'.dump')):
        d=l.strip().split('|'); an=[tuple(map(int,x.split(','))) for x in d[-2].split(';')]
        ce={tuple(map(int,x.split(',')[:2])) for x in d[-1].split(';') if x and int(x.split(',')[2])%2}
        R.append((o,an,ce))
    return R
def destins(o):
    """par fourmi : 'dx,dy' de l'autoroute confirmée ou '-' (lu dans la sortie de src/fourmi)"""
    f=o.split('|'); det=f[-1].split(' boite')[0].split()
    return [('-' if t=='-' else ','.join(t.split(',')[1:3])) for t in det]
def voie(x,y,d):
    """voie d'une autoroute : x−y pour (±2,±2) de même signe, x+y sinon"""
    dx,dy=map(int,d.split(',')); return x-y if dx*dy>0 else x+y
def py_final(sit,T):
    turn,ants,noir=charge(sit)
    for _ in range(T): pas(turn,ants,noir,range(len(ants)))
    return [tuple(a) for a in ants],noir
