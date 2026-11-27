"""T2 — retard de chaque vaisseau d'horloge (fourmis 6-11 d'une machine t2_sym) par rapport à l'horloge seule : à chaque instant où le
vaisseau est libre, (avance de la fourmi libre de même droite − avance du vaisseau) ramené modulo T dans ]−T/2, T/2].
Usage : python3 s2_horloge/t2_retard.py fichier.json rang [pas]"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, ship_dir
from fa_lib import parts_of
from tri import virt
H = json.load(open(sys.argv[1])); h = H[int(sys.argv[2])]; P0 = h['P0']; T = P0 // 3; every = int(sys.argv[3]) if len(sys.argv) > 3 else 6
one = {}
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if w['P'] <= 1200: one.setdefault(w['P'], w)
w = list(one.values())[h['clock']]
def along(v): r, p, tau = v; d = ship_dir(r); return (p[0] * d[0] + p[1] * d[1]) * 8 // (d[0] ** 2 + d[1] ** 2) + tau
def lane(v): r, p, tau = v; d = ship_dir(r); return (r, p[0] * d[1] - p[1] * d[0])
a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
ac, cc = parts_of(w['sit']); B = [list(t) for t in ac]; GB = {tuple(t): 1 for t in cc}
for _ in range(h['t']): step(B, GB)
n0 = len(A) - 6; seq = collections.defaultdict(list)
for t in range(h['P']):
    if t % every == 0:
        fv = [virt(q, GB, 0)[0] for q in B]
        for k in range(6):
            v = virt(A[n0 + k], G, 0)[0]
            if v is None: continue
            ds = [((along(u) - along(v)) % T + T // 2) % T - T // 2 for u in fv if u and lane(u) == lane(v)]
            if ds: seq[k].append((t, min(ds, key=abs)))
    step(A, G); step(B, GB)
for k in range(6):
    s = seq[k]; out = []
    for t, d in s:
        if not out or out[-1][1] != d: out.append((t, d))
    print('vaisseau', k, ': (instant, retard) aux changements :', out)
