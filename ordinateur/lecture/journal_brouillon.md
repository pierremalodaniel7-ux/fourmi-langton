
## R-147 Deux autoroutes 104 sur (presque) la même ligne, SANS pièce : la 2e rattrape la 1re et les deux refont tout le chemin à l'envers (aller-retour exact) — VÉRIFIÉ (2 moteurs, temps fini) / OBSERVÉ (stats) — 26/11 nuit
2 germes R-20 (cap B), le 2e en amont en (2J+sh, −2J−sh+dp) du 1er, J = 20…199, sh = 0…3, dp = −8…8 : 12 240 situations,
`src/fourmi -retour` (T = 40 000). Décalage de voie dp pair (même classe I = x+y+cap mod 2) : 0 retour sur 6 120. dp impair
(classes opposées) : 4 353 retours sur 6 120, dont 3 423 « parfaits » : au même pas t* chaque sonde est EXACTEMENT dans l'état
retourné R du départ de l'autre, et la grille est revenue au départ sauf 28 cases autour de chaque germe (toute la ligne est effacée).
t* de 4 042 à 39 950 pas (médiane 22 612). Exemple J = 60, sh = 0, dp = −7 : t* = 14 416, moteur2.py identique. Voie exacte (dp = 0) :
la 2e autoroute est déviée SE par les débris du 1er germe (480/480). C'est la « gomme mutuelle » de R-141, qui n'a donc PAS besoin de
la pièce. Lien avec R-138/R-139 : seulement entre classes opposées. Littérature : pas trouvé (2 recherches web, deja_connu.md).
`ordinateur/lecture/rattrapage.py`, `deux_sur_ligne.py`.

## R-148 La paire ON/OFF de la bascule T est un aller-retour exact : au pas t* la pièce (185, 186) est revenue EXACTEMENT à son état du pas 0 — VÉRIFIÉ (2 moteurs, temps fini) — 26/11 nuit
`palindrome.py` : 185 : t* = 14 008, grille = départ sauf 56 cases (28 + 28 aux deux sources, 0 près de la pièce), pièce = pièce du
pas 0 ; 186 : t* = 18 344, idem ; 572 : t* = 14 348, 64 cases (8 près de la pièce) ; 1020 : t* = 15 120, 62 (6 près de la pièce).
Conséquence (raisonnement exact, fils idéalisés) : si les sondes revenaient « dans leur fil » au lieu de buter sur leurs germes,
la bascule 185/186 retrouverait exactement l'état de départ après chaque paire ⇒ nombre ILLIMITÉ d'écritures/effacements.
Dans une vraie simulation, les germes retournés relancent 2 autoroutes vers le NO depuis les sources (R-141).

## R-149 Lecture en 2 impulsions sur la ligne a : la mémoire reste intacte, mais aucune sortie ne dépend de l'état — VÉRIFIÉ (2 moteurs, temps fini) / FAUX comme lecture — 26/11 nuit
(a) Depuis S0 : impulsions 1 + 2 → S0 (185, 186, 572, 1020) par l'aller-retour exact R-148 : les 2 sondes reviennent aux sources ; la
sortie « selon l'état » de l'impulsion 1 (NO pour 185 et 186) ne sort jamais (rattrapée). (b) Depuis S1 (écrit par W) : R1 annule W
(paire W–R1), R2 réécrit → S1 (185 jusqu'à 97 144 pas ; 186 ; 572) ; sorties mêlées, dépendantes de l'histoire, ligne non effacée
(29 014 cases contre 15 523). (c) Écart entre impulsions (185, `balayage_delai.py`, 112 + 256 essais) : retour à S0 seulement pour
6/112 (J ≈ −3…0 et 15…16 périodes de décalage) ; J ≥ 43 : 124/256 « S1 gardé + sonde 2 SE » ; `rafale.py` (6 impulsions espacées de
60 périodes, 4 bascules) : la 1re écrit, les 5 suivantes repartent SE, S1 gardé. TÉMOIN (`temoin_trace.py`) : même trace, pièce
remplacée par S0 à toutes les phases → 2 048/2 048 (S0, SE) ; donc la sonde 2 est déviée par les débris du germe 1 AVANT la pièce.

## R-150 Après une paire ON/OFF, la ligne a est BLOQUÉE par les débris des deux sources : aucune impulsion de plus n'atteint la pièce — VÉRIFIÉ (src/fourmi, temps fini) — 26/11 nuit
`passe2.py` : une 3e impulsion (germe au-delà des sources, 40 reculs × 41 voies dp ∈ [−20, 20] = 1 640 essais) : 185, 186, 572, 1020 :
0 écriture, 1 640/1 640 pièce intacte et jamais atteinte. Témoins (même tir sans la paire 1) : 10, 20, 7, 15 écritures (voie exacte,
une avancée sur 4). C'est pourquoi la « 2e paire » de 572 (R-143 a) n'efface pas sa ligne : ce n'est pas une paire — la sonde 3 est
déviée SE au pas 10 810 en (111,−79), près de la source 1 ; les bascules suivantes sont faites par des sondes recyclées (`destin2.py`).
Record honnête (une seule simulation, germes sur la ligne) : 1020, 5 impulsions S0 → S1 (5 400) → S0 (9 900) → S1 (52 500) → S0 (61 000)
→ S1 (79 100) (`chaine.py`, S1F=cyclesS1_c2.json ; 572 : 4) ; ligne effacée seulement après la 1re paire (`lignes.py` : 244 cases
après 2 impulsions = débris de la source 1 ; 1 347 à 1 941 ensuite).

## R-152 Écran 2×2 : 4 bascules T dans une seule simulation, 15 images successives (14 changements) — VÉRIFIÉ (2 moteurs, temps fini) — 26/11 nuit
A = 185 (3 impulsions), B = 572 (4), C = 186 (3), D = 1020 (4 premières), pixels à 6 000 cases ; 66 000 pas. Images (A B / C D) :
0000 → 1000 (5 100) → 1001 (5 400) → 1011 (5 800) → 1111 (6 100) → 1011 (8 400) → 0011 (9 100) → 0010 (9 900) → 0000 (12 800) →
1000 (20 900) → 1100 (21 700) → 1000 (24 200) → 1001 (52 500) → 1011 (56 800) → 1010 (61 000). Jamais d'état intermédiaire « ? »
aux pas multiples de 100. Aucun retard calculé (contrairement à R-142). `ordinateur/bascule/ecran4.py`, resultats/bascule/ecran4_*.png.
