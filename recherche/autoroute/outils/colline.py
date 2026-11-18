#!/usr/bin/env python3
"""colline.py N GRAINE MINUTES : montée de colline sur les boîtes N×N (convention de T(n) : fourmi 0,0 cap H,
cases (i mod N, -(i div N)), y vers le bas). Score = pas certifié (fourmi -cert). À chaque itération : toutes les
inversions d'une case en un lot ; on prend la meilleure si elle améliore, sinon perturbation (inverser 3 à 6 cases
de la meilleure) ; NONCERT (pas d'autoroute certifiée avant T) est signalé à part. Sortie : lignes « t score masque »."""
import sys, re, random, subprocess, time, os
N, seed, minutes = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
GRAINE = sys.argv[4] if len(sys.argv) > 4 else ""   # « n:masque » : record d'une boîte plus petite, recopié au coin
F = os.path.dirname(os.path.abspath(__file__)) + '/../../../src/fourmi'
random.seed(seed); T = '100000000'
def sit(m): return 'RL|0,0,H|' + ';'.join(f'{i%N},{-(i//N)}' for i in range(N*N) if m >> i & 1) + '\n'
def evalue(ms):
    o = subprocess.run([F, '-T', T, '-cert', '-lot'], input=''.join(sit(m) for m in ms), capture_output=True, text=True).stdout.splitlines()
    r = []
    for l in o:
        mm = re.search(r'\|CERT (\d+)', l); r.append(int(mm.group(1)) if mm else -1)
    return r
cur = random.getrandbits(N*N)
if GRAINE:
    n0, m0 = map(int, GRAINE.split(':')); cur = 0
    for i in range(n0*n0):
        if m0 >> i & 1: cur |= 1 << ((i // n0) * N + i % n0)
best_s = evalue([cur])[0]; best = cur; cs = best_s; t0 = time.time()
print(f'0 {best_s} {best}', flush=True)
while time.time() - t0 < 60*minutes:
    nb = [cur ^ (1 << i) for i in range(N*N)]; sc = evalue(nb)
    for m, s in zip(nb, sc):
        if s < 0: print(f'NONCERT {m}', flush=True)
    i = max(range(len(sc)), key=lambda k: sc[k])
    if sc[i] > cs: cur, cs = nb[i], sc[i]
    else:   # bloqué : marche aléatoire (une inversion au hasard parmi les 5 meilleures), parfois retour au meilleur
        if random.random() < 0.2:
            cur = best
            for _ in range(random.randint(2, 5)): cur ^= 1 << random.randrange(N*N)
            cs = evalue([cur])[0]
        else:
            top = sorted(range(len(sc)), key=lambda k: -sc[k])[:5]; i = random.choice(top); cur, cs = nb[i], sc[i]
    if cs > best_s: best_s, best = cs, cur; print(f'{int(time.time()-t0)} {best_s} {best}', flush=True)
print(f'FIN {best_s} {best}', flush=True)
