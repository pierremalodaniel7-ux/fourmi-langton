"""S2 — pour chaque conversion « traversante » (angle 0) des bascules R → R' → R (bascule_hexa.py, R-340) : refait le tir exactement
comme miroir.c (D = 40, T = 720), et mesure le décalage espace-temps du vaisseau sortant par rapport au vaisseau non perturbé.
Sortie : data/shift_<étape>.json  {clé: [voie_décalage, dt, objet_restant, qui_sort]}"""
import sys, json, re
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import rot, step, ship_dir
from fa_lib import parts_of, lotdump
from demi_add_k import fmt
from tri import virt
from exp_osc import hd
D, TT = 40, 720
def kv(s): return dict(re.findall(r'(\w+)=(\S+)', s))
def ctrunc(a, b): return int(a / b)
def setup(Rs, info):
    a, c = parts_of(Rs); p = int(info['p'])
    A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    ocx = ctrunc(sum(t[0] for t in a), len(a)); ocy = ctrunc(sum(t[1] for t in a), len(a))
    for _ in range(int(info['ph'])): step(A, G)
    r, l, ordr = int(info['r']), int(info['l']), int(info['ord'])
    d = ship_dir(r); e = rot((1, 0), r)
    S = (ocx - D * d[0] + l * e[0], ocy - D * d[1] + l * e[1])
    sa = [S[0], S[1], (4 + r) % 6]; cell = (S[0] + e[0], S[1] + e[1])
    ants = [sa] + A if ordr == 1 else A + [sa]
    return ants, list(G) + [cell], (r, S, 0), (ocx, ocy), ordr, len(A)
if __name__ == '__main__':
    which = sys.argv[1]   # s1 ou s2
    K = json.load(open('data/bascules_opp.json'))
    keys = {}
    for f in K:
        Rs, s = (f['R'], f['s1']) if which == 's1' else (f['R2'], f['s2'])
        if which == 's2' and len(sys.argv) > 2:
            pass
        keys[(Rs, s.split(' centre2')[0])] = (Rs, kv(s))
    keys = list(keys.items())
    if len(sys.argv) > 2:   # filtre : n'garder que les R' de la liste
        keep = set(json.load(open(sys.argv[2]))); keys = [k for k in keys if k[0][0] in keep]
    print(which, 'clés :', len(keys), flush=True)
    jobs = []; meta = []
    for (k, (Rs, info)) in keys:
        ants, cells, V0, oc, ordr, na = setup(Rs, info)
        jobs.append(fmt(ants, cells)); meta.append((k, V0, oc, ordr, na))
    out = {}
    B = 4000
    for i in range(0, len(jobs), B):
        res = lotdump(jobs[i:i + B], TT)
        for (k, V0, oc, ordr, na), (ants, cells) in zip(meta[i:i + B], res):
            # vaisseau sortant = fourmi loin de l'objet
            far = [q for q, a in enumerate(ants) if hd(a[0] - oc[0], a[1] - oc[1]) > 30]
            if len(far) != 1: continue
            q = far[0]; a = ants[q]
            v, near = virt(tuple(a), cells, TT)
            if v is None: continue
            r, S, _ = V0; d = ship_dir(r)
            # décalage : v vs V0 (même direction) ; écart de position = lat * e⊥ + long ; on exprime en (voie, dt)
            from demi_add_k import lane
            from fa_lib import along
            dl = lane(*v[1], r) - lane(*S, r)
            # dt : avance le long de la route (along avance de 2 par période)
            da = along(*v[1], r) - along(*S, r)
            dt = 4 * da + (v[2] - 0)     # pas d'avance (≈) ; exact si dl = 0
            obj_ants = [tuple(x) for j, x in enumerate(ants) if j != q]
            obj_cells = sorted(c for c in cells if hd(c[0] - a[0], c[1] - a[1]) > 2)
            who = 'v' if ((ordr == 1 and q == 0) or (ordr == 0 and q == na)) else 'o'
            out[k[0] + ' ## ' + k[1]] = [dl, da, v[2], who, fmt(obj_ants, obj_cells)]
        print(i + B, len(out), flush=True)
    json.dump(out, open('data/shift_%s.json' % which, 'w'))
    import collections
    print(collections.Counter((x[0], x[1], x[2]) for x in out.values()).most_common(15))
