#!/usr/bin/env python3
"""analyse.py "situation" T : rejoue avec src/fourmi -retour -dump, puis compte les cases ≠ départ par tranche le long de
l'autoroute (a = −x + y ; germe vers a ≈ −200, pièce en a ≈ 0) et liste les fourmis finales."""
import sys, subprocess, os, collections
sit=sys.argv[1]; T=sys.argv[2]; f='/tmp/claude-0/an.dump'
if os.path.exists(f): os.remove(f)
E=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../src/fourmi')
out=subprocess.run([E,'-T',T,'-retour','-boite','-8,-8,14,14','-dump',f,sit],capture_output=True,text=True).stdout
print(out.split('|',3)[3][:200])
d=open(f).read().strip().split('|')
ini={tuple(map(int,c.split(',')[:2])) for c in sit.split('|')[2].split(';') if c}
fin={tuple(map(int,c.split(',')[:2])) for c in d[-1].split(';') if c}
diff=ini^fin; C=collections.Counter()
for x,y in diff: C[(-x+y)//20*20]+=1
print('cases ≠ départ par tranche de a :',sorted(C.items()))
print('fourmis :',d[-2])
