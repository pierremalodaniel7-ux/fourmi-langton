#!/usr/bin/env python3
"""run_b.py pieces.json VAR [P] : lecture_b.py sur chaque pièce × 4 rotations, P processus ; reprise (saute les .log finis)."""
import sys, json, subprocess, os
from concurrent.futures import ThreadPoolExecutor
L=json.load(open(sys.argv[1])); V=sys.argv[2]; P=int(sys.argv[3]) if len(sys.argv)>3 else 2
O='../../data/lecture'; os.makedirs(O,exist_ok=True)
jobs=[]
for e in L:
    for r in range(4):
        log=f"{O}/{e['nom']}_{V}_r{r}.log"
        if os.path.exists(log) and 'tirs' in open(log).read(): continue
        jobs.append((e,r,log))
def run(j):
    e,r,log=j
    with open(log+'.tmp','w') as f: subprocess.run(['python3','lecture_b.py',f"{e['nom']}_{V}",e['S0'],str(e['p0']),e[V],str(e['p1']),str(r)],stdout=f)
    os.replace(log+'.tmp',log)
with ThreadPoolExecutor(P) as ex: list(ex.map(run,jobs))
