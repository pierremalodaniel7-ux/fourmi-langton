"""T2 — tri des pixels en aval d'une porte (t2_pixel_aval.py) : on garde les machines où le pixel est synchronisé (période = celle de la
machine de base) et on regarde QUI l'écrit : pour chaque passage d'un vaisseau sur le pixel (droite l), on remonte sa droite jusqu'aux
portes de la machine de base qu'il a traversées tout droit ; si l'une de ces portes fait TOURNER, à d'autres passages, des vaisseaux de
cette même droite, l'écriture du pixel dépend de la décision de la porte (le pixel est « piloté » par la porte).
Usage : python3 s2_horloge/t2_pixel_tri.py hits.json base.json [max]"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from fa_lib import parts_of
from exp_osc import hd
from t2_portes import analyse, segments
H = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2])); mx = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
H = [h for h in H if h['P'] == h['P0']]
print(len(H), 'pixels synchronisés (période = machine de base)')
base_cache = {}
out = []; st = collections.Counter()
for h in H[:mx]:
    n = h['n']; P = h['P']
    if n not in base_cache: base_cache[n] = analyse(B[n]['sit'], P)
    gates, res = base_cache[n]
    a, c = parts_of(h['sit']); pc = (sum(x for x, y, _ in a[:2]) // 2, sum(y for x, y, _ in a[:2]) // 2)
    pos, segs = segments(h['sit'], P, 2)
    # passages sur le pixel : fourmis 2.. (machine) à ≤ 3 du centre du pixel
    writers = []
    for k in range(2, len(segs)):
        for l, t0, t1 in segs[k]:
            ts = [t for t in range(t0, t1 + 1) if hd(pos[t][k][0] - pc[0], pos[t][k][1] - pc[1]) <= 3]
            if ts and ts[0] < P: writers.append((ts[0], k - 2, l, t0))
    # droites variables de la base : (droite, porte) avec issues T et D
    var = {(r['lane'], r['gate']) for r in res if len({x[2] for x in r['seq']}) == 2}
    piloted = []
    for tw, k, l, t0 in writers:
        # portes traversées tout droit par k sur la droite l entre t0 et tw, et variables sur cette droite
        for (lane, gi) in var:
            if lane != l: continue
            gp = gates[gi]['p']
            if any(hd(pos[t][k + 2][0] - gp[0], pos[t][k + 2][1] - gp[1]) <= 4 for t in range(t0, tw)): piloted.append((tw, k, l, gi))
    st[(len(writers), len(piloted) > 0)] += 1
    if piloted: out.append({**h, 'pixel': pc, 'ecrivains': writers, 'pilotes': piloted})
print('(nb de passages sur le pixel, piloté par une porte variable) :', sorted(st.items()))
json.dump(out, open(sys.argv[1].replace('.json', '_pilotes.json'), 'w'))
for o in out[:8]: print(o['n'], 'P', o['P'], 'pixel', o['pixel'], 'écrivains', [(w[0], w[1], w[2]) for w in o['ecrivains']], 'pilotés', o['pilotes'])
