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

## R-511 Horloge DOUBLE (deux trains de 6 vaisseaux sur le même triangle) : 0 cycle sur 184 000 — OBSERVÉ (négatif) (double_horloge.py, double2.py)
Idée : si le 2e train est le 1er avancé de T/2 (T = P/3), la symétrie « rotation + demi-tiers » fait subir à chaque vaisseau les mêmes chocs
(2 croisements de face par arête au lieu d'1) ; la machine devrait refermer avec une période un peu plus courte. Essai : famille R-500
(j = 0, 1, 2, 3, 10, 11, 20, 40, 41 ; toutes les périodes y sont IMPAIRES, donc T/2 n'est jamais entier), puis les 461 horloges de
tri_cycles_rB5.json avec P ≡ 0 mod 6 et P ≤ 800, tous les décalages s ∈ [1, P) : 183 875 machines de 12 fourmis, fourmi_r T = 6P :
126 665 AUTOROUTES, 57 210 MIXTE, 189 INDECIS, 0 CYCLE. Les premières divergences arrivent par 3 (positions 3-symétriques), au milieu des
arêtes : c'est le croisement de face avec l'autre train, qui n'est jamais propre. Commande : python3 s2_horloge/double2.py 0 800

## R-512 HEXAGRAMME : deux horloges couplées par 6 PORTES D'INTERACTION, tous les vaisseaux récupérés — VÉRIFIÉ (CYCLE exact fourmi_r + hx.py, 47/47)
hexagramme.py : horloge triangle A (tri_cycles_rB5.json, centre de rotation = point du réseau, P ≡ 0 mod 6, P ≤ 900 : 150 horloges) +
B = A avancée de s pas puis tournée de 60° autour du centre (étoile à 6 branches), s ∈ [0, P) : 62 706 machines de 12 fourmis ; 38 175 CYCLE
dont 810 avec interaction réelle (trajectoire ≠ superposition) ; hexa_anal.py : 47 sont PROPRES (seuls événements : coins d'une horloge,
croisements, et chocs de DEUX vaisseaux, un de A et un de B ; aucun amas) : 32 horloges distinctes, 3 périodes : 978 (2 horloges de 510),
996 (2 × 522), 2 592 (2 × 522). 2e moteur : hx.py premier retour exact = période, 47/47 (hexa_check.py).
Ce qui se passe (hexa_detail.py, hexa_portes.py) : aux 6 croisements des deux triangles, un vaisseau de A et un de B (un pair, un impair, à 60°)
se tournent l'un l'autre de 120° (porte d'interaction de R-314 : c'est la porte de billard de Fredkin-Toffoli) ; les vaisseaux changent de
triangle et parcourent l'étoile + l'hexagone intérieur (img/hexagramme_978.png). Dans la machine 2 592, une même porte voit des ENTRÉES
VARIABLES d'un passage à l'autre : sur une même droite d'entrée, le vaisseau tantôt arrive seul et passe tout droit, tantôt arrive avec un
partenaire et tourne (zone 0 : droite (0,0) 3 fois « tourne », 6 fois « droit » ; droite (1,−14) 9 / 3 …) ; périodicité 3-symétrique, pas
6-symétrique (zones 0-2 : 9 chocs tournants, zones 3-5 : 3). C'est la consigne 3 sous la forme « horloges qui alimentent des portes de calcul
(ET de billard : a∧b tourne, a∧¬b tout droit) et récupèrent tous leurs vaisseaux », le cycle exact prouvant que ça tourne pour toujours.
Limite honnête : les entrées des portes sont fixées par les horloges elles-mêmes (pas d'entrée extérieure) ; la porte calcule, mais sur
un motif périodique imposé. Le demi-additionneur R-337 n'y est pas (R-509 : il faudrait l'adapter).
Machine 2 592 (12 fourmis) : H:R2L2|-5,5,4;1,38,0;-38,44,2;1,6,1;-6,44,3;-37,37,5;-6,32,5;-25,37,1;-11,18,3;-6,17,2;-10,37,4;-26,33,0|-4,5;0,39;-38,43;0,6;0,7;1,5;-6,43;-5,43;-5,44;-38,38;-37,38;-36,37;-6,18;-11,37;-25,32;-7,34;-26,36;-9,17;-6,17;-10,37;-26,33;-7,33;-25,36;-10,18
Machine 978 : H:R2L2|2,4,1;-4,43,3;-37,37,5;-5,5,4;2,36,0;-36,43,2;-6,15,2;-7,35,4;-26,34,0;-5,33,3;-26,36,5;-8,15,1|1,4;1,5;2,3;-4,42;-3,42;-3,43;-38,38;-37,38;-36,37;-4,5;1,37;-36,42;-6,15;-7,35;-26,34;-5,34;-27,36;-7,14;-5,33;-26,36;-8,15;-4,32;-26,37;-9,15;-5,14;-7,36;-27,34;-4,33;-27,37;-8,14
Commandes : python3 s2_horloge/hexagramme.py 0 900 ; python3 s2_horloge/hexa_anal.py ; python3 s2_horloge/hexa_check.py ;
python3 s2_horloge/hexa_portes.py 2592 ; python3 s2_horloge/img_hexa.py 2592
Déjà connu ? Porte d'interaction = Fredkin-Toffoli 1982 (connu) ; deux horloges de fourmis couplées en étoile : pas trouvé (non cherché sur le web, quota).
Complément R-512 (06:15) : mêmes essais sur les 248 horloges à centre entier avec P ≡ 3 mod 6, P ≤ 700 (hexagramme.py 3 700) : 113 769
machines, 58 675 CYCLE dont 1 196 avec interaction, 49 PROPRES (33 horloges ; périodes 978 (2 × 501), 996 (2 × 507), 2 475 (2 × 501)) ;
hx.py 49/49 (hexa_check.py s2_horloge/hexagramme_propres_3.json). Dans la machine 2 475, mêmes portes à entrées variables (zone 0, droite (0,0) :
6 fois « tourne », 6 fois « droit »). Total : 96 hexagrammes propres, 2 moteurs.

## Session T2 (27-11, « calcul dans la boucle ») — entrées R-513 et suivantes

## R-513 Une horloge triangle n'absorbe PAS le décalage d'UN seul vaisseau — OBSERVÉ (négatif) (t2_tolere.py)
20 horloges de tri_cycles_rB5.json (P ≥ 800, 819 et 825) ; chaque fourmi (6), prise à un instant où elle est vaisseau libre (≥ 9 cases des
autres), décalée de δ (case, distance ≤ 2) et/ou de dt ∈ [−7, 7] pas : 20 × 6 × 284 = 34 080 machines, fourmi_r T = 20 P :
34 080 AUTOROUTES, 0 CYCLE. Le décalage d'une voie que fait le demi-additionneur R-337 (R-509) casse donc toute horloge où on le met tel quel.
Commande : python3 s2_horloge/t2_tolere.py 20 800

## R-514 RÈGLE DE COMPENSATION de l'horloge triangle : δh + rot120(δa) = 0, et la taille reste libre — DÉMONTRÉ (calcul exact) + VÉRIFIÉ (596/596)
Cadre : fermeture 3-symétrique de tri.py (R-500) : un coin (A dir 0, B dir 5) → (A' dir 2, B' dir 3), puis A'(T) = R(A), R(B'(T)) = B,
R = rotation 120° + translation c. On ajoute, à chaque tiers, un décalage d'espace-temps continu δh sur l'horaire et δa sur l'anti-horaire
(δ = case + retard : un retard de dt pas = dt/8 de case le long de la direction). Avec x = position continue du vaisseau virtuel :
  (A) x(A') + δh + T·d₂/8 = rot(x(A)) + c   ⇒ c est fixé ;
  (B) rot(x(B') + δa + T·d₃/8) + c = x(B)   ⇒ T·(rot(d₃) + d₂)/8 + δh + rot(δa) = [constante du choc, = 0 pour un vrai choc d'horloge].
Or rot120(d₃) = d₅ = −d₂ : T disparaît (c'est la dégénérescence « d₂ + d₅ = 0 » de R-500, qui donne les familles de toutes tailles).
Il reste : l'horloge referme ⇔ δh + rot120(δa) = 0 (+ intégralité). Conséquences :
 · un décalage sur UN seul vaisseau n'est jamais absorbé (t2_absorbe.py : 596 chocs × 284 décalages × {h, a}, T ≤ 1 500 : seul δ = 0 referme) ;
 · un retard ÉGAL des deux (croisement de face) est toujours absorbé (d'où P = 3T − 18 / − 36) ;
 · toute paire compensée referme (t2_compense.py : 7 décalages δh dont ceux de R-509, δa = −rot120⁻¹(δh) : 596/596 chocs).
⇒ pour mettre une porte dans une horloge 3-symétrique, il faut qu'elle décale l'anti-horaire de −rot120⁻¹ du décalage de l'horaire.
Le demi-additionneur R-337 ne touche que des vaisseaux PAIRS (R-509) : seul, il ne peut pas être mis dans une horloge (cohérent avec R-508,
R-513) ; il faut une 2e porte qui décale le vaisseau impair (par ex. R-337 tourné de 60°, qui agit sur des impairs).
Statut : DÉMONTRÉ pour le modèle « vaisseaux virtuels + coin » de tri.py (calcul affine exact en fractions) ; vérifié numériquement.
Commandes : python3 s2_horloge/t2_absorbe.py 1500 ; python3 s2_horloge/t2_compense.py

## R-515 Deux horloges DIFFÉRENTES de même période, même centre (« bi-horloge ») : aucune interaction qui referme — OBSERVÉ (négatif) (bihorloge.py)
Toutes les paires d'horloges distinctes de tri_cycles_rB5.json de même P (400 ≤ P ≤ 1 000, centres compatibles), B tournée de 60° (étoile,
k = 1) ou non (k = 0), tous les décalages s ∈ [0, P) : k = 1 : 128 paires, 76 728 machines, 31 308 CYCLE, 0 avec interaction ;
k = 0 : 211 paires, 114 534 machines, 2 616 CYCLE, 0 avec interaction. Lecture (R-514) : une porte d'interaction fait CHANGER de triangle
les deux vaisseaux ; si les deux triangles ne sont pas images l'un de l'autre (hexagramme R-512 : A et rot60(A)), le vaisseau échangé
n'est pas « le bon » pour l'autre horloge et tout casse. Commandes : python3 s2_horloge/bihorloge.py 400 1000 1 ; … 400 1000 0

## R-516 ÉTOILE DÉCALÉE : horloge + son image par une rotation de 180° autour d'un point O ≠ centre — 316 machines propres — VÉRIFIÉ (CYCLE exact fourmi_r + hx.py 316/316)
etoile180.py : horloges de tri_cycles_rB5.json (600 ≤ P ≤ 1 000, une par (P, boîte) : 42), B = rot180_O(A avancée de s), s ∈ {0, P/2}
(les deux valeurs où la superposition a la symétrie d'ordre 2 « état(t + s) = rot180_O(état(t)) »), 2O entier à distance ≤ 30 demi-cases du
double du centre (sinon c'est l'hexagramme R-512) : 115 618 machines, 71 880 CYCLE, 775 avec interaction réelle ; e180_anal.py : 316 PROPRES
(événements mixtes = chocs de 2 vaisseaux, un de A, un de B), 16 horloges, toujours P = P(A) (627 … 981). 2e moteur : hx.py premier retour
= P, 316/316 (hexa_check.py). C'est une 2e famille (après R-512) de machines où deux horloges s'échangent des vaisseaux par des portes
d'interaction et récupèrent tout ; mais sans la symétrie d'ordre 3 commune : les deux triangles sont décalés (nœud papillon / étoile décentrée).
Exemple (P = 627, 12 fourmis) : H:R2L2|0,7,5;-7,28,1;-21,21,3;-5,5,4;0,23,0;-23,28,2;-41,34,2;-34,13,4;-20,20,0;-36,36,1;-41,18,3;-18,13,5|0,6;0,7;-7,28;-6,28;-22,22;-21,21;-4,5;-1,24;-23,27;-41,35;-41,34;-34,13;-35,13;-19,19;-20,20;-37,36;-40,17;-18,14
Sa porte (−11, 12), droite (3, 1) : 12 passages par période, issues D T D T … STRICTEMENT alternées ; chaque fourmi y passe deux fois de suite
(elle y tourne, fait une petite boucle de 59 à 80 pas, repasse tout droit). Écarts irréguliers (39, 59, 31, 80 par tiers) : ce n'est pas une
horloge régulière divisée par 2 (voir R-518). Commandes : python3 s2_horloge/etoile180.py 600 1000 30 ; python3 s2_horloge/e180_anal.py
s2_horloge/etoile180_600_1000.json ; python3 s2_horloge/hexa_check.py s2_horloge/etoile180_600_1000_propres.json

## R-517 Hexagramme + 3e train (même horloge, même centre) : rien — OBSERVÉ (négatif) (hexa3.py)
96 hexagrammes propres (R-512) + C = A avancée de s2 (k3 = 0) ou rot60(A avancée de s2) (k3 = 1), tous les s2 : 89 691 machines (18 fourmis),
1 seul CYCLE (P = 1 020 = 2 × 510) : faux positif, A (P 510) + un petit oscillateur de période 60 formé par B et C collés (ppcm = 1 020).

## R-518 Diviseur par 2 dans une machine à symétrie « tiers » : ce qu'il faudrait — AFFIRMÉ (argument) + recherche (t2_portes.py, t2_regulier.py)
Critère cherché : une droite d'entrée de porte à passages RÉGULIERS (écarts égaux) dont l'issue alterne T, D, T, D (le vaisseau horloge tourne
quand le bit est là, passe sinon). Résultat : 0 sur les 96 hexagrammes (R-512) et les 775 étoiles décalées (R-516) (écarts tolérés jusqu'à
60 pas : seulement des motifs « T D T » répétés par tiers, ou « D T D T » irréguliers).
Argument : si état(T) = R(état(0)), la suite vue par une porte X sur une période est la concaténation de ce que voient X, R⁻¹X, R⁻²X pendant
un tiers ; une alternance régulière demande un nombre PAIR de passages par tiers sur la même droite, donc ≥ 2 vaisseaux par tiers sur un même
côté (deux trains : R-511, toujours cassé) ; deux horloges de périodes T et 2T n'ont aucune symétrie commune (2 ≢ 1 mod 3) et deux horloges
concentriques de rapport 4 (le premier rapport compatible, 4 ≡ 1 mod 3, diviseur par 4) ne se croisent pas (côté ∝ T). OUVERT.

## R-519 Pourquoi le demi-additionneur R-337 n'entre pas dans une horloge : une porte sur UN seul côté n'est jamais absorbée — DÉMONTRÉ (sous hypothèse) ; R-337 dans des horloges concentriques — AFFIRMÉ
Horloge « déformée » : on cherche une machine où chaque coin est le MÊME choc qu'avant, seulement translaté d'un vecteur d'espace-temps u_k
(k = 1, 2, 3), et chaque croisement de face du même type. Sur un côté sans porte, l'horaire impose u_{k+1} − u_k ∈ Z·(d_h, 8) et
l'anti-horaire u_{k+1} − u_k ∈ Z·(d_a, 8) : deux droites distinctes de Z³ ⇒ u_{k+1} = u_k. Avec une porte sur un seul côté, les deux autres
côtés donnent u_1 = u_2 = u_3, puis les coins du côté à porte imposent δh ∈ Z·(d_h, 8), δa ∈ Z·(d_a, 8) : décalage NUL (le vaisseau
avancé le long de sa propre route). Donc une porte qui décale doit être répétée sur les trois côtés (cas 3-symétrique, R-514, avec la
compensation δh + rot120 δa = 0), ou changer le type d'un coin (non couvert par l'argument). Cohérent avec R-513 (0 / 34 080).
R-337 : ses 3 droites d'entrée (B et K3 : x + y = 0 ; A : x = 30 ; K2 : y = −24) forment un PETIT triangle (côté ≈ 6) orienté comme une
horloge ; pour que trois horloges concentriques 3-symétriques de même T aient chacune un côté sur l'une de ces droites, il faudrait
ρ₁ + ρ₂ + ρ₃ ≈ 3 × (rayon du petit triangle) ≈ 5 cases (ρ = distance du centre au côté) : impossible si les trois sont « horaires »
(chaque ρ ≥ ~ 6) ; il faudrait mélanger des horloges tournées de 60° avec un rapport de tailles ≈ 2 à même période (observé au plus 1,76 :
P = 507, côtés 25 à 44). De plus il faut la porte compensatrice (R-337 tourné de 60°) sur les vaisseaux impairs. Objectif 1 avec R-337 : OUVERT,
avec ces obstacles. (Objectif 1 avec une porte R-314 : déjà fait par R-512 et, sans symétrie commune, par R-516.)

## R-520 Le bit M de R-341 DÉPHASÉ par un vaisseau qui passe EXACTEMENT ; deux vaisseaux identiques de suite : rien ne casse — VÉRIFIÉ (fourmi_r + hx.py 256/256, temps fini) (tbascule.py, tb_filtre.py, tb_hx.py)
Relâche de R-503 (bascule T par des vaisseaux identiques, sortie exacte exigée) : 508 objets à 2 fourmis (cycles exacts, boîte ≤ 5, p ≤ 200),
1er vaisseau direction 0 sur les voies −7…7, toutes les phases relatives : 813 600 tirs ; 54 936 ont un effet (tb_filtre.py) : 48 560 « objet
changé + vaisseau retardé », 6 112 « objet changé + vaisseau décalé de voie », 232 « objet changé + vaisseau exact », 32 « objet seulement
DÉPHASÉ + vaisseau exact ». 2e vaisseau identique Δ ∈ [200, 200 + 8 p1) derrière (10 463 conversions distinctes, 1 227 096 flux) : 256 flux où
les deux vaisseaux ressortent exacts et l'objet est dans l'orbite de X0 au même endroit ; ce sont 4 objets seulement, tous du type « déphasé » :
M de R-341 tourné de 2 et de 5 crans (période 21, Δ ≡ 18 mod 21) et un objet de période 30 (Δ ≡ 18 mod 30). Attention : « revenu dans
l'orbite » ne veut pas dire « revenu à la même phase » ; c'est un DÉPHASEUR (le vaisseau ne voit rien, l'objet avance ou recule de phase),
pas encore une bascule T. Aucun objet n'est changé en un AUTRE objet puis remis par un vaisseau identique (0 / 1 227 096) : R-503 confirmé
pour ces 508 objets, même en acceptant des vaisseaux retardés.

## R-521 DOUBLEMENT DE PÉRIODE par la mémoire de phase : horloge (P = 1 131) + bit M → machine de période 2 262 = 2 P — VÉRIFIÉ (CYCLE exact fourmi_r + hx.py premier retour 2 262)
t2_tb_horloge.py : on pose les 4 objets de R-520 (puis les 30 « vaisseau exact » de tb_filtre) relativement aux vaisseaux de toutes les horloges
de tri_cycles_rB5.json (P ≤ 1 200) : 468 000 + 78 867 machines ; CYCLE de période P (pixel synchronisé, comme R-502), 5P ou 7P (objet non touché,
ppcm des périodes) et 72 + 3 de période 2P. Les 3 de P = 414 (objet de période 12) sont triviales (ppcm(414, 12) = 828 : la phase avance comme
sans vaisseau). Les 72 de P = 1 131 (8 écritures de la même horloge × 9 poses, objet = M tourné) sont VRAIES : à chaque tiers l'horaire fait
passer M dans un autre état (période 21 aussi) et l'anti-horaire le remet ; les vaisseaux ressortent exacts (12 pas sur 2 262 où une fourmi
de l'horloge s'écarte, pendant un passage) ; la phase de M au début de chaque tour vaut 0, 18, 0, 18… alors que sans interaction elle ferait
0, 18, 15, 12… (ppcm(1 131, 21) = 7 917). Le « bit » (phase 0 ou 18) change à CHAQUE tour : s ← s ⊕ 1, causé par l'horloge, et la machine
ne revient qu'après 2 tours. Machine (8 fourmis) :
  H:R2L2|-21,24,4;-23,25,3;2,14,0;-14,50,2;-34,34,4;-13,14,1;1,35,3;-34,49,5|2,13;-13,50;-35,35;-12,13;1,36;-35,49;-22,24;-23,25;-21,24;-22,26;-23,26
Limite honnête : la bascule n'ÉMET rien (les vaisseaux ressortent exacts) ; elle ne peut donc pas piloter une 2e bascule : le compteur
causal à 2 étages reste OUVERT. Commandes : python3 s2_horloge/t2_tb_horloge.py 1200 ; python3 s2_horloge/t2_tb_check.py
s2_horloge/t2_tb_horloge.json 0 ; python3 s2_horloge/t2_classes.py s2_horloge/t2_tb_horloge.json 0 0 30 60 90 120
