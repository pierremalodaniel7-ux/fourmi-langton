#!/usr/bin/env python3
"""S1 / R-403 Vérification complète d'une fusion à 2 constants (fusion3_*.json) :
3 cas (2 moteurs) ; 2 usages 9/9 ; 20 usages au hasard dans UNE simulation (3 graines, 2 moteurs) + 20 × x, 20 × y, alterné ;
certificat « tout nombre d'usages » (circuit.certificat, J écarts). Résultat ajouté à s1_fusion/fusion_verif.json.
Usage : python3 s1_fusion/fusion_final.py <fichier fusion3_*.json> <indice> [J]"""
import sys, os, json, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from fusion_reuse import Excl
from circuit import check_multi, check_cases, certificat
def load(z):
    C = Excl([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
    C.outputs = {'O': (lambda e: e['x'] | e['y'], [tuple(z['O'])])}
    return C
if __name__ == '__main__':
    f, i = sys.argv[1], int(sys.argv[2]); J = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    z = json.load(open(f))[i]; C = load(z)
    r = check_cases(C, 4000); print('3 cas :', sum(x[1] for x in r), '/3 ; 2 moteurs', all(x[3] for x in r), flush=True)
    n2 = sum(1 for e1, e2 in itertools.product(C.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(C, [e1, e2], 200)))
    print('2 usages :', n2, '/9', flush=True)
    res = {}
    seqs = {}
    for seed in range(3):
        random.seed(seed); seqs['hasard%d' % seed] = [random.choice(C.cases()) for _ in range(20)]
    seqs['20x'] = [{'x': 1, 'y': 0}] * 20; seqs['20y'] = [{'x': 0, 'y': 1}] * 20
    seqs['alterne'] = [{'x': 1, 'y': 0} if u % 2 else {'x': 0, 'y': 1} for u in range(20)]
    for name, seq in seqs.items():
        sup, good, same, s = check_multi(C, seq, 200, engine2=True)
        print(f'20 usages ({name}) : superposition exacte {sup}, {good}/20 justes, 2 moteurs identiques {same}', flush=True)
        res[name] = dict(suite=[(e['x'], e['y']) for e in seq], sup=sup, justes=good, deux_moteurs=same)
    worst, per, fronts = certificat(C, 200, 4000, J=J, log=lambda *a: None)
    print('certificat : distance minimale', worst, 'par écart', per, '; paires de face', fronts, flush=True)
    out = dict(fichier=os.path.basename(f), indice=i, O=z['O'], pieces=z['pieces'], trois_cas=sum(x[1] for x in r), deux_moteurs=all(x[3] for x in r),
               deux_usages=n2, vingt=res, certificat=dict(distance_min=worst, par_ecart=per, fronts=fronts),
               un_usage={str((e['x'], e['y'])): C.sit(e) for e in C.cases()})
    p = os.path.join(HERE, 'fusion_verif.json'); L = json.load(open(p)) if os.path.exists(p) else []
    L.append(out); json.dump(L, open(p, 'w'), ensure_ascii=False, indent=1)
