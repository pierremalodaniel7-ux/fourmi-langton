"""S2 R-512 — ce que voit UNE porte (un point de croisement de l'hexagramme) au cours d'une période : suite des chocs A-B
(tourne / passe), et passages d'un vaisseau SEUL (sans partenaire) au même endroit. Usage : python3 s2_horloge/hexa_portes.py P [rang]"""
import sys, json, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from tri import virt
from exp_osc import hd
PP = int(sys.argv[1]); rk = int(sys.argv[2]) if len(sys.argv) > 2 else 0
h = [x for x in json.load(open('s2_horloge/hexagramme_propres.json')) if x['P'] == PP][rk]
a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
hist = []; pos = []
for t in range(PP):
    hist.append([virt(q, G, 0)[0] for q in A]); pos.append([tuple(q[:2]) for q in A]); step(A, G)
ev = []
for t in range(PP):
    for i in range(6):
        for j in range(6, 12):
            if hist[t][i] is None and hist[t][j] is None and hd(pos[t][i][0] - pos[t][j][0], pos[t][i][1] - pos[t][j][1]) <= 6:
                ev.append((t, i, j, ((pos[t][i][0] + pos[t][j][0]) // 2, (pos[t][i][1] + pos[t][j][1]) // 2)))
# regrouper en chocs (même paire, temps proches)
ch = []
for t, i, j, p in ev:
    if ch and ch[-1]['i'] == i and ch[-1]['j'] == j and t - ch[-1]['t1'] <= 4: ch[-1]['t1'] = t
    else:
        for x in ch[::-1]:
            if x['i'] == i and x['j'] == j and t - x['t1'] <= 4: x['t1'] = t; break
        else: ch.append({'t0': t, 't1': t, 'i': i, 'j': j, 'p': p})
def before(k, tt): return next((hist[x][k][0] for x in range(tt, -1, -1) if hist[x][k] is not None), None)
def after(k, tt): return next((hist[x % PP][k][0] for x in range(tt, tt + 200) if hist[x % PP][k] is not None), None)
# zones = 6 points de croisement : regrouper les positions
zones = []
for x in ch:
    for z in zones:
        if hd(z[0] - x['p'][0], z[1] - x['p'][1]) <= 12: x['z'] = zones.index(z); break
    else: zones.append(x['p']); x['z'] = len(zones) - 1
    bi, bj, ai, aj = before(x['i'], x['t0']), before(x['j'], x['t0']), after(x['i'], x['t1']), after(x['j'], x['t1'])
    x['type'] = ('tourne' if (bi, bj) != (ai, aj) else 'passe') + ' %s,%s -> %s,%s' % (bi, bj, ai, aj)
print(len(ch), 'chocs A-B,', len(zones), 'zones')
z0 = ch[0]['z']
print('zone', z0, 'centre', zones[z0], ': suite des chocs dans le temps')
for x in ch:
    if x['z'] == z0: print('   t', x['t0'], '-', x['t1'], 'fourmis', x['i'], x['j'], x['type'])
print('par zone :', collections.Counter((x['z'], x['type'].split()[0]) for x in ch))
# passages de vaisseaux dans chaque zone : avec choc A-B (porte « 2 entrées ») ou seuls (porte « 1 entrée »)
pas = collections.Counter(); seq = collections.defaultdict(list)
for zi, zc in enumerate(zones):
    inside = {}
    for t in range(PP):
        for k in range(12):
            d = hd(pos[t][k][0] - zc[0], pos[t][k][1] - zc[1])
            if d <= 4:
                if k in inside and t - inside[k][-1][1] <= 2: inside[k][-1][1] = t
                else: inside.setdefault(k, []).append([t, t])
    for k, L in inside.items():
        for t0, t1 in L:
            avec = any(x['z'] == zi and k in (x['i'], x['j']) and x['t0'] <= t1 + 8 and x['t1'] >= t0 - 8 and x['type'].startswith('tourne') for x in ch)
            bk, ak = before(k, t0), after(k, t1)
            lab = ('choc' if avec else 'seul') + (' tourne' if bk != ak else ' droit')
            pas[(zi, lab)] += 1; seq[zi].append((t0, k, lab, bk, ak))
print('passages par zone :', sorted(pas.items()))
for zi in (0, 3):
    print('zone', zi, sorted(seq[zi])[:24])
# entrées des portes : droites (direction, voie) des 2 vaisseaux d'un choc qui tourne ; puis tous les passages sur ces droites
from hx import ship_dir
def lane(v):
    r, p, tau = v; d = ship_dir(r); return (r, p[0] * d[1] - p[1] * d[0])
def last_free(k, tt):
    return next((hist[x][k] for x in range(tt, -1, -1) if hist[x][k] is not None), None)
portes = collections.defaultdict(set)
for x in ch:
    if not x['type'].startswith('tourne'): continue
    vi, vj = last_free(x['i'], x['t0']), last_free(x['j'], x['t0'])
    if vi and vj: portes[x['z']].add((lane(vi), lane(vj)))
print('entrées des portes (zone : {(droite 1, droite 2)}) :', dict(portes))
# pour chaque zone et chaque droite d'entrée : passages (fourmi libre à ≤ 8 du centre sur cette droite, puis sort tournée ou droite)
for zi, P_ in sorted(portes.items()):
    L = {l for pr in P_ for l in pr}; res = collections.Counter()
    for l in L:
        for k in range(12):
            t = 0
            while t < PP:
                v = hist[t][k]
                if v is not None and lane(v) == l and hd(pos[t][k][0] - zones[zi][0], pos[t][k][1] - zones[zi][1]) <= 8:
                    t1 = t
                    while t1 < PP and (hist[t1][k] is None or lane(hist[t1][k]) == l) and hd(pos[t1][k][0] - zones[zi][0], pos[t1][k][1] - zones[zi][1]) <= 12: t1 += 1
                    out = after(k, t1); res[(l, 'tourne' if out is not None and out != l[0] else 'droit')] += 1; t = t1 + 30
                else: t += 1
    print('zone', zi, dict(res))
