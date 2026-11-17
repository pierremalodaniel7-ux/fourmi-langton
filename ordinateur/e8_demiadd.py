# E8 : demi-additionneur à UNE puissance : voie L-4 = XOR (S), voie L-8 = ET (C, case (133,267)).
# Le XOR demande 2 cases (les chemins (0,1) et (1,0) diffèrent en phase). Sorties lues : S tourne ↙, C tourne ↙ (voies différentes).
import portes as Pt, sim, json, itertools
c,s,dB=-121,-391,64; T=90000; CC=(133,267)
E=[(0,0),(0,1),(1,0),(1,1)]
def g1(a,b):
    g=[]
    if a: g.append(Pt.germe(0,0,0))
    if b: g.append(Pt.germe(dB,dB,0))
    g.append(Pt.germe((c+s)//2,(s-c)//2,3)); return g
P={}
for e in E:
    _,_,_,pos=sim.run('RL|'+Pt.situ(g1(*e)),60000,trace=True)
    P[e]={p[-1] for p in pos if 380<=p[-1][0]+p[-1][1]<=420}
A1=sorted(P[(0,1)]|P[(1,0)]); A2=[None]
print(len(A1),len(A2))
pairs=[(c1,None) for c1 in A1]
r=Pt.run([Pt.situ(g1(*e),extra=[CC,c1]) for c1,c2 in pairs for e in E],T)
good=[]
for i,(c1,c2) in enumerate(pairs):
    o=r[4*i:4*i+4]
    if any(x=='BORD' or x[-1] is None for x in o): continue
    lanes=[(x[-1][0],x[-1][1],x[-1][2]) for x in o]
    sw=[l[:2]==(-2,2) for l in lanes]
    if sw==[False,True,True,True] and lanes[3][2]!=lanes[1][2] and lanes[3][2]!=lanes[2][2]:
        good.append(((c1,c2),lanes))
print(len(good),'demi-additionneurs ; ex :',good[:3])
json.dump([[list(g[0][0]),g[1]] for g in good],open("e8.json","w"))
