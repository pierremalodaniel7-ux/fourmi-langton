#!/usr/bin/env python3
"""R-702 Vérification d'un démultiplexeur 2 → 4 : 4 cas (2 moteurs), N usages au MÊME endroit dans UNE simulation (superposition
exacte, 2 moteurs), certificat « tout nombre d'usages » (méthode de R-338, circuit.certificat).
Usage : python3 demux_verif.py [rang dans data/demux_tries.json] [N] -> demux_retenu.json (dans s4_ecran/)"""
import sys, json, random, time
from traj import *
import circuit
IDX = int(sys.argv[1]) if len(sys.argv) > 1 else 0; N = int(sys.argv[2]) if len(sys.argv) > 2 else 20
K = 200                      # périodes entre deux usages
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
def load(idx=IDX, f='/data/demux_tries.json'):
    return json.load(open(HERE + f))[idx]
def pieces(B):
    """pièces dans l'ordre de jeu, au temps 0 : (nom, pièce, variable ou None)"""
    return [(n, piece_at(tuple(B['T'][n]), 0), n if n in ('a1', 'a0') else None) for n in B['order']]
def use_sit(B, seq, k=K):
    """seq = liste d'adresses (a1, a0) ; usage u reculé de u·k périodes"""
    P = []
    for u, (a1, a0) in enumerate(seq):
        for n, p, v in pieces(B):
            if v is None or {'a1': a1, 'a0': a0}[v]: P.append(circuit.back(p, u * k))
    return fmt([p[0] for p in P], [c for p in P for c in p[1]])
def expected(B, seq, k=K):
    out = []
    for u, c in enumerate(seq): out += [movT(tuple(t), (0, 0), 8 * k * u) for t in B['exp'][str(c)]]
    return sorted(norm(t) for t in out)
def run_both(s, T, engine2=True):
    (a, c), = lotdump([s], T)[:1] if False else [lotdump([s], T)[0]]
    same = None
    if engine2:
        pa, pc = pyrun(s, T); same = sorted(pa) == sorted(map(tuple, a)) and sorted(pc) == sorted(map(tuple, c))
    return a, c, same
def outputs_read(B, labs, seq, k=K):
    """adresse lue pour chaque usage : la sortie O_j (choisie par le tri) présente"""
    S = set(labs); res = []
    O = {c: tuple(o) for c, o in zip(CASES, B['outs4'])}
    for u in range(len(seq)):
        hit = [c for c in CASES if norm(movT(O[c], (0, 0), 8 * k * u)) in S]
        res.append(hit[0] if len(hit) == 1 else None)
    return res
if __name__ == '__main__':
    B = load(); t0 = time.time(); rep = {'source': 'data/demux_tries.json', 'rang': IDX}
    print('ordre de jeu', B['order'], 'instants des chocs', B['times'], 'sorties', [to_label(tuple(o)) for o in B['outs4']])
    # 1. quatre cas
    ok4 = 0; same4 = 0
    for c in CASES:
        s = use_sit(B, [c]); T = B['Tend']
        a, cc, same = run_both(s, T); d = decode(a, cc)
        labs = sorted(of_label(lab_of(z, T)) for z in d) if d else None
        ok4 += labs == expected(B, [c]) and outputs_read(B, labs, [c]) == [c]; same4 += bool(same)
    print('4 cas : justes', ok4, '/ 4 ; 2 moteurs identiques', same4, '/ 4'); rep['quatre_cas'] = f'{ok4}/4'; rep['quatre_cas_2_moteurs'] = f'{same4}/4'
    # 2. N usages au même endroit
    rep['usages'] = []
    for seed in (0, 1, 2, 'tous'):
        if seed == 'tous': seq = [CASES[u % 4] for u in range(N)]
        else:
            random.seed(seed); seq = [random.choice(CASES) for _ in range(N)]
        s = use_sit(B, seq); T = B['Tend'] + 8 * K * (N - 1)
        a, cc, same = run_both(s, T); d = decode(a, cc)
        labs = sorted(of_label(lab_of(z, T)) for z in d) if d else None
        sup = labs == expected(B, seq)
        lus = outputs_read(B, labs or [], seq); just = sum(1 for x, y in zip(lus, seq) if x == y)
        print(f'graine {seed} : {N} usages, {len(a)} fourmis, t = {T} : superposition exacte {sup}, adresses justes {just}/{N}, 2 moteurs {same}')
        rep['usages'].append({'graine': seed, 'adresses': seq, 'justes': f'{just}/{N}', 'superposition': sup, 'deux_moteurs': same, 'fourmis': len(a), 'T': T})
    # 3. certificat
    C = circuit.Circuit(pieces(B))
    worst, per, fronts = circuit.certificat(C, K, B['Tend'], J=12, log=lambda *x: None)
    print('certificat : distance min entre fourmis de 2 usages (écarts 1..12) :', per, '; paires de face :', len(fronts))
    rep['certificat'] = {'distances': per, 'paires_de_face': len(fronts)}
    rep['B'] = B; rep['duree_s'] = round(time.time() - t0)
    json.dump(rep, open(HERE + '/demux_retenu.json', 'w'), ensure_ascii=False, indent=1, default=list)
    print('durée', rep['duree_s'], 's')
