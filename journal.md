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

## R-117 T7, premier essai d'une base à 2 cases : W₂ = blanc + (−127,100) + (−429,400) (T0 = 37 543, dérive (−2,2)) ; c₃ loin (k = 900) : 22 classes, 21 prouvées par `ant multi` (pente 52, NS = 0), la classe demi-tour (pente 104) non prouvée (NS = 1, 2, 3, p* de 50 à 400) — OUVERT — 19/11 S9
`cd data/t7 && python3 ../../recherche/autoroute/outils/relatif.py "-127,100;-429,400" 37543 900 H` : 21 s (machine chargée).
Échec : `BASE="-127,100;-429,400" T0=37543 ant multi -21 901 210722 NS p…` ; le demi-tour au 3e site roule jusqu'au 2e site, pas au
germe : les repères de `multi` (identité près du germe) ne collent pas. Il faudra l'astuce « c₃ fixe » de T6 (base = blanc + c₃) ou
un repère par site. Coût brut T7 (C) : ≈ 20 s × 484 bases ≈ 3 h, plus les demi-tours.

## R-118 Nouveau record 5×5 : masque 11433907 (16 cases), autoroute certifiée dès 351 374 — DÉMONTRÉ (cette configuration) ; record(n) ≥ 351 374 pour n ≥ 5 — OBSERVÉ (minorant) — 19/11 S9
Cases 0,0;1,0;4,0;0,−1;2,−1;3,−1;4,−1;0,−2;2,−2;3,−2;4,−2;2,−3;3,−3;4,−3;1,−4;3,−4 (fourmi 0,0,H). 2ᵉ moteur `ant une 5 11433907` :
début 351 374. Trouvé dans la tranche [11,4 M ; 11,6 M) du parcours exhaustif (box5_fond.sh). Bat R-111 (252 046) de 39 %.
(R-117, suite) Classe demi-tour de c₃ : CERT = 210 722 + 104·(k − 901) (k = 901…909), autoroute finale (2,2) : la fourmi revient en
roulant jusqu'au 2e site (−429,400) qui la renvoie en (2,2), loin de la bande de c₃. Un seul retour (NS = 1 devrait suffire) : l'échec
de `multi` vient donc de ses ensembles d'accord autour de la base (pensés pour un germe à l'origine), pas de la dynamique. À examiner en S10.
(R-117, détail) `multi … 1 90` : s₁ = 158 910, lecture refusée à 168 512, « Z ECHEC » ; borne p sur D = 839 (la trace de la base W₂
couvre des diagonales jusqu'à p = 839, contre ≈ 25 pour le départ blanc) : c'est probablement ce D trop large qui bloque.
(R-114, suite) 8 cases dans [−2,2]² : 735 471/735 471 certifiées ; min 64 (−1,−2;2,−2;−2,−1;1,−1;1,0;0,1;1,1;−2,2), max 181 037
(−1,−2;0,−2;−1,−1;−2,0;0,1;−1,2;0,2;2,2). (Borne R-105 à 8 cases : ≤ 55, hors de ce carré.)
(R-114, suite) 9 cases dans [−2,2]² : 1 307 504/1 307 504 certifiées ; min 56 (0,−2;2,−2;−2,−1;0,−1;1,−1;1,0;0,1;1,1;−2,2), max 179 492
(−2,−2;1,−2;2,−2;−2,−1;−1,−1;1,−1;−2,0;2,0;−2,2).
(R-117, résolu) La classe demi-tour passe avec p* = 900 : `BASE="-127,100;-429,400" T0=37543 ant multi -21 901 210722 1 900` → TOUT OK
(règle 0) ; p* = 900 à 1 700 marchent, ≤ 600 non. Raison : p* = L borne la zone d'accord en repère identité ; elle doit couvrir le
2ᵉ site (p ≈ 829) et pas seulement le germe. Contrôle direct `deux_mondes.sh` : couplage exact sur 173 284 pas. Donc pour cette base
W₂, partie (C) de T7 : 22/22 classes — DÉMONTRÉ sous réserve de relecture (mêmes lemmes que T6). À faire : élargir la liste des p*
de relatif.py (ajouter 900, 1 200, 1 500 ou p* = p(2ᵉ site) + 70) puis lancer les 484 bases (≈ 3 h).

## R-119 T7 (trois cases éparses), partie (C) lancée : 484 bases W₂ = blanc + c₁ + c₂ (une par paire de classes, écart k₀), pivotées pour la dérive (−2,+2) — en cours — 19/11 S9
`outils/t7_bases.py` → resultats/relatif/t7_bases.txt (484 bases : 156 H, 100 D, 146 G, 82 B) ; `outils/t7_lance.sh 0 484` (reprise
automatique) → data/t7/b_<n>.txt et data/t7/bilan.txt. Deux changements de `relatif.py` : p* ∈ {…, 600, 900, 1 200, 1 500} pour NS = 1
(ajoutés en fin de liste : les anciens choix sont inchangés) et balayage des diagonales centré sur la fourmi à T0 (union avec l'ancien
[−450, 450]), sinon les bases pivotées n'avaient aucune classe. Bilan de la séance : voir rapport S9.
(R-119, suite) Classe à pente 156 (deux allers-retours, NS = 2) dans la base n° 18 : passe avec p* = (1 200, 900), règle « un pas »
utilisée 72 fois (comme G2 de T6) ; ajouté en fin de grille NS = 2 de relatif.py ; base 18 refaite : 22/22.
(R-114, suite) 10 cases dans [−2,2]² : PARTIEL, combinaisons [0, 1 200 000) sur 1 961 256 certifiées (0 échec) ; min provisoire 52
(par ex. 0,−2;1,−2;2,−2;−2,−1;0,−1;1,−1;1,0;0,1;1,1;−2,2) ; max provisoire 206 499. Morceaux : data/germes_R2_k10_*.out (relancer
`germes_k.sh 10 2 A B` pour [1 200 000, 1 961 256)).

## R-120 Bilan S9 du fond : 5×5 [0, 12 400 000) certifiées sans trou (+ [13,8 M ; 14,0 M) et [15,4 M ; 15,6 M)), max 351 374 (R-118) ; T7 (C) : 53 bases sur 484 terminées, toutes complètes — DÉMONTRÉ (ces boîtes) / T7 en cours — 19/11 S9
Tranches : resultats/box5/ (64 fichiers). T7 : data/t7/b_<n>.txt (non suivis) ; reprise `recherche/autoroute/outils/t7_lance.sh 0 484`.

## R-121 Germes à 10 cases dans [−2,2]² : les 1 961 256 configurations construisent l'autoroute — DÉMONTRÉ (certificat) ; minimum exact 52, maximum 206 499 — 19/11 S10
Min : −1,−2;0,−2;2,−2;−2,−1;0,−1;1,−1;1,0;0,1;1,1;−2,2 (et une autre) ; max : −2,−2;−1,−2;0,−2;2,−2;−2,−1;−1,−1;2,−1;0,1;2,1;−1,2.
Terminé en fond après S9 (morceaux data/germes_R2_k10_*.out). Minima exacts dans [−2,2]² : 120, 68, 64, 56, 52 pour 6 à 10 cases.

## R-122 Faille de `ant multi` trouvée et corrigée : en repère identité, l'accord « p < L » était admis même quand une case de l'îlot a un petit p — FAUX positifs possibles ; aucun résultat publié touché après recontrôle — VÉRIFIÉ — 19/11 S10
Découverte : récurrence en k₁ de T7, triplet (−130,103) + (−291,299) + (−772,−1014) (décalages) : `multi -27 103 189428 1 90 …` disait
TOUT OK, mais `ant deux` trouve un écart à t = 157 031 et les pas certifiés (k₁ = 103 : 189 428 ; 105 : 111 414) excluent tout couplage.
Cause : en repère identité (NS impair), `multi` accepte toute lecture de p < L_i (« près du germe, les deux mondes coïncident »). C'est faux
si une case de l'îlot (qui diffère entre X(k) et X(k+2)) a elle-même p < L_i : ici c₃, posé sur une autre bande à p ≈ −18.
Correction (ant_controle.c) : L_i ≤ pI = plus petit p des cases de l'îlot. Recontrôles avec le binaire corrigé :
- T6 (C), R-93 : 484/484 toujours OK ; T6 R-94 : seuls les 36 contrôles « bloc » de c₁ = (−119,100) (classe demi-tour) passent de NS1 à
  ECHEC — c'est exactement le cas où le journal (R-94) prescrivait « c₂ fixe en base » ; avec c₂ fixe : 44/44 OK (42 sans la règle, 2 avec,
  comme R-96) et `deux` confirme 44/44 couplages exacts. T6 et ses énoncés sont inchangés.
- Mon `t6_refait.sh` (S9, étape 5) vérifiait G1 avec le paramétrage « bloc » : il obtenait les bons comptes pour une mauvaise raison ;
  corrigé pour utiliser « c₂ fixe ». T1–T5 : îlots compacts à grand p, non concernés (pI ≥ k ≥ 100 > L).
- T7 (C) : audit par `ant deux` de chaque preuve (audit_t7c.sh) : voir R-123.
Leçon : toute preuve `multi` doit être recoupée par `ant deux` (couplage simulé) avant d'être comptée.

## R-123 Audit de T7 (C) par `ant deux` : les 3 300 preuves `multi` des 150 premières bases finies redonnent toutes un couplage exact — VÉRIFIÉ — 19/11 S10
`recherche/autoroute/outils/audit_t7c.sh 0 484` (BASE, T0, H0 de chaque base) ; sortie data/t7/audit_c.out. Les bases faites après la
correction R-122 utilisent le `multi` corrigé.

