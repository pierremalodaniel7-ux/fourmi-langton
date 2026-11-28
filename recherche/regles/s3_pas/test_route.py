#!/usr/bin/env python3
"""R-622 test d'un routage seul : signal s (présent ssi s = 1) amené par virages sur une ligne W ; 2 moteurs, état final = modèle."""
from circ import *
def build_route(C, src_id, A, sol):
    _, seq, ks, out = sol; cur_id, cur = src_id, A
    for (side, o), (K, w, sd, t, oA, oB) in zip(seq, out):
        kid = C.add_ship(K); C.add_gate(t, kid, K, cur_id, cur, oA, oB, 'virage')
        if o == 1: cur = oA
        elif o == 2: cur_id, cur = kid, oB
        else: cur_id, cur = kid, K
    return cur_id, cur
if __name__ == '__main__':
    A = (1, -25, 0, 4)
    for W0, pol, j in [((0, 40, -20, 2), 0, 0), ((0, 40, -20, 2), 1, 0), ((3, -100, 100, 0), 0, 0), ((1, 40, -20, 4), 0, 5)]:
        W = tshift(W0, 3000); sols = route(A, 0, W, 3500, pol); sol = sols[j]
        C = Circ(['s']); sid = C.add_ship(A, C.mask_of(lambda e: e['s'] == 1))
        i, w = build_route(C, sid, A, sol); assert w == W
        C.compile(4000); cf = C.conflicts()
        r = C.check(engine2=True)
        got = [C.present(i, W, 3600) for _ in [0]][0]
        want = C.mask_of(lambda e: e['s'] != pol)
        print(W0, 'pol', pol, 'virages', len(sol[1]), 'conflits', len(cf), 'états finaux = modèle', [x[1] for x in r], '2 moteurs', [x[2] for x in r],
              'signal sur W juste :', got == want)
