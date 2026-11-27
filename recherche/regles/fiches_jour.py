#!/usr/bin/env python3
"""Fiches du bestiaire 27 (26/11 jour) → docs/sources/catalogue.json (ajout) + germes chargeables (germes_2026-11-26_jour.json)."""
import json
def split(s):
    r, a, c = s.split('|')[:3]; return r, a, c
F = json.load(open('resumes/additionneur_complet_reutilisable.json'))
H = json.load(open('resumes/demi_additionneur_reutilisable.json'))
A2 = json.load(open('resumes/additionneur2_tete_beche.json'))
M = json.load(open('resumes/memoire_calcul.json'))
CL = json.load(open('resumes/horloges_6_fourmis.json'))
CL2 = [z for z in CL if z['n'] == 2][0]
from ha_etoile import HAstar
hs = HAstar(0).sit({'a': 0, 'b': 1})
cert = F.get('certificat', {})
E = []
def fiche(id_, nom, sit_, img, situation, deroulement, mesures, statut, interet, deja, commande):
    r, a, c = split(sit_)
    E.append(dict(id=id_, b=27, classe='Règles/Hexa R2L2 (jour 26-11)', nom=nom, regle=r, fourmis=a, points=c, img=img, situation=situation,
                  deroulement=deroulement, mesures=mesures, statut=statut, interet=interet, deja=deja,
                  source='recherche/regles/journal_regles.md (session du 26/11, jour)', commande=commande))
fiche('R-349', 'Additionneur complet réutilisable : a + b + retenue avec 6 vaisseaux, 20 additions au même endroit',
      F['un_usage']['(1, 1, 1)'], [320, 'zoom -20,-70,90,40'],
      "Demi-additionneur R-337 (K3, K2, B = b, A = a) + retenue c = UN vaisseau de direction 4 (56,−28, cap 2 + case 57,−28), joué en 1er. Cas a = b = c = 1.",
      "c croise la zone de la porte juste après le choc A-B : selon le cas il décale, dévie ou laisse passer les vaisseaux sortants. Somme et retenue se lisent comme « un vaisseau sur l'une de 3 positions ».",
      f"8/8 justes (2 moteurs) ; 2 usages : 64/64 suites (superposition exacte) ; 20 usages au hasard, 3 graines : 20/20, superposition exacte, 2 moteurs identiques. Certificat : distance min entre usages {cert.get('distance_min', 'en cours')}.",
      'VÉRIFIÉ (2 moteurs, 20 usages)' + (' ; tout nombre d\'usages DÉMONTRÉ (certificat)' if cert.get('distance_min', 0) > 6 and not cert.get('fronts') else ''),
      "Premier additionneur complet réutilisable de la règle sans miroir : chaque addition recommence au même endroit, sans déchet qui gêne la suivante.",
      'Pas trouvé (Bunimovich-Khlabystova 2002 : calcul par l\'environnement, pas par chocs ; voir deja_connu_regles.md).',
      'python3 recherche/regles/fa_reutilisable.py 0 12')
fiche('R-344', 'Demi-additionneur « HA* » : un seul vaisseau constant égalise les deux horaires de la somme',
      hs, [320, 'zoom -20,-70,90,40'],
      "R-337 + K5 = vaisseau « 31,1,3 » + case (31,2), joué en 1er. Cas (a, b) = (0, 1).",
      "Le choc K5 + S-V renvoie de quoi repousser K3 sur la voie de S, à la place exacte de S-U : S sort au même endroit et au même instant pour (1,0) et (0,1).",
      "4/4 justes, 2 moteurs ; 52 réussites (6 placements distincts) sur ≈ 1,1 million d'essais ; tous remontent un axe d'entrée à contresens ⇒ 2 usages : 8/16.",
      'VÉRIFIÉ (1 usage) ; non réutilisable OBSERVÉ',
      "Montre qu'on peut égaliser des horaires sans retard géométrique ; et pourquoi ça coince pour la réutilisation.",
      'Pas trouvé.', 'python3 recherche/regles/ha_etoile.py 0')
