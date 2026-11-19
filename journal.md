# Journal des résultats (ajouts à la fin uniquement)

Version complète d'origine : docs du projet Claude « journal des résultats » et « journal — R-26 à R-35 ».
Ici : version condensée, commandes et chiffres clés conservés. Programmes : `src/`.

## R-01 Critère exact de cycle — VÉRIFIÉ (preuve)
Si l'état complet revient à l'état initial au pas p, mouvement périodique de période p. Dynamique réversible ⇒ toute orbite bornée revient à l'état initial.

## R-02 Cycles à 2 fourmis — VÉRIFIÉ (simulation finie)
Fourmi 1 (0,0,H), fourmi 2 sur [-10,10]² × 4 caps (1 760), 3·10⁶ pas : 775 cycles (519 orbites), 926 fuites, 59 non tranchés (losanges). Périodes 16 à 57 276 (fourmi 2 en -9,6,H). Phénomène connu (Chopard & Droz 1998, synchrone).

## R-03 Périodes ≡ 0 mod 4 — VÉRIFIÉ (preuve)
Virages ±90° ⇒ alternance pas horizontal / vertical ⇒ p pair et p/2 pair. Toute règle L/R, tout nombre de fourmis.

## R-04 Au plus 2 grilles blanches par cycle — OUVERT (observé sur R-02)

## R-05 Tri des 1 760 placements — VÉRIFIÉ (simulation finie, bestiaire.c)
775 bornés ; 924 deux autoroutes 104 (13 tandems) ; 2 autoroutes à deux de période 102 ; 59 losanges.

## R-06 Losange — OBSERVÉ (qualitativement connu, Chopard 1998)
0,0,H ; 0,1,H : bord noir, intérieur blanc, 2 pas/case, boîte 2^(m+1)+1 = √(2t)+1 aux temps 2^(2m+1) (m = 3…10). Vitesses vues : 2, 10/3, ≈ 6 pas/case.

## R-07 Autoroute 102 à 2 fourmis — OBSERVÉ
0,0,H ; -10,-9,D → période 102, (−3,−5), dès 556. Variante 0,0,H ; 9,-10,G.

## R-08 0,0,H ; 40,0,G — VÉRIFIÉ : cycle exact 42 716 (4 958 cases). L'ancienne « deux autoroutes » était un tronçon défait ensuite.

## R-09 Même classe de parité ⇒ jamais borné — preuve esquissée À RELIRE + simulation
Classe = (x + y + [cap vertical]) mod 2, invariante. Toutes les fourmis RL de même classe ⇒ chaque case traversée toujours dans le même axe ⇒ argument de Bunimovich-Troubetzkoy. Sur R-02 : 880 même classe → 880 fuites.

## R-10 Famille LⁿR — OBSERVÉ
n = 3…30 : autoroute de période 16n+4, (−2,+2), dès le pas 24n+7 (n = 2 : période 18 dès 39). Périodes connues (Gajardo-Lutfalla-Rao 2025) ; formule du début = notre mesure.

## R-11 Espèces connues — OBSERVÉ
LLRL : 384, (+4,−4), dès 256 241. LLRRRLRLRLLR : 1 968, (−16,0), dès 29 891. LLRRRL : 896, (−4,+4), dès 64 416 368 — À REVÉRIFIER (bord de grille). Hexa L1L2NUL2L1R2 : PAS une autoroute (tronçons 698 qui tournent de 60°). Pas d'autoroute : RLR, LLRLRL, LLRR, LRRL jusqu'à 4·10⁸ ; LLRLRLL jusqu'à 9,8·10⁶.

## R-12 Autoroute RL perturbée (1 case inversée) — OBSERVÉ (perturb.c)
Seule la phase s mod 104 compte. Toujours une autoroute 104 à la fin ; récupération 0 à 51 046 pas (médiane ≈ 1 240). Corrigé par R-16.

## R-13 Campagnes de Claude Code (recherche.js), revérifiées — 14/11
Balayage 2 fourmis distance ≤ 20 (6 720) : même classe 0 cycle ; classes opposées 84 % de cycles. VÉRIFIÉS : 0,0,H ; 16,17,H période 309 752 ; cycles 4 fourmis 24, 28, 32, 68 000 ; composé 0,0,B ; 3,-9,D ; 6,-18,G ; 9,-27,H période 1 030 792 = ppcm(2 212, 1 864) ; familles alignées 16, 28, 1 136 (n pair seulement). Autoroutes de groupe OBSERVÉES : 52, 96, 24, 16 (0,−4) vitesse 0,25, 12 (carré 2×2), 48. Suiveuse 108. Rail 12. Borne de vitesse RL ≤ 1/2 sur un axe.

## R-14 Conjecture des phases — OUVERT
Un cycle n'existe que si les deux classes ont autant de fourmis (donc jamais pour n impair). ≈ 177 000 situations, 0 contre-exemple. L'équilibre ne suffit pas.

## R-15 Recherche « déjà connu ? » élargie — voir `deja_connu.md`

## R-16 Bestiaire des collisions, 1 case noire — OBSERVÉ (auto2.c)
22 cases neuves par période sur l'autoroute nue → 22 issues distinctes : même ligne 4, décalée 5, virage gauche 5, virage droite 7, demi-tour 1 (51 046 pas de chaos). Page : https://claude.ai/artifact/LuKuHjhorSKVvZj8UX17dm

## R-17 Germes d'autoroute — OBSERVÉ
Exhaustif fourmi 0,0,H + 1, 2, 3 cases dans [-5,5]² : TOUS → autoroute 104 (2·10⁶ pas). Transitoire le plus court 310 / 162 / 126 (grille vide : 9 977). Recherche locale : 80 pas avec 6 cases.

## R-18 Campagne 2 à 8 fourmis + 0 à 3 cases — OBSERVÉ (multi.c)
Passager rapide 100 sur trace 104 (3 fourmis) ; passager lent 388 (−6,−10) sur trace 102. Rail de R-13 NON reproduit (cycle 11 836) : À REVÉRIFIER.

## R-19 Navette — VÉRIFIÉ (calcul exact)
2,1,B ; 3,-5,H ; 5,2,B : fourmis 1-2 font des allers-retours de ~19 500 cases, cycle exact 2 133 520 dès 2 044 380. Famille : portées ~11 000 et ~13 500. Code : oneh.c, cyc.c, exact.c.

## R-20 Bout d'autoroute minimal = 11 cases — VÉRIFIÉ (preuve + calcul)
Germe minimal unique par phase (cases noires relues). Phases 22 et 93 : 11 cases. Germe 0,0,B ; 0,1 1,2 2,3 2,2 2,1 2,0 3,0 3,-1 2,-2 1,-2 -2,-1. `./tipmin 60 x`.

## R-21 Navette de portée réglable — VÉRIFIÉ (cycles exacts) ; portée arbitraire OUVERT
Portée = 19 797 + 52m. m = 1…52 : 40 navettes, 12 échecs ; record m = 300 (portée 35 397, période 3 686 216). `./nav "2,1,B;3,-5,H;5,2,B" "" 200000 3 1 $((104*m)) 60000000`

## R-22 Passagers posés sur une trace — OBSERVÉ (drop.c)
Trace 104 : rail 12, convertisseur 10 à reculons. Trace 102 : 388, 688, 142 (à reculons).

## R-23 2 fourmis + 0 à 4 cases — OBSERVÉ (pass.c)
Suiveuse 108 et rail 12 à 2 fourmis. Cycles dès le pas 0 : 6,-5,D ; 6,5,B + -2,-1 ; 1,4 (9 704).

## R-24 2 cases noires sur l'autoroute — OBSERVÉ (two.c)
1 683 paires : toutes → 104 ; 34 % de directions non additives. Chaos record 112 480 pas.

## R-25 Collision de 2 autoroutes 104 — OBSERVÉ (col.c)
370/370 → 2 autoroutes 104. « Relais » observé.

## R-26 Nids (cycles derrière une autoroute) — VÉRIFIÉ (exemples) / OBSERVÉ (stats) (explore.c)
3 fourmis → 51 % ; 4 → 40 % ; 5 → 31 %. Jamais de nid à nombre impair. Ex. 1,0,G ; -1,2,H ; 0,-2,G → nid 272 580. Retirer une fourmi partie fausse les passagers.

## R-27 Conjecture des phases + cases noires — OUVERT (≈ 2,5 M situations, 0 contre-exemple)

## R-28 Tourniquet, cycle minimal période 4 — PROUVÉ
-1,-1,H ; 0,0,D + case 0,0.

## R-29 Rouage, 4 fourmis période 8 — VÉRIFIÉ
2,-2,H ; 1,-1,D ; 0,-1,B ; 0,-2,H + 1,0 1,-2 1,-1 2,-2 0,0 0,-3 1,-3.

## R-30 2 fourmis + 1 case : 1 479 périodes de cycle — VÉRIFIÉ (exemples)
Petit Grain période 8 ; Grand Grain 0,-3,B ; 1,2,G + -1,0 (79 552).

## R-31 Cycles de groupe — VÉRIFIÉ
Métronome 56 296 ; Double Navette -1,-1,D ; 1,2,G ; 2,-1,G ; -2,2,D (57 924, sans case noire) ; Sextuor 1 848 ; Rosaces 16, 6 504, 2 112 ; Moulin 265 776 ; Grande Rosace 287 536.

## R-32 Passagers 20 (trace de la Flèche) et 2 620 (trace 102) — OBSERVÉ

## R-33 Lambine — OBSERVÉ (exhaustif)
Fourmi 0,0,H + 1 case en (7,-7) : autoroute au pas 106 258 (×10).

## R-34 Bilan campagne 16/11 — ≈ 2,5 M situations, aucun vaisseau nouveau sur grille blanche.

## R-35 95 directions d'autoroutes — OBSERVÉ (hw.c / hwv.c)
Carré : 32 directions (+ horizontale), surtout règles avec N/U ; hexa : 63. RL à plusieurs fourmis : seulement pentes 0, 1, 5/3. Fichiers : autoroutes_par_direction.csv (Drive).

