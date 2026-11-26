#!/usr/bin/env python3
"""R-337 Le demi-additionneur R2L2 réutilisable choisi : décodage de S et C usage par usage (20 usages au hasard, UNE simulation),
2 moteurs (fourmi_r et hx.py). Usage : python3 demi_add_final.py [graine] [k]"""
import sys, json, random, subprocess
from hx import step, ship_dir
from demi_add_z import usage_parts, multi, AT
from demi_add_k import ships, fmt, OFFS, lane, parse_dump
from exp_osc import hd
good = json.load(open('data/dz_ha_vingt.json'))['ok']
g = min(good, key=lambda g: (g['K2'][0], abs(g['K3'][1]) + abs(g['K3'][2])))       # le plus court zigzag
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7; k = int(sys.argv[2]) if len(sys.argv) > 2 else 200
random.seed(seed); NU = 20
seq = [random.choice([(0, 0), (0, 1), (1, 0), (1, 1)]) for _ in range(NU)]
TT = NU * k * 8 + 4000
Csig = tuple(g['C'][0])           # la sortie qui code C = a∧b
def fourmi_r(s, T):
    out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', s], capture_output=True, text=True).stdout
    return parse_dump([l for l in out.splitlines() if l.startswith('DUMP')][0])
def along(x, y, r):
    from hx import rot
    X, Y = rot((x, y), -r % 6); return X - Y
def detail(ants, cells):
    """vaisseaux avec (r, voie, abscisse le long de la route)"""
    out = []
    for x, y, h in ants:
        near = frozenset((p[0] - x, p[1] - y) for p in cells if hd(p[0] - x, p[1] - y) <= 2)
        from hx import PHASES
        r, ph = PHASES[(h, near)]; gx, gy = x - OFFS[(r, ph)][0], y - OFFS[(r, ph)][1]
        out.append((r, lane(gx, gy, r), along(gx, gy, r)))
    return out
s_multi = multi(g, seq, k)
fa, fc = fourmi_r(s_multi, TT)
# 2e moteur
rule, a_, c_ = s_multi.split('|')
A = [list(map(int, t.split(','))) for t in a_.split(';')]; G = {tuple(map(int, t.split(','))): 1 for t in c_.split(';') if t}
for _ in range(TT): step(A, G)
same = sorted(map(tuple, A)) == sorted(fa) and set(G) == set(fc)
D = detail(fa, fc)
# repères : abscisse de S et de C pour un usage 0 seul (cas (1,0), (0,1), (1,1)) au même instant final
ref = {}
for ab in [(1, 0), (0, 1), (1, 1)]:
    ra, rc = fourmi_r(fmt(*usage_parts(g, ab[0], ab[1], 0, k)), TT); ref[ab] = detail(ra, rc)
alS = {ab: [x[2] for x in ref[ab] if (x[0], x[1]) == (0, 0)] for ab in [(1, 0), (0, 1)]}
alC = [x[2] for x in ref[(1, 1)] if (x[0], x[1]) == Csig][0]
per_period = 2      # l'abscisse d'un vaisseau avance de 2 par période
justes = 0; lignes = []
for u, (a, b) in enumerate(seq):
    S = any((x[0], x[1]) == (0, 0) and any(x[2] == v - per_period * u * k for v in alS[(1, 0)] + alS[(0, 1)]) for x in D)
    C = any((x[0], x[1]) == Csig and x[2] == alC - per_period * u * k for x in D)
    ok = (S == (a ^ b)) and (C == (a & b)); justes += ok
    lignes.append(f'usage {u + 1:2d} : a = {a}, b = {b} → S = {int(S)}, C = {int(C)}  {"OK" if ok else "FAUX"}')
print('\n'.join(lignes))
nK = sum(1 for _ in seq) * 2
print(f'{justes}/{NU} additions justes ; {len(fa)} fourmis ; 2 moteurs identiques : {same} ; cases restantes hors vaisseaux : '
      f'{len(set(fc)) - sum(len([p for p in fc if hd(p[0] - x, p[1] - y) <= 2]) for x, y, h in fa)}')
print('demi-additionneur : K2 =', g['K2sit'], ' K3 =', g['K3sit'], ' C lu sur', Csig)
json.dump({'porte': 'H:R2L2|0,0,4;30,-56,0|1,0,1;29,-55,1', 'K2': g['K2sit'], 'K3': g['K3sit'], 'ordre_K2': g['K2'][5], 'ordre_K3': g['K3'][4],
           'S_voie': (0, 0), 'C_voie': Csig, 'k': k, 'suite': seq, 'justes': f'{justes}/{NU}', 'deux_moteurs': same, 'situation_20_usages': s_multi,
           'un_usage': {str(ab): fmt(*usage_parts(g, ab[0], ab[1], 0, k)) for ab in [(0, 0), (0, 1), (1, 0), (1, 1)]}},
          open('resumes/demi_additionneur_reutilisable.json', 'w'), ensure_ascii=False, indent=1)
