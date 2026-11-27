"""S2 R-512 — détail d'un hexagramme cyclique : 2e moteur (hx.py, premier retour exact), et pour chaque fourmi la suite de ses directions de
vaisseau libre (on voit qui tourne où), plus les chocs A-B (2 fourmis, une de chaque horloge) : directions avant / après.
Usage : python3 s2_horloge/hexa_detail.py P0 P [rang]"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from tri import virt
from exp_osc import hd
P0, PP = int(sys.argv[1]), int(sys.argv[2]); rk = int(sys.argv[3]) if len(sys.argv) > 3 else 0
K = [h for h in json.load(open('s2_horloge/hexagramme_retenus.json')) if h['P0'] == P0 and h['P'] == PP]
h = K[rk]; print('horloge', h['horloge']); print('machine', h['sit'], 's', h['s'], 'centre', h['centre'])
a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
A0 = [tuple(q) for q in A]; G0 = dict(G); ret = None
dirs = [[] for _ in A]; last = [None] * len(A); chocs = collections.Counter(); hist = []
for t in range(3 * PP + 1):
    if t and [tuple(q) for q in A] == A0 and G == G0 and ret is None: ret = t
    if t < PP:
        V = [virt(q, G, 0)[0] for q in A]; hist.append(V)
        for i, v in enumerate(V):
            if v is not None and v[0] != last[i]: dirs[i].append((t, v[0])); last[i] = v[0]
    step(A, G)
print('hx.py : premier retour exact à t =', ret)
for i in range(len(A)): print('fourmi', i, 'A' if i < 6 else 'B', 'directions (t, r) :', dirs[i][:8], '...', len(dirs[i]), 'changements')
# chocs A-B : intervalles où une fourmi de A et une de B sont non libres et proches
a2, c2 = parts_of(h['sit']); A = [list(t) for t in a2]; G = {tuple(t): 1 for t in c2}; ev = []
for t in range(PP):
    for i in range(6):
        for j in range(6, 12):
            if hist[t][i] is None and hist[t][j] is None and hd(A[i][0] - A[j][0], A[i][1] - A[j][1]) <= 8: ev.append((t, i, j))
    step(A, G)
pairs = collections.OrderedDict()
for t, i, j in ev:
    k = (i, j)
    if k in pairs and t - pairs[k][-1][1] <= 3: pairs[k][-1][1] = t
    else: pairs.setdefault(k, []).append([t, t])
out = []
for (i, j), L in pairs.items():
    for t0, t1 in L:
        b = lambda k, tt: next((hist[x][k][0] for x in range(tt, -1, -1) if hist[x][k] is not None), None)
        f = lambda k, tt: next((hist[x][k][0] for x in range(tt, PP) if hist[x][k] is not None), None)
        out.append((t0, t1, i, j, (b(i, t0), b(j, t0)), (f(i, t1), f(j, t1))))
out.sort()
print(len(out), 'chocs A-B ; (début, fin, fourmi A, fourmi B, directions avant, directions après) :')
for o in out[:12]: print('  ', o)
print('types (avant -> après) :', collections.Counter((o[4], o[5]) for o in out).most_common(8))
