#!/usr/bin/env python3
"""R-701 Démultiplexeur 2 → 4 R2L2 : recherche par calcul exact sur les trajectoires (catalogue des chocs propres, R-700).
Pièces d'un usage : W (« écrire », direction 0, toujours présent), a1, a0 (bits d'adresse : vaisseau présent = 1), K (constant).
  G1 : W × a1 → W0 = W tout droit (a1 = 0) ou W1 = une sortie du choc (a1 = 1), l'autre sortie g1 part (déchet) ;
  F  : a0 × K → c1, c2 (deux copies de a0 ; si a0 = 0, K file tout droit) ;
  G2 : c1 × W0 → sorties « 01 » (sinon W0 continue = « 00 ») ;  G3 : c2 × W1 → sorties « 11 » (sinon W1 continue = « 10 »).
Équation exacte (glissements k2, k3 de G2, G3 le long de W0, W1 ; glissement n de F le long de c1) : les deux sorties de F doivent
être EXACTEMENT les trajectoires d'entrée x(k2) de G2 et y(k3) de G3 (phase comprise). Puis simulation des 4 cas (fourmi_r) :
l'état final doit être EXACTEMENT celui prévu par le calcul (aucune interaction imprévue, 0 case).
Usage : python3 demux_cherche.py N_tirages graine  -> data/demux_<graine>.json"""
import sys, json, random, itertools
from traj import *
NT = int(sys.argv[1]) if len(sys.argv) > 1 else 20000; SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0
random.seed(SEED)
cat = catalogue()
W = norm((0, 0, 0, 0)); d0 = D[0]
def solve2(a, b, c):
    """n·a + k·b = c (vecteurs entiers 2D) -> (n, k) entiers ou None"""
    det = a[0] * b[1] - a[1] * b[0]
    if det == 0: return None
    nn = c[0] * b[1] - c[1] * b[0]; kk = a[0] * c[1] - a[1] * c[0]
    if nn % det or kk % det: return None
    return nn // det, kk // det
def candidates(G1, i1, w1, G2, i2, G3, i3, F, j, K2):
    G1 = G1.align(i1, W, 0)
    W1 = G1.outs[i1] if w1 == 0 else G1.outs[1 - i1]
    C2 = G2.align(i2, W, 0); x0 = C2.ins[1 - i2]
    C3 = G3.align(i3, W1, 0); y0 = C3.ins[1 - i3]
    rx, ry, rw1 = x0[0], y0[0], W1[0]
    o1, o2 = F.outs[j], F.outs[1 - j]; rho = (rx - o1[0]) % 6
    if (o2[0] + rho) % 6 != ry: return []
    FR = F.rot(rho); O1, O2 = FR.outs[j], FR.outs[1 - j]
    dtau = O2[3] - O1[3] + x0[3] - y0[3]
    if dtau % 8: return []
    q = dtau // 8; dy = D[ry]; dx = D[rx]; dw = D[rw1]
    Cv = (O2[1] - O1[1] + x0[1] - y0[1] - q * dy[0], O2[2] - O1[2] + x0[2] - y0[2] - q * dy[1])
    a = (dx[0] - dy[0], dx[1] - dy[1]); b = (dy[0] - dw[0], dy[1] - dw[1]); e = (d0[0] - dy[0], d0[1] - dy[1])
    out = []
    for k2 in K2:
        s = solve2(a, b, (-Cv[0] - k2 * e[0], -Cv[1] - k2 * e[1]))
        if s is None: continue
        n, k3 = s
        tG1 = G1.te; tG2 = C2.te + 8 * k2; tG3 = C3.te + 8 * k3
        X = (rx, x0[1] + k2 * d0[0], x0[2] + k2 * d0[1], x0[3] + 8 * k2)
        FA = FR.align(j, X, n, 'outs')
        tF = FA.te
        if min(tG2, tG3) - tG1 < 48 or min(tG2, tG3) - tF < 48 or max(tG2, tG3) - min(tF, tG1) > 900: continue
        out.append((k2, n, k3, FA))
    return out
