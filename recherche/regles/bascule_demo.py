#!/usr/bin/env python3
"""R-341 Bascule RS R2L2 à UN vaisseau par écriture, sans case fixe.
État 0 = oscillateur R, état 1 = oscillateur R' (2 fourmis chacun, au même endroit). « Mise à 1 » = 1 vaisseau s1 (R → R'), « mise à 0 » =
1 vaisseau s2 (R' → R) ; chaque vaisseau ressort. Démo : N écritures alternées 1, 0, 1, 0… au même endroit, tous les vaisseaux posés à t = 0
(chacun arrive quand l'oscillateur est à la bonne phase). Contrôle de l'état entre deux écritures ; 2 moteurs.
Usage : python3 bascule_demo.py [indice dans data/bascules_RS.json] [N]"""
import sys, json, subprocess
from hx import step, sit
from exp_osc import setup, hd, parse
import ecran
I = int(sys.argv[1]) if len(sys.argv) > 1 else 0; N = int(sys.argv[2]) if len(sys.argv) > 2 else 20
X = json.load(open('data/bascules_RS.json'))[I]
def kv(s): return dict(x.split('=') for x in s.split()[1:] if '=' in x)
f1, f2 = kv(X['s1']), kv(X['s2'])
R, R2 = X['R'], X['R2']
def orbit_states(osc):
    a, c = parse(osc); A = [list(x) for x in a]; g = {x: 1 for x in c}; out = []
    A0 = [list(x) for x in a]; g0 = dict(g)
    while True:
        out.append((sorted(map(tuple, A)), sorted(g))); step(A, g)
        if A == A0 and g == g0: return out
OR, OR2 = orbit_states(R), orbit_states(R2)
def kit(osc, f):
    E = setup(osc, int(f['r']), int(f['l']), int(f['ph']), int(f['ord']))
    A = E['ants']; sh = A[-1] if int(f['ord']) == 0 else A[0]
    oa, og = E['states'][int(f['ph'])]
    cells = [c for c in E['g'] if c not in og]
    # état final de l'objet après l'expérience seule
    B = [list(a) for a in A]; g = dict(E['g'])
    for _ in range(E['T']): step(B, g)
    obj = (sorted(tuple(b) for b in B if hd(b[0] - E['center'][0], b[1] - E['center'][1]) <= E['R']), sorted(c for c in g if hd(c[0] - E['center'][0], c[1] - E['center'][1]) <= E['R']))
    return ([list(sh)], {c: 1 for c in cells}), int(f['ph']), E['T'], obj, int(f['ord'])
K1, ph1, T1, end1, o1 = kit(R, f1); K2, ph2, T2, end2, o2 = kit(R2, f2)
i_end1 = OR2.index(end1); i_end2 = OR.index(end2)     # phase de l'objet d'arrivée à la fin de chaque expérience
def backx(Kt, e):
    """vaisseau du kit, posé à t = 0 pour être dans l'état du kit à l'instant e (e quelconque)"""
    m = (e + 7) // 8; a, g = ecran.back(Kt[0], Kt[1], 8 * m)
    A = [list(x) for x in a]; G_ = dict(g)
    for _ in range(8 * m - e): step(A, G_)
    return A, G_
G = 1600
events = []; t = 0; cur = ('R', 0, 0)       # (oscillateur, phase à l'instant de référence, instant de référence)
for n in range(N):
    want = 1 - n % 2
    orb, ph_need, Kt, Tt, iend = (OR, ph1, K1, T1, i_end1) if want == 1 else (OR2, ph2, K2, T2, i_end2)
    e = max(n * G, cur[2])
    while (cur[1] + e - cur[2]) % len(orb) != ph_need: e += 1
    events.append((e, want, Kt)); cur = ('R2' if want == 1 else 'R', iend, e + Tt)
ants = []; cells = {}
a0, c0 = parse(R); ants += [list(x) for x in a0]; cells.update({c: 1 for c in c0})
for e, want, Kt in events:
    a, g = backx(Kt, e)
    ants += a; cells.update(g)                    # vaisseaux joués après l'objet (ord = 0 pour les deux expériences choisies)
assert o1 == 0 and o2 == 0
TEND = events[-1][0] + 2000
def etat(A, g):
    na = sorted(tuple(a) for a in A if hd(a[0], a[1]) <= 8); nc = sorted(c for c in g if hd(*c) <= 8)
    if (na, nc) in OR: return 0
    if (na, nc) in OR2: return 1
    return '?'
checks = [(events[k + 1][0] - 8 if k + 1 < N else TEND, (lambda A, g: etat(A, g))) for k in range(N)]
vals, A, g = ecran.simulate(ants, cells, checks, TEND, None)
justes = sum(1 for k, v in enumerate(vals) if v == events[k][1])
print('écritures :', ''.join(str(e[1]) for e in events)); print('états lus :', ''.join(str(v) for v in vals), f'→ {justes}/{N}')
s0 = sit(ants, sorted(cells))
out = subprocess.run(['./fourmi_r', '-T', str(TEND), '-x', '-dump', s0], capture_output=True, text=True).stdout
d = [l for l in out.splitlines() if l.startswith('DUMP')][0].split(' ', 1)[1]; _, da, dc = d.split('|')[:3]
same = [list(map(int, x.split(','))) for x in da.split(';') if x] == A and {tuple(map(int, x.split(',')[:2])) for x in dc.split(';') if x} == set(g)
print('2 moteurs identiques à la fin :', same, f'({len(ants)} fourmis, t = {TEND})')
json.dump({'R': R, 'R2': R2, 's1': X['s1'], 's2': X['s2'], 'ecritures': [e[1] for e in events], 'lus': vals, 'justes': f'{justes}/{N}', 'deux_moteurs': same,
           'situation': s0}, open('resumes/bascule_rs.json', 'w'), ensure_ascii=False, indent=1)
