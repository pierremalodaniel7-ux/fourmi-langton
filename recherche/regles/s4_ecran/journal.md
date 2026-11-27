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

## R-708 Sondes de lecture du pixel M/R' à 1 vaisseau — VÉRIFIÉ (hx.py, balayage complet) (sonde_scan.py, sonde_retour.py → sondes.json, sondes_retour.json)
6 directions × voies −8..8 × toutes les phases, sur M (21) et R' (12) : M reste M 1 560 fois, R' reste R' 912 fois (toujours sortie = entrée,
comme R-346) ; M → X périodique 71, R' → X 56 ; M → rien + 3 vaisseaux 17 (lecture R-335). Sondes UTILES = transparentes sur R' pour
les 12 phases ET M → X avec sortie différente : (dir 0, voie −3, M ph 6 → X période 21, retour X → M par 1 vaisseau dir 3 voie 1),
(dir 3, voie 2, ph 8 → X 15, retour dir 0 voie −3), (dir 4, voie 2, ph 15 → X 9, retour dir 1 voie 1). Lecture = TEMPS DE VOL :
la sonde ressort sur sa route, à l'heure si ON, 3 pas en avance si OFF (option 0).

## R-709 Lecture d'un pixel : une lecture VÉRIFIÉE ; lecture + réécriture répétée : ÉCHEC (cause identifiée) (lecture_simple.py, lecture_demo.py)
Une lecture (2 moteurs) : ON → sonde à l'heure, R' intact ; OFF → sonde 3 pas en avance, le pixel devient X. Réécriture X → M : le
vaisseau de retour arrive DE FACE sur la route de sortie de la sonde (écart de voie 1 ; même chose pour les 3 options : le retour est
presque le film à l'envers de la déviation) ; avec tout posé à t = 0 ils se croisent forcément, et le croisement n'est jamais
transparent (60 décalages d'une période de X, toutes les phases relatives, 3 options) ⇒ pas de « lecture + réécriture » réutilisable
avec ces sondes (OBSERVÉ). Par adresse : il faudrait en plus 2 ports (sonde, retour) dont les sorties passent par des points DÉJÀ fixés
(4 équations, 2 inconnues) ⇒ à choisir en même temps que l'écran. OUVERT.

## R-710 Écran 4×4 = 4 blocs 2×2 (R-707) translatés de b·400·(D0 + D1), retards fixes (GAP 1 600) : ÉCHEC — OBSERVÉ (2 moteurs) (ecran4_demo.py, 27/11 05:55)
Blocs alignés en direction 30° (bissectrice de 2 directions de vol) : chaque route d'un bloc passe à ≥ 309 (distance hex exacte) des
pixels des autres blocs. Chaque bloc seul et chaque paire de blocs : justes. Tout ensemble : pixels du bloc 2 cassés (« ? ») dès le
dessin 1. Cause isolée : les vaisseaux d'ENTRÉE des opérations FUTURES du bloc 0 (posés à t = 0 loin en amont) croisent des débris
des opérations passées ; le choc produit un vaisseau qui atteint le bloc 2. ⇒ les retards ne peuvent pas être choisis « à l'aveugle ».

## R-711 ÉCRAN 4×4 R2L2 : « visage » puis « anneau » puis tout éteint, 16/16 pixels justes aux 3 lectures — VÉRIFIÉ (2 moteurs + contrôle exact des étiquettes, temps fini) (ecran4_glouton.py → ecran4_glouton.json, ecran4_dessin_1..3.png, 27/11 06:00)
Même géométrie que R-710 ; retards choisis par un glouton : pour l'opération k, premier retard (compatible avec la phase du pixel)
tel que la simulation des opérations 0..k à d + 2 000 donne (a) les 16 pixels dans l'état voulu, (b) un reste qui se décode en
vaisseaux libres dont les étiquettes sont EXACTEMENT celles prévues par le calcul de trajectoires (aucune interaction imprévue).
20 opérations (6 + 6 + 8), 90 fourmis posées à t = 0 ; 18 opérations au 1er essai, op 8 : 8 essais, op 11 : 43 essais (retards refusés
= collisions de vaisseaux en vol). Lectures t = 9 606, 19 261, 34 117 : lu = attendu, fourmi_r = hx.py ; contrôle final des étiquettes
à t = 34 117 : exact. Durée 4 s. Adressage : 2 bits (a1 a0) décodés par le démux du bloc ; le BLOC (2 bits de poids fort) est choisi
par la ligne d'entrée (où l'on tire), pas encore par un démux devant (OUVERT). Simulation finie : aucune affirmation au-delà de t = 34 117.

## R-712 Après une lecture « OFF » (M → X), remise en état par les PORTS D'ÉCRITURE : impossible avec 1 vaisseau — OBSERVÉ (hx.py, balayage) (lecture_kits.py → lecture_kits.json, 27/11 06:05)
3 sondes utiles (R-708) × 4 voies de kit (SET0, SET5, RST2, RST3 = les seules droites que les démux de l'écran savent viser) × retards
Δ = 20..149 (toutes les phases de X, plusieurs fois) : 0 issue propre en M ou R' (X reste un autre objet, ou disparaît en vaisseaux).
Contrôle : sans sonde, SET0 au bon retard donne bien R'. ⇒ une lecture « OFF » abîme le pixel tant qu'on n'a pas un port de retour en plus.

## R-713 Port de LECTURE par adresse (3e démux dont les 4 sorties suivent des droites de sonde) pour les écrans 2×2 trouvés : aucun — VÉRIFIÉ (calcul exact) (lecture_geo.py, 27/11 06:10)
49 démux × 6 rotations × 24 permutations × 6 droites de sonde par pixel (les 3 utiles de R-708 + (1,−3) sur M, (0,2) et (3,−3) sur R',
lisibles mais destructives) ; translation v entière quelconque ; sortie en aval du démux. Pour les 20 meilleurs placements de R-706
(dont celui de R-707) : 0 solution (les 4 équations de voie ne sont jamais compatibles). Contrôle du solveur : retrouve le port
d'écriture A (v = 0). ⇒ il faut choisir l'écran ET le port de lecture ensemble (OUVERT, à suivre).

(Session T4 « écran de la fourmi », 27/11 à partir de 10:55 UTC, branche claude/t4-ecran-fourmi ; fichiers dans t4/.)

## R-714 Écran + port de lecture choisis ensemble (lecture_joint.py) — AFFIRMÉ (d'après rapports/S4_ECRAN_2026-11-26.md, non relancé)
Session S4 précédente (06:10) : 42 configurations à démux A = B, 0 solution ; recherche non terminée (entrée écrite par T4).

## R-715 L'ÉCRAN BRANCHÉ SUR LE PAS : 4 pixels sur les 4 sorties c00' c10' c01' c11' du pas complet R-617 — VÉRIFIÉ (2 moteurs, 256/256) (t4/ecran_un_pas.py, 27/11 11:00)
Les 4 sorties de cases du germe R-617 vont toutes en direction 0 (routes parallèles). Sur chacune, un pixel M (OFF) posé à t = 0,
kit de mise à 1 SET0 (R-705) aligné exactement sur la sortie (t4lib.kit_on), à 20 à 57 cases après la position de la sortie à
TDEC = 11 404, à ≥ 20 (distance hex) de toutes les autres routes (t4/rayons.py : 333 segments = entrées des 256 états + rayons décodés).
Le vaisseau c_ij' (présent ssi c_ij' = 1) allume le pixel en passant. 256/256 états : écran lu (état ET phase exacts) = (c00', c10',
c01', c11') de R-61, reste = vaisseaux libres décodés ; moteur C 256/256 ; hx.py identique sur 64 états (les 16 états de cases avec
x = y = h = 0 + 48 au hasard). T = 12 686. Placement : t4/placement.json. Pas de démultiplexeur : un pixel par sortie (choix noté :
l'adressage R-707 servirait à écrire un pixel choisi, ici chaque case a déjà son propre vaisseau).
Limite (comme R-707) : la mise à 1 suppose le pixel éteint ; une 2e écriture demande de connaître l'état (voir R-716).

## R-716 Pas d'effacement ni de remplissage « aveugle » à 1 vaisseau — VÉRIFIÉ (hx.py, balayage) (t4/effacer_scan.py, t4/remplir_scan.py)
Les 2 droites de mise à 0 (dir 2 voie −2, dir 3 voie −2) jouées sur M à ses 21 phases : M est TOUJOURS détruit (aucun « M reste M »).
Les 2 droites de mise à 1 (dir 0 voie 1, dir 5 voie 1) sur R' à ses 12 phases : R' toujours détruit. Avec R-705 (seules droites qui
écrivent), aucune écriture à 1 vaisseau n'est idempotente ⇒ pour réafficher, il faut un vaisseau qui dépend de l'état affiché.

## R-717 Boucle d'effacement à 2 chocs (0 -> 4 -> 2, vers RST2) : impossible par les phases — OBSERVÉ (calcul exact, t4/boucle_geo.py, 27/11 11:08)
Idée : le vaisseau c_ij' qui a allumé le pixel continue tout droit ; 2 chocs du catalogue R-700 (chacun avec 1 vaisseau horloge posé
à t = 0) le ramènent sur la droite de mise à 0 du MÊME pixel ⇒ le pixel s'éteint ssi il était allumé (effacement « qui dépend de l'état »).
Géométrie : triangle 0, 4, 2 (côtés égaux) ; voie de sortie affine en (n1, n2) ; délai u = arrivée du retour − (a1 + 720).
Catalogue filtré (48 chocs) : u ≡ 0 (mod 12) pour 2 304 familles ; catalogue complet (224, 126 virages distincts) : u ≡ 0, 3, 6, 9 (mod 12),
15 876 familles. R' doit être en phase 2 (u ≡ 2) ou, avec SET0b, 1 : jamais ≡ 0 mod 3 ⇒ aucun. Idem kit SET5/RST3 (pixel tourné).

