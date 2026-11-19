# É6 — Germes (S7, 18-11-2026, début)

Question : combien de cases noires faut-il, au minimum, pour que l'autoroute démarre en t pas ? (fourmi en (0,0) ; cap H ou B,
équivalents par rotation ; pas certifié par `fourmi -cert`, donc chaque configuration citée est DÉMONTRÉE.)

| k cases | transitoire minimal | statut | exemple |
|---|---|---|---|
| 0 | 9 977 | exact | grille blanche |
| 1 | 310 | exact dans [−5,5]² | (0,−2), cap H |
| 2 | 162 | exact dans [−5,5]² | (−1,3);(1,3), cap H |
| 3 | 126 | exact dans [−5,5]² (280 840 configurations, **toutes certifiées**) | (0,−2);(1,−3);(3,−5), cap H |
| 4 | 67 | exact dans [−4,4]² (1 581 580 configurations, **toutes certifiées**, S8) | (−4,−1);(−2,1);(−1,2);(0,3), cap H |
| 5 | ≤ 62 ; exact 62 dans [−3,3]² (1 712 304 configurations, **toutes certifiées**, S8) | | (−3,1);(−2,0);(−1,−1);(−1,1);(1,−3), cap H |
| 6 | ≤ 69 ; dans [−2,2]² : exact 120 (134 596 configurations, **toutes certifiées**, S9) | sous-ensemble du germe R-20 | cap B : 0,1;1,2;2,3;2,1;3,0;−2,−1 |
| 7 | ≤ 61 ; dans [−2,2]² : exact 68 (346 104 configurations, **toutes certifiées**, S9) | idem | cap B : 0,1;1,2;2,3;2,1;3,0;2,−2;−2,−1 |
| 8 | ≤ 55 ; dans [−2,2]² : exact 64 (735 471 configurations, **toutes certifiées**, S9) | idem | |
| 9 | ≤ 44 ; dans [−2,2]² : exact 56 (1 307 504 configurations, **toutes certifiées**, S9) | idem | |
| 10 | ≤ 38 | idem | |
| 11 | **0** | exact (R-20) ; **certifié dès le pas 0 : DÉMONTRÉ** | cap B : 0,1;1,2;2,3;2,2;2,1;2,0;3,0;3,−1;2,−2;1,−2;−2,−1 |

Faits : (1) le bout d'autoroute minimal de R-20 (11 cases) est certifié dès t = 0, donc il construit l'autoroute **pour toujours**
(R-20 ne le vérifiait que sur 60 périodes) ; (2) les 2 048 sous-ensembles de ce germe sont tous certifiés ; (3) toutes les
configurations de 1, 2 ou 3 cases noires dans [−5,5]² (fourmi en (0,0) cap H) sont certifiées (120 + 7 140 + 280 840) : DÉMONTRÉ ;
le plus lent à 3 cases : 161 286. Le germe à 6 cases (69 pas) améliore la recherche locale de R-17 (80 pas).
Graphe : `resultats/germes_transitoire_min.png`. Suite d'É6 : dynamique inverse depuis l'autoroute (bassin à rebours).

## Dynamique inverse (R-106)
`outils/rebours.py` : pas inverse exact (contrôlé par aller-retour de 2 000 pas). Résultats :
- passé du départ blanc : autoroute « à rebours » dès 10 081 pas en arrière (= 9 977 + 104), dérive (2,−2) ;
- passé du germe minimal de R-20 : 4 426 pas de chaos à rebours puis une autoroute à rebours. Lu dans le bon sens : une autoroute
  qui arrive de l'infini (la fourmi « mange » une trace déjà construite), 4 426 pas de chaos, puis l'autoroute pour toujours ;
- 200 boîtes 3×3, 4×4, 5×5 aléatoires : toutes ont une autoroute à rebours (en 300 000 pas), transitoire à rebours médian 2 277,
  max 42 084 — très proche des transitoires directs (médiane ≈ 2 300).
Piste : la dynamique inverse est probablement conjuguée à la dynamique directe par une symétrie (réflexion / déplacement de la
fourmi sur les arêtes) — sans doute connu (réversibilité, Gale–Propp–Sutherland–Troubetzkoy) ; à vérifier avant d'aller plus loin.

## S8 : germes exacts à 4 et 5 cases (R-108, R-110)
Toutes les configurations de 4 cases dans [−4,4]² (1 581 580, max 149 266) et de 5 cases dans [−3,3]² (1 712 304, max 186 217)
construisent l'autoroute pour toujours (certificat). Transitoires minimaux exacts dans ces boîtes : 67 (4 cases), 62 (5 cases).
Avec R-105 : toute configuration de ≤ 3 cases dans [−5,5]², ≤ 4 dans [−4,4]², ≤ 5 dans [−3,3]² est DÉMONTRÉE.

## S9 : carré [−2,2]² (R-114)
Toutes les configurations de 6 et 7 cases dans [−2,2]² (fourmi 0,0,H) sont certifiées ; minima 120 et 68, maxima 105 789 et
167 636. Outil : `outils/germes_k.sh K R [DEBUT FIN]`. 8 cases : voir R-114 (suite) dans le journal.
