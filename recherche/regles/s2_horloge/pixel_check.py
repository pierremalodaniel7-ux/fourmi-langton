"""S2 R-502 — vérifie qu'un pixel trouvé CLIGNOTE : à chaque temps, l'objet local (fourmis du pixel + cases à ≤ 6 de o) est-il dans
l'orbite de R (OFF) ou de R' (ON) ? Liste des basculements sur une période. Usage : pixel_check.py fichier.json [n]"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from exp_osc import hd
from pixel_search import bascule_frame
def orbit_set(ants, cells, p, o):
    A = [[x + o[0], y + o[1], h] for x, y, h in ants]; G = {(x + o[0], y + o[1]): 1 for x, y in cells}; S = set()
    for _ in range(p):
        S.add((frozenset(map(tuple, A)), frozenset(G))); step(A, G)
    return S
def timeline(w, Bs, T=None):
    b1, b2 = bascule_frame(Bs[w['bascule']], w['rot'])
    o = tuple(w['o']); pos = w['pos']
    O0 = orbit_set(b1['ants'], b1['cells'], b1['p'], o); O1 = orbit_set(b2['ants'], b2['cells'], b2['p'], o)
    a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    P = T or w['P']; states = []
    cx, cy = o[0] + b1['ants'][0][0], o[1] + b1['ants'][0][1]
    for t in range(P + 1):
        pa = frozenset(tuple(A[k]) for k in (pos, pos + 1))
        pc = frozenset(q for q in G if hd(q[0] - cx, q[1] - cy) <= 7 and
                       not any(hd(q[0] - A[k][0], q[1] - A[k][1]) <= 2 for k in range(len(A)) if k not in (pos, pos + 1)))
        st = 'OFF' if (pa, pc) in O0 else ('ON' if (pa, pc) in O1 else '?')
        states.append(st)
        if t < P: step(A, G)
    ch = [(t, states[t]) for t in range(1, len(states)) if states[t] != states[t - 1]]
    return states, ch
if __name__ == '__main__':
    W = json.load(open(sys.argv[1])); Bs = json.load(open('data/bascules_exactes.json'))
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    import collections
    kinds = collections.Counter()
    for w in W[:n]:
        st, ch = timeline(w, Bs)
        c = collections.Counter(st)
        seq = ''.join(s[1] if s != '?' else '?' for _, s in ch)
        kinds[(c['ON'] > 0, c['OFF'] > 0)] += 1
        print(w['P'], w['horloge'], w['T'], 'bascule', w['bascule'], 'rot', w['rot'], dict(c), 'changements', ch[:8])
    print(kinds)
