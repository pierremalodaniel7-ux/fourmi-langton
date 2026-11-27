#!/usr/bin/env python3
"""R-610 Conflits STRUCTURELS : un couple de segments qui se touche (distance 0) quelles que soient les longueurs (D, G).
Exemple trouvé (h1', 00:58) : si un nœud N a la même direction que son grand-parent P (côtés + puis −), dans le repère qui suit la
puissance de P les vaisseaux de N sont immobiles et ceux du parent avancent selon une direction fixe vers P ; un débris de N qui part
dans la direction du parent suit EXACTEMENT le trajet du parent et heurte P. Aucun réglage de D, G ne l'évite : il faut changer les côtés.
Ici : pour des côtés F (miroir par nœud), conflits présents à distance 0 pour 3 tirages aléatoires de (D, G) ; descente sur F.
Usage : python3 struct.py module graine secondes"""
import sys, json, random, time
from modules import nodes
from step import build
from nor import Layout
from diag2 import conflicts2
def keys(nm, F, Dm, Gm):
    return {(x[0], x[1], x[2], x[3]) for x in conflicts2(Layout(build(nm, F), Dmap=Dm, Gmap=Gm)) if x[4] == 0}
def structural(nm, F, draws):
    s = None
    for Dm, Gm in draws:
        k = keys(nm, F, Dm, Gm); s = k if s is None else s & k
    return s
if __name__ == '__main__':
    nm, seed, secs = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    rnd = random.Random(seed); names = [n.name for n in nodes(build(nm, None))]
    draws = [({n: rnd.randint(8, 300) for n in names}, {n: rnd.randint(8, 60) for n in names}) for _ in range(3)]
    F = {n: rnd.randint(0, 1) for n in names}; s = len(structural(nm, F, draws)); t0 = time.time()
    log = open(f'data/struct_{nm}_{seed}.log', 'a'); print('départ', s, file=log, flush=True)
    while s > 0 and time.time() - t0 < secs:
        F2 = dict(F)
        for _ in range(rnd.choice((1, 1, 2))): n = rnd.choice(names); F2[n] = 1 - F2[n]
        s2 = len(structural(nm, F2, draws))
        if s2 <= s:
            if s2 < s: print(f'{time.time()-t0:.0f}s structurels {s2}', file=log, flush=True)
            F, s = F2, s2; json.dump(dict(F=F, structurels=s), open(f'data/struct_{nm}_{seed}.json', 'w'))
    print('fin', s, file=log, flush=True)
