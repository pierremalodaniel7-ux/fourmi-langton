# build6.py — bestiaire 6 « autoroutes dans toutes les directions » + germes + tableau, depuis dirs_verif.json.
import json, csv, math
from fractions import Fraction
D = json.load(open('dirs_verif.json'))
def F(n): return format(n, ',').replace(',', ' ')
def nice_hex(a, b):  # pente écran = √3·b/(2a+b)
    fr = Fraction(b, 2 * a + b)
    return '0' if b == 0 else f"√3·{fr.numerator}/{fr.denominator}" if fr.denominator != 1 else f"√3·{fr.numerator}"
B, G, R = [], [], []
C6 = ['E', 'SE', 'SO', 'O', 'NO', 'NE']
for d in D:
    e = d.get('verifie')
    if not e: continue
    hexa = d['grille'] == 'hex'; a, b = d['dir']
    pente = nice_hex(a, b) if hexa else str(Fraction(b, a))
    ang = d['angle']; reg = e['regle']
    lr = (not hexa) and set(reg) <= set('LR')
    rl_multi = reg in ('RL', 'LR')
    if rl_multi: classe = 'Grille carrée, règle RL (plusieurs fourmis)'
    elif hexa: classe = 'Grille hexagonale (règles généralisées)'
    else: classe = 'Grille carrée, règles généralisées (L, R, N, U)'
    P, (dx, dy), deb = e['verif_periode'], e['verif_dep'], e['verif_debut']
    v = math.hypot(dx + dy / 2, dy * math.sqrt(3) / 2) / P if hexa else math.hypot(dx, dy) / P
    idd = ('H' if hexa else 'A') + f"-{a}-{b}"
    nomdir = f"pente {pente}" + (f" ({ang:.1f}°)".replace('.', ',') if ang not in (0, 45) else '')
    deja = ("Probablement connu (catalogue d'autoroutes de Lutfalla-Rao, règles L/R)" if lr and not rl_multi else
            "Connu (autoroute 104 / 102, voir bestiaires 1-2)" if rl_multi and [a, b] in ([1, 1], [3, 5]) else
            "Pas trouvé ailleurs (les autoroutes non diagonales existent : Lutfalla 2025 ; pas de catalogue des directions trouvé)")
    pts = e['cases']
    B.append({'id': idd, 'b': 6, 'classe': classe, 'nom': f"Autoroute de {nomdir}", 'regle': reg, 'fourmis': e['fourmis'], 'points': pts,
              'img': [min(deb + 40 * P, e['verif_T']), ''],
              'situation': (f"{e['n_fourmis']} fourmi(s)" + (f" et {e['n_cases']} case(s) colorée(s)" if e['n_cases'] else ", grille vide") + f", règle {reg[2:] + ' (hexagonale)' if hexa else reg}."),
              'deroulement': f"Après {F(deb)} pas, la fourmi {e['verif_fourmi']} part en autoroute : elle répète le même trajet de {F(P)} pas, décalé à chaque fois de ({dx},{dy})" + (" en coordonnées axiales (q,r)" if hexa else "") + ".",
              'mesures': f"Direction {a}:{b} (forme réduite), pente y = {pente}·x, angle {ang:.2f}° ; période {F(P)} ; vitesse {v:.4f} case/pas ; début {F(deb)}. Direction vue {d['n']} fois avec {len(d['regles'])} règle(s).".replace('.', ',', 0),
              'interet': "Direction rare" if d['n'] < 5 else "Direction fréquente",
              'statut': f"OBSERVÉ (revérifié sans retirer de fourmi jusqu'au pas {F(e['verif_T'])} ; une simulation finie ne prouve pas que l'autoroute dure toujours)",
              'deja': deja, 'source': 'Claude, 16/11 matin (R-35)'})
    G.append({'dossier': 'Autoroutes par direction/' + ('Hexagonale' if hexa else 'Carrée'), 'nom': f"{nomdir} — {reg}", 'regle': reg,
              'grille': 'hexagonale' if hexa else 'carrée', 'fourmis': e['fourmis'], 'points': pts,
              'note': f"Autoroute période {P}, déplacement ({dx},{dy}){' axial' if hexa else ''}, début {deb}. Cases notées x,y:couleur si la règle a plus de 2 couleurs."})
    R.append(['hexagonale' if hexa else 'carrée', f"{a}:{b}", pente, round(ang, 3), reg, e['n_fourmis'], e['n_cases'], P, f"({dx},{dy})", deb, round(v, 5), d['n'], len(d['regles']), e['fourmis'], pts])
B.sort(key=lambda x: (x['classe'], x['id'])); R.sort(key=lambda r: (r[0], r[3]))
json.dump(B, open('catalogue_autoroutes.json', 'w'), ensure_ascii=False, indent=1)
json.dump(G, open('germes_autoroutes.json', 'w'), ensure_ascii=False, indent=1)
with open('autoroutes_par_direction.csv', 'w', newline='') as fh:
    w = csv.writer(fh, delimiter=';'); w.writerow(['grille', 'direction', 'pente', 'angle_deg', 'regle', 'n_fourmis', 'n_cases', 'periode', 'deplacement', 'debut', 'vitesse', 'vue_n_fois', 'n_regles', 'fourmis', 'cases']); w.writerows(R)
print(len(B), 'bêtes')
