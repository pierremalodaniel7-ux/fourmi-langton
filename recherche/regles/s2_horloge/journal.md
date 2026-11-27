# Journal S2 — horloge, boucle, pixel qui clignote (session parallèle du 26/11 soir, entrées R-500 et suivantes)

Cadre : hexa R2L2 (blanc → +120°, noir → −120°), fourmis jouées l'une après l'autre, grille infinie, positions entières.
Moteurs : `../fourmi_r` (C, CYCLE = retour exact de l'état complet = périodique pour toujours, R-01) et `../hx.py` (Python, indépendant).
Tous les scripts se lancent depuis `recherche/regles/` : `python3 s2_horloge/<script>.py …`.

## R-500 FAMILLE INFINIE D'HORLOGES « TRIANGLE » à 6 fourmis — DÉMONTRÉ (certificat exact + convexité) ; terme j construit directement
Idée (calcul « vaisseaux virtuels », tri.py) : 3 vaisseaux horaires (caps pairs, directions 0 → 2 → 4) et 3 anti-horaires (caps impairs,
5 → 3 → 1) ; à chaque coin d'un grand triangle un choc de 2 vaisseaux (60°) tourne l'horaire de +120° et l'anti-horaire de −120° (c'est la
porte d'interaction de R-314). Si R(x) = rot120(x) + c et état(T) = R(état(0)), l'état revient exactement après 3T. Les équations de fermeture
sont dégénérées pour ce type de choc (d₂ + d₅ = 0) : chaque choc propre (596 trouvés) donne une PROGRESSION ARITHMÉTIQUE de tailles possibles.
Sur chaque arête l'horaire et l'anti-horaire se croisent de face au milieu (événement fixe selon la parité de j), ce qui avance chaque vaisseau
de 6 ou 12 pas : P = 3T − 18 ou 3T − 36.
Terme j (formule.py, rien d'autre que des entiers) :
  fourmis (1,6,5) ; (−6, j+19, 1) ; (−(j+12), j+12, 3) ; (−5,5,4) ; (1, j+13, 0) ; (−(j+13), j+19, 2)
  cases (1,5) (1,6) (−6,j+19) (−5,j+19) (−(j+13),j+13) (−(j+12),j+12) (−4,5) (0,j+14) (−(j+13),j+18)
  période P(j) = 363 + 24 j (j pair), 381 + 24 j (j impair) ; triangle de côté ≈ j + 19 cases.
VÉRIFIÉ : CYCLE exact fourmi_r pour j = 0 … 300 (301/301, période exacte) et 18 termes jusqu'à j = 1 949 (P = 47 181) ;
hx.py : premier retour exact = P pour j = 0 … 41 (42/42) et j = 60, 61.
DÉMONTRÉ pour tout j (certif_tri.py) : sur une période, chaque fourmi est soit un vaisseau libre (à > 14, hystérésis 10, de toute autre
fourmi), soit dans un « événement » (21 événements : 3 coins au départ, 3 coins + 3 croisements par tiers, coupés au bord). Pour j = p + 2(i0 + i),
i = 0, 1, 2 : même structure, paramètres (vaisseaux virtuels, temps, centres) AFFINES en i, chaque événement = translaté espace-temps exact
du précédent ; séparations (vaisseau–vaisseau, vaisseau–événement, événement–événement) contrôlées en fractions exactes sur les centres continus
(écart fourmi–centre ≤ 13/8) : la distance hexagonale est une norme ⇒ le minimum sur t est CONVEXE en i ⇒ m(0) ≥ seuil et m(1) ≥ m(0) donnent
m(i) ≥ seuil pour tout i ≥ 0 ; fermeture (état à P = état à 0) affine en i, vraie en i = 0, 1, 2 ⇒ vraie partout ; aucune case orpheline.
Certificat OK pour j pair ≥ 40 (`certif_tri.py 0 20`) et j impair ≥ 33 (`certif_tri.py 1 16`) ; j < 40 : CYCLE direct (2 moteurs).
⇒ pour TOUT j ≥ 0, la configuration revient exactement à elle-même : horloge qui tourne pour toujours, aussi grande qu'on veut.
Commandes : `python3 s2_horloge/formule.py` ; `python3 s2_horloge/famille.py 0 200` ; `python3 s2_horloge/famille_hx.py 0 1 60 61` ;
`python3 s2_horloge/certif_tri.py 0 20` ; `python3 s2_horloge/certif_tri.py 1 16`.
Autres chocs : 48 familles du même type (P = 3T − 18/36), 172 chocs donnant au moins un cycle (tri_test.py ; T ≤ 400).
La famille R-349b (P = 2 322 + 2 736 n, trouvée au hasard) n'est PAS celle-ci : voir R-504.
Déjà connu ? Analogue : McGinnis-Webb 2019 (modèle synchrone) ont une famille d'orbites périodiques à 2 particules (période 4d) ;
une famille de 6 vaisseaux R2L2 en triangle : pas trouvée (deja_connu_regles.md).

## R-501 Horloge branchée sur la bascule R-341 : le vaisseau de l'horloge écrit le bit et revient — VÉRIFIÉ (CYCLE exact, 2 moteurs)
Bascules « traversantes exactes » (bascule_shift.py) : sur les 438 496 bascules R → R' → R de bascule_hexa.py (R-340, regénérées),
294 150 ont deux vaisseaux de directions OPPOSÉES qui passent tout droit ; on mesure le décalage espace-temps du vaisseau sortant :
120 sont EXACTES pour les deux écritures (le vaisseau ressort exactement là où il serait passé sans objet). Parmi elles la bascule R-341
elle-même : M = « 0,0,1;1,−1,0|−1,1 » ↔ R' = « −1,0,3;1,1,0|−1,0;−1,1;0,−1;1,0;1,1 », mise à 1 par le même vaisseau que R-341 (dir 0,
voie 1, M en phase 16) et — nouveau — remise à 0 par un vaisseau de direction OPPOSÉE (dir 3, voie −2, R' en phase 10 ou 11).
Une telle bascule posée sur une arête de l'horloge triangle (le vaisseau anti-horaire écrit 1, l'horaire du tiers suivant écrit 0) ne change
rien à l'horloge : toute la machine est un cycle exact. C'est la consigne 2 (un vaisseau de l'horloge sert d'entrée à la bascule puis revient).

## R-502 PIXEL QUI CLIGNOTE TOUT SEUL POUR TOUJOURS (8 fourmis) — VÉRIFIÉ (CYCLE exact fourmi_r + hx.py : périodique pour toujours)
pixel_search.py : horloge triangle (48 familles) + UNE bascule exacte sur l'arête C0C1 ; on balaie la position du pixel le long de l'arête ;
critère = CYCLE exact de toute la machine. j ≈ 60 : 123 148 machines, 310 cycles (toutes les bascules utilisées clignotent : 6 changements par
période) ; avec la bascule R-341 et j ≈ 150 : 81 258 machines, 148 cycles.
Machine retenue (pixel_cycles_150_150_tri.json n° 0, 8 fourmis, 12 cases) :
  H:R2L2|4,124,0;2,126,3;6,6,5;-6,174,1;-162,162,3;-5,5,4;6,163,0;-163,174,2|6,5;6,6;-6,174;-5,174;-163,163;-162,162;-4,5;5,164;-163,173;4,126;3,124;3,126
(les 2 premières fourmis = le pixel, objet M de R-335/R-341 ; les 6 autres = horloge triangle). Période 4 203 (= horloge seule) ; le pixel
vaut 1 (R') pendant 1 752 pas, 0 (M) pendant 2 203 pas, en écriture 249 pas ; il passe 0 → 1 → 0 trois fois par période (une fois par tiers,
période de clignotement 1 401). 2 moteurs : fourmi_r CYCLE 4 203, hx.py premier retour exact 4 203. GIF : img/pixel_clignotant_R341.gif
(images fixes _ON.png, _OFF.png). Exemple plus petit (bascule R-341, P = 2 043) : pixel_cycles_60_60_tri.json n° 6.
C'est l'équivalent du clignotant du jeu de la vie, mais fait d'une horloge (6 fourmis) + une mémoire (2 fourmis) ; T0/T1 respectés :
aucune fourmi ne part, tout est borné, et le cycle exact prouve « pour toujours ».

## R-503 Bascule T / compteur par un flux de vaisseaux identiques (même route), vaisseaux exacts — 0 trouvé (OBSERVÉ, négatif)
compteur.py : 15 299 conversions traversantes (angle 0) des 95 oscillateurs à 2 fourmis ; 52 laissent le vaisseau exact ; flux de 2, 3, 4
vaisseaux sur la même route espacés de Δ = 200 … 1 399 pas (62 400 flux chacun) : le 2e vaisseau est TOUJOURS perturbé (0 / 62 400).
⇒ avec ces objets, un objet qui change d'état à chaque passage d'un même signal sans abîmer le signal n'existe pas ; un compteur
« causal » (retenue) demanderait un objet qui DÉVIE le signal selon son état, ce qui casse l'horloge (piste ouverte).

## R-504 Famille R-349b (P = 2 322 + 2 736 n) : alignement de deux termes (vieille_famille*.py) — OUVERT
Scripts écrits en vague 1 (alignement par rotation × relabellisation × temps), coupés avant conclusion : aucun résultat à retenir.

## R-505 Bascule T « en deux temps » (objet frappé alternativement par deux routes opposées, vaisseaux exacts) — 0 trouvé (OBSERVÉ, négatif)
compteur2.py / compteur3.py : chaînes de conversions EXACTES X0 →a→ X1 →b→ X2 … ; aucun retour à l'orbite de X0 après 2 tours avec X2 ≠ X0
(bascules_T.json = [], compteur3_K4.json = []). Avec ces objets (oscillateurs à 2 fourmis de data/osc2.txt), pas de diviseur par 2.
