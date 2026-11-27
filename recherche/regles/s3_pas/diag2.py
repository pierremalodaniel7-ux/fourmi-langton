"""R-610 Diagnostic géométrique EXACT par cas (sans simulation) : chaque segment de ligne d'univers reçoit le MASQUE des cas où il
existe vraiment (modèle logique des portes : la 1re entrée présente dévie la puissance). Un couple de segments n'est un conflit que
s'ils passent à < thr l'un de l'autre ET coexistent dans au moins un cas. (diag.py comptait aussi des couples qui ne coexistent jamais,
p. ex. les littéraux x et ~x.) Sert à guider la recherche ; la vérification reste la simulation complète (2 moteurs)."""
import itertools
from collections import defaultdict
from nor import lit
from diag import pmin, INF
def allnodes(n):
    yield n
    for _, it in n.inputs:
        if not isinstance(it, str): yield from allnodes(it)
def segments2(L):
    root = L.root; NN = {n.name: n for n in allnodes(root)}
    G = defaultdict(list)
    for g in L.gates: G[g[0]].append(g)
    W = {nm: w for nm, k, w in L.ships}
    envs = L.cases(); nc = len(envs)
    val = {nm: 0 for nm in NN}; first = {nm: 0 for nm in NN}   # masques : valeur du nœud ; first[nm][i] = masque « 1re entrée présente = i »
    first = {nm: defaultdict(int) for nm in NN}; pres = {}
    for b, e in enumerate(envs):
        bit = 1 << b
        def ev(n):
            f = None
            for i, (_, it) in enumerate(n.inputs):
                p = lit(e, it) if isinstance(it, str) else ev(it)
                if p and f is None: f = i
            first[n.name][f] |= bit
            v = f is None
            if v: val[n.name] |= bit
            return v
        ev(root)
        for g in L.gates:
            pn = g[5]
            if '@' in pn and lit(e, pn.split('@')[0]): pres[pn] = pres.get(pn, 0) | bit
    full = (1 << nc) - 1; segs = []
    pgate = {g[5]: g for g in L.gates}
    for nm, n in NN.items():
        gs = G[nm]; ts = [g[2] for g in gs]
        alive = full; t0 = -INF
        tend = pgate[nm][2] if nm in pgate else INF
        for i, g in enumerate(gs):
            segs.append((nm, W[nm], t0, ts[i], alive, 'K'))
            segs.append((nm, g[4], ts[i], INF, first[nm][i], 'K dévié'))
            alive &= ~first[nm][i] & full; t0 = ts[i]
        segs.append((nm, W[nm], t0, tend, alive, 'K'))
    for nm, n in NN.items():
        for i, g in enumerate(G[nm]):
            pn, tg = g[5], g[2]
            m = pres.get(pn, 0) if '@' in pn else val[pn]
            if '@' in pn: segs.append((pn, W[pn], -INF, tg, m, 'lit'))
            segs.append((pn, g[3], tg, INF, m & first[nm][i], 'dévié'))
            later = 0
            for j in range(i): later |= first[nm][j]
            segs.append((pn, W[pn], tg, INF, m & later, 'droit'))
    return [s for s in segs if s[4]]
def conflicts2(L, thr=7, guard=80):
    S = segments2(L); out = []
    gt = {}
    for node, side, tg, oA, oB, pn in L.gates: gt[frozenset((node, pn))] = tg
    for i in range(len(S)):
        a = S[i]
        for j in range(i):
            b = S[j]
            if a[0] == b[0] or not (a[4] & b[4]): continue
            m, t = pmin(a[1], a[2], a[3], b[1], b[2], b[3], thr)
            if m < thr:
                tg = gt.get(frozenset((a[0], b[0])))
                if tg is not None and abs(t - tg) <= guard: continue
                out.append((a[0], a[5], b[0], b[5], m, t))
    return out