## R-124 T7, récurrences en k₁ et en m (analogue de R-94 pour trois cases) : 3 559/3 564 triplets passent chacune, tous recoupés par `ant deux` (couplage exact) — DÉMONTRÉ sous réserve de relecture (les familles à un paramètre correspondantes) ; 5 + 5 cas OUVERTS — 19/11 S10
Triplets : `outils/t7_triples.py` (3 564 = 162 bases finies × 22 classes de c₃, pas certifiés recalculés dans le repère d'origine : 0 désaccord).
- Récurrence en k₁ (îlot {c₁,c₂,c₃} déplacé en bloc le long de d) : `outils/essai_k1_bloc.sh` : 3 207 OK (3 145 NS0, 35 NS1, 27 NS2),
  3 207/3 207 couplages exacts. 357 ECHEC → « c₃ fixe » (base = blanc + c₃, îlot {c₁,c₂}, `outils/essai_k1_c3fixe.sh`) : 352 OK
  (348 sans la règle), 352/352 exacts. Restent 5 triplets de la base 19 (c₁ = (−127,100), c₂ = (−422,401), c₃ ≈ (900,1097)) : issue stable
  et affine en k₁ (pente 312 par Δk₁ = 2, trois traversées) mais aucune grille NS ≤ 3 ne passe. OBSERVÉ.
- Récurrence en m (base blanc + c₁ pivotée, îlot {c₂,c₃} en bloc le long de la 2ᵉ bande) : `outils/essai_m_bloc.py` : 3 427 OK, tous exacts ;
  137 ECHEC → « c₃ fixe » (base blanc + c₁ + c₃, îlot c₂, `outils/essai_m_c3fixe.py`) : 132 OK sans la règle, tous exacts. Restent 5 :
  base 18 (classe de pente 156) et 4 triplets où c₃ est sur la bande de W₁ (la base blanc + c₁ + c₃ n'a plus la dérive (−2,+2)). OUVERT.
Manque pour T7 : le transport (uniformité, comme R-95/96/98), les zones proches (A) et l'assemblage avec R et D.

## R-125 T7 : directions successives des 3 564 triplets (d → d₂ → d₃ → d₄ ; M = même sens, P = perpendiculaire, X = demi-tour) — VÉRIFIÉ (calcul) — 19/11 S10
MPP 912, MPM 685, MMP 642, MMM 453, PPP 264, PPM 198, PMP 157, PMM 117 (3 428 sans demi-tour) ; avec demi-tour : MPX 75, PPX 22, PXP 13,
PMX 12, PXM 9, MMX 5 (136). Le lemme de transport de T6 (R-95) vaut quand chaque changement est M ou P : il devrait couvrir les 3 428
premiers en l'itérant (m puis m₃) ; les 136 avec X demandent l'analogue de G1 (case fixe en base) ou le transport dual (R-98).
Données : data/t7/directions.txt (non suivi).

## R-126 T7, uniformité testée : le pas certifié est additif en (k₁, m, m₃) — 300/300 prédictions exactes à (k₁+14, m+10, m₃+12) pour les triplets « NS0 + sans demi-tour » ; 496/534 pour les autres — OBSERVÉ (chaque configuration calculée est DÉMONTRÉE) — 19/11 S10
Hypothèses du transport itéré (NS = 0 dans les récurrences « bloc » en k₁ et en m, aucun demi-tour) : 3 030 triplets sur 3 564.
Test : CE(a,b,c) = CE(0) + a·Δ_k₁ + b·Δ_m + c·Δ_m₃ (pentes mesurées un paramètre à la fois ; c₁ += a·d, c₂ += a·d + b·d₂,
c₃ += a·d + b·d₂ + c·d₃). Échantillon de 300 candidats : 300/300 exacts. Les 534 autres (départ décalé d'un pas) : 496 exacts, 38 non
additifs (MPM 22, MPP 16), 0 non certifié. Outil : `outils/t7_uniformite.py 300 10`.

## R-127 T7 : hypothèses du transport (critère de transport.py, R-95) aux deux étages remplies pour 3 123 triplets sur 3 564 — OBSERVÉ (décompte) ; le lemme à deux étages reste À ÉCRIRE ET RELIRE — 19/11 S10
`outils/transport7.py` : K = récurrence en k₁ (bloc, NS0) transportée le long de m (pas d₂) et de m₃ (pas d₃) ; M = récurrence en m
(bloc, repère de blanc + c₁, NS0) transportée le long de m₃. Bilan : K ok et M ok 3 123 ; K non-NS0 / M ok 264 ; les deux non-NS0 155 ;
K ok / M non-NS0 16 ; K refusé par les directions 6. Schéma de preuve visé : (C) à (k₀, m₀) pour tout m₃, puis M (tout m), puis K (tout k₁).
Les 441 restants : variantes « c₃ fixe » (R-124, déjà vérifiées pour 352 + 132 cas) à transporter, et transport dual (R-98).
(R-124, détail) Les 4 cas ouverts « c₃ sur la bande de W₁ » en m sont en fait trois cases alignées sur la bande de départ
(x + y = −21 à −27 : c₁ à k ≈ 100, c₂ à k ≈ 400, c₃ à k ≈ 900 ; d₂ = d₃ = d) : la fourmi enchaîne les sites sur la même bande.
`BASE=-128,101 T0=15917 ant multi -27 400 226322 …` : aucune grille NS ≤ 2 (p* jusqu'à 1 500) ne passe (lecture refusée à 31 556 ou
168 512, la règle « un pas » est sollicitée). Même famille que les « chaînes de demi-tours » de T3 (E2_epars.md, S1) : à traiter à part.

## R-128 Bilan S10 de T7 : (C) 407/484 bases finies, toutes complètes ; chaîne `t7_tout.sh` sur 282 bases (6 204 triplets) : récurrence en k₁ 6 199/6 204, en m 6 196/6 204, toutes recoupées par `ant deux` ; hypothèses du transport à deux étages remplies pour 5 262 — DÉMONTRÉ sous réserve de relecture (familles à un paramètre) / transport OBSERVÉ (décompte) — 19/11 S10
k₁ : 5 473 « bloc » (5 473 couplages exacts) + 726 « c₃ fixe » (exacts), 5 ECHEC (base 19). m : 5 932 « bloc » + 264 « c₃ fixe » (exacts),
8 ouverts (bases 18, 24, 46, 68, 105, 135, 147, 178). Transport : K ok & M ok 5 262 ; K non-NS0 & M ok 594 ; les deux non-NS0 214 ; K ok & M non-NS0 109 ;
K refusé par les directions 25. Audit `deux` de T7 (C) : 5 126/5 126 couplages exacts (233 bases). 5×5 : [0, 16 000 000) certifié sans trou
(80 tranches dans resultats/box5/), max inchangé 351 374. Bilan : resultats/relatif/t7_bilan_S10.txt.

## R-129 Lemme T (transport d'une condition NS = 0 le long d'un autre paramètre) et théorème T7-loin écrits en détail — DÉMONTRÉ sous réserve de relecture — 19/11 S11
recherche/autoroute/E2b_couplage.md §S11. T7-loin : si (C) vaut (recoupé par `deux`), (M) à NS = 0 avec d₃ ∈ {d₂, ⟂ d₂}, et (K) à NS = 0 avec
d₂, d₃ ∈ {d, ⟂ d} (règle des diagonales pour une direction finale opposée), alors X(k₁, m, m₃) construit l'autoroute pour toujours pour tous
k₁ ≥ k₀, m ≥ m₀, m₃ ≥ m₃₀. Preuve : (C) donne m₃ ; lemme T avec les repères de (C) puis récurrence (M) donne m ; lemme T avec (C) puis (M),
puis récurrence (K) donne k₁. Le correctif R-122 est aussi écrit dans le lemme 3 (point 3 : L_i ≤ pI). Outil d'application :
`outils/t7_theoreme.py` (vérifie (i) dans data/t7/audit_c_all.out, (ii)–(iii) dans data/t7/transport7.txt). Bilan : voir R-130.

## R-130 Lemme T' : les preuves (K) « c₃ fixe » (NS = 1, sans la règle) se transportent le long de m et m₃ sous un critère de diagonales — 584/726 cas S10 le remplissent ; contrôle 40/40 à (m+10, m₃+10) — DÉMONTRÉ sous réserve de relecture — 19/11 S11
E2b_couplage.md §S11 (lemme T'). Critère vérifié par `outils/t7_kprime.py` (nouveaux champs de `ant multi` : tc2, tbase, dfix,
horsD_apres_c2, zlow, zd). Sur les 726 preuves « c₃ fixe » de S10 : 584 passent (famille d₂ ⟂ d, d₃ = −d), 128 échouent le long de m
(d₂ = d : p augmente de 4 par pas après c₂, les acceptations « p < L₁ » ne sont pas uniformes), 14 utilisent la règle. Contrôle
indépendant : 40 triplets tirés au hasard, déplacés de 5 pas en m et en m₃ : 40/40 preuves (K') refaites, `deux` exact, règle 0.
Le théorème T7-loin accepte désormais (iii) ou (iii') (`t7_theoreme.py`).

## R-131 Variante (M') du transport (preuves (M) « c₃ fixe ») : 258/264 cas S10 remplissent le critère ; contrôle 30/30 à m₃ + 10 — DÉMONTRÉ sous réserve de relecture — 19/11 S11
`outils/t7_mprime.py` (nouveau champ `tlast` de `multi` : premier contact avec la dernière case de la base, ici c₃). Échecs : 4 (diagonales),
2 (règle). T7-loin accepte (ii) ou (ii').

## R-132 Lemme T' (a') : preuves (K') transportées le long de m avec les repères de (M') quand d₂ = d et s₁(K') ≥ s₁'(M') + 104 — +128 cas S10 ; contrôle 30/30 — DÉMONTRÉ sous réserve de relecture — 19/11 S11
E2b §S11. Critère ajouté à `outils/t7_kprime.py` (lit les s₁' de data/t7/mprime.txt). Contrôle : 30 triplets de la famille d₂ = d,
c₂ déplacé de 5·d₂ et c₃ de 5·d₃ (famille « c₃ absolu » de (M')) : 30/30 preuves (K') refaites, `deux` exact, règle 0.
Sur les données S10 : T7-loin passe de 5 929 à 6 057 classes de triplets sur 6 204.

## R-134 T7 (C) terminé : 484/484 bases W₂ = blanc + c₁ + c₂, chacune avec ses 22 classes de c₃ prouvées par `multi` (10 648 preuves), relatif.py avec p* élargis — DÉMONTRÉ sous réserve de relecture (récurrence en m₃) — 19/11 S11
Audit `ant deux` : voir R-133 (data/t7/audit_c_all.out).

## R-133 T7-loin appliqué : 9 441 classes de triplets sur 9 702 (441 bases sur 484) démontrées « loin » (pour tous k₁ ≥ k₀, m ≥ m₀, m₃ ≥ m₃₀) — DÉMONTRÉ sous réserve de relecture des lemmes T, T' ; audit `deux` de T7 (C) : 10 648/10 648 couplages exacts — 19/11 S11
Chaîne refaite sur 9 702 triplets (0 désaccord de pas certifié). (K) « bloc » : 8 047 OK, 8 047/8 047 exacts ; (K') « c₃ fixe » : 1 628 OK
exacts, 27 ECHEC ; (M) « bloc » : 9 254 OK exacts (0 écart) ; (M') : 440 OK exacts. Critères : transport7 (K ok & M ok 7 652), t7_kprime
1 598/1 628, t7_mprime 431/440. Bilan T7-loin : K & M 7 652 ; K' & M 1 449 ; K & M' 191 ; K' & M' 149 ; non couverts 261 (K et M non NS0 69,
K refusé par les directions avec M' 67, K ok & M non 54, K non & M 47, K non & M' 24). Les 43 bases restantes (441 à 483) ont (C) prouvé
et audité mais pas encore la chaîne k₁/m. Fichiers : resultats/relatif/t7_theoreme_S11.txt, t7_theoreme_detail_S11.txt, t7_transport7_S11.txt.
## R-135 B5 : toute configuration dans un carré 5×5, fourmi n'importe où dans le carré, tout cap → autoroute 104 pour toujours — DÉMONTRÉ (calcul exhaustif + certificat R-83 ; sous réserve de relecture humaine du code de l'arbre) — 19-20/11
Symétrie (quart de tour autour de (2,2)) ⇒ cap haut × 25 positions × 2²⁵ = 838 860 800 cas. Arbre de choix (cases du carré
inconnues, branche à la première lecture ou si une case de Z est inconnue), feuille = premier instant certifié (Z dans
la boîte carré ∪ visité). Par position : poids = 2²⁵ exactement, 0 non résolu (Tmax 5·10⁶), dérive (±2,±2) partout ;
702 113 441 feuilles, ≈ 10 h·cœur. **T(5) = 351 374** (fourmi (0,0) cap haut, masque 11433907, y vers le haut).
Validation : arbre = brut sur 3×3/4×4, = `src/fourmi -cert` sur 4×4 ; T(3) = 51 277, T(4) = 133 984 (les références 51 377
et 134 065 commençaient la recherche dans un trou de phases non certifiables). Contrôles : 100 000 tirages = src/fourmi
(instants identiques) et ant_controle (début ≤ certificat), 25 records et 46 tranches box5 identiques.
Estimation 6×5 : ≈ 765 h·cœur (non calculé). Commande : recherche/B5/lance.sh, agrege.py, controles.py. Détails :
recherche/B5/README.md. Bestiaire 22, germes resultats/germes_2026-11-19_B5.json (dossier B5 du simulateur).

## R-136 Gomme : (x, cap h) → (x − e_h, cap h + 2) fait refaire tout le chemin à l'envers en effaçant — VÉRIFIÉ (preuve + 2 moteurs) — CONNU — 25/11 nuit
Preuve en 2 cas (blanc / noir) : ordinateur/bascule/GOMME.md §1. Règles : 2 couleurs avec t_0 + t_1 ≡ 0 (mod 4) → RL, LR, NN, UU
(pas RR, LL ; pas LLR et plus : une fourmi ne fait que c → c+1). n fourmis : gommer toutes et jouer dans l'ordre INVERSE
(sinon 892 / 488 cases fausses sur 2 exemples). `src/fourmi -gomme t -T 2t+10 "RL|0,0,H|"` → EFFACE au pas 2t (t = 10 … 10⁶ ;
germe R-20 jusqu'à 1 040 000) ; 2e moteur ordinateur/bascule/moteur2.py. Connu : réversibilité (Tsukiji & Hagiwara 2011).
Nouvelles options du moteur : -gomme t, -retour, -boite x0,y0,x1,y1, -dump f (19/19 tests).

## R-137 Une fourmi seule ne repart JAMAIS en gomme sur sa propre trace (aucune pièce de cases ne peut la renvoyer ainsi) — DÉMONTRÉ — 25/11
I = x + y + h (mod 2) est invariant (R-09) et R change I ⇒ l'état R(état passé) n'est jamais atteint. Contrôle : pièces de 1 et
2 cases (22 + 2 574 placements, germe à 50 périodes) : 0 retour ; les 141 « demi-tours » longent la trace (elle double).

## R-138 Gomme par échange : une fourmi de la pièce (classe opposée) repart en gomme exacte — OBSERVÉ (stats) / VÉRIFIÉ (10/10, 2 moteurs, temps fini) — 25/11
Pièce = petit cycle (boîte ≤ 7×7) à 50 périodes du germe R-20 ; critère : fenêtre x∈[35,75], y∈[−75,−35] redevenue blanche (20 000 pas).
2 fourmis : 501 370 essais (2 049 cycles, partiel), 8 152 gommes ; 4 fourmis : 903 776 essais (1 000 cycles sur 3 978), 15 825 gommes.
Pièce : détruite dans 300/300 (2 f., échantillon) et 15 825/15 825 (4 f.). La gomme est souvent décalée (germe abîmé, 28 cases).
Outils : ordinateur/bascule/flux.sh, gen_cycles.py, recherche.py, verif2.py. Fiche BA-2.

## R-139 Loi d'équilibre (conjecture) : un cycle RL a autant de fourmis de chaque classe I — OBSERVÉ — 25/11
0 cycle sur 2 213 888 départs 3+1 (4 fourmis dans [−3,3]², 20 000 pas) et sur 6 × 200 000 tirages déséquilibrés (3, 4, 5, 6 fourmis,
avec/sans case) ; témoins équilibrés : 6 123, 292, 308 cycles / 200 000 ; catalogue : 47 cycles, tous équilibrés. Démontré seulement :
≥ 1 de chaque classe (R-09 ; au coin du domaine visité les visites alternent entre classes). Pas trouvé dans la littérature (1 recherche).
Conséquence (si vraie) : un échange déséquilibre la pièce ⇒ plus de cycle ⇒ elle ne reste pas bornée (R-44). Avec R-137 : aucune pièce
bornée ne renvoie UNE autoroute en gomme en restant intacte (la bascule « par réflexion en gomme » est impossible en RL).

## R-140 BASCULE T : une pièce de 2 fourmis + 1 case alterne S0 / S1 à chaque autoroute 104 qui arrive par la même ligne — VÉRIFIÉ (2 moteurs, temps fini) — 25/11
Recherche : 19 936 déviations « pièce intacte » → 15 257 résidus changés, 393 petits cycles S1 ; 2e tir idéalisé sur chaque S1 (521 368
essais) → 16 retours à S0 ; test honnête (2 germes dans la même simulation, voies voisines de la même ligne, le 2e plus loin) : 11/16,
soit 3 bascules distinctes (pièces 185, 186, 572 de cycles2.json), S0 revenu EN PLACE. Chronologie 572 (moteur2.py) : S0 → S1 (6 100)
→ S0 (8 400) → S0 jusqu'à la fin ; 3e germe : → S1 (21 700) [aussi 185 : 20 900 ; 186 : 56 800]. 4e impulsion : non trouvée
(recul 40–100 périodes, voies ±8 ; recherche 100–220 : voir R-143). Lecture non destructive depuis le NE : pas trouvée (au contact
la pièce est presque toujours détruite). Fichiers : ordinateur/bascule/chaine.py, honnete.py, chaine_*.json. Fiches BA-3 à BA-6.

## R-141 La paire ON/OFF efface sa ligne : les 2 sondes (classes opposées) se gomment mutuellement — VÉRIFIÉ (2 moteurs, temps fini) — 25/11
Bascule 572 : la sonde 2 est dans l'état R d'un état passé de la sonde 1 pendant 8 541 pas, la sonde 1 dans celui de la sonde 2 pendant
5 851 pas ; fenêtre de la ligne : ≈ 309 cases noires au pas 6 000, 0 dès 14 000 (moteur2.py et src/fourmi -boite), mêmes résultats
pour 185 et 186. Restent : des débris aux deux sources, d'où 2 autoroutes repartent vers le NO. C'est la « gomme » demandée, réalisée par
une PAIRE — compatible avec R-137 et R-139 (l'échange se fait entre les deux sondes, la pièce reste équilibrée).

## R-142 Écran de 2 pixels : ON, OFF, ON sur chaque pixel — VÉRIFIÉ (2 moteurs, temps fini) — 25/11
Pixel A = bascule 572 (3 germes) en (0,0) ; pixel B = bascule 186 (3 germes) en (0,4000), retardé de 3 120 pas : son état initial est
son état « 3 120 pas avant », calculé exactement par réversibilité (gomme, ordre inversé, gomme ; retour exact vérifié). Simplement reculer
les germes NE marche pas (le germe d'origine devient un bout de trace, que la 2e autoroute voit). Chronologie : A ON 6 100, OFF 8 400,
ON 21 700 ; B ON 8 900, OFF 15 900, ON 59 900 ; positions finales des 10 fourmis identiques (src/fourmi, moteur2.py). ordinateur/bascule/ecran2.py,
resultats/bascule/4_ecran_2pixels.png. Fiche BA-7.

## R-143 Compléments de la nuit (25/11) : 4e impulsion, flux nul sur chaque arête des cycles, sortie dépendant de l'état
(a) Bascule 572 : 4e germe (recul 100–220 périodes) → S0 → S1 → S0 → S1 → S0 (pas 6 100 / 8 400 / 21 700 / 24 200), S0 reconnu
exactement jusqu'à 84 184 — VÉRIFIÉ (src/fourmi pour la recherche, moteur2.py pour la chronologie). Mais la 2e paire n'efface pas sa
ligne (débris autour de la pièce, ≈ 550 cases dans la fenêtre). chaine.py (REPRISE=1 J0=100 J1=220).
(b) Dans TOUS les cycles testés, chaque arête est traversée autant de fois dans un sens que dans l'autre (sur une arête, les deux sens
correspondent aux deux classes) : 2 049/2 049 (cycles2), 3 978/3 978 (cycles4), 46/46 (catalogue, période ≤ 400 000) — OBSERVÉ.
Cela entraîne la loi d'équilibre R-139. Ce n'est PAS la symétrie par renversement du temps : R(état) est sur l'orbite pour 2 049/2 049
cycles à 2 fourmis mais seulement 776/3 978 à 4 fourmis. Preuve : OUVERT. ordinateur/bascule/aretes.py.
(c) Tirs idéalisés (autoroute neuve) : pièce 185 : S0 → S1 et l'autoroute part au NO (−2,−2) ; S1 → S0 et elle part au SE (2,2) ;
pareil pour 186 ; 572 : SE dans les deux cas (voies x−y = 0 et 3). La sortie dépend donc de l'état (moitié « a » d'un RLEM 2 états) ;
il manque une entrée de lecture « b » pour compléter un RLEM ; non trouvée (≈ 36 000 tirs, 4 directions) — OUVERT.
(d) Piège : retirer la case « inerte » d'un cycle (jamais visitée par ses fourmis) change tout pour l'autoroute qui arrive : sur les
422 cycles sans case inerte, 0 bascule (pipeline complet) ; les 3 bascules ont toutes une case isolée à côté du cycle.

## R-144 Couverture complète des 2 049 pièces « cycle de 2 fourmis (+ 1 case) » : 4 pièces seulement font une bascule T — VÉRIFIÉ (2 moteurs, temps fini) / OBSERVÉ (exhaustivité dans ce montage) — 25/11
`ordinateur/bascule/pipeline.sh c2 cycles2.json` : 1er tir 2,9 M essais → 107 481 déviations « pièce intacte » → 1 532 orbites S1 ;
2e tir → 87 187 déviations → 10 013 résidus changés testés → 40 retours à S0 (idéalisé) → 33 honnêtes (même simulation, traces
comprises) ; pièces : 185 (4), 186 (2), 572 (5), 1020 (22) ; toutes = cycle de 2 fourmis + UNE case isolée. Nouvelle : 1020
(0,0,D ; −1,−1,B + case 3,1 ; cycle 28) : S0 → S1 (5 400) → S0 (10 000), ligne effacée (199 → 0 cases). Fiche BA-8.
Les 422 cycles sans case isolée : 0 bascule. La 5e impulsion de 572 n'a pas pu être cherchée (redémarrage du conteneur).

## R-145 T7-loin sur les 43 dernières bases (441–483) : 476 classes de triplets sur 946 démontrées « loin », 19 bases entièrement ; 28 bases échouent toutes à la 1re fenêtre (s₁) de la récurrence en k₁ — DÉMONTRÉ (sous réserve de relecture des lemmes T, T') / OBSERVÉ (diagnostic) — 25/11 S12
Données data/t7 perdues (conteneur neuf) : (C) refait pour 441–483 (`t7_lance.sh`, 44 s par base), audit `ant deux` 946/946 couplages exacts,
chaîne `t7_tout.sh` (sur une copie de data/t7 réduite à ces bases), `t7_mprime.py` (43 MP:ok), `t7_kprime.py` (154 KP:ok), `t7_theoreme.py`.
Bilan 441–483 : K & M 306, K' & M 154, K & M' 16 → 476 DÉMONTRÉES ; non couvertes 470 (K non NS0 & M 432, K non NS0 & M' 22,
K et M non NS0 11, K dir & M' 5). Récurrence k₁ « bloc » : tout ou rien par base — 15 bases 22/22, 28 bases 0/22 ; sur 40 échecs tirés au
hasard, 40 échouent à la fenêtre s₁ (« L R ECHEC » : recopie de la fenêtre à s₁ + P), quel que soit p* (essayé jusqu'à 6 000, NS = 2 aussi) ;
direction après c₁ : (−2,−2) dans tous les cas, succès comme échecs. Total T7-loin (S11 + S12) : 9 917 classes sur 10 648 (484 bases).
Fichiers : resultats/relatif/t7_theoreme_S12_bases441-483.txt, t7_k1_S12_bases441-483.txt, t7_audit_c_S12_bases441-483.txt.

## R-146 Pourquoi la récurrence en k₁ échoue sur les bases c₁ = (−119,100) : s₁ tombe dans le chaos de c₁ — OBSERVÉ (diagnostic) — 25/11 S12
Les 43 dernières bases = les 2 dernières classes de c₁ : (−119,100) [21 bases, k₁ « bloc » 0/21] et (−118,100) [22 bases, 15 OK, 7 échecs].
c₁ = (−119,100) seule : certificat au pas 79 678 (direction finale (−2,−2)). Dans `ant multi` (NS = 1), s₁ = 15 458 pour tout p* ≥ 50
(déclenchement trop tôt, fenêtre non recopiée) ; p* = 40…10 : s₁ ≈ 70 600–71 400, fenêtre recopiée OK mais « lectures neuves » ECHEC
dès s₁ + 104 ; p* ≤ 0 : s₁ ≈ 71 654–72 880 ou jamais. NS = 2 (8 couples) et la variante « c₃ fixe » : mêmes échecs. Aucun s₁ n'est donc
placé après la fin du chaos de c₁ (79 678). Prochaine piste : déclencher s₁ au certificat de c₁ (ou au-delà) et revoir le lemme 3 pour ce cas.
`ant multi -19 100 CE 1 40 -282 -518 -1617 800` (base 441).

# ===== Ajout du 26/11 (jour) : journal des règles (recherche/regles/journal_regles.md, R-300 à R-350), recopié tel quel =====
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

## R-335 MÉMOIRE 1 bit R2L2 réutilisable 20/20 et écran 2 pixels, sans aucune case fixe — VÉRIFIÉ (2 moteurs, temps fini) (memoire_finale.py, ecran.py)
Bit 1 = oscillateur M = « H:R2L2|0,0,1;1,-1,0|-1,1 » (2 fourmis + 1 case, période 21) ; bit 0 = RIEN (pas même une case).
M est son propre film à l'envers (à une phase près). ÉCRIRE 1 = film à l'envers (gomme collective R-311) de la destruction propre
Da = (vaisseau joué après M, direction 1, voie 0, phase 9) : 3 vaisseaux arrivent, M apparaît, 1 vaisseau repart.
LIRE = sonde Db = (après M, direction 2, voie −2, M en phase 11) : si 1, M part en 3 vaisseaux propres (directions 3, 2, 4) et il ne reste
RIEN ; si 0, la sonde traverse le vide. Lecture destructive, comme une mémoire à tores : bit lu = 3 vaisseaux qui sortent (1) ou 1 (0).
Clé (trouvée en cherchant pourquoi O2 échouait 0/6 000) : toutes les routes d'écriture et de lecture vont dans 3 directions consécutives
(2, 3, 4 : un demi-plan) ⇒ aucune sortie ne croise de face une entrée future. Sur 87 oscillateurs à destructions propres, 3 ont cette
propriété (2 utilisables : périodes 21 ; le 3e, période 36, n'a pas la bonne phase avec des pas de 8).
Résultats (UNE simulation, tous les vaisseaux posés à t = 0, jusqu'à 41-53 fourmis, t = 65 600) : 20 bits au hasard écrits puis relus au
MÊME endroit : 20/20 justes (4 tirages : graines 26, 1, 2, 3) ; 20 « 1 » d'affilée : 20/20 ; 2 moteurs (hx.py, fourmi_r -x -dump) : 5/5 états
identiques à chaque fois. Écran 2 pixels avec ce pixel : P1 = ON, OFF, ON et P2 = OFF, ON, OFF : 3/3.
Ce n'est PAS « un vaisseau qui tourne dans une boucle de miroirs » (impossible, R-331) mais son équivalent borné : une paire de fourmis
qui tourne en rond (orbite de période 21). Une simulation finie ne prouve pas un fonctionnement infini ; mais l'état « 0 » est vide et
l'état « 1 » est un cycle exact, donc chaque usage recommence dans le même état (ce qui est démontré pour les 20 usages simulés).

## R-337 DEMI-ADDITIONNEUR R2L2 RÉUTILISABLE 20/20 (ferme R-329) — VÉRIFIÉ (2 moteurs, temps fini) (demi_add_z.py, demi_add_final.py)
Porte R-327 « H:R2L2|0,0,4;30,-56,0|1,0,1;29,-55,1 » (B r 0 en (0,0) joué en 1er, A r 2 en (30,−56) ; ensemble ils se DÉCALENT).
Géométrie (pourquoi un seul virage ne peut pas marcher, R-325 « les voies s'éloignent ») : la route de sortie de V (B seul) ne croise la
route de U (A seul) qu'au point de porte (30,−30), où V passe au même instant ; donc il faut un zigzag : K2 tourne U vers la gauche
(direction 4) en X1 = (30, −30 + s1), puis K3 remet un vaisseau en direction 0 sur la ROUTE D'ARRIVÉE de B, en amont de la porte.
Recherche systématique (fourmi_r, 2 cœurs) : 99 732 placements de K2 → 6 674 virages propres (0 case) qui n'abîment ni V ni le cas (1,1) ;
40 K2 distincts × 246 960 placements de K3 → 2 163 demi-additionneurs justes pour les 4 cas, 0 case restante ; réutilisation (usages
espacés de k = 200 périodes) avec le critère le plus strict — l'état final de plusieurs usages est EXACTEMENT la superposition des usages
faits seuls (aucune interaction entre usages) : 563 / 2 163 pour les 16 suites de 2 usages, puis 563 / 563 pour 3 suites de 20 usages au hasard.
Exemple retenu : K2 = « 62,−24,4 » + cases (62,−23), (63,−23) (joué en 1er) ; K3 = vaisseau r 0 en (−16,16) (case (−15,16)) ; S = a⊕b
sur la voie 0 de la direction 0 (celle de B seul), C = a∧b sur la voie (2,−28) (A décalé). Dans le cas (1,0), c'est K3 qui est poussé sur
la voie de S. 20 usages au hasard dans UNE simulation (54 à 62 fourmis) : 20/20 additions justes pour 5 tirages ; 2 moteurs (fourmi_r et
hx.py) : états finaux identiques ; 0 case restante hors des vaisseaux. Germes : resumes/demi_additionneur_reutilisable.json.
Ce qui avait raté en R-329 (débris aux virages) est évité en exigeant 0 case à CHAQUE choc et la superposition exacte.
Statut : VÉRIFIÉ pour les usages simulés ; pour tout nombre d'usages, AFFIRMÉ (la superposition exacte de 2 usages pour toutes les suites
le rend très plausible, mais le non-recouvrement de 3 usages ou plus n'est vérifié que sur 3 × 20 usages).

## R-338 Le demi-additionneur R-337 marche pour TOUT nombre d'usages et TOUTE suite d'entrées — DÉMONTRÉ (certificat calculé + argument) (demi_add_certif.py)
Idée : si deux usages ne se « voient » jamais, N usages = superposition exacte des usages seuls (chacun juste, R-337).
Trajectoires exactes de chaque usage SEUL pour tout t ∈ Z (fenêtre simulée [0, 4 000] ; avant et après, chaque fourmi est un vaisseau sur
du blanc : pos(t + 8) = pos(t) + d, contrôlé sur 64 pas à chaque bout). Pour 2 usages d'écart j (j·200 périodes) et les 16 couples
d'entrées : distance minimale EXACTE entre fourmis des 2 usages sur toute la droite des temps = 90 + 100 (j − 1) pour j = 1 … 30
(jamais ≤ 6 : les cases d'un vaisseau sont à ≤ 2 de sa fourmi, il faut ≤ 6 pour qu'un usage perçoive l'autre ; 0 case laissée).
Au-delà de j = 30 : les fenêtres actives sont disjointes, deux routes rectilignes ne peuvent se rapprocher indéfiniment que si elles sont sur
le même axe en sens opposés à ≤ 6 voies : AUCUNE paire (sortie, entrée) de ce type ; sinon leur distance croît avec j (constaté : +100 par usage).
⇒ pour toute suite (a₁,b₁), (a₂,b₂), … espacée de 200 périodes, chaque usage donne S = a⊕b et C = a∧b. Hypothèses : convention
« l'une après l'autre » (sans effet ici : les usages ne se touchent pas), grille infinie, entrées et constantes K2, K3 fournies à chaque usage.

## R-339 La mémoire R-335 marche pour TOUT nombre d'usages et TOUTE suite de bits — DÉMONTRÉ (même certificat que R-338) (memoire_certif.py)
Un usage = écrire b (si b = 1) puis lire ; il part du pixel vide et y revient (0 case laissée, contrôlé). Les usages sont des copies exactes
décalées de 3 200 pas. Distance minimale exacte entre fourmis de deux usages (tous temps, 4 couples de bits) : 101 + 200 (j − 1) pour
j = 1 … 20 ; aucune paire de routes de face. ⇒ N usages = superposition exacte ; chaque lecture rend le bit écrit (R-335).

## R-336 Oscillateurs à 4 fourmis : 23 364 orbites, 0 miroir — OBSERVÉ (miroir.c enum 4 2 0 + tir)
4 fourmis dans [−2,2]² avec 0 ou 1 case dans [−2,2]² (409 204 224 situations testées) → 23 364 orbites distinctes (périodes 12 … 345).
Tir (6 directions × voies × phases × 2 ordres, 3 tranches) : 0 miroir exact, 0 miroir « tourné/déplacé » ; détruits/sales 42 161 060,
transparents 61 780 692, décalés 17 788. Conforme à R-331 (aucun miroir exact possible).

## R-340 Un objet périodique ne peut pas CAPTURER un vaisseau sans rien émettre — DÉMONTRÉ (3 lignes) ; = Thm 3 de McGinnis-Webb 2019 (modèle synchrone)
Si R (périodique) + vaisseau → objet borné pour toujours, tout le système est borné dans le futur, donc périodique (réversibilité, R-44),
donc borné dans le passé : impossible, le vaisseau venait de l'infini. ⇒ « faire entrer un bit avec UN vaisseau » oblige à émettre au
moins un vaisseau : on CHANGE l'objet R en R' (le vaisseau ressort). Recherche (bascule_hexa.py sur les 95 oscillateurs à 2 fourmis de
[−3,3]²) : 20 335 conversions R → R', 11 510 R' distincts, 438 496 retours R' → R AU MÊME ENDROIT (avec doublons).
Bascule « T » (le même vaisseau fait R → R' puis R' → R) : 0 ; avec même direction et même ordre, la voie diffère toujours de ±1 (473 cas).
Bascules « RS » (mise à 1 et mise à 0 par 2 vaisseaux différents) dont toutes les routes tiennent dans un demi-plan : 920.
Aucune n'est idempotente (écrire 1 sur un 1 abîme l'objet pour au moins une phase) : il faut alterner, ou lire avant d'écrire.

## R-341 Bascule RS à UN vaisseau par écriture, 20/20 — VÉRIFIÉ (2 moteurs, temps fini) (bascule_demo.py)
État 0 = M = « H:R2L2|0,0,1;1,-1,0|-1,1 » (le bit de R-335, période 21) ; état 1 = R' = « H:R2L2|-1,0,3;1,1,0|-1,0;-1,1;0,-1;1,0;1,1 »
(2 fourmis + 5 cases, période 12), au même endroit. Mise à 1 : 1 vaisseau direction 0 (voie 1 depuis le centre, M en phase 16), il
TRAVERSE et continue tout droit ; mise à 0 : 1 vaisseau direction 2 (voie −2, R' en phase 2), il traverse aussi. Chaque vaisseau arrive à
la bonne phase (instant choisi au pas près ; germes avancés de 0 à 7 pas). 20 écritures alternées 1, 0, 1, 0… au même endroit, UNE
simulation (22 fourmis posées à t = 0, t = 32 405) : 20/20 états justes entre deux écritures ; 2 moteurs identiques à la fin.
C'est exactement « faire entrer le bit (1) et le faire sortir (0) avec un autre vaisseau » de la consigne 3a, sans miroir.

## R-342 Pas de cycle de bascule « sans mémoire de l'histoire » — OBSERVÉ (bascule_cycle.py, résultat négatif)
Cherché : « mise à 1 éventuelle puis remise à 0 » qui laisse l'objet EXACTEMENT comme si rien n'avait eu lieu, ET remise à 0 sans effet
quand le bit vaut 0. Sur les 230 bascules RS (routes dans un demi-plan, vaisseaux joués après l'objet) × tous les instants possibles de
remise à 0 : 0. La condition (A) est parfois remplie, jamais (B) : remettre à 0 un bit déjà à 0 détruit ou change M. ⇒ avec ces bascules
il faut connaître l'état (alterner, ou utiliser la mémoire R-335 à lecture destructive).

## R-343 La bascule R-341 supporte un nombre QUELCONQUE de cycles « 1 puis 0 » — DÉMONTRÉ (certificat, bascule_certif.py)
Cycle de durée P = 3 075 pas : mise à 1 à t = 16 (M en phase 16), mise à 0 à t = 738 (R' en phase 2) ; à t = P l'objet est EXACTEMENT
l'état de départ (contrôlé ; ce sont les mêmes fourmis, dans le même ordre : les vaisseaux d'écriture ressortent eux-mêmes). Le cycle j est
la copie décalée de j·P. Distances exactes (toute la droite des temps) : vaisseaux de 2 cycles ≥ 145 + ≈ 193 (j − 1) pour j = 1 … 10 ;
hors de son cycle, un vaisseau reste à ≥ 42 du centre (l'objet tient dans un rayon 3). ⇒ par récurrence, chaque cycle se déroule à
l'identique : la bascule fonctionne pour toute suite 1, 0, 1, 0, … (au-delà de j = 10 : croissance linéaire, routes rectilignes divergentes).

## Session du 26/11 (jour) — additionneur complet, calcul → mémoire, boucle (R-344 à R-350)

## R-344 Égaliser les deux horaires de S avec UN vaisseau constant : « HA* » — VÉRIFIÉ 4/4 (2 moteurs, temps fini) ; NON réutilisable (OBSERVÉ)
Rappel : dans R-337, S sort sur la voie 0 à l'abscisse 1000 (cas (0,1), S-V) ou 968 (cas (1,0), S-U = K3 « libre ») : 16 périodes d'écart.
Le retard géométrique demandé (piste 1) bute sur un fait : dans les cas (0,0), (0,1), (1,1), K2 décale K3 sur la voie 1, à 1 abscisse de
la place de S-U ; tout virage qui ramène S-V à cet endroit touche aussi K3' (fa_retard.py etape1 : 5 068 premiers virages propres, mais
la 2e étape revient toujours à cette case occupée). Égaliseur tête-bêche (direction 3, un seul constant) : 0 / 220 320 (gêné par K3').
Recherche d'UN constant de direction quelconque (fa_retard.py un : 225 200 + 896 130 placements, directions 1-5, voies ±5, 8 phases,
2 ordres) : 52 réussites, 6 placements distincts, où S sort sur UNE seule position (voie 0, abscisse 968) dans (1,0) ET (0,1) et C sur
une seule position. Exemple (ha_etoile.py, variante 0) : K5 = « 31,1,3 » + case (31,2), joué en 1er ; C = (1, −29, 973, 0) (direction 1).
Mécanisme : dans le cas (0,1), le choc K5 + S-V renvoie de quoi repousser K3' sur la voie 0 à la place de S-U.
4 cas justes, 2 moteurs identiques. MAIS les 6 placements remontent tous un axe d'entrée à contresens (26 sur l'axe de A, 6 sur celui de K2) :
les déchets de l'usage j qui partent le long de cet axe percutent le K5 de l'usage j + 1 ⇒ 2 usages : 8/16 (variante 0), 12/16 (variante 1),
pas mieux avec k = 300, 400. Statut : égaliseur VÉRIFIÉ (1 usage) ; « aucun égaliseur à un constant n'est réutilisable » OBSERVÉ (sur ces 1,1 M).

## R-345 Additionneur complet « tête-bêche » 8/8 et additionneur 2 bits 16/16 (UN usage) — VÉRIFIÉ (2 moteurs) ; non réutilisable DÉMONTRÉ
Idée (argument de translation) : un vaisseau c de direction 3 qui remonte la voie de S rencontre S-V au point P1 ou S-U au point P2,
8 périodes plus tard et 8 cases plus près de la porte ; les deux rencontres sont la même à une translation près ⇒ même issue pour c,
sans égaliser les horaires. Recherche (fa_complet.py, 340 080 placements de c) : 9 428 additionneurs complets propres 8/8, sommes et
retenues lisibles sur 3 positions chacune (jamais moins). Exemple retenu (resumes/additionneur_tete_beche.json) : c = « 145,−145,1 » +
case (144,−145), joué en 1er : 8/8, 2 moteurs identiques. Enchaînement (add2_tete.py, compose.py) : la sortie C du demi-additionneur R-337
(1 vaisseau, direction 2) devient la retenue c d'un additionneur complet tourné de −60° et posé exactement sur sa route (calcul exact) :
ADDITIONNEUR 2 BITS 16/16, 2 moteurs identiques (resumes/additionneur2_tete_beche.json). Réutilisation : impossible — la route d'entrée de c
est la route de sortie de S parcourue à contresens, donc le c de l'usage j + 1 croise de face les sorties S de l'usage j (constaté : 24/64
suites de 2 usages). DÉMONTRÉ pour toute construction tête-bêche au même endroit (argument : même axe, sens opposés, voies ≤ 6).
Ce qui manque pour un additionneur complet réutilisable : une « fusion » réutilisable de deux signaux exclusifs (même route, même instant).

## R-346 Le calcul écrit dans la mémoire : a∧b → bascule → lecture → remise à 0, 20/20 au même endroit — VÉRIFIÉ (2 moteurs, temps fini)
memoire_cherche.py : les 19 313 mises à 1 distinctes des bascules R → R' → R (bascule_hexa.py, 438 496 cycles avec doublons) sont tournées et
posées sur la route de la sortie C = a∧b du demi-additionneur R-337 (réutilisable, R-338) ; 11 147 sont écrites correctement dans les 4 cas
(R' si a∧b, R sinon ; les déchets des autres cas ne les abîment pas). memoire_demo.py : on ajoute la remise à 0 (vaisseau R' → R, envoyé quand
le pixel lu vaut 1, car aucune bascule n'est idempotente, R-340/R-342) et on enchaîne 20 usages ; les instants des usages sont choisis
(≥ 200 périodes d'écart) pour que l'objet soit à la bonne phase. 8 bascules sur les 8 essayées (après tri des remises à 0 qui arrivaient de
face sur la sortie C) : 20/20 lectures justes pour 3 suites au hasard (graines 0, 1, 2), 20 × (1,1) : 20/20, alterné : 20/20 ; propre ;
2 moteurs identiques. Retenue (resumes/memoire_calcul.json) : R = osc. 9 (p 12), mise à 1 r 0 voie −4 (traverse), remise à 0 r 2 voie 2
(traverse), tournées de 2 crans. Lecture = état de l'objet dans la grille (écran). Tout nombre d'usages : AFFIRMÉ (pas de certificat :
écarts d'usages variables).
Lecture par un vaisseau (lecture_bascule.py) : pour M et R' de R-341, toute sonde qui laisse l'objet intact ressort EXACTEMENT comme si
l'objet n'existait pas (2 112 et 1 248 tirs) ⇒ pas de lecture non destructive à 1 vaisseau pour cette bascule (OBSERVÉ).

## R-347 Boucle : ce que les théorèmes interdisent — DÉMONTRÉ (voir BOUCLE.md)
T0 pas de canon (chaque vaisseau est une fourmi, nombre conservé) ; T1 borné ⇒ périodique ⇒ borné aussi dans le passé (réversibilité) ;
T2 = McGinnis-Webb Thm 3 / R-340 (pas de capture) ; T3 (généralise R-331) : un relais qui reçoit à chaque passage un vaisseau de direction r,
en émet un de direction r' et redevient lui-même après k passages vérifie classe(r') = classe(r) et k·(Q(r) − Q(r')) ≡ 0 (mod 3) ⇒ déviations
de 60°, 180°, 300° impossibles ; ±120° seulement si 3 | k ; k = 1 (relais qui reste lui-même) et k = 2 impossibles. T4 : un circuit fermé de
relais a toutes ses directions dans une même classe, des virages de ±120°, chaque relais à 3k états ; le plus petit est un triangle.
Remarque : deux vaisseaux libres qui se sont croisés ne se rencontrent plus jamais (même vitesse, droites) : une orbite bornée à longs vols
libres demande au moins 3 vaisseaux qui se relancent.

## R-348 Relais à 3 états : 0 trouvé — OBSERVÉ (relais.py)
2 fourmis (95 oscillateurs, toutes directions, voies ±8, phases, 2 ordres) : 198 884 conversions propres à 1 vaisseau sortant, dont 4 398
déviées de ±120° ; 1 953 R1 distincts ; 262 chaînes R0 → R1 → R2 avec la même route d'entrée et de sortie ; 0 retour à R0.
3 fourmis (12 oscillateurs) : 38 762 conversions, 12 déviées, 0 chaîne. Contrôle de T3 : 0 objet dévié redevenu lui-même (comme prévu).
Les phases d'arrivée ne sont même pas imposées (condition plus faible que dans un vrai circuit) : le résultat négatif n'en est que plus net.

## R-349 ADDITIONNEUR COMPLET RÉUTILISABLE (a + b + retenue) — VÉRIFIÉ (2 moteurs, 20 usages) ; tout nombre d'usages DÉMONTRÉ (certificat)
fa_reuse.py : demi-additionneur R-337 + retenue c = UN vaisseau de direction quelconque dont la route n'est l'axe d'aucune entrée à
contresens, et dont aucune sortie n'est sur un axe d'entrée à contresens (412 000 placements : directions 1, 5 → 0 ; 0, 2, 4 → 8,
toutes de direction 4, 2 géométries). Retenu (fa_reutilisable.py, resumes/additionneur_complet_reutilisable.json) : c = « 56,−28,2 » +
case (57,−28), joué en 1er (il croise la sortie de la porte vers t = 224). Somme lue sur (0,0,1000,0), (2,−31,915,0), (4,28,914,2) ;
retenue sur (0,1,999,0), (0,1,999,7), (2,−32,920,1) (au temps 4000 ; « un vaisseau sur l'une des positions »).
8/8 justes, 2 moteurs ; 2 usages (k = 200 périodes) : 64/64 suites en superposition exacte ; 20 usages au hasard dans UNE simulation
(graines 0, 1, 2) : 20/20, superposition exacte, 2 moteurs identiques. Certificat (circuit.certificat, même méthode que R-338) : distance
minimale EXACTE entre fourmis de deux usages, sur toute la droite des temps, pour les 64 couples d'entrées : 90 + 100 (j − 1) pour
j = 1 … 12 ; aucune paire (sortie, entrée) sur le même axe en sens opposés ⇒ N usages = superposition exacte pour tout N et toute suite.
Remarque : la piste 1 (égaliser S) n'était pas nécessaire ; la retenue c agit sur S-V, S-U ou les vaisseaux décalés selon le cas.

## R-349b HORLOGES SANS MIROIR à 6 fourmis — VÉRIFIÉ (CYCLE exact = périodique pour toujours ; 2 moteurs) ; famille infinie OUVERT
horloge.py (3 vaisseaux, symétries 2, 3, 6, rayon 10, 46 056 essais) : 0 cycle. horloge2.py (2 générateurs : 4 vaisseaux symétrie 2 ou
6 vaisseaux symétrie 3, 3 × 200 000 tirages, rayons 8, 12, 16) : 72 cycles à 4 vaisseaux (période ≤ 36), 1 362 à 6 vaisseaux (périodes
jusqu'à 13 266). Famille : P = 2 322 + 2 736 n, boîte 35 + 48 n, rayon 22 + 32 n, pour n = 0, 1, 2, 3, 4 (resumes/horloges_6_fourmis.json) ;
retour exact vérifié par fourmi_r (CYCLE) et hx.py. Vols libres jusqu'à 426 pas. C'est une « boucle » au sens de la consigne 3 : des
signaux font le tour et reviennent, sans miroir et sans relais immobile (compatible avec T3 : les objets qui relancent un vaisseau
sont eux-mêmes des vaisseaux en mouvement). Déjà connu ? McGinnis-Webb 2019 : orbites à 2 particules (synchrone) ; rien trouvé sur des
orbites de 6 particules à longs vols.

## R-350 Enchaînement réutilisable de R-349 derrière R-337 : ÉCHEC (OBSERVÉ, cause identifiée)
add2_reutilisable.py, compose.py (attach : rotation + translation + avance exactes pour que la pièce c de l'étage 1 suive exactement c0 ;
slide : glissement de l'étage 1 le long de la route de c) : 11/16 pour tout glissement D = 20 … 400 (6/16 sans glissement). Cause
(trace des distances) : dans R-349, le constant K2 voyage parallèlement à c, 4 voies à côté ; tourné et posé sur c0, il traverse la porte
de l'étage 0 au moment où c0 y naît (choc B/K2 à t = 233). Le glissement ne change pas sa trajectoire (pièce parallèle à c).
Virage de c0 par UN constant pour l'éloigner (virage_c.py, 172 016 placements) : 0 virage nouveau propre et réutilisable.
L'additionneur 2 bits réutilisable reste OUVERT ; celui à UN usage est R-345 (16/16).

# ===== Journaux des sessions parallèles du 26-27/11 (R2L2), rassemblés le 27/11 09:09 UTC par T1 (copie, les originaux restent dans recherche/regles/s*/journal.md) =====

# ----- recherche/regles/s1_fusion/journal.md -----
# S1 fusion — journal (R-400+)
Début session S1 : 19:30 UTC

Session S1 (fusion / enchaînement), 26/11 soir, automatique (Pierre-Malo absent). Branche claude/s1-fusion (depuis claude/r2l2-additionneur-boucle).
Règle H:R2L2 (hexa, blanc → +120°, noir → −120°), fourmis jouées l'une après l'autre, positions entières. Moteurs : fourmi_r (C) et hx.py (Python).
Commandes à lancer depuis recherche/regles/.

## R-400 Fusion de deux signaux exclusifs avec UN constant : 1 529 fusions (UN usage) — VÉRIFIÉ (2 moteurs, temps fini) (fusion1.py, fusion1v.py)
Fusion = deux routes s1, s2 (au plus un vaisseau à la fois) → UN vaisseau sur UNE trajectoire O (même direction, voie, instant, phase),
O absente quand il n'y a aucun signal, 0 case restante. Recherche EXHAUSTIVE à 1 constant K (vaisseau direction 0) : tous les chocs
propres de R-333 (1 688), rangés modulo la symétrie σ (décaler s de 8 pas et de −d_K laisse K invariant) ; deux chocs qui émettent la
même trajectoire = fusion. 2 360 paires, 1 529 à routes distinctes, toutes revérifiées par simulation directe des 3 cas (fourmi_r)
et par hx.py (0 désaccord). Complément (fusion1b.py) : un signal qui ne touche pas K ne peut pas servir (les 1 904 sorties prolongées
en arrière passent toutes à ≤ 6 de K) ⇒ la liste est complète.

## R-401 À 1 constant, toute fusion RÉUTILISABLE est une « fusion à ombre » — DÉMONTRÉ (calcul exhaustif R-400) (fusion_reuse.py)
Sur les 1 529 : 1 516 ont une sortie qui repart à contresens sur l'axe d'une entrée (≤ 6 voies) ⇒ percutée par l'usage suivant.
Les 13 restantes sont réutilisables (2 usages 9/9, 20 usages × 3 graines 20/20, 2 moteurs, certificat : distance 99 + 100 (j − 1))
MAIS O = K décalé d'UNE voie : dans le cas « aucun signal », K passe sur la voie voisine au même instant (l'« ombre »). C'est un
codage « 2 rails » (O = x∨y, ombre = ¬(x∨y)), pas une sortie seule sur sa route.
Pourquoi (argument géométrique + invariants R-331) : la ligne de O passe par les deux points de choc P1 (s1+K) et P2 (s2+K), qui sont sur la
ligne de K ; donc O est sur l'axe de K (ombre si même sens, route de face si sens opposé) ou P1 ≈ P2 ; dans ce 2e cas toutes les lignes
passent par le même point et (I1)+(I2) forcent les directions des déchets ; ex. type (s1, s2, O) = (1, 2, 2) : le déchet de s1 + K a
forcément la direction 5, à contresens de s2, et part du point de choc, donc sur l'axe de s2.

## R-402 Ombre + 2e constant « séparateur » : 5 640 fusions… toutes encore à ombre — OBSERVÉ (fusion2.py, bases 0 et 1)
K' placé sur la route de O (17 instants, 5 directions, 81 décalages, 8 phases, 2 ordres : 2 × 74 912 placements) : 5 640 réussites à 2 usages
9/9, mais O' est toujours K' retardé de quelques pas (même voie) : l'ombre a seulement changé de constant. Critère corrigé ensuite :
« aucune sortie du cas vide parallèle à O à ≤ 6 voies ».

## R-403 FUSION PROPRE ET RÉUTILISABLE à 2 constants — VÉRIFIÉ (2 moteurs, 20 usages) ; tout nombre d'usages DÉMONTRÉ (certificat) (fusion3.py, fusion_final.py)
Idée : partir d'une fusion à 1 constant non réutilisable dont le SEUL défaut est le déchet forcé de R-401 (type (1, 2, 2)) et ajouter un
constant K' qui percute ce déchet δ périodes après sa naissance, là où s2 est déjà passé. Recherche : 17 432 placements par base,
642 réussites par base (2 usages 9/9, sans ombre, sans route de face).
Exemple retenu (fusion_verif.json, indice 0) : ordre de jeu Kp, s1, s2, K ;
 K = « −85,85,4 » + case (−84,85) (direction 0) ; Kp = « 91,−7,2 » + case (91,−8) (direction 4) ;
 s1 = « −85,1,1 » + cases (−85,0), (−85,1) (direction 1) ; s2 = « −1,−83,2 » + cases (−1,−83), (0,−84) (direction 2) ;
 O = vaisseau direction 2, voie 1, abscisse 833, phase 6 au temps 4 000 (même trajectoire exacte pour s1 et pour s2).
 Cas vide : K et Kp continuent (directions 0 et 4, rien de parallèle à O). 3 cas justes, 2 moteurs ; 2 usages 9/9 ; 20 usages dans UNE simulation :
 3 suites au hasard + 20 × s1 + 20 × s2 + alterné : 20/20, superposition exacte, 2 moteurs identiques à chaque fois.
 Certificat (circuit.certificat, j = 1 … 10) : distance minimale EXACTE entre fourmis de deux usages = 7 (> 6) pour tout écart, aucune paire de face
 (les 7 viennent de deux routes à contresens à 7 voies, qui se croisent toujours à 7) ⇒ N usages = superposition exacte pour tout N.
Commande : python3 s1_fusion/fusion_final.py s1_fusion/fusion3_122_0_2.json 0 10

## R-404 CROISEMENT : deux vaisseaux libres ne s'influencent que s'ils passent à distance ≤ 1 (≤ 2 s'ils sont parallèles) — DÉMONTRÉ (calcul exhaustif) (croisement.py, paralleles.py, croisement_demo.py)
Toutes les géométries relatives proches de 2 vaisseaux de directions différentes (r = 1 … 5, tau, v modulo u, 2 ordres : 1 880, R-333) :
distance minimale des trajectoires libres 0 : 232 / 240 interagissent ; 1 : 184 / 360 ; 2, 3, 4, 5, 6 : 0 / 256 chacune (croisement EXACT :
chaque fourmi suit pas à pas sa trajectoire libre). Au-delà de 6 : transparent exact (R-333). Aucun « vrai choc » ne rend les deux trajectoires
libres (0 échange). 416 géométries interdites en tout (64, 96, 96, 96, 64 pour r = 1 … 5). Parallèles (même direction, [−8, 8]², 8 phases,
2 ordres) : distance 2 : 4 / 296 interagissent ; ≥ 3 : 0. Conséquence : à contresens, deux routes ne se gênent que si la somme de leurs voies
est dans [−3, 1] (au lieu de « ≤ 6 voies » utilisé jusqu'ici, trop prudent).
⇒ Un croisement n'a besoin d'AUCUN constant : il suffit que les deux signaux ne passent pas à ≤ 1 l'un de l'autre. Démonstration
réutilisable (croisement_demo.py) : directions 0 et 1 (60°), puis 0 et 2 (120°), fourmis à distance 2 au plus près : 4 cas justes, 2 moteurs ;
2 usages 16/16 ; 20 usages (3 graines + 20 × (1,1)) 20/20, superposition exacte, 2 moteurs ; certificat (distance entre usages 117 + 200 (j−1),
resp. 17 + 100 (j−1)).
Certificat fin (cert_fin.py) : condition « distance ≥ 7, ou les deux fourmis libres et ≥ 3 / ≥ 2 », sur toute la droite des temps, + argument de
parité (couleur = parité des passages) ⇒ superposition exacte. Contrôle : la fusion R-403 passe (libres à 7, non libres ≥ 180).

## (vague 2, 27/11, début 00:41 UTC) Piste « relais » de la vague 1 (add2_fusion.py) : 0 réussite — OBSERVÉ ; cause trouvée : ORDRE DE JEU
Vague 1 : 1 010 relais (fusions R-402) × placements → « 16 cas : sale » à chaque fois. Vague 2 : même chose avec les fusions R-403 et
l'entrée de l'étage 1 par A, B ou c (add2_relais.py, relais 0 … 400 : 10 800 essais sales). Diagnostic (diverge.py) : les fourmis sont
jouées l'une après l'autre, et dans R-349 la pièce A joue APRÈS K3, K2, B ; en posant HA0 avant l'étage 1, la fourmi qui porte c0 joue
avant les pièces qu'elle rencontre ⇒ autre dynamique au contact. (Pour la piste relais, les 16 cas sales venaient aussi de relais qui
ne font que décaler c0 de quelques voies : l'étage 1 retombe alors presque sur HA0.)

## R-405 ADDITIONNEUR 2 BITS RÉUTILISABLE (a1a0 + b1b0 → c1 s1 s0) — VÉRIFIÉ (2 moteurs, 20 usages) (add2_perm.py, add2_final.py)
Idée : a + b + c est symétrique ⇒ la retenue c0 du demi-additionneur R-337 entre dans l'additionneur complet R-349 par sa pièce A
(même direction 2 que c0 : rotation 0), pas par c (R-350 : K2 parallèle à c traverse la porte de HA0). compose.attach (étage 1 posé pour
que A suive EXACTEMENT c0), glissé de D périodes ; le bloc HA0 joue À LA PLACE de la pièce A dans l'ordre de R-349 (sinon 15/16).
Balayage D = 0 … 400 (pas 10) : pièce A → 16/16 pour TOUT D ≥ 10 (39/39) ; pièce B (rotation 2) → 12/16 au mieux.
Retenu D = 20 : 8 pièces seulement, ordre de jeu : c(étage 1, entrée b1) « 74,−8,2 », K3' « −38,56,4 », K2' « 80,−4,4 », B' (entrée a1)
« −22,40,4 », puis HA0 : K3 « −16,16,4 », K2 « 62,−24,4 », B (b0) « 0,0,4 », A (a0) « 30,−56,0 » (cases : add2_final.json).
Sorties au temps 9 000 : s0 sur (0,0,2218,0) ou (0,0,2250,0) ; s1 sur (0,18,2188,0), (2,−29,2163,0), (4,8,2108,2) ; c1 sur
(0,19,2187,0), (0,19,2187,7), (2,−30,2168,1) (« un vaisseau sur l'une des positions »).
16/16 justes, propres (0 case hors vaisseaux), 2 moteurs identiques ; 2 usages (k = 200) : 256/256 couples en superposition exacte ;
20 usages dans UNE simulation : graines 0, 1, 2, 20 × (1,1,1,1), alterné : 20/20 chaque fois, superposition exacte, 2 moteurs identiques.
PIÈGE : fourmi_r a MAXA = 128 et IGNORE sans message les fourmis suivantes (20 × 1111 = 160 fourmis → faux échec « 0/20, 2 moteurs
différents »). s1_fusion/fourmi_r512 (même source, MAXA = 512) + big.py ; à signaler dans le dépôt commun.
La fusion R-403 n'a pas été nécessaire pour 2 bits (elle servira à rendre c1 « une seule route » pour enchaîner un 3e bit).
Commande : python3 s1_fusion/add2_final.py 20 5   (depuis recherche/regles/)

## R-406 CROISEMENTS dans un vrai circuit (l'additionneur R-405) — OBSERVÉ (16 cas) + R-404 (croisement_add2 : croise_add2.py)
Dans R-405, 50 paires (fourmi de l'étage 0, fourmi de l'étage 1) ont des CHEMINS qui se coupent (même case, instants différents) sans
jamais être à moins de 2 au même instant : ex. B' (entrée a1) coupe le chemin de B (étage 0) à 467 pas d'écart (distance min 40) ;
K3' coupe K3, K2 et B. Par R-404 ce sont des croisements transparents ; le circuit est juste 16/16 et 20/20 avec eux.
Commande : python3 s1_fusion/croise_add2.py 20
Certificat fin de R-405 (cert_fin.py, W = 5 000, écarts j = 1 … 5) : condition fine vraie pour les 256 couples à chaque écart ; distance
minimale EXACTE entre fourmis de deux usages = 156 + 200 (j − 1) (non libres) et 62 + 100 (j − 1) (libres), croissance linéaire ; aucune
paire (sortie, entrée) de face ⇒ N usages = superposition exacte pour tout N et toute suite : DÉMONTRÉ (même argument que R-349, R-403).

## R-407 Additionneur 3 bits, essai direct : ÉCHEC (OBSERVÉ) — la retenue c1 de R-405 sort sur 3 routes (add3_try.py)
c1 = (0,19,2187,0) si c0∧a1∧¬b1 ; (0,19,2187,7) si ¬c0∧a1∧b1 (même voie, UN pas d'écart) ; (2,−30,2168,1) si c0∧b1.
3e étage R-349 posé sur l'une des 3 routes (pièces A, B, c ; D = 20, 60, 150) : au mieux 49/64 cas propres (route de direction 2, pièce A).
Il faut d'abord regrouper les 3 routes en une. Piste : fusion1.json contient 938 fusions à 1 constant entre DEUX signaux de MÊME
direction (dont des paires sur la même voie) : chercher celle qui regroupe (0,19,·,0) et (0,19,·,7), puis une fusion R-403 avec la route
de direction 2 ; rendre le tout réutilisable (R-401 : il faudra un 2e constant). OUVERT.

## R-408 Regrouper les deux routes de c1 qui ne diffèrent que d'UN pas, avec UN constant : 66 fusions, toutes « à ombre » — OBSERVÉ (fus07.py)
V0 = (0,19,2187,0), V7 = (0,19,2187,7). K : 6 directions × disque de rayon 5 autour de V0 × 8 phases × 2 ordres (4 368 K, 21 840 simulations,
1 s) : 66 K donnent V0 + K et V7 + K propres avec une sortie O commune absente du cas « K seul ». Toutes : K de face (direction 3), O de
direction 3 à 1 voie et ~1 abscisse de la route de K seul (l'« ombre » de R-401 : quand c1 = 0, K passe presque au même endroit au même
instant) ⇒ inutilisable pour enchaîner. Il faudra 2 constants (méthode R-403 adaptée). 3 bits : OUVERT.
Commande : python3 s1_fusion/fus07.py 5

## (vague 3, 27/11, début 05:46 UTC) Dernier commit 01:02 → plus de 30 min, je reprends (3 bits).

## R-409 Regrouper 2 routes de c1 avec une fusion du catalogue R-400 posée EXACTEMENT : 4 appariements, tous inutilisables — DÉMONTRÉ (calcul exact sur le catalogue) / OBSERVÉ (simulation) (match3.py, add3_k1.py)
Calcul exact (sans simulation) : on tourne chaque fusion à 1 constant (1 529, R-400) pour que s1 suive EXACTEMENT une route de c1, puis on cherche
un glissement k tel que s2 suive exactement une autre route (condition : même direction, même phase, gY − g(s2) = k (d1 − d2)).
Résultat : 4 appariements seulement, tous (s1 = V2, s2 = V0), type (1,5,3), rotation 1, k = −34 ; aucun avec V7 (la géométrie relative de deux routes
est fixée par R-349 : un seul entier libre, que le catalogue ne couvre presque pas).
Simulation (étage 0+1 de R-405 + ce K, 9 rangs de jeu, 16 cas, T = 11 000) : 5 à 13 cas sales sur 16 pour chacun des 36 montages.
Cause (lue dans les sorties de R-405) : les sorties s1 et c1 de R-349 roulent côte à côte, à UNE voie l'une de l'autre ((0,18)/(0,19), (2,−29)/(2,−30)),
au milieu de constants parallèles ((0,19,2657) même voie que c1, 15 périodes devant ; (2,−31), (4,7), (4,8)…). Par R-404 (interaction ⇔ distance ≤ 1),
tout constant qui touche c1 touche aussi s1 ou un de ces voisins dans un autre cas. ⇒ On ne peut pas trier la retenue de R-349 à la sortie.
Conséquence : pour enchaîner, il faut un additionneur complet dont la retenue sort SEULE sur UNE route : HA + HA + fusion (piste suivante).
Commandes : python3 s1_fusion/match3.py ; python3 s1_fusion/add3_k1.py 11000

## R-410 Les 66 fusions V0/V7 à 1 constant (R-408) dans le VRAI circuit : 246 montages propres 16/16, mais 2 usages ≈ 2/30 — OBSERVÉ (add3_k07.py, k07_reuse.py, sup2.py)
Les 66 K de R-408 (38 distincts) insérés à chacun des 9 rangs de jeu de R-405 (594 montages, T = 11 000) : 246 sont propres dans les 16 cas,
et les cas V0 et V7 émettent les MÊMES vaisseaux (2 sorties communes, absentes des autres cas) : la fusion marche pour UN usage.
2 usages (1 rang par K, 30 couples au hasard, superposition exacte) : 2/30 pour les 36 montages testés.
Cause : les 66 K sont tous de direction 3, c'est-à-dire qu'ils remontent l'axe de c1 à contresens (voie −20 contre 19) ; le K de l'usage j + 1
croise de face tout ce que l'usage j envoie sur cet axe (le constant de la voie 19, déjà dévié par K_j, et les restes) : argument tête-bêche de R-345.
⇒ Il faut frapper V0/V7 DE CÔTÉ : R-411.
Commandes : python3 s1_fusion/add3_k07.py 11000 ; python3 s1_fusion/k07_reuse.py 11000 30 1

## R-411 Fusion V0/V7 à 2 constants DE CÔTÉ dans le vrai circuit : 2 160 montages justes (1 usage, 2 moteurs) mais « 2 rails » et 2 usages 192/256 — VÉRIFIÉ (1 usage) / OBSERVÉ (k1full.py, k2full.py, matchlib.py, k2verif.py, k2reuse.py)
Étape A (k1full.py, 26 208 montages : K1 de direction 1, 2, 4, 5, disque de rayon 5 autour de V0, 8 phases, 9 rangs, 6 cas témoins, T = 9 600, 83 s) :
54 K1 propres, transparents hors V0/V7, qui touchent V0 et V7 ; chacun donne 3 vaisseaux nouveaux (tous différents entre V0 et V7) car le choc
emporte aussi le constant de la voie 19 (15 périodes devant c1). (Le même travail en isolé, k1side/k12iso, donnait 102 fusions, toutes ratées
dans le circuit : les cas V7 portent un vaisseau de plus, (4,7,·,5), et le constant de la voie 19 — il faut chercher DANS le circuit.)
Étape B (matchlib.py : appariement EXACT d'une fusion du catalogue R-400 sur une paire (p0, p7)) : 2 745 appariements ; K2 inséré à 10 rangs :
27 450 montages × 16 cas (T = 12 000, 362 s) : 2 160 propres 16/16 où les cas V0 ET V7 (0011, 0111, 1011, 1110) émettent le MÊME vaisseau
O = (0, 19, 2903, 4) au temps 12 000, absent des 12 autres cas, et V2 intact. Exemple (k2full.json indice 0) : K2 = « 1091,58,5 » joué 1er,
K1 = « 1099,42,1 » (cases dans le fichier) ; 16 cas, 2 moteurs identiques (k2verif.py 0 12000).
DÉFAUTS : (1) « 2 rails » : dans les cas c1 ≠ V0/V7, le constant de la voie 19 passe en (0, 19, 2907, 0), 2 abscisses devant O : O ≈ ce
constant retardé (même défaut que l'« ombre » de R-401) ; (2) 2 usages : 216 montages distincts, 8/12 couples au hasard ; pour l'exemple,
192/256 : les 64 ratés sont EXACTEMENT les couples dont le 1er usage est un cas V0/V7 (un déchet de la fusion gêne l'usage suivant, comme
en R-401 ; remède connu : intercepteur R-403).
Bilan 3 bits : la retenue de R-349 est entremêlée avec le constant de la voie 19 et la somme s1 ; chaque fusion « réussie » se paie d'un
défaut (face, 2 rails, déchet). 3 bits : OUVERT.
Commandes : python3 s1_fusion/k1full.py 5 9600 ; python3 s1_fusion/k2full.py 12000 ; python3 s1_fusion/k2verif.py 0 12000

# ----- recherche/regles/s2_horloge/journal.md -----
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

# ----- recherche/regles/s3_pas/journal.md -----
# S3 — pas de la petite fourmi en R2L2 (journal propre, R-600+)

Entrées R-600 à R-609 écrites après coup (27/11, 00:45 UTC) à partir des commits du 26/11 soir (19:33–20:09) et des fichiers ;
chiffres repris de resultats_modules.json et bibliotheque_portes.json (rien de recalculé à cette heure, sauf mention).

## R-600 Catalogue des chocs de 2 vaisseaux de classe paire — VÉRIFIÉ (2 ordres de jeu, hx.py)
Dir 0 × dir 2 ou 4, toutes positions relatives : en classe paire, seulement des échanges / transparences (pas de déviation utile).
Code : chocs_pairs.py → data/chocs_pairs.json (non versionné).

## R-601 à R-604 Échanges, portes sélectives, couples (g, h), chaînes NOR en classe paire — OBSERVÉ
Pistes « logique de voie » ; abandonnées au profit des chocs DÉVIANTS à 60° (R-605). Code : swaps.py, selectifs.py, combos.py, chaines.py.

## R-605 Compilateur « arbre de NOR » R2L2 — VÉRIFIÉ (par module, tous les cas, 2 moteurs)
Nœud = une puissance K ; ses entrées la croisent l'une après l'autre (choc déviant à 60°, même issue dans les 2 ordres, τ = 2…6) ;
K continue tout droit ssi aucune entrée → K = NOR(entrées). Un vaisseau par littéral vrai et par usage. Code : nor.py.

## R-606 Réutilisation au même endroit + certificat — DÉMONTRÉ (lemme) / VÉRIFIÉ (20 usages, 2 moteurs)
Usage u = même circuit retardé de u·Δ. Lemme : fenêtre d'interaction bornée, rayons libres avant/après qui ne s'approchent plus à < 7,
routes opposées à ≥ 7 voies → tout nombre d'usages est juste. Code : reuse.py (certificate, check_multi).

## R-607 Pas de la petite fourmi RL sur le tore 2×2 (R-61), module par module — VÉRIFIÉ pour h0', x', y', c00'..c11'
État 8 bits c00 c10 c01 c11 x y h1 h0. h0' = ¬h0 ; x' = x ⊕ ¬h0 ; y' = y ⊕ h0 ; cij' = cij ⊕ [x=i ∧ y=j] ; h1' = h1 ⊕ h0 ⊕ c.
| module | puissances | littéraux | cas | justes | 2 moteurs | certificat | Δ (pas) | 20 usages ×3 |
| h0' | 1 | 1 | 2 | 2 | 2 | oui | 2008 | 20/20 ×3 |
| x'  | 3 | 4 | 4 | 4 | 4 | oui | 3864 | 20/20 ×3 |
| y'  | 3 | 4 | 4 | 4 | 4 | oui | 4472 | 20/20 ×3 |
| cij' (×4) | 4 | 6 | 8 | 8 | 8 | oui | 5368–5880 | 20/20 ×3 |
(cas = 2^(variables utilisées) ; les 256 états s'y ramènent.) Commande : python3 modules.py h0 x y c00 c10 c01 c11 → resultats_modules.json.

## R-608 Diagnostic géométrique et recherche des longueurs — OUTIL
diag.py : segments de lignes d'univers à < seuil hors chocs voulus (sans simulation). opt.py / opt2.py : descente (petites échelles).

## R-609 Bibliothèque de portes R2L2 réutilisables — VÉRIFIÉ
NON, COPIE, ET, NOR, OU, ET par NOR, XOR (R-337) : tous les cas justes, 2 moteurs, certificat, 20 usages. Format : bibliotheque_portes.json,
code : portes_lib.py.

## R-610 Module h1' = h1 ⊕ h0 ⊕ c (27/11, 00:41 →) — EN COURS
Arbre de NOR de modules.py (27 puissances, 32 littéraux, 59 vaisseaux, 256 cas). Recherche aléatoire petites échelles (D 8–40, G 8–16,
400 essais) : aucun placement (00:41). Un placement au hasard : 216/256 faux, 0 voie opposée sûre, 195 conflits (diag, seuil 4).
Nouvelle idée : GRANDES échelles (D ≤ 300, G ≤ 60) et descente sur le nombre de conflits géométriques au seuil 7 (opt3.py).
- 00:47 diag2.py : conflits EXACTS par cas (chaque segment porte le masque des cas où il existe ; x et ~x ne coexistent jamais).
  Contrôle : modules x' → 0 conflit ; c00' → 2 couples à distance 4–5 (inoffensifs : le seuil 7 est prudent).
- 00:48–00:57 descentes opt4/opt5/opt6 (D ≤ 300, G ≤ 60, côtés) : plateau à 17 conflits (h1), 27 (h1f), 362 (h1s). OBSERVÉ.
- 00:58 CONFLITS STRUCTURELS — DÉMONTRÉ (argument ci-dessous, contrôlé sur n00/Nc : distance 520 → 2 en t = 3700–3756) :
  les 17 conflits restants sont TOUS à distance 0 et entre directions à 60°. Raison : si un nœud N a la même direction que son
  grand-parent P (côté + puis côté −), dans le repère qui suit la puissance de P, N est immobile et la sortie du parent avance en ligne
  droite vers P ; un débris de N qui part dans la direction du parent suit EXACTEMENT ce trajet et heurte P, quels que soient D et G.
  Remède : changer les côtés (miroirs) → struct.py (descente sur les côtés, conflits présents à distance 0 pour 3 tirages de D, G).
- Variantes de formule (modules.py, vérifiées sur les 256 états) : h1f (c et ¬c en un nœud à 4 sous-nœuds, 19 puissances),
  h1s (NOR des 16 cubes de ¬h1', profondeur 2, 17 puissances mais 80 littéraux).
## R-611 Pas complet en un germe : 7 modules sur 8 côte à côte — VÉRIFIÉ (moteur C) 00:52
step.py : h0', x', y', c00'..c11' translatés (voies opposées ≥ 7 entre modules), 256/256 états propres et justes (moteur C).
- 01:05 Analyse des conflits structurels (repère de la puissance P, où tous les partenaires d'un même côté suivent la MÊME droite
  relative ℓ± vers P) — DÉMONTRÉ (raisonnement) + OBSERVÉ (conflicts2, distance 0 pour tout D, G) :
  (S1) deux sous-nœuds du même côté : les débris immobiles (dans le repère de P) laissés sur ℓ par le 1er sont heurtés par le 2e
       (c'est la règle R-606 « un seul sous-nœud par côté » ; tout-« + » : 21 à 43 conflits à distance 0) ;
  (S2) un nœud N du côté opposé à celui de son parent M a la direction de son grand-parent P : immobile dans le repère de P, ses
       débris de direction M suivent ℓ et heurtent P. Sauf si N = NON d'une seule entrée… mais alors son enfant retombe dans S2.
  Conséquence : dans UN arbre, tout chemin garde le même côté ⇒ chaque nœud (hors racine) a au plus un sous-nœud ⇒ chaînes
  « liste de décision à clauses », qui ne savent pas faire un XOR (preuve : le 1er test devrait être une clause incluse dans {00, 11}).
  C'est pourquoi h0', x', y', cij' passent (profondeur ≤ 2 ou chaîne même côté) et pas h1'.
  REMÈDE choisi : COMPOSER des petits modules. La sortie d'un module (vaisseau tout droit) est posée EXACTEMENT sur la ligne d'univers
  d'un littéral du module suivant (rotation k, translation v, retard s ≡ phase mod 8), loin en amont. Un littéral n'a pas de porte
  à lui, donc pas de débris sur ℓ. → compose.py (R-612).
## R-612 Composition de modules (compose.py) — OUTIL VÉRIFIÉ sur g = h1⊕h0 ; ÉCHEC pour h1' (01:15)
Sous-circuit G (2 feuilles) : 256/256 justes et propres (3 tirages de Dlink). Circuit h1' en 13 modules (8 cubes, c, ¬c, g, ¬g, XOR) :
logique 256/256 mais au mieux 98/256 physiquement (24 tirages de Dlink 40–400) ; sous-circuits c et ¬c (4 cubes → train de 4) : 80–192/256.
Raison (même argument que R-610) : le module amont roule SUR la ligne du littéral, ses portes sont donc des événements sur ℓ± ;
ses débris immobiles (repère de P) bloquent les littéraux suivants du même côté (S1). Composer = greffer un sous-arbre : rien de neuf.
## R-613 Limite du compilateur NOR à chocs déviants — DÉMONTRÉ (sous les règles S1, S2)
Avec S1 et S2, un module = racine NOR de deux chaînes de même côté, chaque nœud de chaîne = NOR(train de littéraux, nœud suivant).
Une chaîne calcule une fonction « canalisante emboîtée » (NCF : f = l ∨ f' ou f = ¬l ∧ f', récursivement) ; la racine = ET de 2 NCF.
Parité de 3 variables : toute NCF qui contient ses 4 points vrais est une seule clause (preuve : la 1re variable canalisante doit être
disjonctive, puis la fonction restante sur 2 variables contient 2 points opposés → b∨c ou b∨¬c) ; 2 clauses ne peuvent exclure les 4
points faux. Donc h1' = h1 ⊕ h0 ⊕ c n'est PAS calculable par un module (ni par composition, qui est géométriquement la même chose).
Statut : DÉMONTRÉ pour ce jeu de portes (côtés + et −). Issue possible : portes « de face » (H), autre mécanisme (XOR R-337, fusion S1).
## R-614 Issue : portes « de face » (H) — EN COURS (01:12)
S2 n'a lieu que pour deux arêtes consécutives (+,−) ou (−,+). Le chemin (H,H) redonne la direction du grand-parent, mais aucun nœud ne
lâche de débris dans la direction a+3 (côtés : a±1, a±2 ; face : a+1, a+2) → pas de S2. Règle (htree.py) : après « + » : +, H ;
après « − » : −, H ; après H ou à la racine : +, −, H ; H = 1re entrée ; un sous-nœud par ligne. Avec H on peut BRANCHER : la limite
R-613 ne s'applique plus. Arbre h1' (27 puissances, 32 littéraux), formule juste sur les 256 états ; conflits à distance 0 : 7, 5, 3
pour 3 tirages de (D, G), tous différents → aucun conflit structurel commun. Descente opt7.py lancée (2 graines).
- 01:12 opt7 (graine 1, 213 s) : placement à 6 conflits géométriques (seuil 7, inoffensifs) → simulation : 256/256 JUSTES ET PROPRES.
  01:17 2e moteur : 256/256 identiques (hx.py), 49 s. → MODULE h1' (1 usage) VÉRIFIÉ : 27 puissances, 32 littéraux, 59 vaisseaux,
  tmax 12 356 pas. Paramètres : h1_param_simple.json (arbre htree.h1_tree()).
- Réutilisation de h1' : NON (critère (c) faux, 0 voie d'écart). Raison DÉMONTRÉE : une porte de face met l'enfant H sur la voie même de
  la puissance parent ; si le parent ressort tout droit (parent = 1 et sa puissance-parent déjà déviée), il file vers l'infini sur cette
  voie et percutera de face l'enfant H (vaisseau constant) de l'usage suivant. Dans l'arbre : Nc (2e entrée de A) et Pc (2e entrée de B)
  ont un enfant H ; B aussi mais A et B ne valent jamais 1 ensemble. Remède envisagé : n'avoir d'enfant H que pour des 1res entrées,
  ou un « balai » (puissance qui dévie la sortie qui s'échappe).
## R-615 LE PAS COMPLET EN UN GERME (1 usage) — VÉRIFIÉ (01:21)
step.py (NOLANES=1 BOX=6000, graine 1) : les 8 modules h0', x', y', c00'..c11', h1' translatés dans un seul germe R2L2 :
256/256 états propres et justes (les 8 sorties = R-61), moteur C (11 s) ; hx.py 256/256 états finaux identiques (54 s).
Commande : NOLANES=1 BOX=6000 python3 step.py 1 3 step8_simple.json h1_param_simple.json
Sans h1' (7 modules, BOX 1500) : certificat OK (Δ = 74 072 pas), 10 usages de suite au même endroit : superposition exacte,
10/10 justes, 2 moteurs identiques (01:15).
## R-616 h1' réutilisable : arbre htree.h1_tree2 (29 puissances) — EN COURS (01:27 →)
Règle ajoutée : un nœud qui a un enfant de face doit être la 1re entrée de son parent (Nc, Pc passent en face sous A, B ; ¬g et g
deviennent NON(NOR(feuilles))). B garde un enfant de face en 2e entrée de la racine, mais A et B ne valent jamais 1 ensemble.
opt9.py : 2 placements 256/256 justes et propres trouvés (graine 4 vers 01:31, graine 3 vers 01:34) ; certificat (Python) en cours.
- 01:41 Certificat de reuse.py trop lent pour 60 vaisseaux (double boucle Python sur 14 000 pas) → cert2.py (numpy, même lemme ; contrôlé identique sur x'). struct.py renommé structurels.py (il masquait le module standard struct).
- 01:43 h1R_param_3 et h1R_param_4 : 256/256 justes et propres, 2 moteurs 256/256 (tmax 10 540 et 9 804). Certificat en cours.
- 01:45 certificat (cert2) des 2 candidats : voies opposées des sorties RÉELLES à 0 (ÉCHEC) ; opp_real.py : 15 couples, tous
  « génériques » (débris ↔ littéraux ou puissances d'autres branches), aucun de la forme structurelle → réglables par D, G.
  opt10.py : descente sur conflits + 5 × couples opposés logiquement possibles (segments infinis de diag2 avec masques), lancée 01:47.
- 01:59 opt10 (graine 8, poids 1 sur les voies opposées, départ = meilleur de la graine 6) : placement à 0 couple opposé, 256/256 justes
  et propres, CERTIFICAT OK (fenêtre 9 877 pas, rayon 1 740, voies opposées ≥ 7 ⇒ tout nombre d'usages pour Δ ≥ 65 733 pas).
  Paramètres : h1R_param_OK.json. Vérification complète (2 moteurs, 20 usages ×3) : h1R_check.py, en cours.
## R-616 MODULE h1' RÉUTILISABLE — VÉRIFIÉ (02:12)
h1R_param_OK.json (arbre htree.h1_tree2, 29 puissances) : 256/256 justes et propres, 2 moteurs 256/256 ; certificat OK
(Δ ≥ 65 733 pas) ; 20 usages ×3 graines au même endroit : superposition exacte, 20/20 justes (moteur C, 900 fourmis) ;
3 usages avec les 2 moteurs : identiques, 3/3. Commande : python3 h1R_check.py h1R_param_OK.json → h1R_verif_OK.json.
## R-617 Pas complet réutilisable (02:05 →)
Germe 8 modules avec ce h1' (step.py graine 1, BOX 6000, voies opposées entre modules vérifiées) : 256/256 propres et justes (C, 8 s),
hx.py 256/256 identiques (47 s). Le certificat cert2 a manqué de mémoire (positions stockées : 130 fourmis × 14 000 pas × 256 cas)
→ cert3.py (sans mémoire, contrôlé identique sur x' et c00') ; step_reuse.py lancé 02:12.
- 02:14 cert3 sur le germe complet (8 modules, h1' réutilisable) : CERTIFICAT OK — fenêtre active max 9 877 pas, rayon 11 709,
  voies opposées ≥ 7 ⇒ tout nombre d'usages pour Δ ≥ 384 741 pas (Δ pris = 384 744). 115 s.
- 02:15 3 usages au même endroit (états au hasard) : superposition exacte, 3/3 (les 8 bits justes à chaque usage), 2 moteurs identiques.
- 02:18–02:20 5 usages ×2 graines (moteur C ; 10 usages : mémoire du moteur C dépassée) : superposition exacte, 5/5 et 5/5.
  STATUT R-617 : VÉRIFIÉ (2 moteurs, 256/256, usages répétés) ; tout nombre d'usages DÉMONTRÉ (certificat R-606, lemme relu en vague 1).
  Résultats : step_reuse_res.json. Commande : python3 step_reuse.py
## R-618 2 pas enchaînés — OUVERT (non tenté, 02:20)
Brancher les sorties du pas 1 sur les littéraux du pas 2 demande UNE copie de module par littéral utilisé (65 vaisseaux-littéraux
dans le pas 2, en comptant les négations) et, d'après S1, un littéral calculé doit être le DERNIER de son côté dans un train : les
feuilles actuelles (trains de 2 à 5 littéraux) ne le permettent pas. Piste : feuilles à 1 littéral calculé par côté + chocs de face,
ou un module « COPIE » (R-609) pour dupliquer.
- 02:21 Dépôts Drive : bestiaire 30 (5 fiches) + catalogue_s3.json → Bestiaires ; germes → 02_Resultats ; rapport (Google Doc) → 05_Methode ;
  versions de 01:25 déplacées dans 99_Archives. PR #15 (vers main) à jour.
- Fichiers de résultats ajoutés : step_res.json (germe 7 modules réutilisable, R-611/R-615), h1R_verif_3.json et h1R_verif_4.json
  (candidats h1' 256/256 dont le certificat a échoué, voies opposées 0, R-616), step8_simple.json (ESSAI RATÉ : 8 modules avec BOX 1500,
  128/256 propres — h1' trop près des autres ; la version juste est celle de R-615, BOX 6000).
## R-619 DEUX PAS ENCHAÎNÉS, 7 bits sur 8 (h0'', x'', y'', c00''..c11'') EN UN GERME — VÉRIFIÉ (27/11, 05:46–06:06, vague 3)
Choix (noté, Pierre-Malo dort) : chaîner par GREFFE (R-612) : chaque littéral v' / ¬v' d'un arbre du pas 2 est un module du pas 1
(double rail : ¬v' par le même arbre aux littéraux inversés) ; la puissance racine de ce module sort tout droit ssi v' = 1 et entre
dans la porte du pas 2. Diffusion = une copie de module du pas 1 par usage (pas de dédoublement de vaisseau). Les arbres du pas 2 ont
au plus 2 sous-nœuds par nœud, donc la règle de côtés de htree.py (portes de face) s'applique toujours (1 usage).
Sous-système fermé : (x, y, h0, cij) ne dépend pas de h1 (sur le tore 2×2, avancer de +1 ou −1 change la même coordonnée) ; F∘F donne
h0'' = h0, x'' = ¬x, y'' = ¬y — mais le germe les calcule EN PASSANT par les vaisseaux x', y', h0' (pas de raccourci).
| module | puissances | littéraux | cas | justes (= F∘F) | 2 moteurs |
| h0'' | 2 | 1 | 2 | 2 | 2 |
| x'', y'' | 11 | 10 | 4 | 4 | 4 |
| cij'' (×4) | 26 | 28 | 16 | 16 | 16 |
Longueurs : descente optc.py (comme opt7), 0 à 280 s par module (c11 : graine 1 ratée en 280 s, graines 2 et 3 OK en 61–102 s).
Germe : les 7 modules translatés (step.choose_offsets2, NOLANES=1, BOX=8000 ; BOX=3000 : pas de place pour c11) : 256/256 états
propres et justes (moteur C, 13 s) ; hx.py 256/256 identiques (108 s). 128 puissances, 143 littéraux.
Commande : python3 chain2.py (formules sur les 256 états) ; python3 optc.py c00 1 280 ; NOLANES=1 BOX=8000 python3 chain_germ.py 1
Résultats : chain_res.json, chain_params.json. Reste : h1'' (le cap) et la réutilisation.

# ----- recherche/regles/s4_ecran/journal.md -----
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
