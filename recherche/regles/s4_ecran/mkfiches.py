#!/usr/bin/env python3
"""Fiches du bestiaire 31 (S4 écran) -> catalogue_s4.json (catalogue À PART, ne touche pas docs/sources/catalogue.json) + germes."""
import json, sys
from traj import *
from exp_osc import setup
import pixel
R = json.load(open(HERE + '/ecran_demo.json'))
def split_sit(s): _, a, c = s.split('|')[:3]; return a, c
a, c = split_sit(R['situation'])
L = R['lectures']
F = [{'id': 'R-707', 'b': 31, 'classe': 'Règles/Hexa R2L2/s4_ecran', 'nom': 'Écran 2×2 adressable : 2 démultiplexeurs + 4 bascules, 3 motifs puis tout éteint',
      'regle': 'H:R2L2', 'fourmis': a, 'points': c, 'img': [L[1]['t'], 'zoom 0,-170,135,-60'],
      'situation': f"{R['fourmis']} fourmis posées à t = 0 : 4 pixels (oscillateur M = OFF, 2 fourmis) et 10 opérations (vaisseau W + vaisseaux d'adresse + K) sur 2 ports (démux n° 8 et sa copie tournée de 180°, translatée de (138, −228)).",
      'deroulement': 'Motif 1 {00, 11} ; motif 2 {01, 10} (image, zoom sur les pixels) ; motif 3 {01, 10, 11} ; tout éteint. Chaque vaisseau traverse le pixel visé et s\'éloigne.',
      'mesures': '; '.join(f"{x['motif']} t = {x['t']} : lu {x['lu']}" for x in L) + ' ; fourmi_r = hx.py aux 4 instants ; fin : 31 vaisseaux libres + 4 × M.',
      'statut': 'VÉRIFIÉ (2 moteurs, temps fini t = 18 036)', 'interet': "Premier écran adressable : on choisit le pixel avec 2 bits d'adresse, on allume ou on éteint.",
      'deja': 'Pas trouvé (écrans en jeu de la vie : oui ; en fourmis de Langton hexagonales R2L2 : non).', 'source': 'recherche/regles/s4_ecran/journal.md (27/11)',
      'commande': 'cd recherche/regles/s4_ecran && cp sauve/demux_tries.json data/ && cp sauve/ecran3_geo_top20.json data/ecran3_geo.json && python3 ecran_demo.py 0'}]
E = setup(pixel.M, 5, 1, 4, 0)
F.append({'id': 'R-705', 'b': 31, 'classe': 'Règles/Hexa R2L2/s4_ecran', 'nom': "Nouvelle mise à 1 du pixel M → R' : vaisseau direction 5 (−60°)",
          'regle': 'H:R2L2', 'fourmis': ';'.join(f'{x},{y},{h}' for x, y, h in E['ants']), 'points': ';'.join(f'{x},{y}' for x, y in sorted(E['g'])),
          'img': [E['T'], 'zoom -12,-12,12,12'], 'situation': "M (2 fourmis, période 21, en phase 4) + 1 vaisseau direction 5, voie 1, joué après.",
          'deroulement': "Le vaisseau traverse : M devient R' (2 fourmis + 5 cases, période 12) et le vaisseau ressort sur sa route, sans retard.",
          'mesures': "Recherche complète (6 directions, voies −8..8, toutes phases) : mises à 1 = (dir 0, voie 1, ph 16/17), (dir 5, voie 1, ph 4) ; mises à 0 = (dir 2, voie −2, ph 2), (dir 3, voie −2, ph 10/11).",
          'statut': "VÉRIFIÉ (hx.py ; utilisé dans R-707, 2 moteurs)", 'interet': "Avec ce 2e couple (écart −120° au lieu de +120°) l'écran 2×2 devient constructible (R-704 / R-706).",
          'deja': 'Interne au projet (prolonge R-341).', 'source': 'recherche/regles/s4_ecran/journal.md (27/11)', 'commande': 'python3 recherche/regles/s4_ecran/kits_scan.py'})
R4 = json.load(open(HERE + '/ecran4_glouton.json')); a4, c4 = split_sit(R4['situation']); L4 = R4['lectures']
F.insert(0, {'id': 'R-711', 'b': 31, 'classe': 'Règles/Hexa R2L2/s4_ecran', 'nom': 'Écran 4×4 : 4 blocs 2×2, dessins « visage » puis « anneau » puis tout éteint',
      'regle': 'H:R2L2', 'fourmis': a4, 'points': c4, 'img': [L4[1]['t'], 'zoom -100,-1450,2650,100'],
      'situation': f"{R4['fourmis']} fourmis posées à t = 0 : 16 pixels (M = OFF) en 4 blocs 2×2 (bloc R-707 translaté de b·400·(2, −1), direction 30°) et 20 opérations ; retards choisis un par un (glouton contrôlé).",
      'deroulement': "Visage (yeux + bouche, 6 pixels) ; anneau (8 pixels : 2 extinctions, 4 allumages) ; tout éteint (8 extinctions). Image : fourmis au pas 19 261 (anneau) ; vue de l'écran lu : ecran4_dessin_2.png.",
      'mesures': '; '.join(f"{x['etape']} t = {x['t']} : lu {'/'.join(x['lu'])}" for x in L4) + " ; fourmi_r = hx.py aux 3 instants ; étiquettes de tous les vaisseaux libres = calcul exact (aucune interaction imprévue).",
      'statut': 'VÉRIFIÉ (2 moteurs + contrôle exact, temps fini t = 34 117)', 'interet': "Premier petit dessin sur un écran 4×4 fait de fourmis. Avec des retards fixes ça casse (R-710) : il faut régler l'heure de chaque tir.",
      'deja': 'Pas trouvé (écrans en jeu de la vie : oui ; en fourmis de Langton hexagonales R2L2 : non).', 'source': 'recherche/regles/s4_ecran/journal.md (27/11, R-710/R-711)',
      'commande': 'cd recherche/regles/s4_ecran && cp sauve/demux_tries.json data/ && cp sauve/ecran3_geo_top20.json data/ecran3_geo.json && python3 ecran4_glouton.py 400 60'})
json.dump(F, open(HERE + '/catalogue_s4.json', 'w'), ensure_ascii=False, indent=1)
G = [{'dossier': 'Règles/Hexa R2L2/s4_ecran', 'nom': f"{e['id']} {e['nom']}", 'regle': e['regle'], 'fourmis': e['fourmis'], 'points': e['points'], 'note': e['mesures']} for e in F]
json.dump(G, open(HERE + '/germes_s4_ecran_2026-11-27.json', 'w'), ensure_ascii=False, indent=1)
print(len(F), 'fiches')
