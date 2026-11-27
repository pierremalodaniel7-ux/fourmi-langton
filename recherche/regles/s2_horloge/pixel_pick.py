import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from pixel_check import timeline
W = json.load(open(sys.argv[1])); Bs = json.load(open('data/bascules_exactes.json'))
rows = []
for i, w in enumerate(W):
    st, ch = timeline(w, Bs)
    c = collections.Counter(st)
    nsw = sum(1 for t in range(1, len(st)) if st[t] in ('ON', 'OFF') and st[t] != next((st[u] for u in range(t - 1, -1, -1) if st[u] != '?'), st[t]))
    rows.append((abs(c['ON'] - c['OFF']), c['ON'], c['OFF'], c['?'], nsw, i, w['bascule'], w['rot'], tuple(w['horloge']), w['T']))
rows.sort()
for r in rows[:12]: print(r)
print('basculements par période :', collections.Counter(r[4] for r in rows))
json.dump([W[r[5]] | {'ON': r[1], 'OFF': r[2], 'trans': r[3], 'nsw': r[4]} for r in rows], open(sys.argv[1].replace('.json', '_tri.json'), 'w'))
