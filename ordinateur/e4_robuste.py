# E4 : robustesse des portes NOR / ET / NON / COPIE : décaler A, B, P de ±1 case (4 directions) et de ±1 phase.
import portes as Pt, sys
c,s,dB=-121,-391,64
GATES={'NOR':((141,260),lambda a,b:not(a or b)),'ET':((133,267),lambda a,b:a and b)}
E=[(0,0),(0,1),(1,0),(1,1)]
def germes(a,b,oA=(0,0),oB=(0,0),oP=(0,0)):
    g=[]
    if a: g.append(Pt.germe(0+oA[0],0+oA[1],0))
    if b: g.append(Pt.germe(dB+oB[0],dB+oB[1],0))
    g.append(Pt.germe((c+s)//2+oP[0],(s-c)//2+oP[1],3)); return g
def table(cell,oA=(0,0),oB=(0,0),oP=(0,0)):
    r=Pt.run([Pt.situ(germes(a,b,oA,oB,oP),extra=[cell]) for a,b in E],90000)
    out=[]
    for o in r:
        if o=='BORD' or any(x is None for x in o): out.append('?')
        else: out.append(1 if (o[-1][0],o[-1][1])==(-2,2) else 0)
    return out
SH=[(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]  # (±1,±1) le long de l'axe = ±1 « phase » (demi-période)
for nom,(cell,f) in GATES.items():
    want=[int(bool(f(a,b))) for a,b in E]; print(nom,'attendu',want,'nominal',table(cell))
    for who in ('A','B','P'):
        ok=0; bad=[]
        for sh in SH[1:]:
            kw={'o'+who:sh}; t=table(cell,**kw)
            if t==want: ok+=1
            else: bad.append((sh,t))
        print(f'  décalage de {who} : {ok}/8 justes ; faux : {bad}')
