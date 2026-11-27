# S4 écran — journal (R-700+)

(Entrées R-700 à R-702 écrites a posteriori le 27/11 00:45 d'après les commits c036ad1, 8a61478 du 26/11 soir.)

## R-700 Catalogue des chocs propres de 2 vaisseaux R2L2 en trajectoires — VÉRIFIÉ (fourmi_r, échantillon hx.py) (catalogue_chocs.py)
Même ensemble fini que R-333 (B dir. 0, A dir. 1..5, avance 0..7, position relative mod d_A − d_B, 2 ordres) ; chaque choc propre
(0 case, 2 vaisseaux sortants) noté par étiquettes (r, voie, V) : on le tourne, translate, retarde en bloc. → data/chocs.json (non versionné).

## R-701 Démultiplexeur 2→4 : recherche exacte sur les trajectoires — OBSERVÉ (demux_cherche.py, demux_filtre.py)
W (écrire) × a1 → W0/W1 ; F : a0 × K → 2 copies ; G2, G3 : copies × W0/W1. Équation exacte en glissements (k2, k3, n), puis 4 cas
simulés (fourmi_r) : 540 démultiplexeurs justes 4/4 ; tri : aucune paire de face (R-338) et place libre ≥ 16 sur chaque sortie.

## R-702 Démultiplexeur 2→4 RÉUTILISABLE — VÉRIFIÉ (2 moteurs, temps fini) + certificat (demux_verif.py → demux_retenu.json)
Rang 0 du tri : 4/4 cas justes (2 moteurs 4/4) ; 20 usages au MÊME endroit, UNE simulation (58-62 fourmis, t = 31 701), 3 tirages +
« tous dans l'ordre » : superposition exacte, 20/20 adresses justes, 2 moteurs identiques. Certificat (méthode R-338) : distance min
entre fourmis de 2 usages = 15 pour les écarts 1..12, 0 paire de face ⇒ tout nombre d'usages (même argument que R-339).
Kits du pixel (pixel.py) : bascule R-341 en trajectoires (mise à 1 = SET, mise à 0 = RST), placée tournée de rho et centrée en c.

## R-703 Écran 2×2 avec 2 COPIES du même démultiplexeur (port 0 = port 1 tourné + translaté) : impossible — VÉRIFIÉ (calcul exact) (ecran_geo.py, 27/11 00:45-00:55)
La bascule R-341 veut mise à 1 en direction ρ et mise à 0 en ρ+2. Sorties du démux R-702 : directions {0, 2, 5, 3} ; rotations
compatibles du 2e port : 2 (même adresse) ou 5 (adresses permutées 00↔11, 01↔10) ; rôles inversés : 4 ou 1. Pour chacune et toute
translation |v| ≤ 500 : aucun v où les 4 centres (croisements des voies, toujours entiers) sont EN AVAL des deux ports (après le
dernier choc + 12). Raison : le centre j doit être dans un cône de 60° (u_j, −R u_j) ; les sorties vont par paires opposées ⇒ 2
parallélogrammes bornés qui ne se coupent pas. (Avec ±40 : 0 sur 6 561, marge max 1.) → prendre un 2e démultiplexeur différent.

## R-704 Écran 2×2 avec 2 démultiplexeurs DIFFÉRENTS et le seul kit R-341 : aucun placement — VÉRIFIÉ (calcul exact) (ecran2_geo.py, ecran2_bande.py)
Recalcul (00:50) du catalogue (2 316 chocs, 224 propres, 2 moteurs 60/60) et du démux (8 graines × 20 000 tirages : 654 justes 4/4,
49 après tri). 49 × 49 démux × 6 rotations × 2 rôles × 24 permutations, |v| ≤ 150 (et ≤ 300, bande lointaine) : 0. Raison : avec un
écart fixe de +120° entre mise à 1 et mise à 0, le cône de faisabilité du pixel j est (θ_j − 60°, θ_j) ; deux sorties de directions
différentes ne laissent au mieux qu'un rayon commun.

## R-705 Toutes les écritures à 1 vaisseau entre M et R' — VÉRIFIÉ (hx.py ; kits recontrôlés plus loin) (kits_scan.py → kits.json)
6 directions × voies −8..8 × toutes les phases, vaisseau joué après (et avant : même résultat) : mise à 1 : (dir 0, voie 1, ph 16 ou 17),
(dir 5, voie 1, ph 4) ; mise à 0 : (dir 2, voie −2, ph 2), (dir 3, voie −2, ph 10 ou 11). Nouveau couple utile : SET5/RST3 (écart −120°).

## R-706 Écran 2×2 : placements trouvés en choisissant le kit pixel par pixel — OBSERVÉ (géométrie exacte ; simulation à suivre) (ecran3_geo.py)
Démux A à 2 directions voisines {θ, θ+60°} : kit −120° (SET5/RST3) sur les sorties θ, kit +120° (SET0/RST2) sur θ+60° ⇒ même cône
pour les 4 pixels. Premier placement : A = B = démux n° 6 du tri (sorties dir 0, 1, 1, 0), port 0 tourné de 180°, v = (237, −141),
marge 16 (≥ 11) de chaque pixel à tous les rayons étrangers, aucune paire de face.

## R-707 ÉCRAN 2×2 ADRESSABLE R2L2 : 3 motifs puis tout éteint, 4/4 lectures justes — VÉRIFIÉ (2 moteurs, temps fini) (ecran_demo.py → ecran_demo.json, ecran_motif_1..4.png)
Placement R-706 rang 0 : port « 1 » = démux n° 8 (sorties dir 0, 5, 5, 0), port « 0 » = le même tourné de 180°, v = (138, −228) ;
pixels (M = OFF / R' = ON) en (113,−114), (59,−151), (22,−77), (76,−114) pour les adresses 00, 01, 10, 11 du port 1 (port 0 : adresses
permutées 10, 00, 11, 01). 10 opérations (1 vaisseau W + adresses + K chacune), retards 0, 1 600, 3 210, … , 14 436 (chaque retard
ajusté au pas près pour la phase du pixel). UNE simulation, 39 fourmis posées à t = 0 : motif 1 {00, 11} ; motif 2 {01, 10} ;
motif 3 {01, 10, 11} ; tout éteint : lectures exactes (état + phase de chaque pixel) 4/4 justes, fourmi_r = hx.py aux 4 instants.
À la fin : 8 fourmis des pixels (4 × M) + 31 fourmis = vaisseaux libres qui s'éloignent (décodés), à ≥ 106 du centre.
Piège trouvé : pixel.ORB TRIE les fourmis ; quand les 2 fourmis de M sont sur la même case, l'ordre de jeu compte ⇒ orbite ordonnée.
Limite : comme R-341/R-342, on n'écrit 1 que sur un 0 et 0 que sur un 1 (il faut connaître l'état). Simulation finie (t = 18 036).
