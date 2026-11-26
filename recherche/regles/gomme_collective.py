#!/usr/bin/env python3
"""R-311 Gomme COLLECTIVE (n fourmis jouées l'une après l'autre) : après T tours, chaque fourmi est posée sur la case qu'elle
vient de quitter, cap retourné, et l'ORDRE DE JEU EST INVERSÉ. On rejoue T tours : la grille revient-elle exactement à l'état
de départ ? Testé sur les 28 portes RL d'ordinateur/germes_ordinateur_2026-11-17.json (+ l'additionneur 4 bits) et sur des
situations au hasard pour RL, H:R2L2, LLR. Usage : python3 gomme_collective.py"""
import json, random, subprocess, sys
from outils_r import geo
def run(sit, T):
    out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input=sit + '\n', capture_output=True, text=True).stdout
    d = [l for l in out.splitlines() if l.startswith('DUMP ')][0][5:]
    r, a, c = d.split('|')
    return [tuple(map(int, s.split(','))) for s in a.split(';') if s], {(int(x), int(y)): int(k) for x, y, k in (s.split(',') for s in c.split(';') if s)}
def capn(s):
    s = s.strip(); return {'H': 0, 'D': 1, 'B': 2, 'G': 3}.get(s, None) if not s.lstrip('-').isdigit() else int(s)
def gomme_coll(rule, ants, cells, T):
    D, M = geo(rule)
    sit = f"{rule}|" + ';'.join(f"{x},{y},{d}" for x, y, d in ants) + '|' + ';'.join(f"{x},{y},{k}" for (x, y), k in cells.items())
    a2, c2 = run(sit, T)
    rev = [(x - D[d][0], y - D[d][1], (d + M // 2) % M) for x, y, d in a2][::-1]
    s2 = f"{rule}|" + ';'.join(f"{x},{y},{d}" for x, y, d in rev) + '|' + ';'.join(f"{x},{y},{k}" for (x, y), k in c2.items())
    a3, c3 = run(s2, T)
    ini = {k: v for k, v in cells.items() if v}
    return c3 == ini, len(c2), sum(1 for k in set(c3) | set(ini) if c3.get(k, 0) != ini.get(k, 0))
if __name__ == '__main__':
    ok = tot = 0
    for g in json.load(open('../../ordinateur/germes_ordinateur_2026-11-17.json')):
        ants = []
        for s in g['fourmis'].split(';'):
            if s.count(',') < 2: continue
            x, y, d = s.split(','); ants.append((int(x), int(y), capn(d)))
        cells = {}
        for s in g['points'].split(';'):
            if s.strip(): x, y = s.split(',')[:2]; cells[(int(x), int(y))] = 1
        for T in (3000, 20000):
            r, n2, nd = gomme_coll(g['regle'], ants, cells, T); tot += 1; ok += r
            if not r: print('ÉCHEC', g['nom'], T, nd)
    print(f"portes RL (28 germes × 2 durées) : {ok}/{tot} remises à zéro exactes")
    random.seed(3)
    for rule in ('RL', 'H:R2L2', 'T:RL', 'H:R1L1', 'LLR', 'H:R1R2'):
        ok = 0; N = 40
        for e in range(N):
            n = random.randint(2, 6)
            ants = [(random.randint(-6, 6), random.randint(-6, 6), random.randint(0, 5 if ':' in rule else 3)) for _ in range(n)]
            cells = {(random.randint(-6, 6), random.randint(-6, 6)): 1 for _ in range(random.randint(0, 8))}
            r, *_ = gomme_coll(rule, ants, cells, random.randint(100, 5000)); ok += r
        print(f"{rule} : {ok}/{N} situations au hasard (2 à 6 fourmis) remises à zéro")
