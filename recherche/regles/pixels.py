#!/usr/bin/env python3
"""R-334 Pixel R2L2 « comme Conway » (sans miroir) : pixel ON = le petit oscillateur O (2 fourmis + 1 case, période 3,
« H:R2L2|0,0,3;1,0,0|1,0 ») ; pixel OFF = 1 case noire seule en (0,−1) (ce que l'effacement laisse : l'invariant Q de R-331 l'impose).
ÉCRIRE = 3 vaisseaux qui convergent (film à l'envers, gomme collective R-311, de l'effacement D1 : r = 1, voie −2) : avec la case
(0,−1) ils fabriquent O EXACTEMENT (O est son propre renversé) ; un 4e vaisseau repart.
EFFACER = 1 vaisseau D2 (r = 3, voie 0, quand O est à sa phase 2, joué après O) : O part en 3 vaisseaux et laisse la case (0,−1).
Toutes les routes (entrée et sortie) vont dans 3 directions seulement (caps 2, 3, 4) : aucun choc frontal en vol.
Démo : écran de 2 pixels P1, P2 ; P1 = ON, OFF, ON et P2 = OFF, ON, OFF, dans UNE seule simulation (tous les vaisseaux sont posés à
t = 0, loin). Vérification : 2 moteurs (hx.py et fourmi_r -x -dump) aux 3 lectures et à la fin. Usage : python3 pixels.py [x2 y2 G]"""
import json, subprocess, sys
from hx import step, rot, sit, reverse, PHASES
from exp_osc import setup, hd
O = "H:R2L2|0,0,3;1,0,0|1,0"
def film(r, l, ph, order):
    E = setup(O, r, l, ph, order); assert E['center'] == (0, 0)
    A, g = [list(a) for a in E['ants']], dict(E['g'])
    probe = [a for a in A if a not in E['states'][ph][0]] if order == 0 else None
    kit = ([list(A[-1])] if order == 0 else [list(A[0])], {c: 1 for c in g if c not in E['states'][ph][1]})
    for _ in range(E['T']): step(A, g)
    return E, kit, (A, g)
E1, _, fin1 = film(1, -2, 0, 0)
CREATE = reverse(*fin1); TC = E1['T']           # après TC tours : O (phase 0) exactement + 1 vaisseau qui repart
E2, ERASE, fin2 = film(3, 0, 2, 0); PH_E = 2; TE = E2['T']
CELL = {p: 1 for p in fin2[1] if hd(*p) <= 6}; assert CELL == {(0, -1): 1} and {p: 1 for p in CREATE[1] if hd(*p) <= 6} == CELL
def rotk(ants, g, k, c):
    ra = []
    for x, y, h in ants: X, Y = rot((x, y), k); ra.append([X + c[0], Y + c[1], (h + k) % 6])
    rg = {}
    for (x, y) in g: X, Y = rot((x, y), k); rg[(X + c[0], Y + c[1])] = 1
    return ra, rg
def back(ants, g, s):
    """chaque vaisseau (séparés) reculé de s/8 cases sur sa route : posé à t = 0, il est dans l'état du kit à t = s ; cases fixes ignorées"""
    assert s % 8 == 0
    out = []; G = {}
    for a in ants:
        cs = [p for p in g if hd(p[0] - a[0], p[1] - a[1]) <= 2]
        B = [list(a)]; gg = {p: 1 for p in cs}
        for _ in range(8): step(B, gg)
        d = (B[0][0] - a[0], B[0][1] - a[1]); k = s // 8
        out.append([a[0] - k * d[0], a[1] - k * d[1], a[2]])
        for p in cs: G[(p[0] - k * d[0], p[1] - k * d[1])] = 1
    return out, G
x2, y2, G = (int(v) for v in sys.argv[1:4]) if len(sys.argv) > 3 else (40, 20, 1600)
P1, P2 = (0, 0), (x2, y2)
def t_erase(t_create, tmin):
    """premier instant e ≥ tmin, multiple de 8, où O (fait au temps t_create + TC, phase 0) est à la phase PH_E"""
    e = (tmin + 7) // 8 * 8
    while (e - (t_create + TC)) % 3 != PH_E: e += 8
    return e
