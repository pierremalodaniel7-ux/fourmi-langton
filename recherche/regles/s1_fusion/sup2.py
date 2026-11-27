#!/usr/bin/env python3
"""S1 : test « 2 usages, superposition exacte » en lot pour une liste de circuits (16 cas chacun, 256 couples, k = 200 périodes).
superpose(circuits, T3) -> liste du nombre de couples en superposition exacte (sur 256)."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from fa_lib import decode, lotdump
from circuit import shiftsh
def superpose(circuits, T3, k=200, pairs=None):
    lines = []; meta = []
    for ci, C in enumerate(circuits):
        cs = C.cases(); P = pairs or list(itertools.product(range(len(cs)), repeat=2))
        for i, j in P: lines.append(C.multi([cs[i], cs[j]], k)); meta.append((ci, i, j))
        for i in range(len(cs)): lines.append(C.multi([cs[i]], k)); meta.append((ci, i, None))
    T = T3 + 2 * k * 8
    R = lotdump(lines, T)
    single = {}
    for (ci, i, j), r in zip(meta, R):
        if j is None: single[(ci, i)] = decode(*r)
    score = [0] * len(circuits)
    for (ci, i, j), r in zip(meta, R):
        if j is None: continue
        d = decode(*r); a, b = single[(ci, i)], single[(ci, j)]
        if d is None or a is None or b is None: continue
        if sorted(map(tuple, d)) == sorted([tuple(x) for x in a] + [shiftsh(x, k) for x in b]): score[ci] += 1
    return score
