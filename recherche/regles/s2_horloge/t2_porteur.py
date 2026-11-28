"""T2 — tri des machines t2_sym de période n tours (n = 2 par défaut) : le retard de l'horloge au début du tour 2 est-il celui d'un
ralentissement régulier (3d) ? Sinon les vaisseaux PORTENT un bit d'un tour à l'autre (comme t2_sym_doublement504 : 0, −4, 0, −4).
Usage : python3 s2_horloge/t2_porteur.py fichier.json [n] → <fichier>_porteurs.json"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, ship_dir
from fa_lib import parts_of
from tri import virt
H = json.load(open(sys.argv[1])); n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
one = {}
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if w['P'] <= 1200: one.setdefault(w['P'], w)
CL = list(one.values())
def along(v): r, p, tau = v; dd = ship_dir(r); return (p[0] * dd[0] + p[1] * dd[1]) * 8 // (dd[0] ** 2 + dd[1] ** 2) + tau
def lane(v): r, p, tau = v; dd = ship_dir(r); return (r, p[0] * dd[1] - p[1] * dd[0])
def delays(A, G, B, GB, nob, T):
    fv = [virt(q, GB, 0)[0] for q in B]; ds = set()
    for k in range(6):
        v = virt(A[nob + k], G, 0)[0]
        if v is None: return None
        ds |= {(along(u) - along(v)) % T for u in fv if u and lane(u) == lane(v)}
    return ds
out = []; st = collections.Counter(); seen = set()
for h in H:
    if h['P'] % n: continue
    L = h['P'] // n; P0 = h['P0']; T = P0 // 3
    if (L - P0) % 3: continue
    d = (L - P0) // 3
    key = (h['P0'], h['P'], h['o'], h['clock'])
    if key in seen: continue
    seen.add(key)
    w = CL[h['clock']]
    a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    ac, cc = parts_of(w['sit']); B = [list(t) for t in ac]; GB = {tuple(t): 1 for t in cc}
    for _ in range(h['t']): step(B, GB)
    nob = len(A) - 6
    # premier instant où tous les vaisseaux sont libres, au début du tour 1 puis du tour 2 (même décalage)
    for s in range(0, 60):
        D0 = delays(A, G, B, GB, nob, T)
        if D0 is not None: break
        step(A, G); step(B, GB)
    for _ in range(L): step(A, G); step(B, GB)
    D1 = delays(A, G, B, GB, nob, T)
    if D0 is None or D1 is None or len(D0) != 1 or len(D1) != 1: st['illisible'] += 1; continue
    x0, x1 = D0.pop(), D1.pop(); lin = (x0 - 3 * d) % T     # un ralentissement de d par tiers retarde de 3d par tour
    if x1 == lin: st['régulier'] += 1
    else:
        st['PORTEUR'] += 1; out.append({**h, 'd': d, 'retards': [x0, x1], 'attendu': lin})
print(dict(st)); print(collections.Counter((o['P0'], o['P'], o['d'], ((o['retards'][1] - o['attendu'] + T // 2) % T) - T // 2) for o in out for T in [o['P0'] // 3]).most_common(15))
json.dump(out, open(sys.argv[1].replace('.json', '_porteurs.json'), 'w'))
