# Journal « quelle règle pour un ordinateur réutilisable ? » (nuit du 25/11, session séparée)
Numéros R-300 et suivants (à fusionner dans journal.md au matin). Moteur : `fourmi_r` = copie de `src/fourmi.c`
+ options `-x` (exactement T pas), `-dump` (état final en format situation), `-z` (arrêt quand la grille est toute blanche),
grille triangulaire `T:` (lettres R L U ; 6 caps, voir l'en-tête de fourmi_r.c). Oracle src/oracle.txt : 13/13 identiques.
Compiler : `gcc -O2 -w -o fourmi_r fourmi_r.c` (dans recherche/regles).

## R-300 La gomme : condition exacte — DÉMONTRÉ (preuve courte ci-dessous) + VÉRIFIÉ (moteur, 78/78 essais) (gomme.py, gomme2.py)
Énoncé. Une fourmi (règle K = (K_0, …, K_{q−1}), virages dans le groupe des caps Z_M, demi-tour = +M/2) a joué T pas.
On la pose sur la case qu'elle vient de quitter, cap retourné, et on la laisse jouer T pas avec la MÊME règle.
La grille revient à son état de départ POUR TOUT T ET TOUT DÉPART ⟺ q = 2 et K_1 ≡ −K_0 (mod M) (ou q = 1, trivial).
Preuve (⇐) : invariant « fourmi sur la case y, cap = inverse du cap avec lequel elle avait quitté y, case y = couleur c+1 ».
Elle lit c+1, tourne de K_{c+1}, la case passe à c+2 = c (q = 2) : la case est remise ; nouveau cap = d + K_c + M/2 + K_{c+1}
= d + M/2 (car K_0 + K_1 ≡ 0) = inverse du cap d d'arrivée sur y ⇒ elle va exactement sur la case précédente. Récurrence.
Preuve (⇒) : q ≥ 3, T = 1 depuis le blanc : la gomme lit 1 et écrit 2 ≠ 0 ⇒ échec. q = 2, K_0 + K_1 = s ≢ 0, T = 2 depuis le blanc :
la gomme efface x_1 mais part vers une case y ≠ x_0 (blanche) qu'elle noircit ⇒ 2 cases noires ⇒ échec.
Règles qui ont la gomme (non triviales) : carré RL (= LR) ; hexa (1,5) = R1L1 et (2,4) = R2L2 (+ miroirs) ; TRIANGLE RL.
Triviales : NN, UU (le mouvement ne dépend pas de la couleur). Précision sur « M pair » : sur un réseau, le demi-tour existe
toujours (on repasse par l'arête d'entrée) ; sur le triangle (3 arêtes) il existe aussi (caps dans Z_6). La vraie condition
est seulement q = 2 et « virage sur noir = inverse du virage sur blanc ».
Balayage (gomme2.py, 6 essais par règle : T au hasard 500–6 000, pairs et impairs, blanc ou 5 cases au hasard) :
q = 2 condition vraie : 13 règles, TOUJOURS ; condition fausse : 48 règles, JAMAIS 33, PARFOIS 15 (toutes à mouvement
quasi indépendant de la couleur : RR, LL, UR, H:R1R1… : coïncidence de parité, échouent pour d'autres T) ; q = 3 : 280 règles,
jamais « toujours » (8 « parfois », même cause). Données : data/gomme2.txt.
Déjà connu : la réversibilité de la fourmi de Langton (et le retour en arrière en retournant la fourmi) est classique
(modèle « flipping rotators » des gaz de Lorentz, Cohen-Wang 1995 ; cf. deja_connu.md) ; l'énoncé général « q = 2 et K_1 = −K_0 »,
hexa et triangle compris : pas cherché plus loin que ces sources (voir R-302).
Commande : `python3 gomme.py 20000 ; python3 gomme2.py`

## R-301 Effacer pour q ≥ 3 ? — DÉMONTRÉ (lemme de comptage) + OBSERVÉ (négatif, 0/9 072 essais) (gomme3.py)
Lemme : la couleur d'une case = couleur de départ + nombre de passages (mod q). Une grille revient à son état ⟺ chaque case
a été visitée un multiple de q fois. Une trace laissée par 1 passage demande donc q − 1 passages de plus SUR CHAQUE CASE.
Pour q ≥ 3 aucune fourmi de la même règle ne peut « défaire un pas » : défaire = décrémenter la couleur, or toutes les fourmis
incrémentent. Le renversé de K est la règle K̃_j = −K_{−j−1} lue avec les couleurs renommées c → −c : c'est la même règle sur la
même grille seulement si q = 2 (renommage = identité) — d'où R-300.
Reste un seul moyen général : la périodicité. Un système borné revient à son état de départ (R-44) ⇒ il efface tout, mais
« globalement » (après un cycle complet), pas à la demande.
Essais (gomme3.py) : après T = 20, 100, 1 000 pas (départ blanc), 1 effaceuse posée sur chaque case à distance ≤ 3 et chaque cap
(196 carré / 294 hexa-triangle), puis gomme + 1 2e fourmi (100 / 150), ≤ 200 000 pas, arrêt dès que la grille est blanche (-z) :
RL : 1/196 (c'est la gomme), 0 paire ; LLR, LLLR, RLLR, LLRRRL, H:R1R2, H:R1L2, H:R1R2L1, T:RLL : 0 partout.
Avec R-66 (3 autoroutes LLR sur la même voie ne lavent rien) : en q ≥ 3, PAS DE GOMME LOCALE connue. OUVERT : gomme à plusieurs fourmis
bien synchronisées (q − 1 passages exacts) — le lemme ne l'interdit pas.
Commande : `python3 gomme3.py`

## R-302 Littérature (1re passe, 25/11 00:40) — voir deja_connu.md (lignes à ajouter au matin)
3 recherches web : (1) « time-reversible generalized Langton's ant » : la réversibilité (le passé est déterminé, fourmi
« symétrique en temps », retour en arrière) est CONNUE (Gajardo et al., Algorithms 4(1) 2011 « Recognizing the repeatable
configurations of time-reversible generalized Langton's ant is PSPACE-hard » ; ci2ma pp11-28) ; condition générale sur la règle
(q = 2, K_1 = −K_0, hexa/triangle) : PAS TROUVÉE énoncée. (2) « generalized ant highways / hexagonal turmite » : LLLR a deux
autoroutes 52 et 156 (arXiv 2506.10482) — retrouvé ici (14/2 626) ; LLRRRL infinité d'autoroutes (arXiv 2505.05426) — retrouvé
(896, 992, 800, 1 088) ; rien sur les périodes hexagonales. (3) « highway collision logic gates » : rien d'autre que Gajardo-Moreira-Goles
(1 fourmi). (4) « hexagonal ant 120° glider no trace » : rien (blog scipython, Wikipedia : mention des virages ±60°/±120°).

## R-303 Départ blanc, 130 règles (carré 8, hexa q=2 et q=3 à miroir près, triangle q=2 et q=3), T = 2^22 — OBSERVÉ (scan_blanc.py)
29 autoroutes, 28 cycles (toutes à U ou triangle à U : mouvement borné), 73 indécises. Données : resumes/scan_blanc.txt.
Autoroutes depuis le blanc : RL 104 (9 977), LLR 18 (39), LLLR 52 (79), L4R 68, L5R 84, L6R 100 ; hexa q=2 : R2L2 A8 (début 2),
R2N A4, UN A3 ; hexa q=3 : R2R1R1 A25, R2L2L2 A98, R2R2L2 A25, R2UL2 A12, R2NR1 A54 (672 364), R2UL1 A1863 dans la direction (11,4) (!),
R2L2R1 A75 (1,5 M), R2R2R1 A1940 (5,1), R2L1R1 A5… Sans autoroute (2^22) : LLRRRL, RLLR, hexa R1L1, R1R2, R1L2, R2R1, R2L1, triangle RL.

## R-304 FIL : petites configurations (fourmi + 0 à 3 cases dans [-2,2]², 2 626 par règle, 2^20 pas) — OBSERVÉ (fil_petits.py)
Part qui donne une autoroute / début médian : RL 100 % / 1 869 ; LLR 100 % / 47 ; LLLR 100 % / 79 (dont 14 en A156) ; L4R 100 % / 103
(105 en A34) ; L5R 100 % / 127 ; L6R 100 % / 151 (3 en A50) ; LLRRRL 4,2 % / 270 955 (A896, A992, A800, A1088) ; RLLR 0 % ;
hexa R2L2 100 % / 2 ; R2N, UN, R2R2L2, R2L1R1 100 % / ≤ 5 ; R2UL2 98 % (48 cycles) ; R2R1R1 100 % / 1 483 ; R2L2L2 100 % / 298 ;
R2UL1 96 % / 62 990 ; R2R2R1 83 % ; R1N 8,6 % ; R2NR1 6,6 % ; R1L1, R1R2, R1L2, R2R1, R2L1 : 0 % ; triangle RL 0 % (6 cycles), RRL 0,15 %.
Résumé : resumes/fil_resume.txt.

## R-305 Germes lanceurs (autoroute dès le départ, début ≤ 2P), glouton = MAJORANT du germe minimal — OBSERVÉ (germe.py)
RL 10 cases (R-20 : 11 avec début 0 ; ici on tolère ≤ 2 périodes de mise en route) ; LLR 2 ; LLLR 4 ; L4R 4 ; L5R 4 ; L6R 3 ; LLRRRL 49 (A896) ;
hexa R2L2 1 ; R2N 1 ; UN 1 ; R2R2L2 1 ; R2UL2 1 ; R2L1R1 1 ; R2R1R1 4 ; R2L2L2 3 ; R2NR1 7 ; R1N 11 ; R2R2R1 10 ; R2UL1 36.
Fichier : resumes/germes_regles.json (fourmi en (0,0), cases, P, D).

## R-306 Le VAISSEAU hexa R2L2 (fourmi + 1 case, période 8, 1 case par période en diagonale) — DÉMONTRÉ (certificat dès t = 0)
H:R2L2 = hexa, blanc → +120°, noir → −120°. Germe : fourmi 0,0 cap 4 + case 1,0. `./fourmi_r -cert "H:R2L2|0,0,4|1,0"` → CERT 0 |V|=4.
Il ne laisse AUCUNE trace : 1 seule case non blanche dans toute la grille après 200 ou 400 périodes (trace.py) ; depuis le blanc,
4 cases au total après 10^5 pas (3 portées + 1 laissée au départ). Même chose pour H:R2UL2 (q=3, période 12, CERT 0, 0 case/période).
Toutes les autres autoroutes laissent une trace : RL 12 cases/période, LLR 2, LⁿR 6, LLRRRL 58, R2UL1 158 (trace.py, resumes/trace.txt).
Déjà connu ? Le vaisseau à 4 fourmis RL (2c/12) est connu ; un vaisseau à UNE fourmi sans trace en hexa ±120° : pas trouvé (R-302 (4)).
Remarque : avec des virages ±120° la fourmi n'utilise que 3 caps sur 6 (classe paire ou impaire) ; c'est le « bon » réseau pour une
fourmi à 3 directions — probablement connu des amateurs (HexTurmite de Golly), à vérifier avant de dire « nouveau ».

## R-307 / R-308 Déviation par obstacles fixes et réutilisation — OBSERVÉ (banc.py, miroirs.py, murs.py)
Protocole commun : germe en (0,0) ; obstacle sur la voie K = 30 périodes plus loin ; 1 case (chaque case visitée dans une période),
2 cases voisines, 1 à 3 cases dans une fenêtre 5×5 (2 625), murs de 5 à 33 cases pleins/pointillés selon chaque axe (144 à 192).
Réutilisation : une 2e autoroute identique, 10 périodes devant (elle touche l'obstacle d'abord) ; on compare la sortie de la 2e à la 1re.
RÉSULTAT PRINCIPAL : pour TOUTES les règles qui laissent une trace (RL, LLR, LⁿR, R2N, …), la 2e autoroute ne ressort JAMAIS sur la même
voie que la 1re : 0 / 2 540 (RL), 0 / 2 383 (LLR), 0 / 1 998 (LLLR), 0 / 2 140 (L4R), 0 / 2 050 (R2N), murs : 0 partout.
(Elle ressort parfois dans la même direction : RL 549, LLR 894, R2N 2 050 sur 2 050 — mais décalée.) Cause : la 2e roule sur la trace de la
1re et est déviée AVANT d'atteindre l'obstacle (LLR : comme R-66). ⇒ en RL et LⁿR un fil n'est pas réutilisable tel quel.
Hexa R2L2 : aucun obstacle fixe ne le dévie (2 625 + 144 murs : il passe toujours dans la même direction ; 272 obstacles le DÉCALENT
d'une voie) ; ces décaleurs sont réutilisables : 272 / 272 avec 10 périodes d'écart (102 / 272 à 3 périodes : les 2 vaisseaux se gênent).
Fichiers : data/banc_*.json, data/miroirs_*.json, data/murs_*.json (non versionnés), résumés dans resumes/.

## R-310 Chocs de 2 vaisseaux R2L2 — OBSERVÉ (collisions.py, 1 215 chocs : 5 angles × 3 instants × 81 décalages)
AUCUN choc ne détruit un vaisseau : 0 / 1 215 « autre » ; transparents 791, décalés 46 (face à face), déviés 337, fusion en
vaisseau double (A8 × 2) 41. Types de déviation (angle d'arrivée r, sortie B, sortie A) : (60°, −120°, +120°) 54, (60°, +120°, −120°) 27,
(60°, 0, +120°) 27 [B continue, A tourne], (120°, ±120°) 54, (240°…) 67, (300°…) 108. C'est la « porte d'interaction » des boules de billard
(Fredkin-Toffoli 1982) : si A et B sont là, ils tournent ; si un seul est là, il continue tout droit.

## R-311 Gomme COLLECTIVE : remise à zéro exacte d'un circuit entier — DÉMONTRÉ (même preuve que R-300) + VÉRIFIÉ (gomme_collective.py)
Avec n fourmis jouées l'une après l'autre : retourner chaque fourmi (case qu'elle vient de quitter, cap inversé) ET inverser l'ordre de jeu.
Preuve : la suite des pas élémentaires est défaite dans l'ordre inverse ; chaque pas défait est un pas de gomme (R-300), la grille étant
exactement celle qui suivait ce pas. VÉRIFIÉ : les 28 portes RL d'ordinateur/germes_ordinateur_2026-11-17.json (NON, NOR, ET, COPIE, OU,
CROISEMENT, demi-additionneur, toutes entrées), 3 000 et 20 000 tours : 56/56 remises à zéro exactes ; l'ADDITIONNEUR 4 BITS
(recherche/ordinateur/germe_ordinateur.json, 8 fourmis, 140 cases) après 420 000 tours (toutes les lectures faites, 383 972 cases changées) :
remis à zéro, 0 case différente. Situations au hasard (2 à 6 fourmis) : RL 40/40, H:R2L2 40/40, T:RL 40/40, H:R1L1 40/40 ; LLR 0/40, H:R1R2 0/40.
⇒ En RL (et R2L2) un ordinateur À USAGE UNIQUE devient RÉUTILISABLE : calculer, lire, tout retourner, attendre le même temps → état initial,
on change les entrées, on recommence. Défaut : le retournement est une intervention extérieure (on retourne les fourmis à la main) ;
en interne, seule la navette (R-19) fait un retour qui efface sa trace. Impossible pour q ≥ 3 (R-301).

## R-312 Objets fixes (cycles exacts à 2 fourmis, [-3,3]² + 0/1 case) — OBSERVÉ (cycles2.py)
H:R2L2 : 772 cycles / 44 928 (périodes 3, 12, 15, 18, 21, 24, 27, 30, 54 ; période 3 : « H:R2L2|0,0,0;-1,0,3|-1,0 ») ; RL : 8 864 / 19 968
(périodes 4 à 64…, cf. R-02/R-28). (LLR : R-52, pas de cycle court.)

## R-313 Miroirs-oscillateurs R2L2 (9 oscillateurs × 49 places) — OBSERVÉ (osc_miroir.py)
Le vaisseau traverse 235 fois, tourne de ±120° 153 fois mais l'oscillateur est alors presque toujours détruit (ses 2 fourmis partent en
vaisseaux) ; 10 déviations propres avec oscillateur intact ; une 2e vaisseau 10, 60 ou 3 780 périodes derrière n'est JAMAIS dévié pareil
(l'oscillateur a changé d'état). ⇒ pas de miroir fixe réutilisable trouvé en R2L2. OUVERT : miroir à 3 fourmis ou plus, « rail » de vaisseaux.

## R-314 Portes R2L2 « boule de billard » : INTERACTION et AIGUILLAGE — VÉRIFIÉ 4/4 chacune (moteur, temps fini) (porte_r2l2.py)
Interaction (choc (60°, −120°, +120°)) : B = 0,0,4 + case 1,0 ; A = −1,−34,5 + case −1,−33 (A joue en 1er). Seule, B part (1,−1),
seule A part (1,0) ; ensemble : A → (−1,1), B → (−1,0). Les 4 sorties codent a∧¬b, ¬a∧b, a∧b (deux fois). Le choc laisse 3 cases.
Aiguillage (« switch gate » de Fredkin) : C = 0,0,4 + 1,0 joue en 1er, X = 2,−34,5 + 2,−33 : C sort toujours (1,−1) (décalé d'une voie
si X est là) ; X sort (1,0) si C absent, (−1,1) si C présent. ATTENTION : l'ordre de jeu compte (X en 1er → les deux tournent).

## R-315 / R-317 Lieu de choc réutilisable, débris — OBSERVÉ (reuse_chocs.py, debris.py)
Même choc rejoué au même endroit (2e paire translatée de k périodes le long de B) : R2L2 178/261 (k = 40 et 100) ; RL 23/339 (k=40),
84/339 (k=100) ; LLR 5/307, 117/307 ; LLLR 37/319, 132/319 (en carré la 2e paire roule sur les traces : coïncidences, voir R-318).
Débris R2L2 (cases restant à moins de 60 du point de choc) : 105 chocs déviés sur 292 ne laissent AUCUNE case ; transparents : 0 case.

## R-316 Soupes 10×10 (densité 1/2, 200 tirages, 2^20 pas) — OBSERVÉ (soupes.py)
R2L2 200/200 vaisseaux (début médian 28) ; RL 200/200 (2 396) ; LLR 200/200 (123) ; LLLR 200/200 (199) ; R2N 200/200 (22) ;
R2UL2 150 autoroutes + 50 cycles.

## R-318 RÉUTILISATION d'une porte à choc (protocole juste) — OBSERVÉ (porte_reuse.py, k = 100 périodes)
2 usages successifs SUR LES MÊMES VOIES (chaque entrée reculée de k périodes sur sa propre voie), 12 suites (a1,b1 ≠ 0,0 ; a2,b2 ≠ 0,0),
comparées à une porte neuve. Porte réutilisable = 12/12.
R2L2 : 42 / 292 portes réutilisables, 2 190 / 2 628 suites justes (83 %). LLR : 0 / 120 (56 / 1 080 suites, 5 %). LLLR : 0 / 120 (51 / 1 080).
(RL : voir fin de nuit.) En carré la trace du 1er usage fait dévier les entrées du 2e AVANT la porte (R-66, R-307).

## R-319 Circuit à 2 étages R2L2 SANS AUCUNE CASE FIXE, puis réutilisé — OBSERVÉ (chaine_r2l2.py, chaine_reuse.py)
Porte 1 = choc réutilisable de R-318 (B, A) ; sa sortie « A déviée » (= a∧b) croise une 3e fourmi C. Sur 5 portes 1 × 6 orientations
× 49 places : 103 placements de C où la sortie de C (direction, voie) ne dépend que de a∧b (8/8 entrées, toutes propres).
Exemple : porte 1 = « H:R2L2|0,0,4;29,-56,0|1,0,1;28,-55,1 », C = germe tourné de 2 crans en (108,−218) : C sort sur la voie −108 si
non (a∧b), −105 si a∧b (décalage de 3 voies = le bit). Réutilisation (2e jeu d'entrées 200 périodes plus tard, 49 suites) : 46/49 justes ;
les 3 échecs suivent tous un 1er usage (1,1,1) (le 2e choc laisse des débris). Résultat complet des 103 : voir R-320.

## R-320 Circuits à 2 étages R2L2 réutilisables — OBSERVÉ (chaine_reuse.py, k = 200 périodes)
Sur les 103 placements de R-319 : 12 sont réutilisables pour les 49 suites (1er usage, 2e usage ∈ {0,1}³ non vides), ex. C en (111,−217),
(112,−219), (113,−221) [r = 2] et (218,−106), (220,−107), (222,−108) [r = 4] ; les autres : 43 à 47/49 (échecs après un 1er usage (1,1,1)).

## R-321 UN circuit utilisé 10 et 30 fois de suite — VÉRIFIÉ 10/10 (2 moteurs : fourmi_r et verif_py.py, positions finales identiques
pour les 19 fourmis à 40 000 tours) ; OBSERVÉ 30/30 (moteur C, k = 100 et 200, 2 placements) (dix_usages.py)
Circuit : porte 1 = « H:R2L2|0,0,4;29,-56,0|1,0,1;28,-55,1 » + C = germe R2L2 tourné de 2 crans en (111,−217) (fourmi + 1 case).
Usage u : les 3 entrées (a, b, c tirées au hasard) sont les mêmes germes reculés de u·200 périodes sur leurs voies. Sortie : C tourne
de 240° (direction (−1,1)) ssi a∧b, sinon continue sur la voie −111. 10/10 usages justes dans UNE seule simulation (19 fourmis, 19 cases) ;
30/30 avec 55 fourmis (k = 100 et k = 200). C'est le premier calcul RÉUTILISÉ du projet sans remise à zéro extérieure : aucune case fixe,
rien n'est consommé dans la zone de calcul (les vaisseaux ne laissent pas de trace, les chocs choisis ne laissent pas de débris).
Défaut : les entrées sont des vaisseaux « fournis de l'extérieur » à chaque usage (comme les boules du billard de Fredkin) ; pas de miroir fixe
(un vaisseau ne tourne que s'il rencontre un autre vaisseau).

## R-311 (suite) gomme collective de l'additionneur 4 bits : VÉRIFIÉE avec un 2e moteur (verif_gomme_py.py, Python pur) : 0 case différente.

## R-322 Hexa R1L1 et triangle RL : même dynamique ? — OBSERVÉ
Depuis le blanc, même nombre de cases noires à 1 000, 77 777 et 10^6 pas (106, 1 405, 6 114) et même abscisse de la fourmi : les deux
fourmis à virages ±60° (hexagones / triangles) semblent conjuguées par un changement de coordonnées. Aucune autoroute en 3,3·10^7 pas
(ni RLLR). À démontrer (OUVERT) ; probablement classique (réseau dual).

## R-318 (suite) portes à choc réutilisables (12/12 suites, k = 100, 120 géométries par règle) : RL 0 (25/1 080 suites), LLR 0 (56), LLLR 0 (51),
R2N 0 (4), UN 0 (369), R2UL2 0/94 (533/846), R2R2L2 0 (156), R2L1R1 0 (0), R2R1R1 0 (0). SEULE R2L2 en a (42/292).

## R-323 Miroir fixe « à direction constante » en hexa R2R2L2 (q = 3) — OBSERVÉ (miroirs.py, multi_passage.py)
Obstacle 3 cases (59,−59) (60,−61) (61,−61) devant le germe R2R2L2 (1 case) : 6 autoroutes successives (10 ou 30 périodes d'écart) tournent
TOUTES de 120°, mais sur des voies différentes (−116, −118, 2, 42, 82, 122). 1 seul des 46 obstacles qui tournent fait cela. Pas un vrai miroir.

## R-324 Littérature (2e passe) — voir deja_connu_regles.md
H:R2L2 = gaz de Lorentz à « flipping rotators » ±2π/3 sur réseau triangulaire : la propagation (dans une bande) est CONNUE
(Kong-Cohen ; Grosfils-Boon, arXiv cond-mat/9905168). Hexa ±60° / triangle RL = rotateurs ±π/3 sur nid d'abeilles : Webb-Cohen 2014
(marche auto-évitante entre retours). Plusieurs particules ±2π/3 : arXiv 1908.06019 (2019) — NON LU (arxiv.org inaccessible) : à lire avant
de dire « nouveau » pour les chocs et portes R2L2.

## R-325 Demi-additionneur R2L2 sans case fixe — OBSERVÉ (demi_add4.py, demi_add5.py) — 307 distincts (les 1 025 « trouvés » contiennent des doublons : plusieurs (r3,i,j) donnent la même place de K3)
Porte d'interaction (B, A) : U = A seule (a∧¬b), V = B seule (¬a∧b), C = A déviée (a∧b). Un seul virage ne peut pas mettre U sur la voie de V
(les voies obtenues s'éloignent : la voie de sortie avance d'1 voie par période de décalage du point de virage, dans le mauvais sens) ;
d'où un ZIGZAG : K2 tourne U vers la 3e direction, K3 la retourne vers la direction de V, et on cale la voie. 1 025 trouvés = 307 demi-additionneurs distincts
(table S = a⊕b sur UNE voie, C = a∧b) avec la porte « H:R2L2|0,0,4;29,-56,0|1,0,1;28,-55,1 » (4 vaisseaux : A, B, K2, K3 constants).

## R-326 / R-327 Réutilisation du demi-additionneur — OBSERVÉ (demi_add_reuse.py, portes_propres.py, demi_add6.py)
Porte 29,−56 : 0 réutilisable sur 307 distincts (meilleurs 15/16 suites ; échec (1,0) puis (1,0) ou (1,1) puis (1,0)). 105 portes d'interaction
sans débris (42 avec A et B dans la même classe de caps, condition pour pouvoir réunir U et V). Porte « H:R2L2|0,0,4;30,-56,0|1,0,1;29,-55,1 » :
demi-additionneurs réutilisables pour les 16 suites de 2 usages ; au total (recherche arrêtée à 02:03 après 9 portes sur 42) :
8 demi-additionneurs DISTINCTS sur 4 portes (resumes/demi_additionneurs_16sur16.json ; les listes brutes contiennent des doublons).

## R-328 Plus de 2 usages : 17/20 — OBSERVÉ (usages_add.py, triplets_add.py)
Les demi-additionneurs « 16/16 » testés donnent 17/20 additions justes sur 20 usages au hasard (k = 150 à 500, même résultat) :
4 suites de 3 usages sur 64 sont fausses, toujours (1,0), x, (1,0) : le 3e zigzag est perturbé par ce qu'a laissé le 1er. Suite : R-329.

## R-329 Pourquoi pas 20/20 : les virages du zigzag laissent des cases — OBSERVÉ (debug, demi_add6.py, demi_add7.py)
Un usage (1,0) laisse 2 paires de cases exactement aux 2 points de virage (K2 et K3) ; le 2e passage les traverse encore correctement,
le 3e non (suites (1,0), x, (1,0) fausses, pour les 16 demi-additionneurs « 16/16 » testés, et indépendamment de l'écart k = 150…500).
En imposant des virages SANS débris (demi_add7.py), ce sont des suites de 2 usages qui échouent ((1,0)(1,0), (1,0)(1,1), (1,1)(1,0)) :
0 demi-additionneur réutilisable sur les portes testées. OUVERT : réunir 2 voies sans débris (autre géométrie de zigzag, ou réunion par
un choc à 3 vaisseaux). En attendant, le demi-additionneur « S sur 2 voies » (S = U ou V, C = A déviée) EST la porte d'interaction,
réutilisable (R-318 : 42 portes 12/12) ; et le circuit à 2 étages R-321 est réutilisé 30/30.

# Nuit du 26/11 (session hexa R2L2 : miroirs) — R-330 et suivants

## R-330 AUCUN obstacle fixe ne peut tourner un vaisseau R2L2 — DÉMONTRÉ (calcul exact, preuve_obstacles.py) ; déjà connu (Grosfils et al. 1999, preuve esquissée)
Énoncé : un vaisseau R2L2 qui a roulé 10 périodes sur du blanc, puis rencontre N'IMPORTE QUELLE configuration de cases (finie ou infinie,
sur toutes les cases qu'il n'a pas encore visitées), ne recule jamais de plus de 3 crans le long de sa direction : a(t) ≥ max a − 3
avec a = x − y pour la direction (1,−1). Les 2 autres directions de vaisseau de sa classe de caps, (0,1) et (−1,0), ont a = −1 : il ne
peut donc JAMAIS être tourné (ni de ±120°, ni renvoyé), seulement décalé de voie. Après un obstacle fini il redevient un vaisseau de
même direction (vérifié depuis chacun des états du certificat).
Preuve : on branche sur la couleur de chaque case inconnue au moment où la fourmi y arrive ; état = (cap, recul, cases connues avec
a ≥ max a − B, relatives à la fourmi). Pour B = 3 l'ensemble des états atteints est FINI et fermé : 14 états (2 branchements), aucun
pas vers une case oubliée ; idem B = 4, 5, 6 (28, 56, 112 états). C'est un certificat valable pour tout temps (pas une simulation finie).
Contre-vérification par force brute (test_preuve_obstacles.py) : 3 000 champs aléatoires (densité 5 % à 90 %, jusqu'à 41×41) :
recul max = 3 exactement, 3 000/3 000 sorties dans la même direction. (Si l'obstacle touche le vaisseau AVANT qu'il soit formé, il peut
partir ailleurs : 476/3 000 dans un 1er test mal cadré — ce n'est pas un miroir.)
Conséquence : les « miroirs » de Fredkin-Toffoli ne peuvent pas être faits de cases. Un miroir R2L2 doit contenir des FOURMIS.
Explique R-307 (2 625 obstacles + 144 murs : jamais tourné). Commande : `python3 preuve_obstacles.py 3`.

## R-331 AUCUN MIROIR EXACT n'existe en R2L2, quel que soit l'objet (fourmis + cases) — DÉMONTRÉ (2 invariants, preuve ci-dessous) + VÉRIFIÉ (invariant.py)
Deux quantités ne changent jamais (pour toute situation, tout ordre de jeu) :
 (I1) le nombre de fourmis de chaque CLASSE de caps (pairs {0,2,4} / impairs {1,3,5}) : une fourmi tourne de ±120° = ±2 crans.
 (I2) Q = (nombre de cases noires) − Σ_fourmis ⌊cap/2⌋  (mod 3). Preuve : sur une case blanche, cap + 2 (⌊cap/2⌋ + 1 mod 3) et la case
      devient noire (+1) ; sur une noire, cap + 4 (⌊cap/2⌋ + 2 ≡ −1) et la case devient blanche (−1) : ΔQ = 0 à chaque pas.
      Vérifié : 300/300 situations au hasard (1 à 6 fourmis, 500 tours, hx.py).
Valeurs pour le vaisseau (constantes le long de sa période) : directions r = 0,1 → Q = 2 ; r = 2,3 → Q = 1 ; r = 4,5 → Q = 0 ;
r pair = fourmi de cap pair. Théorème : si un objet M (n'importe quelles fourmis et cases) reçoit un vaisseau de direction r et
redevient M (à n'importe quelle phase de son orbite, translaté de n'importe quel vecteur, fourmis dans n'importe quel ordre) en
émettant un seul vaisseau propre de direction r', alors r' = r. En effet (I1) impose r' ≡ r (mod 2) (le vaisseau sortant a la classe du
vaisseau entrant, même si ce n'est pas la même fourmi) et (I2) impose Q(r') = Q(r), donc r' ∈ {r, r ± 1 dans la même paire}, donc r' = r.
⇒ un miroir (60°, 120°, 180°, 240° ou 300°) qui se retrouve EXACTEMENT lui-même est impossible. Seuls restent possibles : les objets qui
changent (autre oscillateur, objet TOURNÉ — tourner de 120° un objet à n fourmis change Q de −n — ou qui gardent des cases en plus),
et les chocs à plusieurs vaisseaux (Q total conservé).
Accord avec les recherches (miroir.c, R-332) : 0 miroir exact sur 7 723 oscillateurs à 2, 3 et 4 fourmis × 6 directions × toutes voies
× toutes phases × 2 ordres de jeu. Conséquence pour le billard : un vaisseau ne peut tourner qu'en rencontrant d'autres vaisseaux (constantes,
comme R-314) ou un objet qu'il modifie ; une « boucle de miroirs » fixe est impossible (et R-330 exclut déjà les cases seules).
Remarque : les chocs PROPRES de 2 vaisseaux (sans débris) doivent conserver Q(A) + Q(B) mod 3 et les classes ; ex. (60°, −120°, +120°)
de R-314 : B −120° (Q + 1), A +120° (Q − 1) ✓ ; « B tout droit, A +120° » laisse forcément des cases (R-314 : 3 cases).

## R-332 Recherche de miroirs-oscillateurs (2, 3, 4 fourmis) — OBSERVÉ (miroir.c : enum, tir, flux ; confirmé par R-331)
Oscillateurs = cycles EXACTS (retour à l'état de départ, donc périodiques pour toujours) : 2 fourmis dans [−3,3]² + ≤ 1 case (44 928
situations) → 95 orbites distinctes (à translation, rotation, phase près ; périodes 3, 12 ×87, 15…54) ; 2 fourmis dans [−6,6]² + ≤ 2 cases
(1 971 648) → 1 711 ; 3 fourmis dans [−2,2]² + ≤ 1 case (3 100 032) → 12 (périodes 6, 12, 18, 36 ; NB : McGinnis-Webb laissent ouvert
« N impair périodique ? » dans leur modèle synchrone ; ici, ordre « l'une après l'autre », il en existe) ; 4 fourmis dans [−2,2]² sans case
→ voir R-336. Recoupement : les 9 premiers oscillateurs donnent CYCLE avec la même période dans fourmi_r.
Tir : chaque oscillateur × 6 directions × toutes les voies qui le touchent × toutes ses phases × 2 ordres de jeu (vaisseau avant/après).
2 fourmis (95 + 1 711) et 3 fourmis : 0 miroir exact ; 2 « miroirs » où l'objet ressort TOURNÉ et DÉPLACÉ (osc. p = 36) ; 4 fourmis
(6 000 premiers) : 0. Très souvent le vaisseau tourne en CHANGEANT l'oscillateur (en un autre : 540 442 cas pour les 1 711).
Flux (miroir.c flux) : NV vaisseaux sur la même voie, espacés de 160 à 399 pas : au mieux 4 vaisseaux de suite tournés pareil par le même
objet, jamais 5 (461 candidats). ⇒ conforme au théorème R-331.
Passages « exactement transparents » : parfois une fourmi de l'oscillateur part à la place du vaisseau (échange d'identité), sans aucun
décalage : invisible de l'extérieur, inutile pour lire.

## R-333 « 0 perte » pour TOUS les chocs de 2 vaisseaux R2L2 — DÉMONTRÉ (calcul exhaustif + certificats ; chocs_exhaustif.py, chocs_certif.py)
Ensemble fini : B en direction 0 (rotation globale), A en direction r = 1..5, A avancé de τ = 0..7 pas, position relative v modulo
u = d_A − d_B (décaler les deux de 8 pas = ajouter u), 2 ordres de jeu. Les cases noires d'un vaisseau sont à distance ≤ 2 de sa fourmi :
si les fourmis ne passent jamais à moins de 6 l'une de l'autre, chacune ne voit que du blanc → transparent EXACT (4 852 géométries).
Les 940 autres × 2 ordres = 1 880 chocs, simulés : 1 688 → 2 vaisseaux propres, 168 → 2 vaisseaux + des cases (débris), 24 → 1 vaisseau
DOUBLE (les 2 fourmis liées, période 8, se déplace comme un vaisseau) ; 0 autre issue. Certificats pour tout temps : les 2 vaisseaux
(prolongés seuls 200 périodes) ne se rapprochent jamais à moins de 6 et ne touchent jamais les débris (distances croissantes) ; le vaisseau
double se répète exactement (51 périodes) et s'éloigne de ses débris. 2 moteurs : 1 880/1 880 états finaux identiques (hx.py / fourmi_r).
⇒ THÉORÈME (convention « l'une après l'autre ») : un choc de 2 vaisseaux R2L2 ne détruit jamais un vaisseau. Chaque issue respecte (I1) et
(I2) de R-331. Ce qui bloque le billard complet : pas de miroir (R-330, R-331) ; on ne tourne qu'avec d'autres vaisseaux.

## R-334 Pixel et écran de 2 pixels (version 1 : OFF = 1 case) — VÉRIFIÉ (2 moteurs, temps fini) (pixels.py)
Pixel ON = O = « H:R2L2|0,0,3;1,0,0|1,0 » (2 fourmis, 1 case, période 3 : le plus petit oscillateur). O est son propre film à l'envers
(gomme collective R-311 : la destruction renversée recrée O exactement, au même endroit). EFFACER : 1 vaisseau (r = 3, voie 0, O en
phase 2, joué après O) → O part en 3 vaisseaux et laisse 1 case en (0,−1) (obligatoire : invariant Q, 0 + 1 ≢ 1 + 1 + 2… mod 3).
ÉCRIRE : film à l'envers de l'effacement (r = 1, voie −2) : 3 vaisseaux + la case (0,−1) → O, un 4e vaisseau repart.
Toutes les routes vont dans les directions 2, 3, 4 : aucun choc frontal en vol. Démo (UNE simulation, 11 fourmis posées à t = 0, aucune
case fixe à part la case « OFF » de chaque pixel) : P1 = ON, OFF, ON et P2 = OFF, ON, OFF à t = 1 600, 3 200, 4 800 : 3/3 justes ;
2 moteurs (hx.py et fourmi_r -x -dump) : 4/4 états identiques. Limite : LIRE un pixel OFF déplace sa case (0,−1) → (2,−2) (le vaisseau
la traverse, R-330 : il ne tourne pas mais la décale) ⇒ pas de mémoire lisible avec cette version ; voir R-335.
