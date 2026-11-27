"""T2 — pour une machine t2_sym (horloge + 3 copies d'objet), retard de l'horloge au début de chaque « tour » (tour = P/n pas) par
rapport à l'horloge seule, modulo T : si les tours ne sont pas tous pareils (retard − k·retard moyen ≠ constante), le VAISSEAU porte
une information d'un tour à l'autre. Usage : python3 s2_horloge/t2_tours.py fichier.json n d [max]  (classe (n, d) de t2_sym)"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, ship_dir
from fa_lib import parts_of
from tri import virt
H = json.load(open(sys.argv[1])); n, d = int(sys.argv[2]), int(sys.argv[3]); mx = int(sys.argv[4]) if len(sys.argv) > 4 else 5
one = {}
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if w['P'] <= 1200: one.setdefault(w['P'], w)
CL = list(one.values())
def along(v): r, p, tau = v; dd = ship_dir(r); return (p[0] * dd[0] + p[1] * dd[1]) * 8 // (dd[0] ** 2 + dd[1] ** 2) + tau
def lane(v): r, p, tau = v; dd = ship_dir(r); return (r, p[0] * dd[1] - p[1] * dd[0])
sel = [h for h in H if h['P'] % n == 0 and h['P'] // n - h['P0'] == 3 * d][:mx]
for h in sel:
    P0 = h['P0']; T = P0 // 3; L = h['P'] // n; w = CL[h['clock']]
    a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    ac, cc = parts_of(w['sit']); B = [list(t) for t in ac]; GB = {tuple(t): 1 for t in cc}
    for _ in range(h['t']): step(B, GB)
    nob = len(A) - 6; out = []
    for t in range(h['P']):
        if t % L == 0 or t % L == L // 2:
            fv = [virt(q, GB, 0)[0] for q in B]; ds = []
            for k in range(6):
                v = virt(A[nob + k], G, 0)[0]
                if v is None: continue
                ds += [((along(u) - along(v)) % T) for u in fv if u and lane(u) == lane(v)]
            out.append((t, sorted(set(ds))))
        step(A, G); step(B, GB)
    print('P0', P0, 'P', h['P'], 'tour', L, 'objet', h['o'], ':', [(t, x) for t, x in out])
