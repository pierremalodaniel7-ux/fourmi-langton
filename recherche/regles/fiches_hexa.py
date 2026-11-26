#!/usr/bin/env python3
"""Fiches du bestiaire (nuit 26/11, hexa R2L2) et germes pour le simulateur. Usage : python3 fiches_hexa.py NUMERO_BESTIAIRE
Ajoute (ou remplace) les fiches de ce bestiaire dans catalogue_regles.json et écrit germes_2026-11-26_hexa.json."""
import sys, json, random
from hx import step, ship, HX
import ecran
B = int(sys.argv[1])
def S(ants, cells):
    return ';'.join(f'{a[0]},{a[1]},{a[2]}' for a in ants), ';'.join(f'{c[0]},{c[1]}' for c in cells)
F = []
def fiche(id_, nom, fa, pts, img, situation, deroulement, mesures, statut, interet, deja, source, commande):
    F.append({'id': id_, 'b': B, 'classe': 'Règles/Hexa R2L2 (nuit 26-11)', 'nom': nom, 'regle': 'H:R2L2', 'fourmis': fa, 'points': pts,
              'img': [img, ''], 'situation': situation, 'deroulement': deroulement, 'mesures': mesures, 'statut': statut, 'interet': interet,
              'deja': deja, 'source': source, 'commande': commande})
# 1. vaisseau dans un champ de cases au hasard (R-330)
random.seed(5); (a0, c0) = ship(0, (0, 0)); cells = {c0}
for i in range(-9, 10):
    for j in range(-9, 10):
        p = (40 + i, -40 + j)
        if random.random() < 0.35 and abs(i + j) <= 9: cells.add(p)
fiche('R-330', 'Vaisseau R2L2 à travers un champ de cases au hasard : jamais tourné', f'{a0[0]},{a0[1]},{a0[2]}', ';'.join(f'{x},{y}' for x, y in sorted(cells)), 700,
      'Vaisseau R2L2 (fourmi 0,0 cap 4 + case 1,0) lancé vers un champ de 35 % de cases noires centré en (40,−40).',
      'Il traverse le champ, le dérange, puis ressort en vaisseau dans LA MÊME direction (1,−1), un peu décalé de voie.',
      'Preuve (preuve_obstacles.py) : quel que soit l\'obstacle (fini ou infini), le vaisseau ne recule jamais de plus de 3 crans : 14 états ; 3 000 champs au hasard : recul max 3, 3 000/3 000 même direction.',
      'DÉMONTRÉ (calcul exact, ensemble fermé de 14 états) ; déjà esquissé par Grosfils et al. 1999',
      'Aucun miroir ne peut être fait de cases : il faut des fourmis.', 'Connu (Grosfils, Boon, Cohen, Bunimovich 1999, preuve par cas) ; notre certificat à 14 états : pas trouvé',
      'journal_regles R-330', 'python3 preuve_obstacles.py 3')
# 2. le plus petit oscillateur (période 3)
fiche('R-334-O', 'Le plus petit oscillateur R2L2 : 2 fourmis + 1 case, période 3', '0,0,3;1,0,0', '1,0', 30,
      '2 fourmis de classes opposées (caps 3 et 0) côte à côte, 1 case noire.', 'Revient exactement à son état toutes les 3 étapes. C\'est son propre film à l\'envers.',
      'Cycle exact (fourmi_r CYCLE C3 ; hx.py). Détruit par 1 vaisseau en 3 vaisseaux (il reste 1 case, imposé par l\'invariant Q).',
      'VÉRIFIÉ (cycle exact = périodique pour toujours)', 'Pixel ON de l\'écran version 1 (R-334).', 'Cycles à 2 particules : McGinnis-Webb 2019 (modèle synchrone) ; celui-ci : pas trouvé tel quel',
      'journal_regles R-312, R-334', './fourmi_r "H:R2L2|0,0,3;1,0,0|1,0"')
# 3. le bit de mémoire M (période 21)
fiche('R-335-M', 'Bit de mémoire : oscillateur M (2 fourmis + 1 case, période 21)', '0,0,1;1,-1,0', '-1,1', 63,
      '2 fourmis (caps 1 et 0) et 1 case : une paire qui tourne en rond.', 'Période 21 ; propre film à l\'envers (à une phase près) ; ses destructions propres ne laissent AUCUNE case.',
      'Cycle exact ; écriture (3 vaisseaux) et lecture (1 sonde → 3 vaisseaux) ; 20/20 usages, certifié pour tout nombre d\'usages (R-339).',
      'VÉRIFIÉ', 'Bit 1 = M présent, bit 0 = rien : la « boule dans sa boîte » qui remplace la boucle de miroirs impossible.', 'Pas trouvé',
      'journal_regles R-335, R-339', 'python3 memoire_finale.py 20 26')