fiche('R-345', 'Additionneur 2 bits par enchaînement : la retenue passe d\'un étage à l\'autre (un usage)',
      A2['cas']['(1, 1, 1, 1)'], [700, 'zoom -40,-80,120,80'],
      "Étage 0 = demi-additionneur R-337 (a0, b0) ; étage 1 = additionneur complet « tête-bêche » tourné de −60°, posé pour que sa retenue d'entrée soit exactement la sortie C de l'étage 0. Cas a = 11, b = 11.",
      "La retenue de l'étage 0 est UN vaisseau qui part vers l'étage 1 ; l'étage 1 la reçoit comme 3e entrée.",
      "16/16 additions justes (somme lue sur 2, 3 et 3 positions), 2 moteurs identiques. Réutilisation impossible pour cette version tête-bêche (démontré : la retenue remonte la route de sortie de S).",
      'VÉRIFIÉ (2 moteurs, un usage)',
      "Première addition de nombres à 2 chiffres où la retenue voyage d'un étage à l'autre comme un signal.",
      'Pas trouvé.', 'python3 recherche/regles/add2_tete.py')
fiche('R-346', 'Le calcul écrit dans la mémoire : a ET b → bascule → lecture → remise à 0, 20 fois',
      M['situation_20_usages'], [2420, 'zoom 12,176,36,200'],
      "Demi-additionneur R-337 réutilisé 20 fois ; sa sortie C = a∧b (1 vaisseau) met à 1 une bascule (2 fourmis) posée sur sa route ; remise à 0 par un vaisseau quand le pixel lu vaut 1.",
      "Image : la bascule (centre 24,188) juste après la 1re écriture (bit 1). Les vaisseaux d'écriture et de remise à 0 traversent l'objet et repartent.",
      "20/20 lectures justes pour 3 suites au hasard, 20 × (1,1) : 20/20, alterné : 20/20 ; propre ; 2 moteurs identiques (t = 36 936).",
      'VÉRIFIÉ (2 moteurs, 20 usages)', "Premier branchement calcul → mémoire réutilisable dans la règle sans miroir.",
      'Pas trouvé.', 'python3 recherche/regles/memoire_demo.py data/memoire_sub.json 20 0 8')
fiche('R-349b', 'Horloge sans miroir : 6 vaisseaux qui partent à 86 cases et reviennent exactement (période 7 794)',
      CL2['situation'], [3897, ''],
      "6 vaisseaux, symétrie d'ordre 3 (2 vaisseaux « générateurs » + leurs rotations de 120° et 240°).",
      "Les vaisseaux volent en ligne droite (jusqu'à 426 pas), se relancent par chocs et reviennent à l'état de départ. Image : mi-période.",
      "CYCLE exact (fourmi_r, preuve par réversibilité) et retour exact vérifié par hx.py ; famille P = 2 322 + 2 736 n (n = 0…4), rayon 22 + 32 n.",
      'VÉRIFIÉ (2 moteurs ; périodique pour toujours) ; famille infinie OUVERT',
      "Un signal qui fait le tour et revient, sans miroir : impossible avec des relais immobiles (théorème T3), possible avec des vaisseaux qui se relancent.",
      'Pas trouvé (McGinnis-Webb 2019 : orbites à 2 particules, modèle synchrone).', 'python3 recherche/regles/horloge2.py 200000 8 8000 1')
cat = json.load(open('../../docs/sources/catalogue.json'))
ids = {e['id'] for e in cat}
cat += [e for e in E if e['id'] not in ids]
json.dump(cat, open('../../docs/sources/catalogue.json', 'w'), ensure_ascii=False, indent=1)
G = [dict(dossier='Règles/Hexa R2L2', nom=e['id'] + ' — ' + e['nom'], regle=e['regle'], fourmis=e['fourmis'], points=e['points'], note=e['mesures']) for e in E]
# germes supplémentaires : les 8 cas de l'additionneur complet réutilisable, les 16 de l'additionneur 2 bits
for k, s in F['un_usage'].items():
    r, a, c = split(s); G.append(dict(dossier='Règles/Hexa R2L2/Additionneur complet réutilisable', nom=f'R-349 (a,b,c) = {k}', regle=r, fourmis=a, points=c, note='somme et retenue : voir fiche R-349'))
for k, s in A2['cas'].items():
    r, a, c = split(s); G.append(dict(dossier='Règles/Hexa R2L2/Additionneur 2 bits', nom=f'R-345 (a0,a1,b0,b1) = {k}', regle=r, fourmis=a, points=c, note='un usage'))
for z in CL:
    r, a, c = split(z['situation']); G.append(dict(dossier='Règles/Hexa R2L2/Horloges 6 fourmis', nom=f"R-349b horloge n = {z['n']} (P = {z['P']})", regle=r, fourmis=a, points=c, note=f"période {z['P']}, rayon {z['rayon']}"))
json.dump(G, open('germes_2026-11-26_jour.json', 'w'), ensure_ascii=False, indent=1)
print(len(E), 'fiches ;', len(G), 'germes')
