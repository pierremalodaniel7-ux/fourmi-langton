#!/usr/bin/env python3
"""S1 / R-405 ADDITIONNEUR 2 BITS RÉUTILISABLE (permutation) : vérification complète.
Étage 0 = demi-additionneur R-337 (a0, b0) → s0, c0 ; étage 1 = additionneur complet R-349 posé pour que sa pièce A (pas c !) suive
exactement c0 (a + b + c est symétrique), glissé de D périodes ; le bloc HA0 joue à la place de la pièce A dans l'ordre de R-349.
(1) 16 cas, 2 moteurs ; (2) 2 usages k = 200 : 256 couples, superposition exacte ; (3) 20 usages dans UNE simulation (3 graines,
20 × (1,1,1,1), alterné), 2 moteurs ; (4) certificat fin (cert_fin.py) pour J écarts. Écrit s1_fusion/add2_final.json au fur et à mesure.
Usage : python3 s1_fusion/add2_final.py D J"""
import sys, os, json, random, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from add2_perm import build, T
from circuit import check_multi, check_cases
from cert_fin import certificat_fin
import big; big.patch()   # fourmi_r ignore les fourmis au-delà de 128 : moteur à 512
D, J = int(sys.argv[1]), int(sys.argv[2]); K = 200
OUT = os.path.join(HERE, 'add2_final.json'); res = dict(D=D, k=K)
def save(): json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
ALL = build('A', 0, D); t0 = time.time()
res['pieces'] = [(n, p, v) for n, p, v in ALL.pieces]
res['sorties'] = {o: pos for o, (f, pos) in ALL.outputs.items()}
res['un_usage'] = {''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1')): ALL.sit(e) for e in ALL.cases()}
r = check_cases(ALL, T, engine2=True)
res['seize'] = sum(z[1] for z in r); res['seize_2moteurs'] = all(z[3] for z in r); save()
print('16 cas :', res['seize'], '/16 ; 2 moteurs identiques', res['seize_2moteurs'], '%.0f s' % (time.time() - t0), flush=True)
nb = sum(all(x if i == 0 else x == 2 for i, x in enumerate(check_multi(ALL, [e1, e2], K, T0=T)[:2]))
         for e1, e2 in itertools.product(ALL.cases(), repeat=2))
res['deux_usages'] = nb; save(); print('2 usages :', nb, '/ 256', '%.0f s' % (time.time() - t0), flush=True)
cs = ALL.cases(); one = [e for e in cs if all(e.values())][0]
seqs = {}
for seed in range(3):
    random.seed(seed); seqs['graine %d' % seed] = [random.choice(cs) for _ in range(20)]
seqs['20 x 1111'] = [one] * 20; seqs['alterné'] = [cs[0] if i % 2 else one for i in range(20)]
res['vingt'] = {}
for name, seq in seqs.items():
    sup, good, same, s = check_multi(ALL, seq, K, T0=T, engine2=True)
    res['vingt'][name] = dict(superposition=sup, justes=good, deux_moteurs=same); save()
    print(f'20 usages ({name}) : superposition exacte {sup}, {good}/20 justes, 2 moteurs identiques {same}', '%.0f s' % (time.time() - t0), flush=True)
ok, per, fronts = certificat_fin(ALL, K, 5000, J=J, log=lambda *a: print(*a, flush=True))
res['certificat'] = dict(ok=ok, par_ecart=per, fronts=fronts); save()
print('certificat fin :', ok, '; paires de face', fronts, '%.0f s' % (time.time() - t0), flush=True)
