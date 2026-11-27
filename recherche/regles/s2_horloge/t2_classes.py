"""T2 — suit l'état d'un objet (fourmis 0, 1 et cases à ≤ 5) posé dans une horloge : classe d'orbite (objet seul) à des instants donnés
de chaque tiers, et passages des vaisseaux (distance ≤ 4). Usage : python3 s2_horloge/t2_classes.py fichier.json rang [pas_dans_tiers…]"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from exp_osc import hd
def classes(sit, P, T, offs):
    a, c = parts_of(sit); o0 = (a[0][0], a[0][1]); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    snap = {}; near = []
    for t in range(P + 1):
        if t % T in offs: snap[t] = (tuple(map(tuple, A[:2])), frozenset(q for q in G if hd(q[0] - o0[0], q[1] - o0[1]) <= 5))
        near.append(min(hd(A[k][0] - o0[0], A[k][1] - o0[1]) for k in range(2, len(A))) <= 4)
        step(A, G)
    def orb(st):
        A = [list(x) for x in st[0]]; G = {q: 1 for q in st[1]}; S = set()
        for _ in range(300): S.add((tuple(map(tuple, A)), frozenset(G))); step(A, G)
        return S
    cl = []; lab = []
    for t in sorted(snap):
        for i, S in enumerate(cl):
            if snap[t] in S: lab.append((t, i)); break
        else: cl.append(orb(snap[t])); lab.append((t, len(cl) - 1))
    ev = [t for t in range(1, P) if near[t] and not near[t - 1]]
    return lab, ev
if __name__ == '__main__':
    H = json.load(open(sys.argv[1])); h = H[int(sys.argv[2])]; offs = [int(x) for x in sys.argv[3:]] or [0]
    T = h['P0'] // 3
    lab, ev = classes(h['sit'], h['P'], T, offs)
    print('P0', h['P0'], 'P', h['P'], 'T', T); print('classes', lab); print('passages', ev[:40])
