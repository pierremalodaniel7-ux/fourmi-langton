#!/usr/bin/env python3
"""Tri automatique des sorties de ./fourmi : je ne lis QUE ce résumé, jamais les sorties brutes.
Usage : python3 outils/tri.py data/NOM.out [--ajouter]   (--ajouter : range les nouveautés dans connus.txt)
Une signature est découpée en morceaux (« + ») : C<P> = cycle, A<P>(dx,dy)x<k> = autoroute de k fourmis,
N<k> = k fourmis non classées (nid, navette, losange… : à examiner, jamais une découverte en soi).
Morceau connu = REGLE|morceau présent dans connus.txt. Une situation n'est détaillée que si elle contient
un morceau inconnu ; on donne l'exemple le plus court (le plus simple à revérifier)."""
import sys, collections, pathlib

racine = pathlib.Path(__file__).resolve().parent.parent
fconnus = racine / "connus.txt"
connus = {l.split("#")[0].strip() for l in fconnus.read_text(encoding="utf-8").splitlines()} if fconnus.exists() else set()
connus.discard("")
issues, morceaux, combos = collections.Counter(), collections.Counter(), collections.Counter()
ex, nonclasses = {}, collections.Counter()
total = 0
for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
    for l in open(f, encoding="utf-8"):
        p = l.rstrip("\n").split("|")
        if len(p) < 6 or p[3] == "ERREUR": continue
        total += 1; regle, issue, sig = p[0], p[3], p[4]; issues[issue] += 1; combos[sig] += 1
        sit = "|".join(p[:3])
        for m in sig.split("+"):
            if m.startswith("N"): nonclasses[m] += 1; continue
            cle = f"{regle}|{m}"
            if cle in connus: continue
            morceaux[cle] += 1
            if cle not in ex or len(sit) < len(ex[cle]): ex[cle] = sit
print(f"{total} situations : " + ", ".join(f"{k} {v} ({100*v/max(total,1):.1f} %)" for k, v in issues.most_common()))
print("Signatures les plus fréquentes : " + " ; ".join(f"{s} {k}" for s, k in combos.most_common(5)))
if nonclasses: print("Fourmis non classées (nids, navettes, losanges à examiner) : " + ", ".join(f"{m} {k}" for m, k in nonclasses.most_common()))
print(f"{len(morceaux)} morceaux INCONNUS (30 premiers) :" if morceaux else "Aucun morceau inconnu.")
for cle, k in morceaux.most_common(30):
    print(f"  {k:7d}  {cle:28s}  ex. {ex[cle]}")
if "--ajouter" in sys.argv and morceaux:
    with open(fconnus, "a", encoding="utf-8") as o:
        for cle in morceaux: o.write(f"{cle}  # vu dans {sys.argv[1]}, à vérifier\n")
    print("ajoutés à connus.txt")