# 4. écriture : 3 vaisseaux fabriquent M
ecran.O2 = "H:R2L2|0,0,1;1,-1,0|-1,1"; p = ecran.Pair((0, 1, 0, 9), (0, 2, -2, 11))
fa, pts = S(p.CREATE[0], sorted(p.CREATE[1]))
fiche('R-335-E', 'ÉCRIRE 1 : trois vaisseaux qui fabriquent le bit M', fa, pts, p.TC,
      'Film à l\'envers (gomme collective) d\'une destruction propre de M : 3 vaisseaux qui convergent vers (0,0).',
      'Au pas 720, M est là exactement (phase 2) et un 4e vaisseau repart vers la gauche.', 'hx.py et fourmi_r identiques ; aucune case en trop.',
      'VÉRIFIÉ (temps fini ; M est ensuite un cycle exact)', 'Écriture d\'une mémoire sans aucune case fixe.', 'Pas trouvé', 'journal_regles R-335', 'python3 memoire_finale.py')
# 5. lecture : sonde + M → 3 vaisseaux
st = p.states[11]
fa = ';'.join(f'{a[0]},{a[1]},{a[2]}' for a in st[0]) + ';' + ';'.join(f'{a[0]},{a[1]},{a[2]}' for a in p.ERASE[0])
pts = ';'.join(f'{x},{y}' for x, y in sorted(list(st[1]) + list(p.ERASE[1])))
fiche('R-335-L', 'LIRE : la sonde détruit M en 3 vaisseaux propres (bit 1)', fa, pts, 720,
      'M (phase 11) + 1 vaisseau-sonde de direction (0,1) joué après M.', 'M part en 3 vaisseaux (directions 3, 2, 4) ; il ne reste RIEN. Sans M, la sonde passe seule.',
      'Bit lu = 3 vaisseaux sortants (1) ou 1 (0). 20/20 sur 4 tirages ; 2 moteurs identiques.', 'VÉRIFIÉ', 'Lecture destructive, comme une mémoire à tores.', 'Pas trouvé',
      'journal_regles R-335', 'python3 memoire_finale.py')
# 6. mémoire : 6 usages dans une simulation (lisible)
import memoire_finale as mf
plan, ants, cells, vals, TEND = mf.demo_memoire([1, 0, 1, 1, 0, 1])
fa, pts = S(ants, sorted(cells))
fiche('R-335-6', 'Mémoire 1 bit : 6 usages au même endroit (1, 0, 1, 1, 0, 1)', fa, pts, 1600,
      f'{len(ants)} fourmis, toutes en vaisseaux venus de loin à t = 0 ; aucune case fixe. Usage i : écriture (si 1) à 3 200·i, lecture vers 3 200·i + 1 600.',
      'Image au pas 1 600 : le bit 1 du 1er usage est écrit (M au centre) ; les vaisseaux des usages suivants approchent.',
      '6/6 lectures justes ; version 20 usages : 20/20 (4 tirages), 2 moteurs ; certificat pour tout nombre d\'usages (R-339).', 'VÉRIFIÉ / DÉMONTRÉ (R-339)',
      'Premier bit réinscriptible du projet sans remise à zéro extérieure.', 'Pas trouvé', 'journal_regles R-335, R-339', 'python3 memoire_finale.py 20 26')
# 7. écran 2 pixels
plan, a2, c2, SNAP, v = ecran.screen(p)
fa, pts = S(a2, sorted(c2))
fiche('R-335-X', 'Écran de 2 pixels : P1 = ON, OFF, ON ; P2 = OFF, ON, OFF', fa, pts, 1600,
      f'P1 en (0,0), P2 en (40,20) ; {len(a2)} fourmis posées à t = 0 (kits d\'écriture et d\'effacement).', 'Lectures à t = 1 600, 3 200, 4 800 : (ON, OFF), (OFF, ON), (ON, OFF).',
      '3/3 justes ; version 1 (pixel 2 fourmis + 1 case, OFF = 1 case) : 3/3, 2 moteurs 4/4 (pixels.py).', 'VÉRIFIÉ (temps fini)', 'Pixel « comme Conway » : ON = une paire qui tourne, OFF = vide.',
      'Pas trouvé', 'journal_regles R-334, R-335', 'python3 pixels.py ; python3 memoire_finale.py')
