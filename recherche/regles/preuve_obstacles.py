#!/usr/bin/env python3
"""R-330 Calcul EXACT : aucun ensemble de cases fixes (fini ou infini, n'importe quelle couleur sur les cases non encore visitées)
ne peut faire reculer un vaisseau R2L2 de plus de B crans le long de sa direction (donc ni le tourner, ni le renvoyer).

Méthode (preuve par ensemble fermé d'états) : le vaisseau a roulé 10 périodes sur du blanc (cases visitées connues) ; devant lui
TOUTE case jamais visitée est INCONNUE : quand la fourmi y arrive on essaie les 2 couleurs (branchement). On suit a = x − y
(le vaisseau avance de +2 par période dans la direction (1,−1) ; les 2 autres directions de vaisseau de la même classe de caps,
(0,1) et (−1,0), ont a = −1 : elles reculent). F = plus grand a atteint. On ne garde que les cases connues avec a ≥ F − B
(fenêtre) ; si la fourmi entre sur une case a < F − B (peut-être visitée et oubliée) → ÉCHEC du certificat.
État canonique = (cap, F − a, cases connues de la fenêtre, relatives à la fourmi). Si l'ensemble des états atteints est FINI,
fermé et sans ÉCHEC, c'est une preuve pour tout temps et toute configuration : a(t) ≥ F(t) − B pour toujours.
Usage : python3 preuve_obstacles.py B [limite]"""
import sys
from hx import HX, K, SHIP
B = int(sys.argv[1]) if len(sys.argv) > 1 else 4
LIM = int(sys.argv[2]) if len(sys.argv) > 2 else 3_000_000
A = lambda x, y: x - y
# départ : vaisseau 10 périodes sur blanc
(x, y, h), c0 = SHIP
known = {c0: 1, (x, y): 0}
for t in range(80):
    c = known.get((x, y), 0); h = (h + K[c]) % 6; known[(x, y)] = 1 - c
    x += HX[h][0]; y += HX[h][1]; known.setdefault((x, y), 0)
F = max(A(*p) for p in known)        # toutes les cases connues sont derrière ou sous la fourmi
def canon(x, y, h, F, known):
    win = frozenset((px - x, py - y, c) for (px, py), c in known.items() if A(px, py) >= F - B)
    return (h, F - A(x, y), win)
def decode(s):
    h, f, win = s
    return 0, 0, h, f, {(px, py): c for px, py, c in win}      # fourmi en (0,0), F = f
seen = set(); st = [canon(x, y, h, F, known)]; seen.add(st[0]); fail = None; nb_branch = 0; fmax = 0
while st:
    s = st.pop()
    x, y, h, F, kn = decode(s)
    p = (x, y)
    cols = [kn[p]] if p in kn else [0, 1]
    if p not in kn and A(x, y) < F - B: fail = s; break
    if len(cols) == 2: nb_branch += 1
    for c in cols:
        k2 = dict(kn); h2 = (h + K[c]) % 6; k2[p] = 1 - c
        x2, y2 = x + HX[h2][0], y + HX[h2][1]
        if (x2, y2) not in k2 and A(x2, y2) < F - B: fail = (s, c); break
        F2 = max(F, A(x2, y2))
        s2 = canon(x2, y2, h2, F2, k2)
        fmax = max(fmax, s2[1])
        if s2 not in seen:
            seen.add(s2); st.append(s2)
            if len(seen) > LIM: break
    if fail or len(seen) > LIM: break
if fail: print(f'B={B} ÉCHEC du certificat (la fourmi peut reculer de plus de {B}) après {len(seen)} états :', fail)
elif len(seen) > LIM: print(f'B={B} limite atteinte ({LIM} états) : pas de conclusion')
else: print(f'B={B} PREUVE : {len(seen)} états, ensemble fermé, recul max F−a = {fmax} ; {nb_branch} branchements')
# 2e partie : depuis chaque état du certificat, si toutes les cases inconnues sont BLANCHES (sortie de l'obstacle), la fourmi
# redevient-elle un vaisseau de direction (1,−1) (r = 0) ? (les cases oubliées ne sont jamais revisitées : 1re partie)
if not fail and len(seen) <= LIM:
    from hx import PHASES
    ok = 0; bad = []
    for s in seen:
        x, y, h, F, kn = decode(s)
        g = {p: c for p, c in kn.items() if c}
        for t in range(400):
            c = g.get((x, y), 0); h = (h + K[c]) % 6
            if c: del g[(x, y)]
            else: g[(x, y)] = 1
            x += HX[h][0]; y += HX[h][1]
        near = frozenset((cx - x, cy - y) for cx, cy in g if abs(cx - x) + abs(cy - y) <= 3)
        far = [p for p in g if abs(p[0] - x) + abs(p[1] - y) > 3]
        k = PHASES.get((h, near))
        if k and k[0] == 0: ok += 1
        else: bad.append(s)
    print(f'   sortie sur du blanc : {ok}/{len(seen)} états redeviennent un vaisseau de MÊME direction (1,−1)', 'échecs :' if bad else '', bad[:3])
