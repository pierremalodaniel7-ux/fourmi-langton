# R-71 application à R-24 (2 cases noires sur l'autoroute) : échantillon de paires parmi les cases neuves des périodes 10 à 14
import sys, random; sys.argv=[sys.argv[0]]
from lemme_r16 import run
W9,_=run([],104*9,True); W14,_=run([],104*14,True); C=sorted(W14-W9)
random.seed(24); P=random.sample([(a,b) for i,a in enumerate(C) for b in C[i+1:]],60)
res=[run([a,b])[0] for a,b in P]
print('R-24 échantillon :',sum(t is not None for t in res),'/',len(P),'VÉRIFIÉS pour toujours ; max',max(t for t in res if t),'; cases candidates',len(C))
