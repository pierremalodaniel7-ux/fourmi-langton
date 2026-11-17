# Ordinateur à fourmis — additionneur 4 bits (R-39)

Germe : `germe_ordinateur.json` (dossier « Ordinateur », réglé sur **3 + 2**). Règle RL, y vers le bas,
8 fourmis jouées dans l'ordre : S0, K0, S1, K1, S2, K2, S3, K3 (fourmi 1 = S0 … fourmi 8 = K3).
Module m = additionneur complet : S_m calcule le bit de somme, K_m la retenue. La retenue part de K_m
en autoroute ↗ et traverse les lecteurs S_(m+1), K_(m+1). Les 4 modules sont la même copie, décalée de
(1311, −1091) ; les germes des fourmis sont reculés de 950 périodes par module (retard de la retenue).

## Entrer a et b (a = a0 + 2a1 + 4a2 + 8a3, idem b)
Partir des cases « fixes » (`entrees.json`, clé `fixes`), puis pour chaque module m :

| m | si a_m = 1 : noircir | si b_m = 1 : noircir | si b_m = 0 : noircir |
|---|---|---|---|
| 0 | 57,-30 ; 35,14 ; 359,-329 ; 376,-304 | 84,-7 ; 18,-11 ; 27,22 ; 59,40 ; 384,-296 | 385,-353 |
| 1 | 1368,-1121 ; 1346,-1077 ; 1670,-1420 ; 1687,-1395 | 1395,-1098 ; 1329,-1102 ; 1338,-1069 ; 1370,-1051 ; 1695,-1387 | 1696,-1444 |
| 2 | 2679,-2212 ; 2657,-2168 ; 2981,-2511 ; 2998,-2486 | 2706,-2189 ; 2640,-2193 ; 2649,-2160 ; 2681,-2142 ; 3006,-2478 | 3007,-2535 |
| 3 | 3990,-3303 ; 3968,-3259 ; 4292,-3602 ; 4309,-3577 | 4017,-3280 ; 3951,-3284 ; 3960,-3251 ; 3992,-3233 ; 4317,-3569 | 4318,-3626 |

Attention : b_m = 0 demande UNE case noire (la dernière colonne), b_m = 1 en demande cinq.
Pour passer de 3+2 au calcul voulu : enlever/ajouter les cases des lignes concernées.

## Lire le résultat
| fourmi | pas de lecture | lecture |
|---|---|---|
| S0 (n°1) | 95 000 | ↘ = 0, ↙ = 1 → bit 0 |
| S1 (n°3) | 193 800 | ↘ = 0, ↙ = 1 → bit 1 |
| S2 (n°5) | 292 600 | ↘ = 0, ↙ = 1 → bit 2 |
| S3 (n°7) | 391 400 | ↘ = 0, ↙ = 1 → bit 3 |
| K3 (n°8) | 411 400 | ↗ = 1, ↘ = 0 → bit 4 (retenue finale) |

Exemple 3 + 2 = 5 = 00101 : S0 ↙, S1 ↘, S2 ↙, S3 ↘, K3 ↘.
À l'œil après la fin : la trace qui sort du module m vers le bas part ↙ (1) ou ↘ (0) ; plus tard une
sortie ↙ peut heurter les traces des modules précédents (loin du module), c'est pourquoi la lecture
exacte se fait au pas indiqué. Laisser tourner au moins 420 000 pas. Vue : `vue_3plus2.png`.

Version 2 bits : ne garder que les modules 0 et 1 (fourmis 1 à 4) ; lire S0, S1, puis K1 au pas 213 800.

## Vérification
`python3 chaine.py 4 436400 95000` (256 entrées, moteur C) ; `node verif_independante.js tout`
(2e programme, JavaScript, grille à blocs, 256 entrées). Les deux : 0 échec.
