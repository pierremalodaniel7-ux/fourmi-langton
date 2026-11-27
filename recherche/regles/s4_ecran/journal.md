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
