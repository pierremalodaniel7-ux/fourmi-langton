#!/usr/bin/env python3
"""Génère des situations pour ./fourmi -lot (une par ligne : REGLE|fourmis|cases).
Exemples :
  python3 outils/gen.py --nb 100000 --fourmis 3 --rayon 6                 # 3 fourmis RL au hasard
  python3 outils/gen.py --nb 50000 --fourmis 2-5 --cases 0-4 --rc 3       # + 0 à 4 cases noires
  python3 outils/gen.py --nb 20000 --regle rand4:5 --fourmis 1            # règles carrées à 5 couleurs au hasard
  python3 outils/gen.py --nb 20000 --fourmis 4 --sym 4                    # placements de symétrie d'ordre 4
  python3 outils/gen.py --nb 5000 --fourmis 6 --droite 2 --pas 3          # fourmis sur y = 2x, espacement 3
Options : --regle MOT | rand4:q | rand6:q | rand4:q-q2 ; --fourmis n ou a-b ; --rayon R ; --cases k ou a-b ;
          --rc rayon des cases ; --sym 0|2|4 ; --droite a --pas e ; --graine s ; --classes egales (R-09/R-14)"""
import argparse, random

ap = argparse.ArgumentParser()
ap.add_argument("--nb", type=int, default=1000); ap.add_argument("--regle", default="RL")
ap.add_argument("--fourmis", default="2"); ap.add_argument("--rayon", type=int, default=6)
ap.add_argument("--cases", default="0"); ap.add_argument("--rc", type=int, default=4)
ap.add_argument("--sym", type=int, default=0); ap.add_argument("--droite", type=int)
ap.add_argument("--pas", type=int, default=1); ap.add_argument("--graine", type=int, default=1)
ap.add_argument("--classes", choices=["egales"], help="garder seulement autant de fourmis dans chaque classe de parité (carré L/R)")
a = ap.parse_args(); rnd = random.Random(a.graine)

def intervalle(s): lo, _, hi = s.partition("-"); return int(lo), int(hi or lo)
def regle():
    if not a.regle.startswith("rand"): return a.regle
    m, q = a.regle[4], intervalle(a.regle.split(":")[1]); q = rnd.randint(*q)
    if m == "4":
        while True:
            w = "".join(rnd.choice("LRNU") for _ in range(q))
            if any(c in "LR" for c in w): return w
    jet = ["N", "R1", "R2", "U", "L2", "L1"]
    return "H:" + "".join(rnd.choice(jet) for _ in range(q))
def rot(x, y, d, k):                      # quart de tour (carré) autour de l'origine, k fois
    for _ in range(k): x, y, d = -y, x, (d + 1) % 4
    return x, y, d
CAP = "HDBG"
vus = set(); faits = 0; essais = 0
while faits < a.nb and essais < 50 * a.nb:
    essais += 1; r = regle(); hexa = r.startswith("H:"); M = 6 if hexa else 4
    n = rnd.randint(*intervalle(a.fourmis)); k = rnd.randint(*intervalle(a.cases))
    if a.droite is not None:
        x0 = rnd.randint(-2, 2)
        F = [(x0 + i * a.pas, a.droite * (x0 + i * a.pas), rnd.randrange(M)) for i in range(n)]
    elif a.sym in (2, 4):
        base = [(rnd.randint(-a.rayon, a.rayon), rnd.randint(-a.rayon, a.rayon), rnd.randrange(4)) for _ in range(max(1, n // a.sym))]
        F = [rot(*f, (4 // a.sym) * j) for j in range(a.sym) for f in base]
    else:
        F = [(rnd.randint(-a.rayon, a.rayon), rnd.randint(-a.rayon, a.rayon), rnd.randrange(M)) for _ in range(n)]
    if len({(x, y) for x, y, _ in F}) < len(F): continue        # deux fourmis sur la même case : on évite
    if a.classes and sum((x + y + d) % 2 for x, y, d in F) * 2 != len(F): continue
    C = {(rnd.randint(-a.rc, a.rc), rnd.randint(-a.rc, a.rc)) for _ in range(k)}
    if a.sym in (2, 4): C = {rot(x, y, 0, (4 // a.sym) * j)[:2] for j in range(a.sym) for x, y in C}
    f = ";".join(f"{x},{y},{d if hexa else CAP[d]}" for x, y, d in F)
    c = ";".join(f"{x},{y}" for x, y in sorted(C))
    ligne = f"{r}|{f}|{c}"
    if ligne in vus: continue
    vus.add(ligne); print(ligne); faits += 1
