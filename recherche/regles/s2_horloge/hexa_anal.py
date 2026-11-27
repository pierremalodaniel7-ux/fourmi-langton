"""S2 R-512 — analyse des hexagrammes cycliques avec interaction : événements (fourmis non libres groupées), mélange A/B, directions.
Usage : python3 s2_horloge/hexa_anal.py [n]"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from tri import virt
from exp_osc import hd
from outils_r import lot
def events(sit, P):
    a, c = parts_of(sit); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    ev = []; cur = None; xs = []; ys = []
    for t in range(P):
        busy = [i for i, q in enumerate(A) if virt(q, G, 0)[0] is None]
        # groupes : fourmis non libres à ≤ 6 l'une de l'autre
        grp = []
        for i in busy:
            for g in grp:
                if any(hd(A[i][0] - A[k][0], A[i][1] - A[k][1]) <= 8 for k in g): g.add(i); break
            else: grp.append({i})
        ev.append([frozenset(g) for g in grp])
        xs += [q[0] for q in A]; ys += [q[1] for q in A]
        step(A, G)
    kinds = collections.Counter()
    for t in range(P):
        for g in ev[t]:
            if t and g in ev[t - 1]: continue
            na = sum(1 for i in g if i < 6); nb = len(g) - na
            kinds[(na, nb)] += 1
    return kinds, (max(xs) - min(xs), max(ys) - min(ys))
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    H = [h for h in json.load(open('s2_horloge/hexagramme_0.json')) if h['diff'] > 0]
    seen = {}; 
    for h in H: seen.setdefault((h['horloge'], h['P']), h)
    U = sorted(seen.values(), key=lambda h: (h['P0'], h['P']))
    print(len(H), 'hexagrammes cycliques avec interaction ;', len(U), 'distincts (horloge, période)')
    stats = collections.Counter(); keep = []
    for h in U:
        k, box = events(h['sit'], h['P'])
        mixte = sum(v for (na, nb), v in k.items() if na and nb)
        big = box[0] > 20 and box[1] > 20
        stats[(big, mixte > 0)] += 1
        if big and mixte: keep.append({**h, 'evenements': {'%d+%d' % kk: v for kk, v in k.items()}, 'boite': box})
    print('(étendu, chocs A-B) :', dict(stats))
    keep.sort(key=lambda h: h['P'])
    for h in keep[:n]: print(h['P0'], '->', h['P'], 's', h['s'], 'boite', h['boite'], h['evenements'])
    json.dump(keep, open('s2_horloge/hexagramme_retenus.json', 'w'))
