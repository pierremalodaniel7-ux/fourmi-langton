"""R-328 : quels enchaînements de 3 usages cassent le demi-additionneur ? (64 suites, on lit le 3e usage)"""
import json, itertools, sys, subprocess
idx = sys.argv[1] if len(sys.argv) > 1 else '0'
src = open('usages_add.py').read().split("random.seed")[0]
import os
exec(src.replace("sys.argv", "['x', '" + idx + "', '3', '200']"))
bad = []
AB = ((0,0),(1,0),(0,1),(1,1))
lines = []; meta = []
for seq in itertools.product(AB, repeat=3):
    al = []; ce = {}; owner = []
    for u, (a, b) in enumerate(seq):
        for n, on in (('B', b), ('A', a), ('K2', 1), ('K3', 1)):
            if not on: continue
            x, cc = src_[n] if False else src[n]; v = (-u * k * dd[n][0], -u * k * dd[n][1])
            al.append((x[0] + v[0], x[1] + v[1], x[2])); owner.append(u); [ce.__setitem__((c[0] + v[0], c[1] + v[1]), 1) for c in cc]
    lines.append(sit(R, al, ce)); meta.append((seq, owner))
for l, (seq, owner) in zip(lot(lines, 1 << 20), meta):
    t = tracks(l); a, b = seq[2]
    mine = [t[i] for i in range(len(owner)) if owner[i] == 2]
    got = (sum(1 for x in mine if x == S), sum(1 for x in mine if x == C))
    if got != (a ^ b, a & b) or any(x is None for x in mine): bad.append((seq, got))
print(len(bad), 'suites de 3 fausses sur 64 :', bad)