# 8. demi-additionneur réutilisable : un usage (1,0) et 20 usages
D = json.load(open('resumes/demi_additionneur_reutilisable.json'))
def split(s):
    _, a, c = s.split('|'); return a, c
fa, pts = split(D['un_usage']['(1, 0)'])
fiche('R-337-10', 'Demi-additionneur réutilisable : un usage a = 1, b = 0 (S sur la voie de V)', fa, pts, 1400,
      'Porte R-327 (B en (0,0), A en (30,−56)) + K2 (62,−24) + K3 (−16,16) ; ici seul A est présent.',
      'K2 tourne U vers la gauche, puis U pousse K3 sur la voie de sortie de B : S = 1 sur la même voie que dans le cas b = 1. Aucune case ne reste.',
      '4 cas justes, 0 case ; 563 variantes trouvées ; 20 usages au hasard : 20/20 (5 tirages), 2 moteurs ; certificat pour tout nombre d\'usages (R-338).',
      'VÉRIFIÉ / DÉMONTRÉ (R-338)', 'Ferme R-329 : demi-additionneur à sortie S unique, réutilisable sans remise à zéro.', 'Pas trouvé (billard de Fredkin-Toffoli sans miroir)',
      'journal_regles R-337, R-338', 'python3 demi_add_final.py 7 200')
fa, pts = split(D['situation_20_usages'])
fiche('R-337-20', 'Demi-additionneur : 20 additions au hasard au même endroit', fa, pts, 3200,
      f'{len(fa.split(";"))} fourmis (entrées et constantes de 20 usages espacés de 200 périodes), toutes posées à t = 0.', 'Chaque usage sort S = a⊕b (voie 0) et C = a∧b (voie (2,−28)) ; les usages ne se touchent jamais (distance ≥ 90).',
      '20/20 justes, 2 moteurs identiques, 0 case restante.', 'VÉRIFIÉ', 'Calcul réutilisé 20 fois.', 'Pas trouvé', 'journal_regles R-337', 'python3 demi_add_final.py 7 200')
# 9. vaisseau double (fusion de 2 vaisseaux)
fiche('R-333-D', 'Vaisseau DOUBLE : 2 vaisseaux qui se collent et repartent ensemble', '-25,25,4;0,-25,0', '-24,25;-1,-24', 500,
      'Choc de 2 vaisseaux (directions (1,−1) et (0,1)) dans l\'une des 24 géométries « liées » de R-333.', 'Après le choc, les 2 fourmis restent liées : un objet de période 8 qui avance comme un vaisseau.',
      'Répétition exacte sur 51 périodes ; s\'éloigne de ses débris (certificat chocs_certif.py).', 'VÉRIFIÉ (certificat de périodicité)',
      'Une des 3 issues possibles d\'un choc (jamais de perte, R-333).', 'Pas trouvé', 'journal_regles R-333', 'python3 chocs_exhaustif.py && python3 chocs_certif.py')
# 10. oscillateur à 3 fourmis
fiche('R-332-3', 'Oscillateur à 3 fourmis (nombre impair), période 6', '0,0,2;1,-2,4;0,-1,0', '1,-2', 30,
      '3 fourmis + 1 case dans un carré 3×3.', 'Cycle exact de période 6.', '12 orbites distinctes à 3 fourmis trouvées ([−2,2]², ≤ 1 case) ; fourmi_r : CYCLE.',
      'VÉRIFIÉ (cycle exact)', 'McGinnis-Webb (2019) laissent ouvert « N impair périodique ? » dans leur modèle SYNCHRONE ; ici, ordre « l\'une après l\'autre » (les fourmis se croisent sur une même case).',
      'Différent du cadre de 1908.06019 (convention)', 'journal_regles R-332', './miroir enum 3 2 1 4096')
cat = json.load(open('catalogue_regles.json'))
cat = [c for c in cat if c.get('b') != B] + F
json.dump(cat, open('catalogue_regles.json', 'w'), ensure_ascii=False, indent=1)
G = [{'dossier': 'Règles/Hexa R2L2', 'nom': f"{f['id']} — {f['nom']}", 'regle': 'H:R2L2', 'fourmis': f['fourmis'], 'points': f['points'],
      'note': f['deroulement'] + ' Statut : ' + f['statut'] + '.'} for f in F]
json.dump(G, open('germes_2026-11-26_hexa.json', 'w'), ensure_ascii=False, indent=1)
print(len(F), 'fiches (bestiaire', B, ') ;', len(G), 'germes')
