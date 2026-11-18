# R-71 : toutes les paires parmi les 110 cases neuves des périodes 10–14 (tranche k sur K)
import sys, json
from lemme_r16 import run
k,K=int(sys.argv[1]),int(sys.argv[2])
W9,_=run([],104*9,True); W14,_=run([],104*14,True); C=sorted(W14-W9)
P=[(a,b) for i,a in enumerate(C) for b in C[i+1:]][k::K]
res=[run([a,b],120000)[0] for a,b in P]
print(k,'paires',len(P),'vérifiées',sum(t is not None for t in res),'max',max(t for t in res if t),'non', [P[i] for i,t in enumerate(res) if t is None][:5],flush=True)
