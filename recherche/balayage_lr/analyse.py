#!/usr/bin/env python3
"""Analyse du balayage LR : fusion des passes, classes finales, statistiques, relations de la section 1.
Usage : python3 analyse.py data/balayage  -> écrit recherche/balayage_lr/{regles_lr.csv,stats.md,relations.md}"""
import sys, glob, csv, collections, math, os
D = sys.argv[1]
OUT = os.path.dirname(os.path.abspath(__file__))
COLS = "regle,q,classe,pas,P,dx,dy,debut,cert,t_cert,boxw,boxh,ratio,ngram,noirs,sym,symok,symtest,ms".split(",")
rows = {}
def load(pattern):
    for f in sorted(glob.glob(os.path.join(D, pattern))):
        for line in open(f):
            v = line.strip().split(",")
            if len(v) != len(COLS): continue
            r = dict(zip(COLS, v))
            old = rows.get(r["regle"])
            if old is None or int(r["pas"]) >= int(old["pas"]) or r["classe"] in "VB":
                rows[r["regle"]] = r
load("part_a?.csv"); load("p2_*.csv"); load("p3_*.csv")
SYMN = ["miroir|", "miroir-", "diag", "antidiag", "centrale", "rot90"]
def final(r):
    c = r["classe"]
    if c == "B": return "B"
    if c == "V": return "V" if r["cert"] == "1" else "V?"
    if c == "E": return "E"
    so, st = int(r["symok"]), int(r["symtest"])
    if so >= 3 and so * 2 >= st: return "S"
    if int(r["ngram"]) < 120000: return "C"
    return "X"
for r in rows.values():
    r["cl"] = final(r)
    r["symn"] = "+".join(SYMN[i] for i in range(6) if int(r["sym"]) >> i & 1)
    if r["cl"] == "B": r["statut"] = "VÉRIFIÉ (cycle exact)"
    elif r["cl"] == "V": r["statut"] = "VÉRIFIÉ (certificat)"
    elif r["cl"] == "V?": r["statut"] = "OBSERVÉ (cap périodique, certificat refusé : longe probablement un bord)"
    else: r["statut"] = "OBSERVÉ (rien de prouvé)"
with open(os.path.join(OUT, "regles_lr.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["regle", "q", "classe", "pas_simules", "periode", "dx", "dy", "debut", "t_certificat",
                "boite", "ratio_boite_t/t2", "ngrammes20", "cases_non_blanches", "symetries", "sym_ok/tests", "statut"])
    for k in sorted(rows, key=lambda s: (len(s), s)):
        r = rows[k]
        iv = r["cl"] in ("V", "V?")
        w.writerow([k, r["q"], r["cl"], r["pas"], r["P"] if iv else "", r["dx"] if iv else "",
                    r["dy"] if iv else "", r["debut"] if iv else "",
                    r["t_cert"] if r["cert"] == "1" else "", f'{r["boxw"]}x{r["boxh"]}', r["ratio"], r["ngram"],
                    r["noirs"], r["symn"], f'{r["symok"]}/{r["symtest"]}', r["statut"]])
# statistiques
L = ["# Statistiques du balayage LR (grille carrée, 1 fourmi, départ blanc)\n",
     "Règles = mots primitifs, avec L et R, un représentant par paire L↔R (commence par L).\n",
     "| q | règles | B | V (certifiées) | V? (non certifiées) | C | S | X | E |", "|---|---|---|---|---|---|---|---|---|"]
byq = collections.defaultdict(list)
for r in rows.values(): byq[int(r["q"])].append(r)
tot = collections.Counter(); totc = 0
for q in sorted(byq):
    c = collections.Counter(r["cl"] for r in byq[q]); nc = sum(1 for r in byq[q] if r["cl"] == "V" and r["cert"] == "1")
    tot.update(c); totc += nc
    L.append(f"| {q} | {len(byq[q])} | {c['B']} | {c['V']} | {c['V?']} | {c['C']} | {c['S']} | {c['X']} | {c['E']} |")