plan = [('écrit', P1, 0)]; tc = {P1: 0}
plan += [('efface', P1, t_erase(0, G)), ('écrit', P2, G)]; tc[P2] = G
plan += [('efface', P2, t_erase(G, 2 * G)), ('écrit', P1, 2 * G)]
ants = []; cells = {}
for P in (P1, P2): cells.update({(P[0] + x, P[1] + y): 1 for x, y in CELL})          # écran éteint : 1 case par pixel
for kind, P, s in plan:
    a, g = back(*rotk(*(CREATE if kind == 'écrit' else ERASE), 0, P), s)
    ants += a; cells.update(g)
SNAP = [G, 2 * G, 3 * G]; TEND = 3 * G + 1600
ref_states = E1['states']
def lire(A, g, P):
    na = sorted(tuple(a) for a in A if hd(a[0] - P[0], a[1] - P[1]) <= 6)
    nc = sorted(p for p in g if hd(p[0] - P[0], p[1] - P[1]) <= 6)
    if not na and nc == [(P[0] + x, P[1] + y) for x, y in CELL]: return 'OFF'
    for sa, sg in ref_states:
        if na == sorted((x + P[0], y + P[1], h) for x, y, h in sa) and nc == sorted((x + P[0], y + P[1]) for x, y in sg): return 'ON'
    return '?'
A = [list(a) for a in ants]; g = dict(cells); lectures = []; t = 0
s0 = sit(A, sorted(g))
attendu = [('ON', 'OFF'), ('OFF', 'ON'), ('ON', 'OFF')]
for ts, att in zip(SNAP, attendu):
    while t < ts: step(A, g); t += 1
    etat = (lire(A, g, P1), lire(A, g, P2)); lectures.append((ts, etat))
    print(f't = {ts} : P1 {etat[0]}, P2 {etat[1]}  (attendu {att})', 'OK' if etat == att else 'FAUX')
while t < TEND: step(A, g); t += 1
ok = 0; used = set()
for a in A:
    near = frozenset((p[0] - a[0], p[1] - a[1]) for p in g if hd(p[0] - a[0], p[1] - a[1]) <= 2)
    if (a[2], near) in PHASES: ok += 1; used |= {(a[0] + x, a[1] + y) for x, y in near}
reste = sorted(set(g) - used)
print(f'fin (t = {TEND}) : {ok}/{len(A)} fourmis = vaisseaux propres qui s\'en vont ; cases restantes : {reste}')
fr = []
for ts in SNAP + [TEND]:
    out = subprocess.run(['./fourmi_r', '-T', str(ts), '-x', '-dump', s0], capture_output=True, text=True).stdout
    fr.append([l for l in out.splitlines() if l.startswith('DUMP')][0].split(' ', 1)[1])
B = [list(a) for a in ants]; gb = dict(cells); t = 0; same = 0
for ts, d in zip(SNAP + [TEND], fr):
    while t < ts: step(B, gb); t += 1
    _, da, dc = d.split('|')[:3]
    fa = [list(map(int, x.split(','))) for x in da.split(';') if x]; fc = {tuple(map(int, x.split(',')[:2])) for x in dc.split(';') if x}
    if fa == B and fc == set(gb): same += 1
print(f'2 moteurs : {same}/{len(fr)} états identiques (hx.py et fourmi_r)')
json.dump({'situation': s0, 'P1': P1, 'P2': P2, 'instants': SNAP, 'lectures': lectures, 'fin': TEND, 'propres_fin': f'{ok}/{len(A)}',
           'cases_fin': reste, 'deux_moteurs': f'{same}/{len(fr)}', 'plan': plan}, open('resumes/pixels.json', 'w'), ensure_ascii=False, indent=1)