def build(G1, i1, w1, G2, i2, G3, i3, F, j, k2, k3, FA, ra0):
    """trajectoires d'entrée, ordre de jeu, résultats attendus pour les 4 cas"""
    G1 = G1.align(i1, W, 0)
    W1 = G1.outs[i1] if w1 == 0 else G1.outs[1 - i1]; g1 = G1.outs[1 - i1] if w1 == 0 else G1.outs[i1]
    a1 = G1.ins[1 - i1]
    C2 = G2.align(i2, W, k2); C3 = G3.align(i3, W1, k3)
    a0, Kc = FA.ins[ra0], FA.ins[1 - ra0]
    x, y = FA.outs[j], FA.outs[1 - j]
    assert same(x, C2.ins[1 - i2]) and same(y, C3.ins[1 - i3])
    ant_of_F = {0: 'a0' if ra0 == 0 else 'K', 1: 'K' if ra0 == 0 else 'a0'}
    c1ant, c2ant = ant_of_F[j], ant_of_F[1 - j]
    w1ant = 'W' if w1 == 0 else 'a1'
    cons = []   # (avant, après)
    def pair(first_idx, names): cons.append((names[first_idx], names[1 - first_idx]))
    pair(G1.first, ['W', 'a1'] if i1 == 0 else ['a1', 'W'])
    pair(C2.first, ['W', c1ant] if i2 == 0 else [c1ant, 'W'])
    pair(C3.first, [w1ant, c2ant] if i3 == 0 else [c2ant, w1ant])
    pair(FA.first, ['a0', 'K'] if ra0 == 0 else ['K', 'a0'])
    order = next((p for p in itertools.permutations(['W', 'a1', 'a0', 'K']) if all(p.index(u) < p.index(v) for u, v in cons)), None)
    if order is None: return None
    T = {'W': W, 'a1': a1, 'a0': a0, 'K': Kc}
    exp = {(0, 0): [W, Kc], (0, 1): [C2.outs[0], C2.outs[1], y], (1, 0): [W1, g1, Kc], (1, 1): [g1, C3.outs[0], C3.outs[1], x]}
    times = {'G1': G1.te, 'G2': C2.te, 'G3': C3.te, 'F': FA.te}
    outs = {(0, 0): [W], (0, 1): list(C2.outs), (1, 0): [W1], (1, 1): list(C3.outs)}
    return {'order': order, 'T': T, 'exp': {k: sorted(norm(t) for t in v) for k, v in exp.items()}, 'times': times, 'outs': outs}
def shift_all(B, dt):
    B = dict(B); B['T'] = {k: movT(v, (0, 0), dt) for k, v in B['T'].items()}
    B['exp'] = {k: sorted(movT(t, (0, 0), dt) for t in v) for k, v in B['exp'].items()}
    B['outs'] = {k: [movT(t, (0, 0), dt) for t in v] for k, v in B['outs'].items()}
    B['times'] = {k: v + dt for k, v in B['times'].items()}; return B
def case_sit(B, a1, a0):
    names = [n for n in B['order'] if n in ('W', 'K') or (n == 'a1' and a1) or (n == 'a0' and a0)]
    return sit_of([B['T'][n] for n in names], 0)
def check_batch(Bs):
    """simule les 4 cas de chaque candidat (un seul lot fourmi_r) ; renvoie la liste des candidats justes et les causes d'échec"""
    cases = [(0, 0), (0, 1), (1, 0), (1, 1)]; lines = []; Ts = []
    for B in Bs:
        Tend = max(B['times'].values()) + 640; B['Tend'] = Tend
        for c in cases: lines.append(case_sit(B, *c)); Ts.append(Tend)
    good = []; why = {}
    # fourmi_r prend un seul T par lot : on groupe par Tend
    byT = {}
    for k, T in enumerate(Ts): byT.setdefault(T, []).append(k)
    res = [None] * len(lines)
    groups = sorted(byT); allk = []; alll = []
    for T in groups:
        ks = byT[T]; R = lotdump([lines[k] for k in ks], T)
        for k, r in zip(ks, R): res[k] = r
    for b, B in enumerate(Bs):
        ok = True
        for ci, c in enumerate(cases):
            a, cc = res[4 * b + ci]; d = decode(a, cc)
            if d is None: why['sale ' + str(c)] = why.get('sale ' + str(c), 0) + 1; ok = False; break
            if sorted(of_label(lab_of(z, B['Tend'])) for z in d) != B['exp'][c]: why['autre ' + str(c)] = why.get('autre ' + str(c), 0) + 1; ok = False; break
        if ok: good.append(B)
    return good, why
if __name__ == '__main__':
    found = []; tried = 0; sims = 0; WHY = {}
    K2 = range(6, 70); batch = []
    while tried < NT:
        G1, G2, G3, F = (random.choice(cat) for _ in range(4))
        i1, w1, i2, i3, j = (random.randrange(2) for _ in range(5))
        tried += 1
        cs = candidates(G1, i1, w1, G2, i2, G3, i3, F, j, K2)
        if not cs: continue
        k2, n, k3, FA = random.choice(cs)
        B = None
        for ra0 in (0, 1):
            B = build(G1, i1, w1, G2, i2, G3, i3, F, j, k2, k3, FA, ra0)
            if B: break
        if not B: continue
        B = shift_all(B, 400 - min(B['times'].values()))
        B['choix'] = [i1, w1, i2, i3, j, k2, n, k3, ra0]; B['G'] = [G1.__dict__, G2.__dict__, G3.__dict__, F.__dict__]
        batch.append(B)
        if len(batch) >= 1500 or tried >= NT:
            g, why = check_batch(batch); sims += 4 * len(batch); batch = []
            for k, v in why.items(): WHY[k] = WHY.get(k, 0) + v
            found += g
            print(tried, 'tirages', sims, 'simulations', len(found), 'trouvés', WHY, flush=True)
    if batch:
        g, why = check_batch(batch); sims += 4 * len(batch); found += g
        for k, v in why.items(): WHY[k] = WHY.get(k, 0) + v
    for B in found:
        B['exp'] = {str(k): v for k, v in B['exp'].items()}; B['outs'] = {str(k): v for k, v in B['outs'].items()}
    json.dump(found, open(HERE + f'/data/demux_{SEED}.json', 'w'))
    print(tried, 'tirages', sims, 'simulations', len(found), 'démultiplexeurs justes 4/4', WHY)