L.append(f"| total | {len(rows)} | {tot['B']} | {tot['V']} | {tot['V?']} | {tot['C']} | {tot['S']} | {tot['X']} | {tot['E']} |\n")
V = [r for r in rows.values() if r["cl"] == "V"]
L.append("## Périodes d'autoroute (histogramme, classes log2)\n")
h = collections.Counter(int(math.log2(int(r["P"]))) for r in V)
for k in sorted(h): L.append(f"- [{2**k}, {2**(k+1)}) : {h[k]} " + "█" * max(1, h[k] * 60 // max(h.values())))
pc = collections.Counter(int(r["P"]) for r in V)
L.append("\nPériodes les plus fréquentes : " + ", ".join(f"{p} ({n})" for p, n in pc.most_common(15)))
L.append("\n## Records\n")
for lab, key in [("Plus longue période", lambda r: int(r["P"])), ("Plus long transitoire (début)", lambda r: int(r["debut"]))]:
    for r in sorted(V, key=key, reverse=True)[:10]:
        L.append(f"- {lab} : {r['regle']} P={r['P']} D=({r['dx']},{r['dy']}) début={r['debut']} cert={r['cert']}")
dirs = collections.Counter()
for r in V:
    a, b = abs(int(r["dx"])), abs(int(r["dy"])); g = math.gcd(a, b) or 1; dirs[(min(a, b) // g, max(a, b) // g)] += 1
L.append("\nDirections (pente réduite, à symétries près) : " + ", ".join(f"{a}/{b}:{n}" for (a, b), n in sorted(dirs.items(), key=lambda x: -x[1])))
open(os.path.join(OUT, "stats.md"), "w").write("\n".join(L) + "\n")
# relations
sw = lambda w: w.translate(str.maketrans("LR", "RL"))
canon = lambda w: w if w[0] == "L" else sw(w)
def look(w):
    c = canon(w); r = rows.get(c)
    if r is None: return None
    return r, (c != w)
def sig(r): return (r["cl"], int(r["P"]) if r["cl"] == "V" else 0)
def disp(r, flipped):
    dx, dy = int(r["dx"]), int(r["dy"]); return (-dx, dy) if flipped else (dx, dy)
iso = {"identité": lambda x, y: (x, y), "miroir x": lambda x, y: (-x, y), "miroir y": lambda x, y: (x, -y),
       "rot180": lambda x, y: (-x, -y), "rot90": lambda x, y: (-y, x), "rot270": lambda x, y: (y, -x),
       "diag": lambda x, y: (y, x), "antidiag": lambda x, y: (-y, -x)}
R = ["# Relations testées (section 1), sur toutes les règles balayées\n"]
for name, f in [("(a) mot lu à l'envers", lambda w: w[::-1]),
                ("(b) décalage circulaire d'un cran", lambda w: w[1:] + w[0]),
                ("(c) complément puis envers", lambda w: sw(w)[::-1])]:
    nvv = nvvp = 0
    n = same_cl = same_sig = 0; isoc = collections.Counter(); ex = []
    for k, r in rows.items():
        o = look(f(k))
        if o is None: continue
        r2, fl = o
        if r2 is r and not fl: continue
        n += 1
        if r["cl"] == r2["cl"]: same_cl += 1
        if sig(r) == sig(r2): same_sig += 1
        elif len(ex) < 5: ex.append(f"{k} {sig(r)} / {f(k)} {sig(r2)}")
        if r["cl"] == "V" and r2["cl"] == "V":
            nvv += 1; nvvp += r["P"] == r2["P"]
        if r["cl"] == "V" and r2["cl"] == "V" and r["P"] == r2["P"]:
            a = (int(r["dx"]), int(r["dy"])); b = disp(r2, fl)
            m = [nm for nm, g in iso.items() if g(*a) == b]; isoc[m[0] if m else "aucune"] += 1
    R.append(f"## {name}\npaires comparées {n} ; même classe {same_cl} ; même classe et même période {same_sig}.")
    R.append(f"Paires V–V : {nvv}, dont même période : {nvvp}.")
    R.append("Isométrie des déplacements (autoroutes de même période) : " + ", ".join(f"{a}:{b}" for a, b in isoc.most_common()))
    R.append("Contre-exemples : " + " ; ".join(ex) + "\n")
open(os.path.join(OUT, "relations.md"), "w").write("\n".join(R) + "\n")
print(open(os.path.join(OUT, "stats.md")).read()[:3000]); print("\n".join(R))

# Théorème des paires (Gale-Propp et al.) : mots formés de lettres doublées (LLRR, LLRRRRLL...), aussi à rotation près
def paired(w): return len(w) % 2 == 0 and all(w[i] == w[i+1] for i in range(0, len(w), 2))
def paired_rot(w): return any(paired(w[i:] + w[:i]) for i in range(len(w)))
P1 = [k for k in rows if paired(k)]; P2 = [k for k in rows if paired_rot(k) and not paired(k)]
S = [k for k in rows if rows[k]["cl"] == "S"]
T = ["## Théorème des paires (déjà connu : Gale, Propp, Sutherland, Troubetzkoy 1995)",
     f"mots à lettres doublées : {len(P1)} ; classes : {dict(collections.Counter(rows[k]['cl'] for k in P1))}",
     f"rotations de tels mots (non doublés eux-mêmes) : {len(P2)} ; classes : {dict(collections.Counter(rows[k]['cl'] for k in P2))}",
     f"classe S : {len(S)} règles, dont doublées {sum(paired(k) for k in S)}, doublées à rotation près {sum(paired_rot(k) for k in S)}",
     "S hors paires : " + " ".join(sorted([k for k in S if not paired_rot(k)], key=len)[:30])]
open(os.path.join(OUT, "relations.md"), "a").write("\n".join(T) + "\n"); print("\n".join(T))
