#!/usr/bin/env python3
"""epars_RD.py : bornes R (distance à l'origine) et D (écart entre les deux cases) du théorème « deux cases éparses ».
Pour chaque classe c1 de T1 à k0 = 100/101 : simule blanc + c1 jusqu'à T0+104 (T0 = certificat), sépare les positions
après l'impact en partie « translation » (avant s1 pour le demi-tour, tout sinon) et partie « identité » (après s1),
et le début de la 2e bande Z2 (paramètre k < 400 dans le repère de relatif.py). Norme : max(|x|,|y|).
D_i = max |c - c1| sur (translation hors bande de départ) ∪ Z2 proche (classes non demi-tour) ;
R_u = max |c| sur (identité hors bande de départ) ∪ Z2 proche (classe demi-tour)."""
import re
def rot(x,y,r):
    for _ in range(r%4): x,y=-y,x
    return x,y
bases=[]
for l in open('bases9.txt'): b,t=l.split(); bases.append((b,int(t),0,b))
for l in open('bases13.txt'): b,t,cap,orig=l.split(); bases.append((b,int(t),'HDBG'.index(cap),orig))
S1={'-119,100':69356}            # s1 du demi-tour (ant multi -19 100 79678 1 90)
def strip(x,y): return -28<=x+y<=-18      # bande de départ (diagonales x+y, y vers le bas)
# une case de la bande de départ AVANT c1 (y < y(c1)) est touchée avant c1 : on échange alors les rôles de c1 et c2
D=0; Ru=0; Rtr=0
for b,T0,r,orig in bases:
    c1=tuple(map(int,orig.split(','))); g={c1}; x=y=d=0; dx=[0,1,0,-1]; dy=[-1,0,1,0]; imp=-1
    Ptr=[];Pid=[]; s1=S1.get(orig,10**12)
    for t in range(T0+105):
        if imp<0 and (x,y)==c1: imp=t
        if imp>=0: (Ptr if t<s1 else Pid).append((x,y))
        c=(x,y) in g; d=(d+(3 if c else 1))%4; g^={(x,y)}; x+=dx[d]; y+=dy[d]
    err=open((f'rel13_{b}.err' if r else f'rel_{b}.err')).read()
    js=re.search(r'diagonales touchées \[(-?\d+), .*?\[.*?(-?\d+)\] 11',err); j0,j1=int(js.group(1)),int(js.group(2))
    # Z2 proche : cases (j-k,k) du repère de la base, k de -50 à 399, ramenées au repère d'origine (rotation inverse)
    Z2=[rot(j-k,k,4-r) for j in range(j0,j1+1) for k in range(-50,400)]
    behind=lambda c: strip(*c) and c[1]<c1[1]
    Z2=[c for c in Z2 if not behind(c)]
    tr=[c for c in Ptr if not behind(c)]; idl=[c for c in Pid if not behind(c)]
    cheb=lambda a,b_:max(abs(a[0]-b_[0]),abs(a[1]-b_[1]))
    if orig in S1:
        ru=max(max(abs(a) for a in c) for c in idl+Z2); Ru=max(Ru,ru)
        di=max(cheb(c,c1) for c in tr) if tr else 0
        print(orig,'demi-tour : R_u =',ru,' D (partie translation) =',di); D=max(D,di)
    else:
        di=max(cheb(c,c1) for c in tr+Z2); D=max(D,di); print(orig,'T0',T0,'positions',len(Ptr),'D_i',di)
    Rtr=max(Rtr,max(max(abs(a) for a in c) for c in Pid) if Pid else 0)
print('D =',D,' R_u =',Ru)
