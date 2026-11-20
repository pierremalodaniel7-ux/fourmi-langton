#!/usr/bin/env python3
"""Fabrique un bestiaire PDF à partir de docs/sources/catalogue.json.

Usage :
  python3 outils/mkbestiaires.py B "Titre" [--ids A-T4,A-142 (prioritaire sur B)] [--sortie fichier.pdf] [--catalogue chemin]
  B = numéro de bestiaire (champ "b" des fiches). --ids : ne garder que ces fiches.
Exemple :
  python3 outils/mkbestiaires.py 13 "Conjecture de l'autoroute, séance S2 (18-11)"

Chaque fiche = une page : image de la grille au pas img[0] (moteur Python intégré, entiers exacts),
puis situation, déroulement, mesures, statut, intérêt, déjà connu, source, commande, germe JSON.
Moteur intégré : même convention que src/fourmi (carré : y vers le bas, caps H D B G, lettres L R N U ;
hexa : préfixe "H:", lettres N R1 R2 U L2 L1, coordonnées axiales ; fourmis jouées l'une après l'autre).
Ce moteur sert à DESSINER ; les statuts viennent des fiches (calculées avec src/fourmi).
Dépendances : matplotlib, reportlab, police DejaVu.
"""
import argparse, json, os, re, sys, tempfile
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

SQ = [(0, -1), (1, 0), (0, 1), (-1, 0)]                       # H D B G
HX = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]     # E SE SO O NO NE
TURN_SQ = {"L": -1, "R": 1, "N": 0, "U": 2}
TURN_HX = {"N": 0, "R1": 1, "R2": 2, "U": 3, "L2": -2, "L1": -1}
CAP = {"H": 0, "D": 1, "B": 2, "G": 3}
HCAP = {"E": 0, "SE": 1, "SO": 2, "O": 3, "NO": 4, "NE": 5}

def parse_rule(r):
    if r.startswith("H:"):
        return "hex", [TURN_HX[t] for t in re.findall(r"R1|R2|L1|L2|N|U", r[2:])]
    return "sq", [TURN_SQ[ch] for ch in r]

def simulate(rule, fourmis, points, T):
    kind, turns = parse_rule(rule)
    D, m = (SQ, 4) if kind == "sq" else (HX, 6)
    q = len(turns)
    g = {}
    for p in [p for p in points.split(";") if p.strip()]:
        v = [int(s) for s in p.split(",")]
        g[(v[0], v[1])] = (v[2] if len(v) > 2 else 1) % q
    ants = []
    for a in [a for a in fourmis.split(";") if a.strip()]:
        x, y, h = a.split(",")
        h = (CAP if kind == "sq" else HCAP).get(h) if not h.lstrip("-").isdigit() else int(h)
        ants.append([int(x), int(y), h])
    starts = [tuple(a) for a in ants]
    for _ in range(T):
        for a in ants:
            c = g.get((a[0], a[1]), 0)
            a[2] = (a[2] + turns[c]) % m
            g[(a[0], a[1])] = (c + 1) % q
            a[0] += D[a[2]][0]; a[1] += D[a[2]][1]
    return kind, g, starts, ants

def xy(kind, x, y):
    return (x, y) if kind == "sq" else (x + y / 2, y * 0.8660254)

