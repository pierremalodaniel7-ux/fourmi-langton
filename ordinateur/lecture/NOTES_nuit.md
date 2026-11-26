# Notes de la nuit 26/11 (au fil de l'eau, résumés ; détails dans data/ ignoré par git)

## 1a Lecture en 2 impulsions (bascules 185, 186, 572, 1020)
- `destin2.py` sur les chaînes : 2 impulsions depuis S0 → S0 (4/4), RETOUR EXACT : au pas t* (185 : 14 008 ; 186 : 7 016 / 18 344 ;
  572 : 14 348) la sonde 2 est en R(départ de la sonde 1) et la sonde 1 en R(départ de la sonde 2) ; diff = 56 cases (185).
  Puis 2 autoroutes NO partent des SOURCES (germes retournés). Rien ne sort du côté de la pièce.
- 3 impulsions (écriture W puis lecture R1, R2) → S1 (185, 186, 572, jusqu'à 97 144 pas). Sorties mélangées, dépendantes de l'histoire.
- `balayage_delai.py` (185) : 2e germe reculé de J périodes (J = −3 … 24, 4 avancées) : retour à S0 seulement pour 6/112
  (J ≈ −3…0 et 15…16) ; ailleurs pièce abîmée, ou S1 (sonde 2 déviée SE).
- J ≥ 43 (`balayage_delai.py 40 104`) : 124/256 → S1 gardé et sonde 2 SE ; `rafale.py` : 6 impulsions espacées de 60 périodes,
  les 4 bascules : 1re écrit, les 5 suivantes repartent SE, S1 gardé.
- TÉMOIN (`temoin_trace.py`, 185) : avec la trace de la 1re sonde, pièce S1 : 128/128 (S1, SE) ; même trace mais pièce remplacée par S0
  à toutes les phases : 2048/2048 (S0, SE) ⇒ la sonde 2 est déviée par les débris du germe 1 AVANT la pièce : la sortie ne dépend
  PAS de l'état. Pas de lecture.
- `deux_sur_ligne.py` SANS pièce : 2 germes sur la même ligne (J 55–69, sh 0–3, dp −8…8) : 446/1 020 RETOUR exact
  (le 2e rattrape le 1er, échange, tout repart en arrière) ⇒ la « gomme mutuelle » (R-141) est un phénomène de 2 autoroutes,
  pas de la pièce. Voie exacte (dp = 0) : 480/480 déviées SE par les débris du germe 1.

## 1b Lecture b
- `lecture_b.py` (critère faible ajouté : une phase de chaque état suffit) sur les 4 bascules, 4 rotations : 0 forte, 0 faible
  (S1 n'est jamais une déviation intacte non triviale ; S0 : miroirs SE sur 1–2 voies).
- `rlem.py` (nouvelle chaîne : écriture / effacement / lecture, débris compris, critère anneau) ; témoin 185 : retrouve l'écriture
  et l'effacement connus (S1 période 16, 4 retours). Faux positifs écartés : lecture par la trace (v1), décalages de voie ≤ 4.
- `funcseq.py` / `fonctionnel.py` (fils idéalisés, on garde les débris à ≤ 3 de la pièce) : témoin 185 : 0/35 suites ; la 2e opération
  abîme toujours la pièce (la trace de la 1re autoroute passe à ≤ 3 cases).

## R-147 (candidat) rattrapage SANS pièce — `rattrapage.py` (data/lecture/rattrapage_*.txt)
12 240 situations (J 20–199, sh 0–3, dp −8…8), T = 40 000 : 4 353 RETOUR ; dp pair (même classe) : 0/6 120 ; dp impair : 4 353/6 120.
3 423 : les DEUX sondes en R(départ de l'autre) au même pas t*, grille = départ sauf 28 cases autour de chaque germe (diff = 56).
t* de 4 042 à 39 950 (médiane 22 612). moteur2 identique (exemple J=60, sh=0, dp=−7 : t* = 14 416).
## R-148 (candidat) la paire ON/OFF est un aller-retour exact — `palindrome.py`
185 : t* = 14 008, 56 cases ≠ départ (28 + 28 aux sources, 0 près de la pièce), pièce = pièce du pas 0 (décalage de phase 8/16).
186 : t* = 18 344, idem 56, pièce = pas 0. 572 : t* = 14 348, 64 (8 près de la pièce). 1020 : t* = 15 120, 62 (6 près de la pièce).
## Partie 2 — ligne bloquée — `passe.py` / `passe2.py` (SANS=1 : témoin sans la paire 1)
Après la paire 1, une impulsion de plus sur la ligne (a = recul, dp −20…20, 40 × 41 = 1 640 essais) : 185, 186, 572, 1020 :
0 écriture, 1 640/1 640 pièce intacte non atteinte. Témoins sans la paire 1 : 185 : 10 écritures (dp = 0, une avancée sur 4),
186 : 20, 572 : 7. Dans chaine_2 (572), la sonde 3 est déviée SE à (111,−79) au pas 10 810 (destin2.py) : la « 2e paire » n'en est pas une.
Chaîne 1020 (chaine.py, S1F=cyclesS1_c2.json) : 5 impulsions S0→S1(5 400)→S0(9 900)→S1(52 500)→S0(61 000)→S1(79 100).
Lignes (lignes.py) : 2 imp. 244 cases (base : débris de la source 1) ; 3 : 1 568 ; 4 : 1 347 ; 5 : 1 941.
## Partie 3 — écran 2×2 — `ordinateur/bascule/ecran4.py`
A=185 (3 imp.), B=572 (4), C=186 (3), D=1020 (4), pixels à 6 000 cases, une seule simulation, 66 000 pas : 15 images, 14 changements,
jamais d'état « ? » ; src/fourmi = moteur2 à 66 000. resultats/bascule/ecran4_*.png, ecran4_bande.png.