## R-36 Recherche massive RL, 10 à 100 fourmis, ± cases noires — 16/11 après-midi (src/fourmi, campagne.sh)
3 069 situations, 400 000 pas max (≈ 20 min de calcul sur 2 cœurs) : au hasard 950 (10-100 fourmis, rayon 10-40, 0-50 cases), symétrie d'ordre 2 919 (coupée par une pause), symétrie d'ordre 4 900, alignées y = ax 300 (a = 0..3, e = 1, 3, 5).
Issues : MIXTE 3 025 (98,6 %), AUTOROUTES 31, CYCLE 12, INDÉCIS 1. Fourmis non classées N<k> : dans 3 026 situations (pas des découvertes).
Autoroutes « inconnues » à 400 000 pas (232, 316, 756, 820, 3 112) : TOUTES disparaissent à 4 000 000 de pas (tronçons transitoires) → FAUX.
12 cycles exacts nouveaux (périodes absentes de connus.txt), tous de symétrie d'ordre 4 — VÉRIFIÉ (cycle exact, retrouvé à 4 M pas) :
8 fourmis sans case : 2 904, 3 316, 5 960, 9 048, 9 712, 253 760 (4 paires qui partent en diagonale puis reviennent : quadruple navette) ;
8 fourmis + cases : 1 012 (48), 12 696 (16), 15 824 (44), 33 200 (44), 36 932 (4) ; 12 fourmis + 8 cases : 110 896.
Même famille que les Rosaces de R-31 ; record de période pour 8 fourmis sans case : 253 760.
Avec 13 fourmis ou plus : aucun cycle, aucune autoroute nouvelle. ATTENTION : 11 cycles ont 8 fourmis (< 10) à cause d'un arrondi de gen.py (--sym 4 avec n = 10 ou 11 donnait 8 fourmis) ; corrigé (arrondi au-dessus).
Germes : resultats/germes_2026-11-16.json ; fiches : resultats/bestiaire_2026-11-16.pdf. Commande : src/fourmi -T 4000000 "<situation>".

## R-39 Additionneur par modules enchaînés (ordinateur à fourmis) — VÉRIFIÉ (temps fini, toutes entrées) — 16/11 soir
Module = additionneur complet à 2 lecteurs (S somme ↘/↙, K retenue ↘/↗) ; retenue = autoroute ↗ sur voie exacte,
qui décale de 8 voies le lecteur suivant ; 2 cases d'aiguillage par feuille ramènent les 3 cas « retenue 1 » sur
la même autoroute, donc module recopiable (décalage (1311,−1091), retard 950 périodes). 2, 3, 4, 5 bits : 16/16,
64/64, 256/256, 1024/1024 justes au pas de lecture ; 4 bits recalculé en JavaScript (256/256). Lecture à la fin
fausse dans 120/256 cas (sorties ↙ heurtées plus tard). Principe connu : Gajardo-Moreira-Goles 2002.
Commande : cd recherche/ordinateur && python3 chaine.py 4 436400 95000 ; node verif_independante.js tout.
Source : recherche/ordinateur/COMPTE_RENDU.md, fiche.md, germe_ordinateur.json.

## R-40 Banc « câblabilité » des autoroutes (17/11, 13:49–13:54) — OBSERVÉ (ordinateur/banc1.py, score1.py)
Remarque : le Drive a déjà R-36 à R-39 « ordinateur » (R-39 = additionneur 4 bits par modules). Numérotation reprise à R-40.
Chaque autoroute contre 1 case noire posée sur chacune des cases de son chemin sur 1 période (toutes les phases), et contre
8 murs (4 directions × plein/pointillé) décalés de 0 à 7 cases. Classement par fourmi (moteur C) ; contact mesuré par sim.py (2e moteur).
Classement (case seule : % propre / % virage ±90 / chaos médian / % parasites) :
LLR A18 100/87/28/0 ; LLLR A52 100/78/68/0 ; LLLLR A68 100/78/86/0 ; RL A104 100/62/5 988/0 ;
puis toutes les autoroutes RL à plusieurs fourmis (102, 96, 52, 16, 108) : 0 à 16 % propres, 83 à 100 % parasites
(elles éclatent en plusieurs 104). => pour câbler en RL : la 104 à UNE fourmi, rien d'autre.
Murs (8 décalages, même issue partout) : LLR mur vertical −90° en 6 pas de chaos, mur horizontal demi-tour (1 235 pas),
mur diagonal perpendiculaire TRAVERSÉ sans effet (3 pas). RL 104 : le mur dépend du décalage sauf la ligne posée dans l'axe (−90°, ~3 250 pas).
Piège : fourmi s'arrête à 4 096 pas si l'autoroute est déjà confirmée ⇒ obstacle placé trop loin = jamais touché (corrigé : obstacle à 8 périodes).

## R-41 Porte « compteur » par traversée de traces : NOR, ET, NON — OBSERVÉ (ordinateur/e1…e4, gate.c)
Germe 104 (11 cases) tourné ; A, B = autoroutes ↙ (entrées, présente = 1) ; P = « puissance » ↘ lancée plus loin (arrive après).
E1 : P traverse la trace de A : 8 classes (voie c = x−y de P mod 4 × demi-phase de P). Classe c ≡ 3 (mod 4) : décalage −4, propre, 4/4 phases.
Classes paires : P fait demi-tour, rattrape A, tout se mélange (à éviter).
E2 : P traverse A puis B : voie finale = L − 4·(a+b), 24/24 (4 phases × 2 voies × 3 positions de B). Les décalages S'ADDITIONNENT.
E3 : 1 case d'aiguillage touchée par une seule voie : (141,260) ⇒ P tourne ↙ ssi a=b=0 (NOR) ; (133,267) ⇒ ↙ ssi a=b=1 (ET).
Sorties ↙ = même sens que les entrées ⇒ enchaînables. NON = NOR sans B.
E4 robustesse (A, B ou P décalé de ±1 case / ±1 demi-période) : NOR 4/8, 3/8, 1/8 justes ; ET 2/8, 1/8, 2/8 ⇒ voies EXACTES nécessaires (comme R-39).
Commande : cd ordinateur && gcc -O2 -o gate gate.c && python3 e2_nor.py && python3 e3_demux.py && python3 e4_robuste.py

## R-42 Deux étages enchaînés : OU = NON(NOR(a,b)) — OBSERVÉ, table 4/4 (ordinateur/e5_chaine.py)
Piège : A et B continuent ↙ pour toujours ; une 2e puissance ↘ recroise leurs traces et compte a+b+O1 (voies −306/−310).
Solution : la 2e puissance P2 arrive de l'autre côté (↖, départ x+y ≈ 1 900) : elle lit la trace de O1 AVANT de croiser A et B,
et sa case d'aiguillage est placée entre les deux. 16/16 placements de P2 essayés ont des cases qui donnent OU juste (4/4).
Règle de conception qui en sort : une puissance ne doit croiser, avant sa case de lecture, QUE les traces qu'elle doit lire.

## Point mi-parcours (14:00) : objectif 1 fait (R-40), NOR/ET/NON/OU + enchaînement (R-41, R-42). Reste : COPIE, croisement, affichage, vérif Python, livrables.

## R-43 COPIE, CROISEMENT, demi-additionneur, écran — VÉRIFIÉ (2 moteurs, temps fini) (ordinateur/e6…e8, ecran.py, verif.py)
COPIE : case (135,265) ⇒ P tourne ↙ ssi a=1 ; A continue ↙ : 1 entrée, 2 sorties (13 cases conviennent).
Collecteur : 1 case n'existe pas ; 63 paires de cases renvoient les voies L et L−4 sur la MÊME sortie ↙ (voie 397).
CROISEMENT : X (↙) passe d'abord, Y (↘) traverse sa trace puis le collecteur (137,264)+(148,267) ⇒ trace de sortie de Y
identique case par case pour x=0 et x=1 (5 paires sur 63). Y ne garde aucune trace de x.
Demi-additionneur à UNE puissance : cases (130,254)+(133,267) : S ⇒ ↙ voie 337, C ⇒ ↙ voie 369, (0,0) ⇒ reste ↘ (14 cases XOR conviennent).
Écran (objectif 3) : bande y = 900, pixels S (x=−563) et C (x=−531) = case noire dans un carré 13×11 : 4/4 juste.
Vérification indépendante (verif.py, moteur Python) : 9 portes, 28 cas, 28 justes. Germes : ordinateur/germes_ordinateur_2026-11-17.json.
Déjà connu ? Gajardo-Moreira-Goles 2002 (1 fourmi, cases préparées) ; rien trouvé sur des portes par traversée de traces à plusieurs fourmis
(2 recherches web + deja_connu.md) ⇒ « pas trouvé », pas « nouveau ».

## R-44 Pas de puits définitif — PROUVÉ (argument court, À RELIRE)
Si, à partir d'un instant t0, toutes les fourmis restent dans une zone bornée, l'état (zone + fourmis) ne prend qu'un nombre fini de valeurs,
donc il devient périodique ; la dynamique étant réversible (R-01), l'orbite ENTIÈRE est périodique : l'état de départ revient,
donc l'autoroute est ré-émise (c'est une navette, R-19). Toute règle L/R, tout nombre de fourmis. Un signal ne peut donc pas être
« absorbé » pour toujours : on peut seulement l'envoyer à l'infini (décharge) ou le renvoyer (navette = horloge, VÉRIFIÉ R-19/R-21).

