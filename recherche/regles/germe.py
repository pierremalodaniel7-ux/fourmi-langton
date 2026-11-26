#!/usr/bin/env python3
"""R-305 FIL : lanceur (germe) de chaque règle = état pris sur l'autoroute, tronqué derrière la fourmi, puis allégé case par case
(glouton) tant que l'autoroute (même période, même déplacement) démarre AUSSITÔT (début <= 2P). Le nombre de cases obtenu est
un MAJORANT du germe minimal (glouton). Sortie : data/germes_regles.json"""
import sys, json, subprocess
from outils_r import parse, geo
EXE = './fourmi_r'
def one(sit, T, opts=()):
    out = subprocess.run([EXE, '-T', str(T), *opts, '-lot'], input=sit + '\n', capture_output=True, text=True).stdout.splitlines()
    return out
def state(sit, T):
    out = one(sit, T, ('-x', '-dump'))
    d = [l for l in out if l.startswith('DUMP ')][0][5:]
    r, a, c = d.split('|')
    ants = [tuple(map(int, s.split(','))) for s in a.split(';') if s]
    cells = {}
    for s in c.split(';'):
        if s: x, y, k = map(int, s.split(',')); cells[(x, y)] = k
    return ants, cells
def sitstr(rule, ants, cells):
    return f"{rule}|" + ';'.join(f"{x},{y},{d}" for x, y, d in ants) + '|' + ';'.join(f"{x},{y},{k}" for (x, y), k in sorted(cells.items()))
def ok(rule, ant, cells, P, D):
    l = [x for x in one(sitstr(rule, [ant], cells), 60 * P + 64) if not x.startswith(('DUMP', 'PATH', 'ZERO'))][0]
    d = parse(l)
    if d['issue'] != 'AUTOROUTES' or not d['ants'] or d['ants'][0] is None: return False
    p, dx, dy, deb = d['ants'][0]
    return p == P and (dx, dy) == D and deb <= 2 * P
def germe(rule, start):
    d = parse([x for x in one(start, 1 << 22) if not x.startswith(('DUMP','PATH','ZERO'))][0])
    if d['issue'] != 'AUTOROUTES': return None
    P, dx, dy, deb = d['ants'][0]
    ants, cells = state(start, deb + 4 * P)
    ax, ay, ad = ants[0]
    tri = rule.startswith('T:')
    # recentrer : fourmi en (0,0) (triangle : décalage de parité paire)
    sx, sy = ax, ay
    if tri and (sx + sy) % 2: sx -= 1
    ant = (ax - sx, ay - sy, ad)
    cells = {(x - sx, y - sy): k for (x, y), k in cells.items()}
    n2 = dx * dx + dy * dy
    def proj(c): return -((c[0] - ant[0]) * dx + (c[1] - ant[1]) * dy) / n2     # en périodes, derrière la fourmi > 0
    for r in range(0, 200):
        cur = {c: k for c, k in cells.items() if proj(c) <= r}
        if ok(rule, ant, cur, P, (dx, dy)): break
    else: return None
    for c in sorted(cur, key=lambda c: -proj(c)):              # glouton : les plus loin d'abord
        t = dict(cur); del t[c]
        if ok(rule, ant, t, P, (dx, dy)): cur = t
    return {'regle': rule, 'fourmi': list(ant), 'cases': [[x, y, k] for (x, y), k in sorted(cur.items())],
            'P': P, 'D': [dx, dy], 'debut_blanc': deb, 'depart': start}
if __name__ == '__main__':
    res = {}
    try: res = json.load(open('data/germes_regles.json'))
    except Exception: pass
    for a in sys.argv[1:]:
        rule, _, start = a.partition('@')
        g = germe(rule, start or f"{rule}|0,0,0|")
        print(rule, None if g is None else f"P={g['P']} D={g['D']} germe {len(g['cases'])} cases", flush=True)
        if g: res[rule] = g
    json.dump(res, open('data/germes_regles.json', 'w'), indent=0)
