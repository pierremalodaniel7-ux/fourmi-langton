#!/usr/bin/env python3
"""T4 : fiches du bestiaire 34 -> t4/catalogue_t4.json (catalogue À PART) + germes resultats (dossier « Règles/Hexa R2L2/écran de la fourmi »).
Les mesures sont relues dans les fichiers de résultats (rien de recopié à la main)."""
import sys, os, json, glob
os.environ['LECT'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import ecran_un_pas as E1, ecran_deux_pas as E2, deux_pas_long as DL, lecture_port as LP
I = 77; e0 = STEP.cases()[I]
def split(s): _, a, c = s.split('|')[:3]; return a, c
def zoom(c, r=10): return f'zoom {c[0] - r},{c[1] - r},{c[0] + r},{c[1] + r}'
U = json.load(open(os.path.join(T4, 'ecran_un_pas.json')))
a1, c1 = split(E1.situation([e0]))
F = [dict(id='R-715', b=34, classe='Règles/Hexa R2L2/écran de la fourmi', nom="Écran 2×2 branché sur le pas complet de la petite fourmi (1 pas)",
          regle='H:R2L2', fourmis=a1, points=c1, img=[U['T'], zoom(DL.PL['c10']['c'])],
          situation=f"Germe du pas complet R-617 (état initial n° {I} : cases 00 10 01 11 = {e0['c00']}{e0['c10']}{e0['c01']}{e0['c11']}, x = {e0['x']}, y = {e0['y']}, cap = {e0['h1']}{e0['h0']}) + 4 pixels M (OFF) posés sur les 4 sorties de cases.",
          deroulement="Le germe calcule le pas de la fourmi RL sur le tore 2×2 ; chaque sortie c_ij' est un vaisseau présent ssi la case vaut 1 ; en passant, il allume son pixel (M -> R'). Image : pixel c10 après le pas.",
          mesures=f"256 états : écran lu (état + phase) = c' : {U['justes']}/256 ; reste propre {U['propres']}/256 (moteur C) ; hx.py identique {U['py_identiques']}/{U['py_n']} ; T = {U['T']}.",
          statut='VÉRIFIÉ (2 moteurs, les 256 états, temps fini)', interet="Premier écran qui montre la grille calculée par un germe de fourmis : « la fourmi dans la fourmi » se voit.",
          deja="Analogue : le jeu de la vie dans le jeu de la vie (métapixels, OTCA). En fourmis de Langton hexagonales R2L2 : pas trouvé.", source='recherche/regles/s4_ecran/journal.md (R-715, 27/11)',
          commande='cd recherche/regles/s4_ecran && python3 t4/rayons.py && python3 t4/placer.py && python3 t4/ecran_un_pas.py 64')]
# R-722 : port de lecture, pixel c10 seul, OFF, 2 lectures
L1 = json.load(open(os.path.join(T4, 'lecture_c10_40000.json'))); L2 = json.load(open(os.path.join(T4, 'lecture_c10_80000.json')))
p = LP.PL['c10']; ph0 = (kit('SET0a')['ph'] - p['arrivee']) % 21
s = LP.pixel_sit('c10', 0, ph0, [tuple(t[1]) for t in L1['toks']] + [tuple(t[1]) for t in L2['toks']]); a2, c2 = split(s)
F.append(dict(id='R-722', b=34, classe='Règles/Hexa R2L2/écran de la fourmi', nom="Port de lecture d'un pixel, réutilisable et neutre (2 lectures d'un pixel éteint)",
          regle='H:R2L2', fourmis=a2, points=c2, img=[L2['e'] + 1500, zoom(p['c'], 14)],
          situation="Pixel M (OFF) seul + 2 lectures (sonde dir 4 + 3 horloges chacune), posées à t = 0, lues vers t = 40 000 et 80 000.",
          deroulement="OFF : la sonde change M en X et ressort 2 voies à côté ; 3 chocs la ramènent sur la droite de réécriture X -> M ; M reprend la phase qu'il aurait eue sans lecture. ON : la sonde traverse R'. Lu = sonde sur sa droite d'origine.",
          mesures=f"Pré-tests (hx.py) pour les 4 pixels × 2 lectures, cas ON et OFF : pixel à la phase prévue, lu juste, reste propre. Délais w = {L1['w']} et {L2['w']} (≡ 9 mod 63).",
          statut="OBSERVÉ (hx.py ; dans la démo complète R-723 : 2 moteurs)", interet="Lecture non destructive et réutilisable d'un pixel ; R-709/R-712/R-713 avaient échoué.",
          deja='Interne au projet.', source='recherche/regles/s4_ecran/journal.md (R-722)', commande='cd recherche/regles/s4_ecran && python3 t4/lecture_port.py c10 40000 && PREV=lecture_c10_40000.json python3 t4/lecture_port.py c10 80000'))
# R-723 : démo complète
R = {}
for f in glob.glob(os.path.join(T4, 'data_deux_pas', 'hx_lect_*.json')): R.update(json.load(open(f))['res'])
C = json.load(open(os.path.join(T4, 'data_deux_pas', 'c_tC_lect.json')))
nh = len(R); ok_h = sum(all(v[k]['juste'] and v[k]['propre'] for k in ('tA', 'tA2', 'tB', 'tC')) and v['sorties_usage2'] for v in R.values())
same = sum(1 for i, v in R.items() if C['res'][str(i)]['empreinte'] == v['empreinte']) if isinstance(next(iter(C['res'])), str) else 0
okC = sum(v['juste'] and v['propre'] for v in C['res'].values())
a3, c3 = split(DL.sit_of(e0))
F.append(dict(id='R-723', b=34, classe='Règles/Hexa R2L2/écran de la fourmi', nom="Deux pas de la fourmi à l'écran, avec effacement automatique et 8 lectures",
          regle='H:R2L2', fourmis=a3, points=c3, img=[DL.TA, zoom(DL.PL['c11']['c'])],
          situation=f"Germe R-617 utilisé 2 fois au même endroit (2e usage retardé de D = {DL.D}, ses entrées = l'état après 1 pas), 4 pixels, 4 boucles d'effacement (12 horloges), 8 ports de lecture ; {a3.count(';') + 1} fourmis posées à t = 0.",
          deroulement="Pas 1 : l'écran montre c' ; lectures des 4 pixels vers t = 40 000 et 80 000 ; chaque vaisseau qui a allumé un pixel fait une boucle de ≈ 380 000 pas et revient l'éteindre juste avant le pas 2 ; pas 2 : l'écran montre c''.",
          mesures=f"hx.py : {ok_h}/{nh} états justes aux 4 lectures (t = {DL.TA}, {DL.TA2}, {DL.TB}, {DL.TC}) + 8 lectures + sorties du pas 2 ; moteur C à t = {DL.TC} : {okC}/256 justes et propres ; états finaux identiques (2 moteurs) : {same}/{nh}.",
          statut=f"VÉRIFIÉ (2 moteurs, {nh} états, temps fini t = {DL.TC})" if ok_h == nh and okC == 256 and same == nh else 'voir mesures',
          interet="L'écran suit la vraie fourmi RL du tore 2×2 sur 2 pas, au même endroit, et on peut le lire sans l'abîmer.",
          deja="Analogue : métapixels du jeu de la vie. En fourmis R2L2 : pas trouvé.", source='recherche/regles/s4_ecran/journal.md (R-720, R-723)',
          commande='cd recherche/regles/s4_ecran && LECT=1 python3 t4/deux_pas_long.py C && LECT=1 python3 t4/deux_pas_long.py hx 0 256'))
json.dump(F, open(os.path.join(T4, 'catalogue_t4.json'), 'w'), ensure_ascii=False, indent=1)
G = [{'dossier': 'Règles/Hexa R2L2/écran de la fourmi', 'nom': f"{e['id']} {e['nom']}", 'regle': e['regle'], 'fourmis': e['fourmis'], 'points': e['points'], 'note': e['mesures']} for e in F]
json.dump(G, open(os.path.join(T4, 'germes_t4_ecran_2026-11-27.json'), 'w'), ensure_ascii=False, indent=1)
print(len(F), 'fiches'); [print(e['id'], e['mesures']) for e in F]
