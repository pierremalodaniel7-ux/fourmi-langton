"""R-616 Diagnostic : couples (sortie RÉELLE, vaisseau entrant) de directions opposées à < 7 voies, avec leurs noms."""
import sys, json
from htree import build, h1_tree2
from nor import Layout
from s3lib import *
from reuse import lane_of
p = json.load(open(sys.argv[1])); L = Layout(build(h1_tree2()), Dmap=p['D'], Gmap=p['G'])
envs = L.cases(); T = L.tmax + 1200; R = run_c([L.sit(e) for e in envs], T)
outs = {}
for e, (a, c) in zip(envs, R):
    for w in decode(a, c, T): outs.setdefault(w, e)
name = {}
for nm, k, w in L.ships: name[w] = nm + ' (tout droit)'
for g in L.gates: name.setdefault(g[3], f'{g[5]} dévié à {g[0]}'); name.setdefault(g[4], f'{g[0]} dévié par {g[5]}')
seen = set()
for o in outs:
    for nm, k, i in L.ships:
        if (o[0] - i[0]) % 6 == 3:
            lo = [lane_of(antpos(o, t), o[0]) for t in range(8)]; li = [lane_of(antpos(i, t), o[0]) for t in range(8)]
            m = min(abs(x - y) for x in lo for y in li)
            if m < 7 and (name.get(o), nm) not in seen:
                seen.add((name.get(o), nm)); print(m, 'sortie', name.get(o, o), '| entrant', nm, '| ex. cas', outs[o])
