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
