#!/usr/bin/env python3
"""R-300 : la « gomme ». Une fourmi joue T pas ; on la remet sur la case qu'elle vient de quitter, tête à l'envers,
et on la laisse jouer T pas avec LA MÊME règle. La grille revient-elle à son état de départ ?
Moteur : fourmi_r (copie de src/fourmi + -x -dump). Usage : python3 gomme.py [T]"""
import subprocess, sys, random, itertools
EXE = './fourmi_r'
def run(sit, T):
    out = subprocess.run([EXE, '-T', str(T), '-x', '-dump', '-lot'], input=sit + '\n', capture_output=True, text=True).stdout
    d = [l for l in out.splitlines() if l.startswith('DUMP ')][0][5:]
    r, a, c = d.split('|')
    ants = [tuple(map(int, s.split(','))) for s in a.split(';') if s]
    cells = {}
    for s in c.split(';'):
        if s: x, y, k = map(int, s.split(',')); cells[(x, y)] = k
    return r, ants, cells
SQ = [(0,-1),(1,0),(0,1),(-1,0)]; HX = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]; TR = [(1,0),(1,0),(0,1),(-1,0),(-1,0),(0,-1)]
def geo(rule):
    if rule.startswith('H:'): return HX, 6
    if rule.startswith('T:'): return TR, 6
    return SQ, 4
def gomme(rule, T, init=None, start=(0, 0, 0)):
    init = init or {}
    D, M = geo(rule)
    sit = f"{rule}|{start[0]},{start[1]},{start[2]}|" + ';'.join(f"{x},{y},{k}" for (x, y), k in init.items())
    _, ants, cells = run(sit, T)
    x, y, d = ants[0]
    px, py = x - D[d][0], y - D[d][1]               # case qu'elle vient de quitter
    g = f"{rule}|{px},{py},{(d + M // 2) % M}|" + ';'.join(f"{a},{b},{k}" for (a, b), k in cells.items())
    _, ants2, cells2 = run(g, T)
    ok = cells2 == {k: v for k, v in init.items() if v}
    return ok, len(cells), len(cells2), ants2[0]
if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    rules = ['RL', 'LR', 'LLR', 'LLLR', 'RLLR', 'LLRRRL', 'RN', 'RU', 'NU', 'RR', 'UU', 'NN',
             'H:R1L1', 'H:R2L2', 'H:R1R2', 'H:R1L2', 'H:R1U', 'H:R2N', 'H:UN', 'H:R1L1N', 'H:R1L1R1L1', 'T:RL', 'T:LR', 'T:RU', 'T:RR', 'T:RLL']
    random.seed(1)
    for rule in rules:
        res = []
        for essai in range(4):
            init = {}
            if essai:                                   # départ non blanc : quelques cases au hasard
                q = len([c for c in rule[2:] if c in 'RLNU']) if ':' in rule else len(rule)
                for _ in range(6):
                    init[(random.randint(-3, 3), random.randint(-3, 3))] = random.randint(1, max(1, q - 1))
            ok, n1, n2, a = gomme(rule, T, init)
            res.append('oui' if ok else f'non({n2})')
        print(f"{rule:12s} T={T}  efface : {' '.join(res)}")
