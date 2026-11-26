#!/usr/bin/env python3
"""2e moteur pour R-311 : additionneur 4 bits RL, 420 000 tours, puis gomme collective (fourmis retournées, ordre inversé), 420 000 tours."""
import json
SQ = [(0,-1),(1,0),(0,1),(-1,0)]; K = [1, 3]
g0 = json.load(open('../ordinateur/germe_ordinateur.json'))[0]
C = {'H':0,'D':1,'B':2,'G':3}
ants = [[int(s.split(',')[0]), int(s.split(',')[1]), C[s.split(',')[2].strip()]] for s in g0['fourmis'].split(';') if s.count(',') >= 2]
g = {(int(s.split(',')[0]), int(s.split(',')[1])): 1 for s in g0['points'].split(';') if s.strip()}
ini = dict(g); T = 420000
def run(ants, T):
    for _ in range(T):
        for a in ants:
            k = g.get((a[0], a[1]), 0); a[2] = (a[2] + K[k]) % 4; g[(a[0], a[1])] = 1 - k; a[0] += SQ[a[2]][0]; a[1] += SQ[a[2]][1]
run(ants, T)
changed = sum(1 for p, v in g.items() if v != ini.get(p, 0))
rev = [[a[0] - SQ[a[2]][0], a[1] - SQ[a[2]][1], (a[2] + 2) % 4] for a in ants][::-1]
run(rev, T)
diff = sum(1 for p in set(g) | set(ini) if g.get(p, 0) != ini.get(p, 0))
print(f"Python : {changed} cases changées après {T} tours ; après la gomme collective : {diff} case(s) différente(s) de l'état initial")
