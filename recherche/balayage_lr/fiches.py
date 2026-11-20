#!/usr/bin/env python3
"""Choisit les bêtes du balayage LR et écrit les fiches (catalogue.json, bestiaire B) + germes.
Usage : python3 fiches.py B DATE   (lit recherche/balayage_lr/regles_lr.csv)"""
import csv, json, sys, os, math, collections
B, DATE = int(sys.argv[1]), sys.argv[2]
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(H, "../.."))
rows = list(csv.DictReader(open(os.path.join(H, "regles_lr.csv"))))
by = {r["regle"]: r for r in rows}
V = [r for r in rows if r["classe"] == "V"]
I = lambda r, k: int(r[k]) if r[k] not in ("", None) else 0
sw = lambda w: w.translate(str.maketrans("LR", "RL"))
def paired(w): return len(w) % 2 == 0 and all(w[i] == w[i+1] for i in range(0, len(w), 2))
def paired_rot(w): return any(paired(w[i:] + w[:i]) for i in range(len(w)))
chosen = collections.OrderedDict()
def add(rule, cat, why):
    if rule in chosen: chosen[rule]["why"] += " ; " + why; return
    chosen[rule] = {"cat": cat, "why": why}
# 1 référence
add("RL", "Référence", "fourmi de Langton, test du code (autoroute 104 vers 10 000)")
# 2 records de période (certifiés d'abord)
for r in sorted(V, key=lambda r: -I(r, "periode"))[:12]: add(r["regle"], "Records de période", f"période {r['periode']} (rang parmi les plus longues)")
# 3 records de transitoire
for r in sorted(V, key=lambda r: -I(r, "debut"))[:12]: add(r["regle"], "Records de transitoire", f"autoroute qui n'apparaît qu'au pas {r['debut']}")
# 4 directions : autoroutes droites (dx ou dy = 0) et pentes rares
dirs = collections.defaultdict(list)
for r in V:
    a, b = abs(I(r, "dx")), abs(I(r, "dy")); g = math.gcd(a, b) or 1
    dirs[(min(a, b) // g, max(a, b) // g)].append(r)
for d, L in sorted(dirs.items(), key=lambda x: len(x[1])):
    if d == (1, 1): continue
    L.sort(key=lambda r: (int(r["q"]), I(r, "periode")))
    add(L[0]["regle"], "Directions d'autoroute", f"pente {d[0]}/{d[1]} ({len(L)} règle(s) dans le balayage), la plus courte")
# 5 plus petite règle de chaque période fréquente
pc = collections.Counter(I(r, "periode") for r in V)
for p, n in pc.most_common(6):
    r = min([r for r in V if I(r, "periode") == p], key=lambda r: (int(r["q"]), r["regle"]))
    add(r["regle"], "Périodes fréquentes", f"période {p} partagée par {n} règles ; la plus courte")
# 6 cycles
for r in [r for r in rows if r["classe"] == "B"][:5]: add(r["regle"], "Cycles exacts", "retour exact à l'état de départ")
# 7 symétriques : doublées (théorème connu) et hors paires
S = [r for r in rows if r["classe"] == "S"]
for r in sorted([r for r in S if paired(r["regle"])], key=lambda r: int(r["q"]))[:3]: add(r["regle"], "Symétriques (paires)", "motif symétrique, règle à lettres doublées (théorème connu)")
for r in sorted([r for r in S if not paired_rot(r["regle"])], key=lambda r: int(r["q"]))[:5]: add(r["regle"], "Symétriques hors paires", "motif symétrique sans être une règle à lettres doublées")
for r in sorted([r for r in S if paired_rot(r["regle"]) and not paired(r["regle"])], key=lambda r: int(r["q"]))[:2]: add(r["regle"], "Symétriques (paires à rotation près)", "rotation d'une règle à lettres doublées")
# 8 constructeurs les plus réguliers
C = [r for r in rows if r["classe"] == "C" and I(r, "pas_simules") >= 2000000]
for r in sorted(C, key=lambda r: (I(r, "ngrammes20"), int(r["q"])))[:7]: add(r["regle"], "Constructeurs réguliers", f"suite des virages très régulière ({r['ngrammes20']} 20-grammes distincts sur 2^20 pas)")
# 9 étranges : croissance très lente, croissance linéaire sans autoroute, sorties
G = [r for r in rows if r["classe"] in "CSX"]
def side(r): w, h = r["boite"].split("x"); return max(int(w), int(h))
for r in sorted(G, key=lambda r: (side(r) / math.sqrt(I(r, "pas_simules"))))[:5]: add(r["regle"], "Étranges : presque immobiles", f"boîte {r['boite']} seulement après {r['pas_simules']} pas")
for r in sorted([r for r in G if float(r["ratio_boite_t/t2"] or 0) > 1.7], key=lambda r: -float(r["ratio_boite_t/t2"]))[:5]: add(r["regle"], "Étranges : croissance linéaire sans autoroute", f"boîte x{r['ratio_boite_t/t2']} quand t double")
for r in [r for r in rows if r["classe"] == "E"][:3]: add(r["regle"], "Étranges : sortie de zone", "sort de la zone ±65 536 sans autoroute détectée")
# 10 relations : contre-exemples (a) envers, (b) rotation
for w in ["LLLR", "LLRL"]: add(w, "Relations (section 1)", "contre-exemple : l'envers / la rotation n'ont pas le même comportement")
# 10b faux amis : cap périodique tardif mais certificat refusé
for r in sorted([r for r in rows if r["classe"] == "V?"], key=lambda r: int(r["q"]))[:4]:
    add(r["regle"], "Faux amis (certificat refusé)", f"cap périodique de période {r['periode']} dès le pas {r['debut']}, mais le certificat échoue : la fourmi longe sans doute un bord")
# 11 famille LᵃRᵇ (conjecture)
for w, why in [("LLLLLLLLLLLLLR", "famille LⁿR : P = 16n+4 = 212, début 24n+6 = 318 (connu, Gajardo-Lutfalla-Rao)"),
               ("LLLLLLLRRRRR", "famille LᵃRᵇ, b impair : P = 16(a+b)−20 = 172"),
               ("LLLLLLRRRRR", "famille LᵃRᵇ : demi-période 78 = (16·11−20)/2"),
               ("LLLLLLLLLRRRRRRR", "famille LᵃRᵇ : demi-période (16·16−20)/2 = 118, q = 16"),
               ("LLRRR", "seule exception à « b impair, a ≥ b−1 ⇒ autoroute » : chaotique"),
               ("LLLLLLLLLLRR", "famille LᵃRR (b pair) : jamais d'autoroute, boîte minuscule")]:
    add(w, "Famille LᵃRᵇ (conjecture)", why)
# compléter jusqu'à >= 55 avec les plus grands déplacements par période
for r in sorted(V, key=lambda r: -(abs(I(r, "dx")) + abs(I(r, "dy"))) / max(1, I(r, "periode")))[:200]:
    if len(chosen) >= 60: break
    add(r["regle"], "Autoroutes rapides", f"vitesse {abs(I(r,'dx'))+abs(I(r,'dy'))}/{r['periode']} cases par pas")
cat = json.load(open(os.path.join(ROOT, "docs/sources/catalogue.json")))
cat = [e for e in cat if e.get("b") != B]
germes = []
for i, (w, c) in enumerate(chosen.items(), 1):
    r = by.get(w) or by.get(sw(w))
    if r is None: continue
    flip = r["regle"] != w
    cl = r["classe"]; P = I(r, "periode"); st = I(r, "debut"); ps = I(r, "pas_simules")
    if cl == "V?": img = min(st + 4 * P + 2000, 3000000)
    if cl == "V":
        img = min(st + 4 * P + 2000, 3000000); dx, dy = I(r, "dx"), I(r, "dy")
        if flip: dx = -dx
        comp = f"Autoroute de période {P}, déplacement ({dx},{dy}) par période, à partir du pas {st}."
        mes = f"période {P} ; déplacement ({dx},{dy}) ; début {st} ; certificat au pas {r['t_certificat'] or '—'} ; boîte {r['boite']}" + (f" ; IMAGE au pas {img} seulement (encore le chaos : l'autoroute vient bien plus tard)" if img < st else "")
        statut = "DÉMONTRÉ (certificat d'autoroute exact, balaye.c)" if r["t_certificat"] else "OBSERVÉ (autoroute non certifiée)"
    elif cl == "B":
        img = min(ps, 2000000); comp = f"Cycle exact : retour à l'état initial au pas {ps}."; mes = comp; statut = "DÉMONTRÉ (cycle exact)"
    else:
        if cl != "V?": img = min(ps, 2000000)
        nm = {"C": "constructeur (virages réguliers)", "S": "motif symétrique", "X": "chaotique", "E": "sortie de zone", "V?": f"cap périodique {P} depuis le pas {st}, certificat refusé"}[cl]
        comp = f"Classe {cl} ({nm}) jusqu'au pas {ps} ; boîte {r['boite']}, rapport de boîte {r['ratio_boite_t/t2']} quand t double."
        mes = f"boîte {r['boite']} ; cases non blanches {r['cases_non_blanches']} ; 20-grammes {r['ngrammes20']} ; symétries {r['symetries'] or 'aucune'} ({r['sym_ok/tests']})"
        statut = "OBSERVÉ (simulation finie : rien de prouvé au-delà)"
    deja = "Déjà connu (fourmi de Langton)" if w == "RL" else (
        "Déjà connu (théorème des paires, Gale-Propp et al. 1995)" if paired(w) else
        "Probablement connu (catalogues d'autoroutes langtonsant.es / Lutfalla, non consultables ici)" if cl == "V" else
        "Pas trouvé ailleurs (littérature web inaccessible depuis la session ; pas trouvé ≠ nouveau)")
    e = {"id": f"LR-{i:02d}", "b": B, "classe": f"Balayage LR — {c['cat']}", "nom": f"{w} — {c['cat'].lower()}",
         "regle": w, "fourmis": "0,0,H", "points": "", "img": [img, ""],
         "situation": f"Règle {w} (q = {len(w)}), une fourmi en (0,0) cap haut, grille blanche infinie.",
         "deroulement": comp + (" Règle obtenue par échange L↔R du représentant " + r["regle"] + " (motif miroir, déplacement dx changé de signe)." if flip else ""),
         "mesures": mes + (f" ; simulé {ps} pas" if cl != "V" else ""),
         "statut": statut, "interet": c["why"], "deja": deja,
         "source": f"recherche/balayage_lr ({DATE}), balaye.c, regles_lr.csv"}
    cat.append(e)
    germes.append({"dossier": f"Balayage LR/{c['cat']}", "nom": f"{w} — {c['why'][:60]}", "regle": w, "grille": "carrée",
                   "fourmis": "0,0,H", "points": "", "note": comp})
json.dump(cat, open(os.path.join(ROOT, "docs/sources/catalogue.json"), "w"), ensure_ascii=False, indent=1)
json.dump(germes, open(os.path.join(ROOT, f"docs/sources/germes_{DATE}_balayage_lr.json"), "w"), ensure_ascii=False, indent=1)
print(len(chosen), "bêtes ;", collections.Counter(c["cat"] for c in chosen.values()))
