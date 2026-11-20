#!/usr/bin/env python3
"""Section 1 : vérifications exactes (moteur Python, entiers) des réductions.
1) échange L<->R = miroir x -> -x (5 règles, 200 000 pas, trajectoire entière comparée)
2) w^k a la même trajectoire que w (5 règles, 200 000 pas)
3) L^q : cycle exact de période 4q (q=2..16)"""
DX=[0,1,0,-1]; DY=[-1,0,1,0]
def traj(w,T):
    q=len(w); g={}; x=y=d=0; out=[]
    for t in range(T):
        c=g.get((x,y),0); d=(d+(1 if w[c]=='R' else 3))%4; g[(x,y)]=(c+1)%q
        x+=DX[d]; y+=DY[d]; out.append((x,y,d))
    return out,g
sw=lambda w:w.translate(str.maketrans("LR","RL"))
T=200000
for w in ["RL","LLR","LRRL","LLRRRL","LRRRRRLLR"]:
    a,_=traj(w,T); b,_=traj(sw(w),T)
    ok=all(bx==-ax and by==ay and bd==(4-ad)%4 for (ax,ay,ad),(bx,by,bd) in zip(a,b))
    print("miroir",w,sw(w),"OK" if ok else "ECHEC")
for w,k in [("RL",3),("LLR",2),("LRRL",2),("LLRRRL",2),("LRL",4)]:
    a,_=traj(w,T); b,_=traj(w*k,T); print("puissance",w,k,"OK" if a==b else "ECHEC")
for q in range(2,17):
    w="L"*q; x=y=d=0; g={}; t=0
    while True:
        c=g.get((x,y),0); d=(d+3)%4; g[(x,y)]=(c+1)%q; x+=DX[d]; y+=DY[d]; t+=1
        if x==0 and y==0 and d==0 and all(v==0 for v in g.values()): break
    assert t==4*q, (q,t)
print("L^q : cycle exact de période 4q pour q=2..16 OK")
