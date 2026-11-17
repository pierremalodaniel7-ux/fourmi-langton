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
