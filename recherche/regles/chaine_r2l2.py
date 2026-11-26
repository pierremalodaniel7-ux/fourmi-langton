#!/usr/bin/env python3
"""R-319 Enchaîner 2 portes à choc en R2L2 (3 entrées a, b, c ; présence = 1 ; sans aucune case fixe).
Porte 1 = choc B (origine) × A (géométrie réutilisable de R-318). Sa sortie « A déviée » (= a ET b) croise C (porte 2).
On cherche les placements de C (6 orientations × décalages) tels que la sortie de C ne dépende que de (a ET b, c) et soit propre,
pour les 8 entrées. Puis RÉUTILISATION : le circuit entier rejoué 2 fois de suite (2e jeu d'entrées 200 périodes plus tard sur les
mêmes voies), 64 suites d'entrées."""
import json, itertools, collections, subprocess
from banc import launcher, sit, outcome, rotv
from outils_r import lot, parse
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1)
EX = json.load(open('data/porte_reuse_H_R2L2_k100.json'))['exemples']
def parse_sit(s):
    r, a, c = s.split('|')
    return [tuple(map(int, t.split(','))) for t in a.split(';')], {tuple(map(int, t.split(',')[:2])): 1 for t in c.split(';') if t}
def state(s, T):
    out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input=s + '\n', capture_output=True, text=True).stdout.splitlines()
    return [tuple(map(int, t.split(','))) for t in [l for l in out if l.startswith('DUMP')][0].split('|')[1].split(';')]
def dirof(a):   # direction du vaisseau au cap a (le germe tourné de r crans a le cap 4+r)
    return rotv(R, D, (a - 4) % 6)
found = []
for gate in EX[:5]:
    ants, cells = parse_sit(gate)
    B = (ants[0], {(1, 0): 1}); A = (ants[1], {k: 1 for k in cells if k != (1, 0)})
    n = 70; Tn = n * P
    st = state(gate, Tn)                       # positions au temps n·P : sortie A' = fourmi 1
    out1 = parse(lot([gate], 1 << 16)[0])
    dA = (out1['ants'][1][1], out1['ants'][1][2])
    Y = st[1][:2]
    m = 40                                      # C arrive en Y vers le temps (n+m)·P ; Y' = Y + m·dA
    Yp = (Y[0] + m * dA[0], Y[1] + m * dA[1])
    for r in range(6):
        DC = rotv(R, D, r)
        if DC == dA or DC == (-dA[0], -dA[1]): continue
        for i in range(-3, 4):
            for j in range(-3, 4):
                st0 = (Yp[0] - (n + m) * DC[0] + i, Yp[1] - (n + m) * DC[1] + j)
                C = launcher(G, r, st0)
                L = []
                for a, b, c in itertools.product((0, 1), repeat=3):
                    al = []; ce = {}
                    for on, (x, cc) in ((b, B), (a, A), (c, C)):
                        if on: al.append(x); ce.update(cc)
                    L.append((a, b, c, sit(R, al, ce) if al else None))
                res = lot([l[3] for l in L if l[3]], 1 << 18, ncpu=2)
                k = 0; outs = {}
                for a, b, c, s in L:
                    if not s: continue
                    d = parse(res[k]); k += 1
                    if not c: continue
                    oc = outcome(R, res[k - 1], (b + a), P, DC)        # C est la dernière fourmi
                    outs[(a, b)] = (oc[0], oc[1], oc[2])
                if len(outs) < 4 or any(o[0] != 'propre' for o in outs.values()): continue
                vals = {o for (a, b), o in outs.items() if not (a and b)}
                if len(vals) == 1 and outs[(1, 1)] != next(iter(vals)):
                    found.append((gate, r, st0, outs))
    print(gate, 'placements de C trouvés (cumul) :', len(found), flush=True)
json.dump([{'porte1': f[0], 'r': f[1], 'C': list(f[2]), 'sorties_C': {str(k): v for k, v in f[3].items()}} for f in found], open('data/chaine_r2l2.json', 'w'))
