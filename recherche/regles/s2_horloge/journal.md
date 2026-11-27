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

## R-506 DEUX PIXELS QUI CLIGNOTENT EN ALTERNANCE (10 fourmis) — VÉRIFIÉ (CYCLE exact fourmi_r + hx.py premier retour 4 203)
Idée : sur une arête, le pixel A (bascule R-341) est allumé par le 1er vaisseau du tiers, éteint par le 2e : fenêtre ON centrée sur le
croisement. La même bascule tournée de 180° est allumée par le 2e et éteinte par le 1er du tiers suivant : fenêtre ON décalée de P/6.
Sur la même arête les places compatibles sont mal centrées (anti_pixel.py, k = 0…5 : 4 + 2 + 2 cycles, au mieux 73 % du temps opposés) ;
on la pose donc sur l'arête suivante (l'horloge est symétrique : état(t + P/3) = R(état(t)), R = rotation 120° + translation (−168, 174),
calculée exactement) : anti_pixel2.py m = 1, 58 611 machines, 6 CYCLE (P = 4 203). Machine retenue (anti2_m1.json n° 0) :
  H:R2L2|-41,40,1;-41,40,2;4,125,4;5,125,1;-83,84,1;5,85,3;-84,173,5;5,85,2;-84,173,4;-83,84,0|3,125;6,83;-83,174;-85,85;-82,83;5,86;-85,173;6,84;-84,174;-84,84;-41,40;-39,38;-40,38;-39,39;-40,40
(fourmis 0,1 = pixel B ; 2,3 = pixel A ; 4–9 = horloge R-502). Sur une période : A et B dans des états OPPOSÉS pendant 3 676 pas,
JAMAIS dans le même état (0 pas) ; les 527 autres pas = écritures (ni M ni R'). A ON 1 714, B ON 1 962 ; 3 alternances par période.
2 moteurs : fourmi_r CYCLE 4 203 ; hx.py premier retour exact 4 203. GIF : img/pixels_opposes_R506.gif (image fixe _img.png).
Commandes : python3 s2_horloge/anti_pixel2.py 1 30 ; python3 s2_horloge/anti_hx.py s2_horloge/anti2_m1.json 0 ;
python3 s2_horloge/gif_anti.py s2_horloge/anti2_m1.json 0 s2_horloge/img/pixels_opposes_R506.gif 15

## R-507 COMPTEUR 2 BITS (00, 01, 10, 11, 00, …) par deux horloges P et 2P — VÉRIFIÉ (CYCLE exact fourmi_r + hx.py premier retour 1 884)
compteur4.py : les familles d'horloges triangle (tri_cycles_rB5.json) se prolongent linéairement (T, centre, P) ; 375 paires P / 2P
(P ≥ 900, prolongées, contrôlées par CYCLE). Pose du pixel R-341 « relative au vaisseau » : on copie (vaisseau qui allume + pixel), 160 pas
avant l'allumage, depuis R-502 ; contrôle : 45 CYCLE sur l'horloge de référence. Paires où les deux horloges acceptent un pixel :
924/1 848, 942/1 884, 972/1 944. Sur ces petites horloges (famille P ≈ 1,5 T) le pixel clignote UNE fois par période.
compteur5.py : bit 0 = pixel de l'horloge P1 = 942 (6 fourmis + 2), bit 1 = pixel de l'horloge P2 = 1 884 (posée 300 cases plus loin,
déphasée de 510 pas) ; lectures toutes les P1/2 = 471 pas à partir de t = 861 ; marge = 103 pas (chaque lecture est à ≥ 103 pas de tout
changement d'état). Machine (16 fourmis ; bit 0 = fourmis 0,1 ; bit 1 = fourmis 8,9) :
  H:R2L2|-34,37,2;-32,35,5;-10,11,1;1,67,3;-66,78,5;2,8,4;-8,79,0;-69,69,2;249,53,0;249,52,3;287,79,2;235,144,4;222,92,0;236,77,3;288,93,5;220,145,1|2,8;-8,79;-69,69;1,10;-9,78;-67,68;-9,10;1,68;-67,78;1,9;-8,78;-68,69;-32,34;249,54;236,77;288,93;220,145;287,78;236,144;221,93;248,52;250,53;237,78;286,94;221,143;249,52;249,53;236,78;287,93;221,144
2 moteurs : fourmi_r CYCLE 1 884 ; hx.py premier retour exact 1 884 ; lectures hx sur 3 périodes : 00 01 10 11 00 01 10 11 00 01 10 (11).
Limite (honnête) : c'est un compteur « par construction » (deux horloges indépendantes de périodes 1 et 2), pas un compteur causal avec
retenue (le bit 1 ne « voit » pas le bit 0) ; le diviseur par 2 causal reste OUVERT (R-503, R-505 négatifs).
Commandes : python3 s2_horloge/compteur4.py 900 2200 8 ; python3 s2_horloge/compteur5.py ; python3 s2_horloge/compteur_check.py s2_horloge/compteur5.json 0

## R-508 Deux horloges triangle qui se croisent : aucune machine cyclique avec interaction — OBSERVÉ (négatif) (deux_horloges.py)
Objectif 3, version la plus simple : la « porte » = le choc d'un vaisseau de l'horloge A avec un vaisseau de l'horloge B (R-500, j = 20, P = 843
chacune ; B tournée de k crans, translatée, déphasée ; rencontre tirée au hasard, distance minimale 1 à 3 entre fourmis, recouvrement < P/4).
1 642 machines (12 fourmis), fourmi_r T = 4P : 1 529 CYCLE, 111 AUTOROUTES, 2 MIXTE. Les 1 529 CYCLE n'ont AUCUNE interaction (trajectoire
jointe = superposition exacte des deux horloges seules, contrôle hx.py) : les fourmis passent près sans toucher les cases de l'autre.
Toutes les machines où il y a vraiment eu choc se sont cassées. Explication (raisonnement) : un choc décale le vaisseau (voie ou temps) ;
au coin suivant son partenaire, lui, n'est pas décalé, et le coin (choc exact de 2 vaisseaux) rate. Commande : python3 s2_horloge/deux_horloges.py 20 20 3000 2