def draw(e, fn):
    kind, g, starts, ants = simulate(e["regle"], e["fourmis"], e.get("points", ""), int(e["img"][0]))
    fig, ax = plt.subplots(figsize=(6, 4.6))
    cols = {}
    for (x, y), c in g.items():
        if c: cols.setdefault(c, []).append(xy(kind, x, y))
    shades = ["#000000", "#555555", "#999999", "#bbbbbb"]
    for c, pts in sorted(cols.items()):
        xs, ys = zip(*pts)
        col = shades[(c - 1) % 4] if max(cols) <= 4 else plt.cm.viridis((c - 1) / max(1, max(cols) - 1))
        ax.scatter(xs, ys, s=.4, color=col, marker="s", lw=0)
    init = [p for p in e.get("points", "").split(";") if p.strip()]
    if init and len(init) <= 60:
        P = [xy(kind, *map(int, p.split(",")[:2])) for p in init]
        ax.scatter(*zip(*P), s=40, facecolors="none", edgecolors="#d62728", lw=1.2, label="cases de départ")
    ax.scatter(*zip(*[xy(kind, s[0], s[1]) for s in starts]), s=25, c="#2ca02c", label="départ des fourmis")
    ax.scatter(*zip(*[xy(kind, a[0], a[1]) for a in ants]), s=45, c="#1f77b4", marker="^",
               label=f"fourmis au pas {int(e['img'][0]):,}".replace(",", " "))
    ax.invert_yaxis(); ax.set_aspect("equal"); ax.legend(loc="best", fontsize=7)
    ax.set_title(f"{e['id']} — état au pas {int(e['img'][0]):,}".replace(",", " "))
    fig.tight_layout(); fig.savefig(fn, dpi=160); plt.close(fig)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("b", type=int); ap.add_argument("titre")
    ap.add_argument("--ids", default=""); ap.add_argument("--sortie", default="")
    ap.add_argument("--catalogue", default=os.path.join(os.path.dirname(__file__), "..", "docs", "sources", "catalogue.json"))
    A = ap.parse_args()
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    F = "/usr/share/fonts/truetype/dejavu/"
    pdfmetrics.registerFont(TTFont("D", F + "DejaVuSans.ttf")); pdfmetrics.registerFont(TTFont("DB", F + "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("DM", F + "DejaVuSansMono.ttf"))
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    cat = json.load(open(A.catalogue))
    if A.ids: ids = A.ids.split(","); fiches = [e for e in cat if e["id"] in ids]   # --ids : quel que soit "b"
    else: fiches = [e for e in cat if e.get("b") == A.b]
    if not fiches: sys.exit(f"aucune fiche avec b={A.b}")
    N = ParagraphStyle("n", fontName="D", fontSize=9, leading=12); L = ParagraphStyle("l", parent=N, fontName="DB")
    H = ParagraphStyle("h", fontName="DB", fontSize=14, leading=18, spaceAfter=4)
    T = ParagraphStyle("t", fontName="DB", fontSize=19, leading=24, spaceAfter=8)
    M = ParagraphStyle("m", fontName="DM", fontSize=7.5, leading=9.5)
    esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    st = [Paragraph(esc(f"Bestiaire {A.b} — {A.titre}"), T),
          Paragraph(f"{len(fiches)} fiche(s). Images : moteur intégré de outils/mkbestiaires.py (dessin seulement) ; "
                    "statuts et mesures : ceux des fiches (src/fourmi). Texte noir sur fond blanc.", N), PageBreak()]
    tmp = tempfile.mkdtemp()
    for e in fiches:
        fn = os.path.join(tmp, e["id"] + ".png"); draw(e, fn)
        pts = e.get("points", "")
        if len(pts) > 1200:   # longues listes (traces) : abrégées sur la fiche, complètes dans catalogue.json et les germes
            pts = pts[:600] + f" … [{pts.count(';') + 1} cases ; liste complète dans catalogue.json, fiche {e['id']}]"
        sit = f'{e["regle"]}|{e["fourmis"]}|{pts}'
        germe = {"dossier": e.get("classe", ""), "nom": e["nom"], "regle": e["regle"], "fourmis": e["fourmis"],
                 "points": pts, "note": e.get("mesures", "")}
        rows = [("Classe", e.get("classe", "")), ("Situation", e.get("situation", "")), ("Déroulement", e.get("deroulement", "")),
                ("Mesures", e.get("mesures", "")), ("Statut", e.get("statut", "")), ("Intérêt", e.get("interet", "")),
                ("Déjà connu ?", e.get("deja", "")), ("Source", e.get("source", "")),
                ("Commande", Paragraph(esc(f'./fourmi -T {int(e["img"][0])} "{sit}"' + (f'  |  {e["commande"]}' if e.get("commande") else "")), M)),
                ("Germe", Paragraph(esc(json.dumps(germe, ensure_ascii=False)), M))]
        t = Table([[Paragraph(a, L), b if not isinstance(b, str) else Paragraph(esc(b), N)] for a, b in rows],
                  colWidths=[3.2 * cm, 13.8 * cm])
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        st += [Paragraph(esc(f"{e['id']} — {e['nom']}"), H), Image(fn, width=14 * cm, height=14 * cm * 4.6 / 6),
               Spacer(1, 4), t, PageBreak()]
    st.pop()
    out = A.sortie or f"resultats/Bestiaire {A.b} - {A.titre}.pdf".replace("/", "-", 0)
    SimpleDocTemplate(out, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm,
                      title=f"Bestiaire {A.b} — {A.titre}").build(st)
    print("écrit :", out)

if __name__ == "__main__":
    main()
