# É4 — Transitoires extrêmes (S6, 18-11-2026)

Convention de T(n) : boîte n×n, fourmi en (0,0) au coin, cap haut, cases (i mod n, −⌊i/n⌋) (y vers le bas).
Score = pas où l'autoroute est **certifiée** (`fourmi -cert`), donc DÉMONTRÉE pour la configuration trouvée.

## Méthode
`outils/colline.py N GRAINE MINUTES [n:masque]` : à chaque itération, toutes les inversions d'une case sont évaluées en
un lot ; on prend la meilleure si elle améliore, sinon une marche aléatoire parmi les 5 meilleures (ou, 1 fois sur 5,
une perturbation du meilleur). Graine optionnelle : le record d'une boîte plus petite recopié au coin (même configuration,
même transitoire) ⇒ record(n+1) ≥ record(n).

## Résultats (minorants, sauf n = 3, 4 exacts)
| n | record trouvé | origine | 2ᵉ moteur (`ant une`) |
|---|---|---|---|
| 3 | 51 277 | exhaustif (512) | 51 277 |
| 4 | 133 984 | exhaustif (65 536) | 133 984 |
| 5 | ≥ 209 637 | exhaustif partiel (6 M / 33,5 M) ; la montée de colline seule ne trouve que 136 663 | 209 637 |
| 6, 7 | ≥ 209 637 | recopie du 5×5 (montée de colline : 185 471 au mieux en 6×6 sans graine) | — |
| 8 | **≥ 220 334** | montée de colline depuis le record 5×5 : 4 cases ajoutées (6,−1), (7,−1), (1,−6), (0,−7) | 220 333 (début de période ; certificat 1 pas après) |
| 9, 10 | ≥ 220 334 | recopie du 8×8 (la recherche de 9 min n'a rien amélioré) | — |
Aucune configuration non certifiée rencontrée (0 NONCERT sur toutes les évaluations).
Record 8×8 : `RL|0,0,H|1,0;3,0;0,-1;2,-1;3,-1;6,-1;7,-1;2,-2;4,-2;2,-3;3,-3;4,-3;0,-4;1,-4;1,-6;0,-7` → 220 334.
Graphe : `resultats/records_transitoire.png`.

## Leçons
- La montée de colline est **faible** ici : en 9–12 min elle reste loin du vrai maximum 5×5 (136 663 contre ≥ 209 637).
  Le paysage est très accidenté (une inversion change tout le chaos). Les records viennent surtout de l'exhaustif et de la recopie.
- Le transitoire record croît lentement avec n (≈ 2,1·10⁵ dès n = 5, ≈ 2,2·10⁵ en 8×8 trouvé) — ce n'est qu'un minorant.
- Littérature : le plus proche est l'article MFCS 2026 sur le temps d'échappement (arXiv 2606.26677), non lu (arxiv.org
  inaccessible depuis le conteneur) : rien ne peut être dit « nouveau » ici avant de l'avoir lu.

## Suite
Recherche plus forte (recuit simulé sur plusieurs heures, ou génétique), et surtout finir l'exhaustif 5×5 (É3), qui donnera T(5) exact.

## Mise à jour S8 (R-111)
L'exhaustif 5×5 couvre [0, 9 200 000) : nouveau maximum **252 046** (cases 0,0;1,0;2,0;0,−1;0,−2;2,−2;3,−2;0,−3;1,−3;4,−3;1,−4;2,−4,
masque 6927399), confirmé par `ant une`. Donc record(n) ≥ 252 046 pour n ≥ 5 (recopie au coin), au-dessus du 8×8 trouvé par montée
de colline (220 334) : nouvelle preuve que la recherche locale est faible ici.
