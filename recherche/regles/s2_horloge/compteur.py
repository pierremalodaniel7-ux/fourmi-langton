"""S2 R-503 — objets à k états qu'un FLUX de vaisseaux identiques (même route, espacés de Δ pas) fait tourner en rond :
X0 → X1 → … → X(k−1) → X0, chaque vaisseau ressortant EXACTEMENT non perturbé. k = 2 : bascule T ; k = 4 : compteur modulo 4.
Étape 1 : conversions traversantes (angle 0) de miroir2 tir (data/tir1.txt) dont le vaisseau ressort exact.
Étape 2 : flux de NV vaisseaux pour Δ ∈ [D0, D0 + NΔ) ; on note le premier k où l'objet revient exactement (même place, orbite de X0)
et tous les vaisseaux sont exacts. Moteur : fourmi_r (-x -dump), décodage Python.
Usage : python3 s2_horloge/compteur.py NV D0 NΔ"""
import sys, json, re, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of, lotdump
from demi_add_k import fmt
from tri import virt, adv, at
from bascule_shift import setup, kv
from exp_osc import hd
TT = 720
def orbit_set(ants, cells, p):
    A = [list(t) for t in ants]; G = {tuple(c): 1 for c in cells}; S = set()
    for _ in range(p):
        S.add((frozenset(map(tuple, A)), frozenset(G))); step(A, G)
    return S
if __name__ == '__main__':
    NV, D0, ND = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    L = [l for l in open('data/tir1.txt') if ' angle=0 ' in l]
    conv = []
    for l in L:
        head, Rs = l.split(' | ')[0], l.split(' | ')[1].strip()
        conv.append((Rs, kv(head), head))
    # étape 1 : un seul vaisseau, exact ?
    jobs = []; meta = []
    for Rs, info, head in conv:
        ants, cells, V0, oc, ordr, na = setup(Rs, info)
        jobs.append(fmt(ants, cells)); meta.append((Rs, info, head, V0, oc, ordr, na))
    res = lotdump(jobs, TT)
    exact = []
    for m, (ants, cells) in zip(meta, res):
        Rs, info, head, V0, oc, ordr, na = m
        q = 0 if ordr == 1 else na
        v = virt(tuple(ants[q]), cells, TT)[0]
        if v == V0: exact.append(m)
    print('conversions traversantes :', len(conv), ' dont exactes :', len(exact), flush=True)
    # étape 2 : flux
    jobs = []; meta2 = []
    for m in exact:
        Rs, info, head, V0, oc, ordr, na = m
        a, c = parts_of(Rs); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
        for _ in range(int(info['ph'])): step(A, G)
        for Dl in range(D0, D0 + ND):
            vs = [adv(V0, -k * Dl) for k in range(NV)]
            sh = [at(v, 0) for v in vs]
            shipants = [s[0] for s in sh]; shipcells = [x for s in sh for x in s[1]]
            ants = shipants + [tuple(x) for x in A] if ordr == 1 else [tuple(x) for x in A] + shipants
            jobs.append(fmt(ants, list(G) + shipcells)); meta2.append((m, Dl, vs))
    print('flux à simuler :', len(jobs), flush=True)
    found = []; cnt = collections.Counter()
    B = 20000
    for i in range(0, len(jobs), B):
        part = meta2[i:i + B]
        Tend = max((NV - 1) * Dl + TT for (_, Dl, _) in part)
        # on simule chaque job au temps (NV-1)·Δ + TT : regroupés par Δ ; ici un seul temps par lot → on refait par Δ
        byT = collections.defaultdict(list)
        for k, (m, Dl, vs) in enumerate(part): byT[(NV - 1) * Dl + TT].append(i + k)
        for Tf, idx in byT.items():
            rr = lotdump([jobs[k] for k in idx], Tf)
            for k, (ants, cells) in zip(idx, rr):
                m, Dl, vs = meta2[k]; Rs, info, head, V0, oc, ordr, na = m
                qs = list(range(NV)) if ordr == 1 else list(range(na, na + NV))
                okv = all(virt(tuple(ants[q]), cells, Tf)[0] == vs[n] for n, q in enumerate(qs))
                if not okv: cnt['vaisseau perturbé'] += 1; continue
                obj = [tuple(x) for q, x in enumerate(ants) if q not in qs]
                oc_ = [x for x in cells if not any(hd(x[0] - ants[q][0], x[1] - ants[q][1]) <= 2 for q in qs)]
                found.append((m, Dl, obj, oc_)); cnt['vaisseaux exacts'] += 1
        print(i + B, dict(cnt), flush=True)
    # retour à X0 ?
    win = []
    orbs = {}
    for m, Dl, obj, oc_ in found:
        Rs, info, head, V0, oc, ordr, na = m
        if Rs not in orbs:
            a, c = parts_of(Rs); orbs[Rs] = orbit_set(a, c, int(info['p']))
        if (frozenset(obj), frozenset(oc_)) in orbs[Rs]:
            win.append({'R': Rs, 'conv': head, 'Delta': Dl, 'NV': NV})
    print('retours exacts à X0 après', NV, 'vaisseaux :', len(win))
    json.dump(win, open('s2_horloge/compteur_NV%d_%d_%d.json' % (NV, D0, ND), 'w'))
    for w in win[:10]: print(w)
