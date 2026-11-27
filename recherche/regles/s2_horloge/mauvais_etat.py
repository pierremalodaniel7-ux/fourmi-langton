"""S2 R-510 — que fait le vaisseau « mise à 1 » de R-341 quand la bascule est DÉJÀ à 1 (R') ? (et la remise à 0 sur M ?)
On prend, dans la machine R-502 n° 0, le vaisseau qui écrit (instantané 120 pas avant l'écriture), on l'isole avec le pixel, et on remplace
le pixel par l'autre état à toutes ses phases (période propre de l'objet). Simulation hx.py 900 pas, bilan : vaisseaux sortants
(direction, voie, retard par rapport au vaisseau libre), objet restant (M, R', autre). Usage : python3 s2_horloge/mauvais_etat.py"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, PHASES, ship_dir
from fa_lib import parts_of
from exp_osc import hd
import anti_pixel as ap
W = ap.W; P = W['P']
a, c = parts_of(W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
M = ap.local(A, G, (0, 1)); O_M = ap.orbit(*M)
st = []; snaps = []
for t in range(P):
    st.append(ap.norm(*ap.local(A, G, (0, 1))) in O_M); snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
ev = [t for t in range(1, P) if st[t] != st[t - 1]]
def obj_period(o):
    B = [list(q) for q in o[0]]; g = {q: 1 for q in o[1]}; s0 = ap.norm(*ap.local(B, g, range(2)))
    for n in range(1, 400):
        step(B, g)
        if ap.norm(*ap.local(B, g, range(2))) == s0: return n
def snapshot_ship(t0):
    """le vaisseau libre le plus proche du pixel à l'instant t0 : (fourmi, cases)"""
    Aq, Gq = snaps[t0]; px = Aq[0]
    best = min(range(2, len(Aq)), key=lambda i: hd(Aq[i][0] - px[0], Aq[i][1] - px[1]))
    q = Aq[best]; cl = [p for p in Gq if hd(p[0] - q[0], p[1] - q[1]) <= 2]
    return q, cl
def bilan(ants, g):
    sh = []
    for x, y, h in ants:
        cl = frozenset((cx - x, cy - y) for cx, cy in g if hd(cx - x, cy - y) <= 2)
        sh.append(PHASES.get((h, cl)))
    return sh
if __name__ == '__main__':
    print('événements du pixel (changement M <-> non M) :', ev[:8])
    # 1er passage 0 -> 1 : ev[0] ; on prend le vaisseau 120 pas avant
    res = {}
    for nom, tw, autre_t in (('S sur R\'', ev[0], ev[0] + 150), ('R sur M', min(t for t in ev if t > ev[0] + 300), 5)):
        t0 = max(tw - 120, 0); q, cl = snapshot_ship(t0)
        # autre état : instantané du pixel à un instant où il est dans l'autre état
        Ao, Go = snaps[autre_t % P]; o = ap.local([list(x) for x in Ao], Go, (0, 1)); n = obj_period(o)
        # référence : vaisseau libre seul (même durée)
        S = [list(q)]; gs = {p: 1 for p in cl}
        for _ in range(900): step(S, gs)
        out = collections.Counter()
        for ph in range(n):
            B = [list(x) for x in o[0]]; g = {p: 1 for p in o[1]}
            for _ in range(ph): step(B, g)
            ants = B + [list(q)]; g.update({p: 1 for p in cl})
            for _ in range(900): step(ants, g)
            sh = bilan(ants, g); shp = ants[2]
            obj = ap.norm(*ap.local(ants, g, (0, 1)))
            kind = 'M' if obj in O_M else ('pixel parti' if sh[0] and sh[1] else '?')
            d = hd(shp[0] - S[0][0], shp[1] - S[0][1])
            out[(tuple(sh), 'objet ' + kind, 'écart au vaisseau libre %d' % d, 'cases', len(g))] += 1
        print(nom, ': période propre de l\'objet', n, 'vaisseau pris à t =', t0)
        for k, v in out.most_common(3): print('   ', v, k)
        print('    total :', collections.Counter(k[1] for k in out.elements()))