## R-509 Bilan des vaisseaux du demi-additionneur R-337 : 4 vaisseaux PAIRS, directions conservées, calcul par petits décalages — VÉRIFIÉ (hx.py, calcul exact)
porte_sorties.py. Entrées : K2 (dir 4, ouest), K3 (dir 0, nord-est), B = b (dir 0), A = a (dir 2, sud) : uniquement des caps pairs (classe {0,2,4},
celle des vaisseaux horaires de l'horloge triangle). Dans les 4 cas, le multiensemble des directions sortantes = celui des entrantes ; chaque
vaisseau sortant est, à ≤ 2 cases près, la trajectoire libre d'un vaisseau entrant de même direction (« ils se traversent ») :
  (0,0) K3 (1,0), K2 (1,2) ; (0,1) idem + B (0,0) exact ; (1,0) A (1,−2), K3 et K2 exacts ; (1,1) K3 (1,0), K2 (1,2), A (−2,0), B (0,1).
Donc la porte ne tourne aucun vaisseau : elle calcule par des DÉCALAGES de voie de 1 ou 2 (S et C se lisent sur des voies). Analogie : calcul
par collisions de solitons à déphasage (Jakubowski-Steiglitz-Squier, AFFIRMÉ, non revérifié). Conséquence pour la consigne 3 : récupérer les
vaisseaux = les tourner de ±120° (seul virage possible, T4 de R-347) par des coins d'horloge, et ces coins doivent absorber les décalages.

## R-510 La bascule R-341 frappée dans le mauvais état est détruite — OBSERVÉ (hx.py, toutes les phases) (mauvais_etat.py)
Vaisseau « mise à 1 » de R-502 envoyé sur R' (déjà à 1), 12 phases de R' : 11 fois les 2 fourmis du pixel partent en vaisseaux, 1 fois autre débris.
Vaisseau « remise à 0 » envoyé sur M (déjà à 0), 21 phases : 15 fois le pixel part ; 1 fois (phase 1) le vaisseau est DÉVIÉ de 60° (dir 3 → 2)
et M devient un objet immobile X de période 24 (≠ M, ≠ R'), conforme à T3 (une déviation de 60° interdit de redevenir soi-même).
Cohérent avec R-340/R-342 (aucune bascule idempotente, déjà su) : une horloge doit écrire le pixel en stricte alternance 1, 0, 1, 0.
