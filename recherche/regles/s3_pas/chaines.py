#!/usr/bin/env python3
"""R-604 Chaînes NOR en classe paire : la puissance K (dir 0) rencontre des littéraux L_1, L_2, … (dir 2 ou 4), chacun placé selon une
géométrie d'échange g_i (valable dans les 2 ordres). Après un échange K est décalé de σ_i. compat[i][j] = le littéral placé selon g_j
est transparent (2 ordres) pour K décalé de σ_i. On cherche les plus longues suites g_1 … g_n avec compat[i][j] pour tout i < j."""
import json, itertools
from swaps import issue, shift
S = json.load(open('data/swaps.json'))
U = [x for x in S if x['autre_ordre'] == 'échangé' and x['ordre'] == 0]
print(len(U), 'géométries d\'échange valables dans les 2 ordres')
def TT(wA, wB): return all(issue(wA, wB, o, 880) == 'T' for o in (0, 1))
n = len(U); C = [[False] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i == j: continue
        C[i][j] = TT(tuple(U[j]['A']), shift(tuple(U[j]['B']), tuple(U[i]['sB'])))
for i in range(n): print(i, U[i]['r'], U[i]['tau'], U[i]['v'], 'σK', U[i]['sB'], ''.join('1' if C[i][j] else '.' for j in range(n)))
# plus longue chaîne (DFS)
best = []
def dfs(seq):
    global best
    if len(seq) > len(best): best = list(seq)
    for j in range(n):
        if j not in seq and all(C[i][j] for i in seq): dfs(seq + [j])
dfs([])
print('plus longue chaîne :', len(best), [(U[i]['r'], U[i]['tau'], U[i]['v']) for i in best])
json.dump(dict(U=U, C=C, best=best), open('data/chaines.json', 'w'))
