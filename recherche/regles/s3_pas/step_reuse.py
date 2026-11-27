#!/usr/bin/env python3
"""R-617 Le pas complet RÉUTILISABLE : germe à 8 modules (h1' = h1R_param_OK.json), translations de step.py (graine 1, BOX 6000,
voies opposées vérifiées entre modules) ; certificat sans mémoire (cert3) ; puis usages répétés au même endroit (step.multi_check).
Usage : python3 step_reuse.py"""
import json, random, sys, time
from step import Step, load_params, multi_check
from cert3 import certificate3
P = load_params(); P['h1'] = json.load(open('h1R_param_OK.json'))
off = {'h0': (0, 0), 'x': (-3799, 3325), 'y': (-4967, -1821), 'c00': (-4069, 2117), 'c10': (1364, 1737), 'c01': (4675, 219),
       'c11': (-2561, -4463), 'h1': (3116, 4523)}
S = Step(P, off); t0 = time.time(); out = dict(translations=off)
ok, delta, info = certificate3(S, log=lambda s: print(s, flush=True)); D = delta + (-delta) % 8
out.update(certificat=ok, delta=D, fenetre=info['span'], rayon=info['R'], voies_opposees=info['opposees']); print(f'({time.time()-t0:.0f} s)', flush=True)
json.dump(out, open('step_reuse_res.json', 'w'), ensure_ascii=False, indent=1)
if ok:
    envs = S.cases(); out['usages'] = []
    for g, (n, e2) in enumerate(((3, True), (10, False), (10, False))):
        rnd = random.Random(g); seq = [rnd.choice(envs) for _ in range(n)]
        r = multi_check(S, seq, D, engine2=e2); r['graine'] = g; out['usages'].append(r); print('usages', r, flush=True)
        json.dump(out, open('step_reuse_res.json', 'w'), ensure_ascii=False, indent=1)