## R-45 Convois 104×N (piste 1, 17/11 15:00–) — OBSERVÉ (ordinateur/v2/convoi.py, lacher.py, cascade.py)
Construction gloutonne depuis le Tandem (0,0,H ; −2,0,B) : 104×3 = 1 seul placement (−2,2,D, autoroute dès 17 131) ; 104×4 : 0 sur 664 (R=6).
Lâcher : Tandem + 1 bloc (1 ou 2 cases, toutes phases) : 172/252 lâchent UNE fourmi 104, l'autre continue ; 104×3 : 153/402.
Mais ces « convois » ne sont PAS groupés : ce sont des 104 parallèles (Tandem : 14 voies d'écart ; 104×3 : 48 voies, 60 cases).
Cascade 3→2→1 : 0/40 (bug de ma part : le chemin du 2e étage était pris AVANT le 1er lâcher ; à refaire si le temps).
## R-46 Réservoir « ruban » : N germes 104 parallèles (voies x+y espacées de 20), lâchés un par un vers ↘ par la case virage (R-43),
de la voie extérieure vers l'intérieure, 40 périodes plus loin à chaque fois — OBSERVÉ (moteur C) : N = 2, 3, 5, 8 : N/N lâchers propres ↘,
voies x−y = −56 − 160k. N ≥ 9 : « casse » = BUG de mon outil gate.c (8 fourmis max) ; corrigé (64) ⇒ N = 10, 12, 15 : N/N. VÉRIFIÉ (2 moteurs, N = 8 et 15).
## Point 15:06 : piste 1 en cours (ruban jusqu'à 8). Ensuite : diagnostic N≥9, puis piste 5 (pièges).
Conséquence : un convoi groupé de N > 3 n'a pas été trouvé ; le réservoir utile = ruban de 104 parallèles. Mais il ne fait
rien de plus que N germes posés : seul gain, les puissances partent d'un même bord et leur instant de lâcher se règle par la case.
Voies des lâchées x−y = −56 − 160k (≡ 0 mod 4) ; pour servir de P (classe 3) il faut placer les entrées en conséquence (piste 3).
Commande : cd ordinateur/v2 && python3 ruban.py && python3 verif_ruban.py

## R-47 Pièges à autoroute (piste 5) — VÉRIFIÉ (cycles exacts, 2 moteurs) / OBSERVÉ (stats) (ordinateur/v2/trap.c, pieges*.py)
Source 104 ↙ (0,0,D + 11 cases), piège = Tourniquet 4, Petit Grain 8, Rouage 8, Petite Rosace 16 × 4 rotations, origine
(−160+p+s, 160+p−s), p = −8…8, s = 0…3 : 1 088 essais, 200 000 pas. trap.c : cycle EXACT des fourmis bornées (état + boîte ≤ 400, ≤ 150 000 pas).
Issues : pas de contact 576 ; capture (cycle exact + UNE 104 éjectée) 88 (source éjectée 42, fourmi du piège éjectée 46) ;
bornées sans cycle trouvé 43 ; 2 à 9 autoroutes 399 ; TOUT COINCÉ : 0 (R-44 tient).
Cycles finaux : périodes 148 à > 16 000 (jamais 4 ni 8). Plus courts : Tourniquet r1 p2 s1 → 148, éjection ↗ ; Petit Grain r0 p2 s1 → 220, éjection ↘.
Revérifié Python (retour exact de l'état piégé + boîte) : 9/9.
CORRECTION du test du chat : Petit Grain p=−1 s=3 = cycle de période 840 (boîte 163×164), pas 4 ; p=1 s=0 = PAS une capture
(2 autoroutes ↘ + 1 fourmi rapide sur une trace). Le « cycle 4 » venait d'une boîte trop petite. Mon 1er banc (boîte 64) avait le même défaut.
Piège universel : NON (au mieux 16 positions capturées sur 68 pour Tourniquet r1 ; directions d'éjection variées). OBSERVÉ.
## Point 15:10 : pistes 1 et 5 faites (sauf 5c réutilisable, 5d LLR). Suite : piste 2 (additionneur 2 bits + écran).

## R-48 Additionneur complet à 1 puissance — VÉRIFIÉ (2 moteurs, temps fini) (ordinateur/v2/fa*.py)
Entrées a, b, c = germes ↙ (voies x+y = 0, 128, 256), P ↘ voie x−y = −121 : voie de P = L − 4k, k = a+b+c, 8/8 (2 voies de P testées).
Les décalages s'additionnent sur 3 traces. Cases (130,254) + (231,369) : k=0 → ↘ voie −126 ; k=1 → ↙ 337 ; k=2 → ↙ 369 ; k=3 → ↙ 597.
Écran y = 900 : S = pixel k1 ou k3, C = pixel k2 ou k3 : 8/8 (Python) ; sorties 8/8 (C).
Échec instructif : une case qui ne touche QUE la voie du milieu (k=1) n'existe pas (0/1 766) ; on lit par la voie de SORTIE, pas par une case par voie.

## R-49 ORDINATEUR EN UN GERME : additionneur 2 bits (a1a0 + b1b0) + écran — VÉRIFIÉ (2 moteurs, 16/16) (ordinateur/v2/add2*.py)
Idée : poids 2 = 2 germes parallèles (a1 → voies 256 et 384 ; b1 → 512 et 640) ; a0 → 0 ; b0 → 128. UNE puissance P ↘ (voie −121)
traverse toutes les traces : voie = L − 4v, v = a0 + b0 + 2a1 + 2b1, 16/16 (6 traces s'additionnent).
« Épluchage » : 6 cases, une par valeur, du bord vers l'intérieur : (341,460) + v·(78,82), v = 0…5 ; la valeur v sort ↙ sur la voie 781 + 160v ; v = 6 reste ↘.
Écran : bande y = 1 100, un pixel par valeur (x = −319 + 160v ; v = 6 en x = 950) ; binaire lu par la position. 16/16 Python, 16/16 C.
Taille : 1 puissance + 6 germes d'entrée au plus + 6 cases. MAIS pour n bits : 2^i copies du bit i et 2^(n+1) − 2 cases ⇒ EXPONENTIEL
(comme R-36) ; le linéaire demande l'enchaînement par retenue (R-39) — pas fait ici.
## Point 15:21 : pistes 1, 5, 2 faites. Suite : piste 3 (règles de déplacement), puis livrables.

## R-50 Règles de déplacement des portes (piste 3) — VÉRIFIÉ moteur C (ordinateur/v2/regles.py)
Additionneur 2 bits, 16 entrées par test : translation d'ensemble (37,−11) et (−100,64) 16/16 ; une entrée glissée le long de son axe
de ±5, ±20 × (2,−2) 16/16 ; puissance reculée de 5 ou 40 × (−2,−2) 16/16 ; entrée décalée sur le côté de (2,2) ou (8,8) 16/16,
de (1,1) 14/16, de (1,0) 8/16 ; cases glissées de 3 × (2,2) le long de P 16/16 (sortie décalée de 12 voies).
Règle : on peut glisser une entrée le long de son axe, reculer une puissance, translater le tout ; sur le côté, seulement par
multiples de (2,2) (voie x+y ≡ mod 4) ; une case d'aiguillage se glisse par (2,2)·m le long de P (sortie +4m).
Contradiction « R-35 bis » : le test e2 (R-41) montre que l'addition n'a lieu qu'en classe x−y ≡ 3 mod 4 (24/24).
En classe 1 : une seule trace donne soit un demi-tour (6/12), soit −8 (6/12), et deux traces donnent un demi-tour ou un mélange
⇒ « ne s'additionnent pas » était vrai dans les autres classes. Le sens de traversée compte aussi (↖ : +2 ou −6 selon la phase, R-41 E1).
OUVERT : piège réutilisable (5c), pièges LLR (5d), portes LLR, mémoire réinscriptible.

## R-51 Piège réutilisable (piste 5c) — OBSERVÉ (stats) / VÉRIFIÉ (4 cycles, 2 moteurs) (ordinateur/v2/reuse.py)
Les 12 captures aux cycles les plus courts × 2e source 104 venant des 4 directions × 7 voies (336 essais, 200 000 pas) :
2e source sans contact 247 ; contact suivi d'un cycle exact + 2 autoroutes au total : 89 (2e source PIÉGÉE, une fourmi du piège part
à sa place : 31 ; 2e source déviée, cycle changé : 58). Dans plusieurs cas le piège REVIENT à un cycle de période 4 (Tourniquet)
ou 8 (Petit Grain) : remise à zéro. Ex. Tourniquet r0 p1 s2 + 2e source r0 off 3 → cycle 4. Revérifié Python 4/4.
⇒ un piège = « miroir à usage multiple » ou fusible réarmable (à étudier).

## R-52 Pas de cycle court en LLR / LLLR (piste 5d) — OBSERVÉ (src/fourmi, CYCLE exact)
LLR : 2 fourmis (+ 0 ou 1 case) dans [−3,3]² : 19 968 essais ; 3 fourmis dans [−2,2]² : 17 664 ; 4 fourmis en symétrie d'ordre 4
(± cases symétriques) : 24 200 ; LLLR symétrique : 24 200. 0 cycle exact (100 000 pas). L'autoroute LⁿR part trop vite (≈ 40 pas)
pour qu'un cycle se forme ⇒ pas de piège LLR à base de cycles (le « cycle » vu dans le chat = boîte trop petite, comme en RL).

## R-53 Additionneur 3 bits en un germe, cases PRÉDITES — VÉRIFIÉ 64/64 (2 moteurs : Python, C grille 16 384²) (ordinateur/v2/add3.py)
Poids 1, 2, 4 = 1, 2, 4 germes parallèles (emplacements (64i,64i), i = 0…13). Une puissance P ↘ (voie −121) traverse jusqu'à 14 traces :
additivité tenue jusqu'à 14. Les 14 cases = cases de R-49 glissées de 256 × (2,2) le long de P (règle R-50), (853+78v, 972+82v), AUCUNE recherche.
Valeur v sort ↙ voie 1805 + 160v ; v = 14 reste ↘ (voie −182). 300 000 pas, 78 s en Python.
Taille n bits : 1 puissance + 2(2^n − 1) germes d'entrée + 2^(n+1) − 2 cases ⇒ exponentiel (mais construit sans recherche).

## R-51 CORRIGÉ (15:30) — l'essai R-51 était FAUX dans son interprétation
Dans reuse.py la 2e source partait à ≈ 62 cases du piège, la 1re à ≈ 226 : la « 2e » arrivait AVANT. Les « remises à zéro (cycle 4) » = FAUX.
Refait (reuse2.py) avec la 2e source à ≈ 600 cases (arrive après la capture), 336 essais, 200 000 pas : contact suivi d'un cycle exact
+ 2 autoroutes : 121 cas ; dont 86 « 2e source déviée, cycle de même période », 17 « cycle changé », 5 « 2e source piégée ».
Témoin SANS le piège : 46 des 86 déviations viennent des traces de la 1re source ; 40 viennent du CYCLE.
Pour ces 40 : MIROIR-CYCLE RÉUTILISABLE — le cycle (ex. Tourniquet r1 p2 s1, période 148) dévie une 2e autoroute et garde EXACTEMENT
la même orbite (positions des fourmis piégées identiques au pas 200 000 avec ou sans 2e autoroute : 6/6, Python). VÉRIFIÉ (2 moteurs, fini).
Mémoire réinscriptible : pas trouvée (OUVERT).

## R-54 LLR : une trace est un MIROIR, pas un décaleur (piste 4) — OBSERVÉ (ordinateur/v2/llr_croise.py, trapL)
LLR, A = 0,0,H (autoroute 18 ↙), B = 32,32,H (↙, voie x+y ≈ 65), P = cap G (↘) sur 32 voies × 4 phases, 30 000 pas (128 situations × 4 entrées).
P qui traverse une trace TOURNE ↙ (−90°) et repart parallèle à l'entrée ; la 1re trace rencontrée décide : (1,0) et (1,1) donnent la même
sortie, (0,1) une autre ; P continue ↘ seulement si a = b = 0. Même issue pour les 4 phases de P (103 cas propres, 25 sales).
Additivité : 0/103. ⇒ en LLR, logique « par déviation » : NOR immédiat, priorité ; pas de compteur. À explorer.
## Point final (15:31) : pistes 1, 5, 2, 3 faites ; piste 4 : contradiction expliquée, LLR mesuré, mémoire non trouvée.
## R-55 Porte NOR LLR en 3 fourmis, 0 case — VÉRIFIÉ 4/4 (2 moteurs, 30 000 pas)
A = 0,0,H (entrée a), B = 32,32,H (entrée b), P = −141,−40,G. P sort ↘ (voie x−y = −100) ssi a = b = 0 ; sinon P tourne ↙.
Une entrée = UNE fourmi (pas de germe de 11 cases en LLR). Enchaîner : la sortie ↘ doit être tournée ↙ (mur vertical, R-40) — à faire.
## R-56 OU LLR à 2 étages = NON(NOR) : 4 fourmis, 0 case — VÉRIFIÉ (C : 64/64 placements de P2 donnent 4/4 ; Python 4/4) (llr_ou.py)
P1 = −141,−40,G (NOR) ; P2 = −250,450,B part ↗ sur la voie x+y = 200 et croise la ligne de P1 plus loin : P2 continue ↗ ssi a OU b ;
si P1 est passée (a=b=0), P2 tourne ↘. TOUTES les voies L2 = 200…231 et 2 phases testées marchent (64/64) : en LLR l'enchaînement
est ROBUSTE (contraste avec RL : voies exactes). NOR seul : 103/128 placements propres. ⇒ piste prioritaire : ordinateur LLR.
## R-57 3 étages LLR (NOR → OU → NOR), 5 fourmis, 0 case — VÉRIFIÉ pour P3 = 540,560,D (C + Python 4/4) ; OBSERVÉ 38/64 placements (llr_3.py)
P3 part ↖ (voie x−y = w3, départ x+y ≈ 1 100) et lit la sortie ↗ de P2 : continue ↖ ssi a = b = 0. 38 des 64 placements testés (w3 = −20…11) : 4/4.
Robustesse du 3e étage moindre que du 2e (64/64), mais pas de réglage fin.
## R-58 ET LLR = NOR(NON a, NON b), 5 fourmis, 0 case — VÉRIFIÉ 4/4 (2 moteurs, 60 000 pas) ; OBSERVÉ 12/224 placements (llr_et.py)
A = −500,500,H (part de x−y = −1 000) ; B = 32,32,H ; NON a = −822,378,G (↘ sur x−y = −1 200, croise A, passe la ligne de B AVANT B) ;
NON b = 161,461,D (↖ sur x−y = −300 : croise B, pas de trace de A à cet endroit) ; Q = −840,862,B (↗ sur x+y ≈ 22) continue ↗ ssi a ET b.
Astuce : on choisit OÙ commence chaque entrée le long de son axe pour qu'une puissance ne voie que sa trace. Fragile (5 % des placements).
## Point final (15:35) : avec NOR (R-55), OU (R-56), ET (R-58) et l'enchaînement (R-57), le LLR a un jeu de portes complet sans case ;
manquent COPIE et croisement en LLR. Suite proposée : demi-additionneur LLR, puis ordinateur LLR.
## R-59 COPIE LLR (2 fourmis, 0 case) — VÉRIFIÉ 2/2 (2 moteurs) ; croisement LLR OUVERT
A = 0,0,H ; P = −141,−40,G : a = 1 ⇒ A ↙ (voie 1) ET P tourne ↙ (voie 7) = 2 copies ; a = 0 ⇒ P continue ↘ (= NON a).
Croisement en LLR : impossible directement (une trace dévie toujours celle qui passe après) ⇒ il faudra 3 XOR (OUVERT).
Fin de session 15:36. Bilan : RL = additionneurs 2 et 3 bits en un germe ; LLR = NOR, OU, ET, NON, COPIE sans case, enchaînables.
## R-60 Porte NOR LLR « à poser n'importe où » — OBSERVÉ (moteur C, 96/96)
A glissée le long de son axe k·(−1,1), k = −10…10 : 21/21 ; A décalée de k·(1,1) : 11/11 ; de k·(1,0) : 11/11 ;
P glissée le long de son axe k·(−1,−1), k = 0…20 : 21/21 ; P décalée sur le côté k·(1,−1), k = −10…10 : 21/21 ; tout translaté (k,3k) : 11/11.
Contraste avec RL (R-50 : (1,0) ⇒ 8/16). En LLR, pas de classe mod 4 : la porte se pose où l'on veut. ⇒ ordinateur LLR = prochaine étape.

## R-61 Circuit d'UN pas de la fourmi RL sur le tore 2×2 — VÉRIFIÉ 256/256 (ordinateur/v3/pas.py, schema.py) — 17/11 15:44–
État 8 bits : cases c00 c10 c01 c11, position x y, cap h1 h0 (0=H…3=G). Pas : lire, tourner (R si blanc), inverser, avancer mod 2.
Équations : h0' = ¬h0 ; h1' = h1 ⊕ h0 ⊕ c ; x' = x ⊕ ¬h0 ; y' = y ⊕ h0 ; cᵢⱼ' = cᵢⱼ ⊕ [x=i ∧ y=j] ; c = case lue (multiplexeur).
Seul h1' lit la couleur ; la position ne dépend que du cap. Circuit : 3 NON + 8 ET + 3 OU + 8 XOR = 22 portes + 19 copies.
Placement en couches (6 couches) : 188 croisements → 33 après minimisation (barycentres + échanges). Minimal ? OUVERT.

## R-62 Compilateur LLR (prototype) : fonctions booléennes → UN germe sans case — VÉRIFIÉ (2 moteurs) (ordinateur/v3/compilateur.py)
Principe : en LLR une puissance continue ssi elle ne croise aucune trace (NOR de tout ce qu'elle croise, R-55). Entrées en double voie
(une fourmi ↙ par littéral vrai et par usage). Niveau 1 : une puissance ↘ par clause (continue ssi la clause est fausse) ;
niveau 2 : une puissance ↙ croise un INTERVALLE de portes de niveau 1 (continue ssi toutes les clauses sont vraies) ⇒ forme CNF.
Pas de croisement parasite : chaque rayon ne commence qu'à hauteur de sa porte (escalier : voies w décroissantes, bandes λ croissantes).
CNF par Quine-McCluskey + couverture gloutonne. Lecture = direction ET voie (une fourmi déviée peut revenir ↙ sur une autre voie !).
Erreurs corrigées en route : rayon et puissance arrivaient au même pas au croisement (collision) ; sortie de niveau 1 inversée.
Demi-additionneur (S = XOR, C = ET) : 3 portes niv. 1 + 1 niv. 2, 4/4 C et Python. Module cap ± 1 (h1' = h1⊕h0⊕c, h0' = ¬h0) :
5 + 1 portes, 8/8 C et Python. ⇒ XOR LLR obtenu par le compilateur (étape 2, en partie).
## Point 15:56 : étapes 1 et 3 faites (prototype). Suite : pas complet compilé, croisement, étape 4.

## R-63 Le pas complet compilé en LLR, module par module — VÉRIFIÉ 7/8 modules à 256/256 (moteur C) (ordinateur/v3/pas_modules.py)
Une sortie = un module (germe à part, recentré par translation). c00' c10' c01' c11' : 3 + 1 portes, ≤ 8 fourmis, 256/256 chacun ;
x', y' : 2 + 1 portes, ≤ 5 fourmis, 256/256 ; h0' : 1 porte, 2 fourmis, 256/256 ; h1' (h1⊕h0⊕case lue, 18 clauses) : 18 + 1 portes,
≤ 67 fourmis : 197/256 (paramètres serrés, grille 16 384 : 29 sorties de grille + 30 erreurs) ; 156/256 avec la grille 32 768 ⇒ erreurs RÉELLES
avec les paramètres serrés (DA = 60, SP = 30). Paramètres larges : en cours.
Germe unique pour les 8 sorties : compilé (35 + 7 portes, 127 littéraux, T ≈ 148 000) mais trop grand pour vérifier ici (OUVERT).
Bugs de mes outils corrigés : translation de recentrage non reportée dans la lecture des voies.

## R-64 Croisement en LLR — OBSERVÉ
Direct : dans les 128 placements de R-54, une trace dévie TOUJOURS l'autoroute qui passe après (0 traversée transparente) ⇒ pas de croisement direct.
Contournement : dans le compilateur, chaque littéral est une fourmi neuve qui ne commence qu'à hauteur de sa porte ⇒ aucun croisement
n'est nécessaire en logique à 2 niveaux. Pour enchaîner des pas (sorties → entrées), il faudra des croisements : 3 XOR (OUVERT).
Mur LLR (x = −60) : dévie une 1re autoroute ↙ en ↘ (voie −124) ; une 2e sur la même voie est aussi déviée ↘ mais sur la voie −8
(elle roule sur la trace de la 1re). OBSERVÉ.

## R-65 Étape 4 : une boucle infinie (horloge + mémoire) est-elle possible ? — argument (AFFIRMÉ, à relire) + 1 test
POUR (rien ne l'interdit) : le pas de la petite fourmi est une BIJECTION des 256 états (la fourmi RL est réversible), donc son orbite
est périodique. Un système borné de fourmis est périodique (R-44) : cela n'empêche pas de simuler une bijection, au contraire —
une orbite périodique du grand système peut contenir l'orbite de la petite fourmi. R-44 n'est donc PAS un obstacle de principe.
Les navettes (R-19, R-21) montrent qu'un signal peut revenir ET effacer sa trace (portée réglable) : retour + effacement existent.
CONTRE (notre architecture actuelle) : chaque porte consomme une puissance qui part à l'infini et laisse une trace définitive ;
avec N fourmis on ne fait qu'un nombre fini de pas. Pour boucler il faut : (1) des signaux qui reviennent (navettes = horloge,
VÉRIFIÉ R-19) ; (2) des miroirs réutilisables — mur LLR : la 2e autoroute est encore déviée mais sur une autre voie (R-64),
miroir-cycle RL réutilisable (R-51 corrigé) ; (3) des portes SANS déchet ni perte : c'est exactement le modèle des boules de billard
(Fredkin-Toffoli 1982, réversible et conservatif, universel) ; nos déviations LLR ressemblent à sa « porte d'interaction »
(un signal continue, l'autre est dévié) ; (4) des traces effaçables : en LLR une case revient blanche après 3 passages, en RL après 2.
À TROUVER : une porte d'interaction LLR « propre » (les deux sorties réutilisables, pas de trace qui bloque la suite) et un miroir
qui ne garde aucune mémoire du passage (case(s) revenues à leur état). Sans cela, l'ordinateur reste « à usage unique ».

## R-63 (suite, 16:06) — le pas complet en 8 modules : VÉRIFIÉ 2 048/2 048 (moteur C) ; Python : 7 modules 1 792/1 792 + h1' 29/29 (échantillon)
Les erreurs de h1' venaient d'un BUG de mon outil trapL (64 fourmis max ; h1' en a 67) — même bug qu'en R-46. Corrigé (128, puis 256).
Paramètres larges (DA = 200, SP = 40, POFF = 200). Tailles : c..' 3+1 portes / 8 fourmis ; x', y' 2+1 / 5 ; h0' 1 / 2 ; h1' 18+1 / 67.
Germe UNIQUE du pas (35 + 7 portes, ≤ 110 fourmis, T ≈ 239 000) : trop grand pour la grille C ; test Python sur 16 états en cours.
## Point 16:06 : étapes 1, 3 faites ; 2 (XOR via compilateur ; croisement direct impossible) ; 4 argument écrit.

## R-66 Effacement par passages répétés en LLR — OBSERVÉ (négatif)
1, 2 ou 3 fourmis LLR sur la même voie (la 2e et la 3e partent derrière, écart 40 ou 100) : la 2e et la 3e TOURNENT ↘ en touchant la
trace de la 1re (elles ne roulent pas dessus) ; la trace (1 300 cases non blanches sur le tronçon témoin) reste identique.
⇒ « une case revient blanche après 3 passages » ne s'obtient pas en envoyant 3 autoroutes sur la même voie. OUVERT : autre géométrie.

## R-67 Le pas COMPLET de la petite fourmi en UN SEUL germe LLR (sans case) — OBSERVÉ 16/16 états tirés au hasard (Python) (pas_unique_py.py)
35 portes niv. 1 + 7 niv. 2 (h0' lu au niveau 1), ≤ 110 fourmis, T = 238 940 pas ; les 8 sorties justes pour les 16 états testés.
Trop grand pour la grille du moteur C (32 768) ⇒ 1 seul moteur ; ≈ 22 s par état en Python. Échantillons supplémentaires en cours.
Avec R-63 (chaque module VÉRIFIÉ 256/256, 2 moteurs), c'est le 1er « pas de fourmi calculé par des fourmis ».
Suite R-67 (16:22) : 2e tirage 16/16, 3e tirage arrêté (mémoire) après 1 état juste ⇒ 33/33 états distincts justes (Python). Les 8 sorties chaque fois.
## Point final 16:22. Bestiaire 10 complet (7,5 Mo, avec le germe unique) NON envoyé au Drive (limite 4,2 Mo) : la version de 16:11 (sans le germe unique) y est.

## R-68 Le pas complet de la petite fourmi en un germe — VÉRIFIÉ 256/256 (moteur JavaScript du simulateur v7, indépendant) — 17/11 soir
docs/test_circuits.js tout R67 : les 8 sorties justes pour les 256 états (254 s). Avec le moteur Python (33/33 états tirés au hasard, R-67),
deux moteurs indépendants. Aussi, avec le moteur JS : R-39 additionneur 4 bits 256/256, R-53 64/64, les 8 modules R-63 256/256 chacun,
et les 37 circuits de la bibliothèque v7 justes. Vérification finie (temps fini), comme toujours.

## R-82 Contrôle croisé des deux moteurs + écart « demi-tour » — VÉRIFIÉ (calcul, 2 moteurs) — 18/11 S1
`src/fourmi` et `ant_controle.c` d'accord sur le départ blanc (9 977), 512/512 configs 3×3 (même dérive, même début)
et les 22 collisions 1 case (mêmes 22 durées de chaos). Le « demi-tour » de R-16 est la PREMIÈRE autoroute ; `ant obst`
notait la DERNIÈRE (critère de boîte) : le demi-tour retraverse le germe et finit en virage (66 924 pas). Correction :
T(3) = 51 277, T(4) = 133 984 (fourmi coin bas-gauche, cap haut) — OBSERVÉ. Détails : recherche/autoroute/E0_controle.md.
Commande : `./ant obstf 150` (nouveau mode), `./ant box 3 v`.

## R-83 Lemme du certificat d'autoroute — DÉMONTRÉ (preuve écrite) + implémenté — 18/11 S1
Une fourmi, période p : si les p pas « à blanc » depuis l'état courant lisent V, reviennent au même cap avec d ≠ 0
(F1), si le motif se recopie (F2 : Pa(v+d) = Pv(v)), si les cases neuves sont blanches (F3), si V est convexe le
long de d (F4) et si la bande ⋃(V+kd) \ V est blanche, alors autoroute pour toujours (récurrence sur les périodes).
Toute règle à une fourmi. Vérification finie (au-delà de la boîte support ∪ visité, tout est blanc).
Conséquences VÉRIFIÉES par calcul exact + lemme = DÉMONTRÉ : départ blanc → autoroute 104 pour toujours dès 9 977 ;
512/512 configs 3×3 (fourmi coin, cap H) certifiées, max 51 277 ; 122 obstacles 1 case certifiés.
Le moteur s'arrêtait à 16 384 sur une autoroute non certifiée (obstacle plus loin) : corrigé avec -cert.
Commande : `./fourmi -cert "RL|0,0,H|"` ; `-c0 T`. Détails : recherche/autoroute/E1_certificat.md.

## R-84 Boîtes 3×3 et 4×4 — DÉMONTRÉ (calcul exact + certificat R-83) — 18/11 S1
Fourmi (0,0) cap H au coin (bas-gauche en y vers le haut) de la boîte, cases (i mod N, −⌊i/N⌋) : 512/512 et
65 536/65 536 configurations construisent l'autoroute 104 pour toujours. T(3) = 51 277, T(4) = 133 984
(cases 2,0;3,0;2,-1;3,-1;3,-3). ≈ 1 min sur 2 cœurs. Commande : data/box4.in, `fourmi -T 4000000 -cert -lot`.

## R-85 Théorème T1 : une case noire n'importe où → autoroute 104 pour toujours — DÉMONTRÉ (A, B) + (C) À RELIRE — 18/11 S1
(A) c ∈ [−150,150]² : 90 601/90 601 certifiées ; plus court 310 (c = 0,−2), plus long 106 258 (c = 7,−7).
(B) hors boîte et hors bande : certifié à 9 977 (argument direct). (C) loin dans la bande : 22 classes = R-16 ;
pas certifié exactement affine en k (pente 52, demi-tour 104) pour k = 100…1 150 (5 533 calculs) ; lemme de
translation esquissé. Le demi-tour est la seule issue qui roule sur la trace (obstacle pour plusieurs îlots).
Détails : recherche/autoroute/E2_epars.md. Germes : resultats/germes_2026-11-18.json.

## R-86 T1, partie (C) : lemme de translation — DÉMONTRÉ pour 21 classes sur 22 — 18/11 S1
Couplage X_{k+2}(t+104) = X_k(t) + d hors de D (D = écart fixe près du germe, p = −x+y ≤ 25 sur D), stable par
récurrence car p augmente de 4 par translation. Condition vérifiée une fois à k₀ = 100/101 avec le 2ᵉ moteur :
min p après impact ∈ [157, 225] > 21 pour 21 classes. Reste la classe du demi-tour (c = (−19−k, k), k pair ≥ 100) :
OBSERVÉE (certifiée pour k ≤ 1 150), plan de preuve dans E2_epars.md. Commande : `./ant pmin J K T`.

## R-87 Théorème T1 complet : départ blanc + UNE case noire quelconque → autoroute 104 pour toujours — DÉMONTRÉ (à faire relire) — 18/11 S1
Classe du demi-tour (c = (−19−k, k), k pair ≥ 100) traitée par double couplage : translation jusqu'au milieu de la
trace, puis identité sans translation (X_{k+2} = X_k décalée de 208 pas). Conditions finies U1–U4 vérifiées à
k₀ = 100 (`./ant uturn -19 100 150 79678`) ; prédiction cert(k+2) = cert(k)+208 vérifiée (79 678 / 79 886 / 80 094).
Avec R-85 (A, B) et R-86 (21 classes) : T1 démontré pour toute position de la case. Pas trouvé dans la littérature
(2 recherches). Détails : recherche/autoroute/E2_epars.md.

## R-75 Deux cases noires loin l'une de l'autre — OBSERVÉ (2 684 configurations, toutes certifiées) — 18/11 S1
1re case dans chacune des 22 classes (k = 100/101), 2e case à 200 cases devant l'autoroute qui en sort (122 positions) :
toutes construisent l'autoroute pour toujours (certificat R-83 ⇒ chacune DÉMONTRÉE ; la famille infinie : pas encore).
22 cases touchables par autoroute (484 doubles collisions) ; retard max 198 026. Détails : E2_epars.md.

## R-76 Théorème T2 : îlot de 2 cases voisines (côté ou coin) n'importe où → autoroute 104 pour toujours — DÉMONTRÉ (à faire relire) — 18/11 S1
Même schéma que T1. (A) 362 404/362 404 certifiées dans [−150,150]² (plus court 197, plus long 117 736 :
{(−29,11),(−29,12)}). (C) 128 classes lointaines exactement affines (k = 100…300) : 91 par translation (pmin OK),
5 demi-tours (uturn OK, + condition « diagonales disjointes » pour les 3 qui repartent dans la direction d'origine),
32 non touchées. Commandes : data/dom.in, data/domfar.in (python, voir E2_epars.md), outils/preuves_dominos.txt.

## R-77 Chaîne de 4 demi-tours successifs — OBSERVÉ (chaque configuration certifiée) — 18/11 S1
Chaque case ajoutée dans l'unique classe demi-tour de l'autoroute courante : 4 étapes, toutes certifiées
(dernière : 4 cases, autoroute dès 3 361 062). Directions (−2,2) → (−2,−2) → (2,2) → (−2,−2) → (2,2). Pas de ping-pong.
Commande : `recherche/autoroute/outils/chaine_demitours.py 5 150`. Détails : E2_epars.md.

## R-78 Théorème T3 : îlot de 3 cases en L ou en ligne, n'importe où → autoroute 104 pour toujours — DÉMONTRÉ (à faire relire) — 18/11 S1
(A) 246 072/246 072 certifiées ([−100,100]² ∪ bande) ; plus rapide 158 (ligne −1,3;0,3;1,3), plus lent 93 138 (L 11,10;12,10;11,11).
(C) 228 classes lointaines affines : 148 translations OK, 4 demi-tours OK (dont un qui repart en −d), 76 non touchées.
Outils génériques ajoutés : `ant pmin/uturn` à n cases, `outils/preuves_loin.py`. Détails : E2_epars.md.
5×5 (É3) : tranches [0,200 000) et [1 600 000,1 800 000) faites, 400 000/400 000 certifiées, max 155 668.
(R-78, complément) 5×5 : 1 200 000 masques certifiés ([0,600 000) et [1 600 000,2 200 000)), max 184 622.

## R-79 Juge des demi-tours raffiné (diagonales Δ) ; T1–T3 revérifiés — DÉMONTRÉ — 18/11 S2
La condition U4/Z de S1 ignorait les diagonales de la trace ; avec Δ = diagonales x+y touchées après 9 977 (+ îlot),
les 10 demi-tours de T1, T2, T3 passent (p* = 90). Outils : `outils/juge_uturn.py`, `outils/cherche_s.sh`.
Détails : E2_epars.md (section S2).

## R-80 Théorème T4 : tout îlot contenu dans un carré 3×3 (400 formes), n'importe où → autoroute 104 pour toujours — DÉMONTRÉ sous réserve de relecture — 18/11 S2
(A) 1 813 428/1 813 428 certifiées (plus rapide 142, plus lent 228 739 : −56,28;−54,28;−54,30). Trou y = 99 (aussi dans
T3) comblé : 76 000/76 000. (C) 15 200 classes lointaines : 4 032 hors bande (cert 9 977), 10 690 translations, 439 demi-tours,
42 aller-retour triples, 3 quadruples ; toutes prouvées (bases k₀ = 100/101 ou 200/201, k = 100…600 calculés pour les 62 cas
difficiles). Commandes : outils/gen_ilots.py A|C, preuves_loin.py, cherche_s.sh, cherche_triple.sh, preuves_ilots_3x3*.txt.

## R-81 Couplages multiples (aller-retours sur la trace) — DÉMONTRÉ sous réserve de relecture du code — 18/11 S2
Repères alternés translation (site) / identité (germe), ensembles d'accord étendus par la règle « un pas de translation »
fermée par chaînes. `ant triple2` : 42/42 classes de pente 156 ; `ant multi` NS=3 : 3/3 de pente 208 ; contrôles :
multi NS=1 = uturn (423), NS=2 = triple2 (42), triple2 échoue sur les pentes 208. Détails : E2_epars.md (S2).
(R-81, complément) Relecture de `ant multi` : faille du test Z pour NS impair (accord de la phase NS−2 oublié) corrigée ;
les 3 classes de pente 208 restent démontrées.
(R-80, complément) Contrôle indépendant des récurrences : 200 classes lointaines tirées au hasard + les 62 classes
difficiles, pas certifié prédit par la formule affine à k = 2 000/2 001 puis calculé : 262/262 exacts (pas et direction), 7 s.
(É3, S2) 5×5 : tranches [600 000, 1 000 000) et [2 200 000, 2 600 000) certifiées ; total 2 000 000 masques, max 188 466.

(Renumérotation 18/11, demande de Pierre-Malo) Les entrées de la séance autoroute S1 numérotées R-69 à R-74 faisaient doublon
avec la branche lucid-clarke : renumérotées R-82 (contrôle croisé), R-83 (certificat), R-84 (boîtes 3×3/4×4), R-85 (T1 A-B),
R-86 (T1 translation), R-87 (T1 complet), partout dans le dépôt. R-75 à R-81 inchangés. Bestiaires : fiches autoroute S1 → n° 12,
S2 → n° 13.

## R-88 Contrôle direct « deux mondes » des couplages — VÉRIFIÉ (calcul exact) — 18/11 S3
`./ant deux J K CE NS s1..sNS offsets` simule X_k et X_{k+2} et vérifie pas à pas (de 9 977 à CE+104) qu'au temps
t + 104(i+1) la fourmi de X_{k+2} est en a_k(t) (+d si i pair), même cap, même couleur lue. Résultats : 45/45 classes
aller-retour (NS = 2, 3), 423/423 demi-tours où `multi` dit OK, 300/300 translations tirées au hasard : couplage EXACT.
Contrôles négatifs : sans changement de repère, ou changement trop tard → écart détecté ; les 2 demi-tours où `multi`
échoue (p* mal choisi) montrent aussi un écart. Le vérificateur `multi` n'a donc jamais dit OK à tort sur ces 768 cas
(ce contrôle porte sur k₀ → k₀+2 ; la récurrence reste celle de `multi`). Outil : `outils/deux_mondes.sh`.

## R-89 Lacune de `pmin` (direction finale −d) trouvée et comblée ; T4 tient — DÉMONTRÉ (sous réserve de relecture) — 18/11 S3
`pmin` (S1) ne vérifiait pas la direction finale ; si l'autoroute finale part en −d, sa bande Z descend en p et peut
traverser D. Nouvelle condition (dans `ant multi` NS = 0) : direction −d ⇒ diagonales x+y de la fenêtre finale hors de
celles de D (d conserve x+y) ; sinon p > MPD−4. Recensement : T1, T2, T3 n'ont AUCUNE translation finissant en −d (résultats
inchangés) ; T4 en a 92. `multi` NS = 0 sur les 10 690 translations de T4 (bases 100/101 et 200/201) : toutes OK
(les 5 échecs à la base 100 sont les classes déjà reprises à la base 200). Aussi corrigé : NS = 0 lisait HV[−2] (bug).

## R-90 T5 : « C₀ + une case noire n'importe où » pour une base C₀ quelconque certifiée — exemple DÉMONTRÉ (sous réserve de relecture) — 18/11 S3
`ant multi`/`deux` acceptent une base (BASE, T0). Exemple C₀ = {(−56,28),(−54,28),(−54,30)} (T0 = 228 739, MPD = 149) :
(A) [−100,70]×[−50,125] ∪ bande x+y ∈ [70,120], y < 300 : 39 429/39 429 certifiées (plus rapide 310 avec (0,−2), plus lent
333 741 avec (−56,78)) ; (B) hors zone et hors bande : certifié à T0 ; (C) 22 classes (x+y ∈ [90,100]), toutes de pente 52,
`multi` 22/22, `deux` 22/22. Commande : `BASE="-56,28;-54,28;-54,30" T0=228739 ./ant multi J K CE 0`. Détails : E2_epars.md (S3).

## R-91 Deux cases loin, 1re case fixée : la 2e n'importe où loin dans la nouvelle bande — DÉMONTRÉ (partie lointaine, sous réserve de relecture) — 18/11 S3
Pour les 9 positions de c₁ (k = 100/101) dont l'autoroute repart en (−2,+2) : base C₀ = blanc + c₁ ; `outils/relatif.py`
trouve 22 classes par base (21 translations, 1 demi-tour qui revient au 1er site) : 198/198 preuves `multi` OK (seuils p*
au-dessus de la zone D de la base, ≥ 300 pour le demi-tour), 198/198 couplages exacts (`deux`). Zone proche (A) des 9 bases
(264 470 cas) : lancée en fin de S3, résultat en S4. Résultats : resultats/relatif/.

## R-92 Faille du point 2 du lemme 3 (cases hors Δ) corrigée ; T1–T4 revérifiés — DÉMONTRÉ (sous réserve de relecture) — 18/11 S4
« Hors des diagonales Δ_i : blanches partout » est faux pour les cases du germe (touchées avant T0, sur d'autres
diagonales). Correct : repère identité (i impair) → ces cases valent la même chose dans les deux mondes (même germe, jamais
retouchées) : Δ_i d'origine suffit ; repère translation (i pair) → il faut aussi exclure les diagonales de D (germe, base).
`ant multi` corrigé (Δ_i ⊇ diagonales de D pour i pair). Revérification complète : 439/439 demi-tours (T1–T4, p* recherché,
`outils/preuves_demitours_S4.txt`), 42/42 triples, 3/3 quadruples, 10 690 translations (NS = 0, déjà avec D en S3) : tout OK.

## R-93 Deux cases noires : la 1re dans l'une des 22 classes de T1 à k = 100/101, la 2e n'importe où → autoroute 104 pour toujours — DÉMONTRÉ (sous réserve de relecture) — 18/11 S4
Base C₀ = blanc + c₁ (13 bases pivotées d'un quart de tour, cap initial D/B/G, pour ramener la dérive à (−2,+2)).
(C) 22 × 22 = 484 classes de c₂ lointaines : 484/484 `multi` + 484/484 couplages exacts (`deux`). (A) zones proches :
264 470 + 418 610 = 683 080 cas, tous certifiés. (B) direct. Plus lent : c₁ = (−119,100) (le demi-tour), c₂ = (7,−19) :
264 331 ; puis c₁ = (−121,101), c₂ = (−144,104) : 181 641. Outils : `outils/relatif.py "BASE" T0 K2 CAP`, H0 pour `ant`.
Fichiers : resultats/relatif/ (bases9.txt, bases13.txt, preuves rel_*.txt / rel13_*.txt).

## R-94 Deux cases loin : récurrence en k₁ (la 1re case s'éloigne aussi) — 968 familles à un paramètre DÉMONTRÉES ; double récurrence OUVERTE — 18/11 S4
Pour les 22 classes de c₁ × 22 classes de c₂ × 2 écarts (k₂ = k₀, k₀+20), on vérifie avec `ant multi` les conditions de la
récurrence k₁ → k₁+2 : 908 en NS = 0, 50 en NS = 1, 2 en NS = 2 (îlot {c₁, c₂} déplacé en bloc le long de d). Les 8 cas
restants (c₁ = demi-tour) demandent de garder c₂ FIXE (l'autoroute repart du germe, indépendante de k₁) : c₂ mis en base
(BASE = c₂, T0 = 9 977), îlot c₁ seul, NS = 1 : 8/8 OK. Chaque cas vérifié prouve la famille « k₁ ≥ 100 » à écart fixé.
Ce qui manque pour le théorème « deux cases loin » complet : montrer que ces conditions valent pour TOUS les écarts k₂
(uniformité, vue ici sur 2 à 4 valeurs). Outils : `outils/essai_k1.sh`, resultats/relatif/recurrence_k1.txt.
(R-94, complément) Uniformité en k₂, test : 30 paires de classes tirées au hasard × 11 écarts (k₂ = k₀ … k₀+200, pas 20) :
330/330 configurations certifiées, et la récurrence en k₁ passe pour les 330 (NS = 0 partout). OBSERVÉ (pas une preuve).

## R-95 Deux cases LOIN (les deux distances variables) : 454 paires de classes sur 484 — DÉMONTRÉ (sous réserve de relecture) — 18/11 S5
Lemme de transport (E2b_couplage.md, S5) : la condition NS = 0 de la récurrence en k₁ se transporte de m à m+1 par les repères
de la récurrence en m (R-93), quand d₂ = d ou d₂ ⟂ d (p ne diminue pas). D'où : pour 454 des 484 paires (classe de c₁, classe de
c₂), toute position k₁ ≥ k₀, m ≥ m₀ mène à l'autoroute pour toujours. Restent 30 paires : 25 + 1 dont la récurrence en k₁
change de repère (NS = 1, 2), 4 à « c₂ fixe » (c₁ = demi-tour). Contrôle : 40/40 prédictions exactes à (k₀+40, m₀+10).
Outil : `outils/transport.py` ; résultats : resultats/relatif/transport.txt.

## R-96 Deux cases loin : 28 paires de plus (récurrence en k₁ avec changement de repère) — 482/484 DÉMONTRÉES (sous réserve de relecture) — 18/11 S5
`ant multi` compte maintenant par quel critère chaque lecture est acceptée (fenêtre, hors Δ, p, règle « un pas »). Sans la
règle, la vérification se transporte en m (E2b_couplage.md, S5). G1 (c₁ = demi-tour, c₂ fixe en base) : 21/22 sans la règle ;
G2 (d₂ = d) : 7/8. Avec R-95 : 454 + 28 = 482 paires sur 484. Restent OBSERVÉES : c₁ = (−119,100) avec c₂ = (−401,−409)
(règle utilisée 50 fois) et c₁ = (−127,100) en NS = 2 (règle 72 fois).
(R-96, vérifications) G1 : les lectures acceptées « hors Δ » APRÈS le 1er contact avec c₂ ont des diagonales ≤ −746, sous
Δ₁ = [−82, 56] : elles s'en éloignent quand c₂ glisse (x+y −4 par pas) ; pour c₂ = (−401,−409) elles vont jusqu'à +102 →
reste OBSERVÉE (même avec p* = 110, sans règle). G2 : après s₁, max p = 96 ≪ p(c₂) ≈ 820 : aucune lecture de phase 1 près
de c₂. Bilan inchangé : 482/484.

## R-97 Théorème T6 : deux cases noires éparses (|cᵢ| ≥ 417, |c₁−c₂| ≥ 545, norme max) → autoroute pour toujours — DÉMONTRÉ sous réserve de relecture, sauf 2 paires de classes (OBSERVÉES) — 18/11 S5
Assemblage de T1 (c₁ seule), de l'argument (B) relatif à la base blanc + c₁, et de R-95/96 (deux cases loin). R et D
calculés sur les 22 classes (`outils/epars_RD.py` : D = 544 atteint pour c₁ = (−128,100) ; R = 417 pour la classe du
demi-tour, dont la 2e bande part du germe). Contrôle : 300/300 paires aléatoires du domaine certifiées. Détails : E2_epars.md.

## R-98 Transport dual : les 2 dernières paires → 484/484 ; T6 (deux cases éparses) SANS exception — DÉMONTRÉ (sous réserve de relecture) — 18/11 S5
Pour les 2 paires restantes, c'est la vérification de la récurrence en m (a), sans la règle « un pas », qu'on transporte le
long de k₁ par les repères de (b), prouvée à m₀ seulement. Détails : E2b_couplage.md. Contrôle : 6/6 prédictions exactes.
D'où R-95/96/98 : 484/484 paires de classes, et T6 : |c₁|, |c₂| ≥ 417, |c₁ − c₂| ≥ 545 ⇒ autoroute pour toujours.
(R-98, vérifications de chronologie) G2 (c₁ = (−127,100)) : changement de repère de (a) à t = 101 288, avant celui de (b)
(106 488 ; 2e à 115 872). G1 (c₁ = (−119,100), c₂ = (−401,−409)) : (b) passe en repère identité à 68 836, avant le 1er
contact avec c₂ (99 410). Les deux hypothèses du transport dual sont donc vérifiées.

## R-99 Outil « T1 relatif » complet ; exemple : domino le plus lent + une case n'importe où — DÉMONTRÉ (sous réserve de relecture) — 18/11 S5
`outils/t1relatif.py "BASE" CAP [K2]` fait (A) + (C) pour une base déjà pivotée (dérive (−2,+2)). Base {(−29,11),(−29,12)}
pivotée (cases (−11,−29),(−12,−29), cap D), T0 = 117 736 : (C) 22/22 classes (toutes de pente 52) + 22/22 couplages exacts ;
(A) 20 793/20 793 certifiées (plus lent 298 348) ; (B) direct. Brique pour « trois cases éparses ».

## R-100 Trois cases éparses (|cᵢ| ≥ 417, écarts ≥ 545) : 300/300 triplets aléatoires certifiés — OBSERVÉ — 18/11 S5
Tirage : chaque case sur la bande de départ (k ∈ [417, 1 500]) avec probabilité 0,4, sinon uniforme dans [−3 000, 3 000]².
Le plus lent : 216 750. Indice pour un théorème T7 « trois cases éparses » (même assemblage que T6, bases à deux cases).
(É3, S5) 5×5 : [4 000 000, 6 000 000) certifiées ; tout [0, 6 000 000) est certifié ; nouveau max 209 637 (tranche 4,0–4,2 M).

## R-101 Transitoires extrêmes (É4), boîtes n×n : record(8) ≥ 220 334, record(n+1) ≥ record(n) — OBSERVÉ (minorants ; chaque configuration trouvée est DÉMONTRÉE par certificat) — 18/11 S6
Montée de colline (`outils/colline.py`), graines par recopie au coin. Résultats : 6×6 185 471 sans graine ; 5×5 136 663
seulement (l'exhaustif partiel a 209 637) ; 8×8 220 334 (= record 5×5 + 4 cases), confirmé par `ant une` (220 333, début de
période). 0 NONCERT. Méthode faible sur ce paysage. Détails : recherche/autoroute/E4_transitoires.md, graphe resultats/records_transitoire.png.
Littérature : article MFCS 2026 (temps d'échappement) non lu (arxiv.org inaccessible).

## R-102 Boucle gelée sur l'autoroute nue : suite périodique (104), 34 valeurs, max 152 ; boucle à ≤ 11 cases de la fourmi — VÉRIFIÉ (calcul exact) ; corrige l'acquis « L ≤ 112 » — 18/11 S7
Près du germe L monte à 172 ; juste après le début d'autres autoroutes jusqu'à 4 072 ; L est toujours ≡ 0 mod 4. Aucun seuil
sur L ne sépare chaos et autoroute (chaos : L de 4 à 1 388). Commande : `./ant obs N MASQUE DEBUT TFIN PAS`.

## R-103 Conjecture C-L : si L(t) imite la suite de l'autoroute nue pendant 104 pas, la fourmi construit une autoroute — OBSERVÉ (4 612 configurations) — 18/11 S7
Hors des plages d'autoroute (trace périodique ≥ 104 pas), imitation ≤ 49 pas ; autoroute temporaire de 1 054 pas trouvée dans le
record 5×5 (imitation 758 pas, pendant la plage) ; calage final de −4 à +623 pas après le début. Commande : `./ant imite N MASQUE DEBUT`.
Détails : recherche/autoroute/E5_observables.md ; données : resultats/imite_campagne.txt.
(R-103, complément) 700 configurations diverses (T1, deux cases loin, îlots 3×3 ; 302 avec autoroute temporaire) : imitation
hors autoroute ≤ 83 pas ; le max est atteint juste APRÈS la cassure d'une autoroute temporaire (la boucle locale ne voit pas
encore le choc). C-L tient (83 < 104) mais la marge est mince ; variante à 208 pas proposée. Données : resultats/imite_divers.txt.

## R-104 Statistiques du transitoire, boîtes aléatoires — OBSERVÉ — 18/11 S7
6 800 000 boîtes 5×5 certifiées (exhaustif partiel) : pas certifié médian dans [2 048, 4 096) ; 15,2 % ≥ 8 192 ; 4,8 % ≥ 16 384 ;
0,05 % ≥ 65 536 (le départ blanc, 9 977, est donc parmi les ≈ 15 % les plus lents). Régression : corrélation nulle entre le nombre
de cases noires et log(transitoire) (r² = 0,000 en 5×5 sur 800 boîtes aléatoires ; 0,005 en 6×6 sur 300).
(R-103, grande échelle) Les 65 536 boîtes 4×4 : imitation hors autoroute ≤ 73, calage de −34 à +940 pas, 6 autoroutes temporaires ;
5 968 îlots/paires : ≤ 89 ; 491 configurations éparses : ≤ 22. Total ≈ 74 300 configurations distinctes : C-L tient (max 89 < 104).

## R-105 Germes (É6) : transitoire minimal en fonction du nombre de cases ; germe R-20 certifié dès 0 ; 1 à 3 cases dans [−5,5]² toutes certifiées — DÉMONTRÉ (cas cités) / bornes OBSERVÉES — 18/11 S7
k = 0…11 : 9 977, 310, 162, 126 (exacts dans [−5,5]², k ≤ 3), ≤ 114, ≤ 106 (faisceau), ≤ 69, ≤ 61, ≤ 55, ≤ 44, ≤ 38 (sous-ensembles
du germe de R-20), 0 (germe de R-20, CERT 0 : autoroute pour toujours, DÉMONTRÉ). 288 100 configurations à ≤ 3 cases dans [−5,5]² :
toutes certifiées (max 161 286). Détails : recherche/autoroute/E6_germes.md ; graphe resultats/germes_transitoire_min.png.

## R-106 Dynamique inverse : passé du départ blanc (autoroute à rebours dès 10 081 = 9 977 + 104), passé du germe minimal (4 426 pas de chaos), 200/200 boîtes aléatoires ont une autoroute à rebours — OBSERVÉ — 18/11 S7
Outil : `recherche/autoroute/outils/rebours.py` (pas inverse exact, aller-retour contrôlé). Probablement lié à une symétrie connue
(réversibilité de la fourmi) : à vérifier dans la littérature. Détails : E6_germes.md.

## R-107 Explication de R-106 : le passé = le futur de la fourmi retournée — DÉMONTRÉ (calcul direct, sans doute connu) — 18/11 S8
Le pas inverse (revenir en a−dir(h), retourner la case, tourner selon sa couleur) est exactement un pas direct de la fourmi placée
en a−dir(h) avec le cap h+2 (la couleur avant retournement donne le même virage ; reculer = avancer avec le cap opposé). Donc le
passé d'une configuration est le futur de la même grille avec la fourmi retournée ; « toute configuration a une autoroute à rebours »
est équivalent à la conjecture. Vérifié : 60/60 boîtes aléatoires, positions et grilles identiques sur 3 000 pas.

## R-108 Germes à 4 cases : toutes les configurations de 4 cases dans [−4,4]² (1 581 580) construisent l'autoroute — DÉMONTRÉ (certificat) ; transitoire minimal à 4 cases dans [−4,4]² = 67 — 18/11 S8
Plus court : −4,−1;−2,1;−1,2;0,3 (cap H) → 67 pas (la borne de S7 était 114) ; plus long : −3,−1;−3,0;−2,4;2,−2 → 149 266.

## R-109 É7, « ping-pong le plus court » : 8 renversements successifs avec 8 cases dans une boîte de rayon 67 (certifié à 136 818), puis plus de case renversante proche — OBSERVÉ — 18/11 S8
Méthode gloutonne `outils/pingpong.py` (case la plus proche devant la fourmi qui renverse la direction finale). Pas de décor fini
qui occupe la fourmi indéfiniment ; explication de l'échec et pistes : recherche/autoroute/E7_contre_attaque.md.

## R-110 Germes à 5 cases : toutes les configurations de 5 cases dans [−3,3]² (1 712 304) construisent l'autoroute — DÉMONTRÉ ; transitoire minimal à 5 cases dans [−3,3]² = 62 — 18/11 S8
Plus court : −3,1;−2,0;−1,−1;−1,1;1,−3 → 62 ; plus long : −3,0;−2,−3;0,2;1,−2;1,2 → 186 217. Détails : E6_germes.md.

## R-111 Boîtes 5×5 : [0, 9 200 000) certifiées (27 % des 33,5 M) ; nouveau max 252 046 — DÉMONTRÉ pour ces boîtes ; record(n) ≥ 252 046 pour n ≥ 5 — 19/11 S8 (fin)
Record : cases 0,0;1,0;2,0;0,−1;0,−2;2,−2;3,−2;0,−3;1,−3;4,−3;1,−4;2,−4 (fourmi 0,0,H, masque 6927399) : certifié à 252 046 ;
2ᵉ moteur `ant une 5 6927399` : début 252 046. Il dépasse le record 8×8 de R-101 (220 334) ; par recopie au coin, record(n) ≥ 252 046
pour tout n ≥ 5 (OBSERVÉ, minorant). Tranches : resultats/box5/.

## É8 Synthèse S1–S8 (séance S9) — 19/11
`recherche/autoroute/SYNTHESE.md` mise à jour (germes R-105/108/110, rebours R-107, observations R-101 à R-104, R-109, R-111) +
tableau de nouveauté résultat par résultat + liste de relecture (certificat, couplage, transport, `ant multi`, R-107).
1 recherche web : MFCS 2026 (Etse, arXiv 2606.26677) borne le temps d'ÉCHAPPEMENT d'un domaine fini (borne factorielle pour
les carrés), pas le transitoire avant l'autoroute : nos records (R-101, R-111) restent non trouvés. PDF : resultats/Synthese autoroute S1-S9.

## R-112 É7 « autoroute × vieille trace » : 328 collisions (trace de 200 périodes, 4 orientations, tous décalages utiles) → 328 autoroutes certifiées ; perpendiculaire : 8 classes (traverse, relais le long de la trace, remonte la trace, demi-tour) — DÉMONTRÉ (ces 328 configurations) / « une trace = un site de plus » OBSERVÉ — 19/11 S9
`recherche/autoroute/outils/trace_croise.sh 200 50 58 350 358 1` (et rot 3 : -350 -342 -50 -42 ; rot 2 : -500 -496 488 513 ; rot 0 : -100 -96 88 113).
Données : tableau dans recherche/autoroute/E7_contre_attaque.md §5. Aucune boucle. Au passage : `src/fourmi` tronquait les lignes
> 16 ko (bug silencieux ; sans effet sur les résultats autoroute, dont les configurations ont ≤ 25 cases ; autres usages anciens non revérifiés) ; corrigé (1 Mo), 19/19 tests.
(R-112, contrôle croisé) 2ᵉ moteur : nouveau mode `recherche/autoroute/ant lot [MAXS]` (lit le format de src/fourmi). Les 328
configurations : même direction finale 328/328 ; début (ant) et certificat (fourmi) à ≤ 1 pas près 322/328, ≤ 3 pas pour les 6
autres (le certificat arrive 2 à 3 pas après le début de la trace périodique). Un premier essai donnait 2 désaccords : bug de lecture
du cap dans le nouveau mode (corrigé ; une simulation directe a tranché pour fourmi).

## R-113 Croisement d'une vieille trace (perpendiculaire) : loin des bouts (20 ≤ s ≤ 160 sur 200), les 8 classes ne dépendent ni de la longueur P (120 à 400) ni du point de croisement ; temps linéaires (longer : 22 826 − 4s ; remonter : 12 638 + 20s) — OBSERVÉ — 19/11 S9
Boucle sur s : `a=$((2*s-150)); b=$((2*s+150)); recherche/autoroute/outils/trace_croise.sh 200 $a $((a+4)) $b $((b+2)) 1`.
Tableau : recherche/autoroute/E7_contre_attaque.md §5. Piste : théorème « départ blanc + une trace d'autoroute quelconque loin » par couplage.
(R-113, suite) Perpendiculaire construite vers (2,2) : 8 classes (4 longent, 3 traversent, 1 demi-tour), indépendantes de s pour
20 ≤ s ≤ 190. De face : 88/100 issues indépendantes de P (150, 200, 300) ; les 12 autres remontent toute la trace jusqu'à son germe
et dépendent de P. Même sens : 100/100 indépendantes de P. Toutes certifiées. Fichiers data/tc_r*_P*.txt (non suivis).

## R-114 Germes dans le carré [−2,2]² : toutes les configurations de 6 cases (134 596) et de 7 cases (346 104) construisent l'autoroute — DÉMONTRÉ (certificat) ; minima exacts dans ce carré : 120 (6 cases), 68 (7 cases) — 19/11 S9
`recherche/autoroute/outils/germes_k.sh K 2` (fourmi 0,0,H, cases ≠ (0,0)). 6 cases : min 120 (1,−2;2,−2;−2,1;2,1;1,2;2,2), max 105 789
(0,−2;1,−2;1,−1;1,0;−1,1;−1,2). 7 cases : min 68 (2,−2;−2,−1;1,−1;1,0;0,1;1,1;−2,2), max 167 636 (−2,−2;−1,−2;2,−2;1,−1;2,−1;−1,2;2,2).
Les bornes de R-105 (≤ 69 à 6 cases, ≤ 61 à 7 cases) viennent de boîtes plus grandes : le carré [−2,2]² ne fait pas mieux.

## R-115 Collision de face avec une vieille trace, cas où la fourmi remonte toute la trace : l'issue dépend de la longueur P seulement par P mod 12 (P = 100 à 161, 2 décalages) ; les pas certifiés croissent linéairement en P — OBSERVÉ (chaque configuration DÉMONTRÉE) — 19/11 S9
Pointe de la trace fixée ; `for P …; a=$((-100-2*P)); b=$((100+2*P-12+j)); trace_croise.sh $P $a $((a+1)) $b $((b+1)) 2` (j = 7, 13).
j = 7, P ≡ 0 (mod 4) : (2,2), (2,2), (−2,2) selon P mod 12 = 4, 8, 0 (P = 100…160) ; P impair : toujours (2,2), pas de période 3.
j = 13 : (2,2) / (−2,−2) / (2,2)-autre classe, période 12 en P. Lecture : la fourmi roule sur la trace jusqu'à son germe et y
arrive avec une phase qui dépend de P mod 12 (le rouleur n'avance pas d'un multiple de la période de la trace).

## Relecture (S9) du code du certificat `certifie()` (src/fourmi.c) — pas d'erreur trouvée — AFFIRMÉ (relecture par Claude, pas humaine) — 19/11
Points vérifiés : V et couleurs lues à blanc sur une copie ; F2/F3 + Z donnent nouveau(v+d) = ancien(v) sur tout V+d ; F4 (convexité)
garantit que V∖(V+d) n'est jamais relu ; borne K du test Z prudente (|v| ≤ p) ; au 2e passage, la grille est remise à l'état initial
et la boîte utilisée est celle de la fin du 1er passage (⊇ cases visitées jusqu'à l'instant certifié) ; hors boîte tout est blanc.
Seule remarque : le pas « CERT » rendu est le premier instant certifié dans la fenêtre [début − p, début + 50p], pas forcément le
premier absolu (sans effet sur les statuts). Bug voisin trouvé et corrigé ce jour : lignes > 16 ko tronquées (R-112).

## R-116 T6 reproductible : les étapes R-94 (récurrence en k₁, 968 vérifications `ant multi`) et R-95 (transport, 484 paires) refaites depuis zéro redonnent exactement les résultats gardés (0 ligne différente) — VÉRIFIÉ — 19/11 S9
`recherche/autoroute/outils/t6_refait.sh` (45 s). Constat : les entrées de `transport.py` (gap.cert, dbl22.res) n'étaient pas gardées ;
gap.cert = `fourmi -cert` sur les 22 classes de c₁ (gardé maintenant dans resultats/relatif/), dbl22.res = resultats/relatif/recurrence_k1.txt.
Les 968 pas certifiés recalculés sont identiques. Non refait par ce script : R-96/R-98 (G1, G2, transport dual) et la partie (A) proche.
(R-116, suite) R-96 refait (`t6_refait.sh`, étapes 5–6) : G1 (c₁ = −119,100) 17/18 sans la règle + 8/8 vérifications « c₂ fixe »
(base = blanc + c₂, NS = 1, p* = 90) ; G2 (d₂ = d) 7/8 sans la règle ; mêmes 2 exceptions (règle utilisée 50 et 72 fois).
R-98, contrôles à la main : (a) pour G2, base −127,100 (T0 = 21 929), `ant multi -21 401 158602 1 300` : s₁ = 101 288, règle 0 ✓ ;
(a) pour G1, base pivotée 100,119 (cap G, T0 = 79 678) : 22/22 sans la règle ✓ ; (b) pour G1, c₂ = (−401,−409) :
s₁ = 68 836 avec p* = 110 (69 356 avec p* = 90 : le journal ne notait pas p*) ✓. T6 : seules les zones proches (A, 683 080 cas)
et R-97 (assemblage, epars_RD.py) ne sont pas dans le script.
