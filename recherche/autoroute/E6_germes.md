# É6 — Germes (S7, 18-11-2026, début)

Question : combien de cases noires faut-il, au minimum, pour que l'autoroute démarre en t pas ? (fourmi en (0,0) ; cap H ou B,
équivalents par rotation ; pas certifié par `fourmi -cert`, donc chaque configuration citée est DÉMONTRÉE.)

| k cases | transitoire minimal | statut | exemple |
|---|---|---|---|
| 0 | 9 977 | exact | grille blanche |
| 1 | 310 | exact dans [−5,5]² | (0,−2), cap H |
| 2 | 162 | exact dans [−5,5]² | (−1,3);(1,3), cap H |
| 3 | 126 | exact dans [−5,5]² (280 840 configurations, **toutes certifiées**) | (0,−2);(1,−3);(3,−5), cap H |
| 4 | ≤ 114 | recherche en faisceau | (0,−2);(1,−3);(2,−1);(3,−5), cap H |
| 5 | ≤ 106 | faisceau | (−1,3);(0,−2);(1,−3);(2,−1);(3,−5), cap H |
| 6 | ≤ 69 | sous-ensemble du germe R-20 | cap B : 0,1;1,2;2,3;2,1;3,0;−2,−1 |
| 7 | ≤ 61 | idem | cap B : 0,1;1,2;2,3;2,1;3,0;2,−2;−2,−1 |
| 8 | ≤ 55 | idem | |
| 9 | ≤ 44 | idem | |
| 10 | ≤ 38 | idem | |
| 11 | **0** | exact (R-20) ; **certifié dès le pas 0 : DÉMONTRÉ** | cap B : 0,1;1,2;2,3;2,2;2,1;2,0;3,0;3,−1;2,−2;1,−2;−2,−1 |

Faits : (1) le bout d'autoroute minimal de R-20 (11 cases) est certifié dès t = 0, donc il construit l'autoroute **pour toujours**
(R-20 ne le vérifiait que sur 60 périodes) ; (2) les 2 048 sous-ensembles de ce germe sont tous certifiés ; (3) toutes les
configurations de 1, 2 ou 3 cases noires dans [−5,5]² (fourmi en (0,0) cap H) sont certifiées (120 + 7 140 + 280 840) : DÉMONTRÉ ;
le plus lent à 3 cases : 161 286. Le germe à 6 cases (69 pas) améliore la recherche locale de R-17 (80 pas).
Graphe : `resultats/germes_transitoire_min.png`. Suite d'É6 : dynamique inverse depuis l'autoroute (bassin à rebours).
