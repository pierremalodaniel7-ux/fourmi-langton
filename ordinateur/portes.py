# portes.py — fabrique de situations à base de germes 104 tournés, et appel du banc C gate.
import subprocess
GX=[-2,-1,0,1,-2,1,-2,0,-1,0,0]; GY=[-2,-2,-1,0,1,1,2,2,3,3,4]
DIRS={0:(-2,2),1:(-2,-2),2:(2,-2),3:(2,2)}   # r -> déplacement par période ; r=0 ↙, 1 ↖, 2 ↗, 3 ↘
def rot(r,x,y):
    for _ in range(r): x,y=-y,x
    return x,y
def germe(px,py,r):
    cells=set()
    for x,y in zip(GX,GY):
        a,b=rot(r,x,y); cells^={(px+a,py+b)}
    return (px,py,'HDBG'[(1+r)&3]),cells
def situ(germes,extra=()):
    ants=[];cells=set()
    for g in germes:
        a,c=g; ants.append(a); cells^=c
    for c in extra: cells^={c}
    return ';'.join(f'{x},{y},{d}' for x,y,d in ants)+'|'+';'.join(f'{x},{y}' for x,y in sorted(cells))
def run(situs,T):
    inp=''.join(f'{s} {T}\n' for s in situs)
    p=subprocess.run(['./gate'],input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.strip().split('\n'):
        if l.startswith('BORD'): out.append('BORD'); continue
        out.append([None if t=='X' else tuple(map(int,t.split(','))) for t in l.split()])
    return out