## R-718 Boucle d'effacement à 3 chocs (0 -> 4 -> 2 -> 3, vers RST3) — OBSERVÉ (moteur C, 256/256 pour chacun des 4 pixels, 1 usage) (t4/boucle3.py, t4/boucle_choix.py)
Avec un virage de +60° en plus, u prend toutes les valeurs mod 12. Phases (SET0a, RST3a/b, D ≡ 0 mod 21) ⇒ u ≡ 22 ou 23 (mod 84).
Retenu (même forme pour les 4 pixels) : chocs [158, 217, 22] du catalogue complet, u = 1 282, vaisseaux horloges posés à t = 0
(ordre de jeu imposé par chaque choc, t4/boucle_choix.order). Pixel + germe + boucle, 256 états : allumé ssi c' = 1 puis éteint
(M, phase prévue au pas près), reste propre. Fichiers t4/boucle_c00.json … boucle_c11.json.

## R-719 Deux pas de suite avec les boucles COURTES de R-718 : pas 1 juste, effacement juste, pas 2 FAUX (cause trouvée) — OBSERVÉ (2 moteurs sur l'exemple) (t4/ecran_deux_pas.py, t4/dbg_deux.py, dbg2.py, dbg3.py, 27/11 11:12–11:35)
UNE simulation par état (189 fourmis, usage 2 retardé de D = 384 888, entrées = R-61(s0)) : lecture t_A = 12 666 (écran = c') 256/256,
t_B = 14 638 (tout éteint) 256/256 (moteur C) ; t_C = 397 574 : faux (ex. s0 = 0 : c00'' absent). Sans pixels ni boucles, l'usage 2
donne bien c00'' (hx.py). Cause : après la mise à 0 RST3, le vaisseau de retour repart en direction 3, sur une voie voisine (écart 1-2)
de la route d'ENTRÉE de la puissance du module c00 à l'usage 2 ⇒ choc de face vers 24 000 cases (ce que la condition « voies opposées »
de R-617 interdit pour les débris du germe). D plus grand (420 000) : même échec (les deux s'éloignent/approchent à la même vitesse).
Défaut secondaire : avec une boucle courte, l'écran montre c' seulement ≈ 1 300 pas, puis s'éteint jusqu'au pas 2.
⇒ boucle LONGUE (u ≈ D − 1 440 − δ, l'écran garde c' presque tout l'intervalle) finissant sur RST2 (retour en direction 2) : R-720.

## R-721 Chocs SÉLECTIFS EN TEMPS : 16 des 224 chocs propres deviennent transparents si le signal arrive 3 pas plus tard — VÉRIFIÉ (2 moteurs, 16/16) (t4/choc_selectif.py → t4/choc_selectif.json, 27/11 12:00)
Pour lire un pixel (la sonde R-708 option 0 ressort 3 pas en avance si OFF) : un tel choc dévie la sonde « OFF » et laisse passer
la sonde « ON ». Types trouvés : virage du signal −120° (horloge à 60°) ×8, +120° ×8. (Finalement non utilisé : l'option 2 sépare
déjà ON et OFF de 2 voies, R-722.)

## R-720 Boucles d'effacement LONGUES (0 -> 4 -> 3 -> 2, vers RST2) — OBSERVÉ (hx.py, 2 usages, 4 états par pixel) (t4/boucle_long.py, t4/conflits.py, 27/11 11:40–12:05)
u ≈ D − 1 440 − δ (δ ∈ [300, 3 000]) : l'écran garde c' presque tout l'intervalle, s'éteint juste avant le pas 2. Retour en direction 2
(jamais de face avec une entrée de l'usage 2). Phases (SET0a, RST2, D ≡ 0 mod 168) : u ≡ 14 (mod 84). Recherche affine exacte
(entiers) puis 3 filtres : (1) géométrie (t4/conflits.py : distances min. exactes à ±2 entre trajectoires rectilignes, vectorisé)
contre le germe (2 usages) et les 4 pixels ; (2) pré-test hx.py de la boucle seule (horloges seules jusqu'à D + 13 000 : propre ;
signal + horloges : le retour est exactement sur RST2) ; (3) 2 usages + pixel, 4 états (c', c'') = (1,1), (1,0), (0,1), (0,0).
Pièges rencontrés : une horloge à 60° du front des sorties parallèles heurte TOUJOURS un débris voisin du module (décalages (−32, 32) et
(23, 23) en (latéral, abscisse), sur les diagonales à 60°) ; horloge parallèle au signal dévié (rel. 4) : sans signal elle file avec le
« fantôme » du signal et croise l'horloge suivante (souvent proprement : à tester par simulation, pas par distance).
Retenu (mêmes chocs pour les 4 pixels, catalogue complet n° 68, 115, 196) : u = 380 534, D = 384 888. Fichiers t4/boucle_long_*.json.
Vérification complète (4 pixels, 12 horloges, 256 états, 2 moteurs) : t4/deux_pas_long.py (en cours).
