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
