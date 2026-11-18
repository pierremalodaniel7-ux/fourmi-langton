# É2 — Collisions et configurations éparses (S1, 18-11-2026) — 1re étape : UNE case noire

## Théorème T1 (une case noire n'importe où)
Fourmi RL en (0,0), cap H, grille blanche sauf **une** case noire c ∈ ℤ² quelconque.
Alors la fourmi construit l'autoroute 104 pour toujours.

Statut : **DÉMONTRÉ** pour (A) et (B) ; (C) **DÉMONTRÉ, preuve esquissée À RELIRE** (lemme de translation) ;
vérifié par calcul exact + certificat pour 90 601 + 3 311 + 2 222 positions.

### (A) c ∈ [−150,150]² : calcul exhaustif
90 601 configurations, toutes **certifiées** (`fourmi -cert`, lemme R-70). Temps de calcul : ≈ 100 s sur 2 cœurs.
- 87 760 certifiées dès 9 977 (la case ne gêne pas), 2 841 autres.
- Plus court : c = (0,−2), autoroute certifiée dès **310** pas ; puis (1,3) : 313.
- Plus long : c = **(7,−7)**, certifiée seulement à **106 258** (≈ 10,6 × le départ blanc).
- Histogramme du pas certifié : [2⁸,2⁹) 6 · [2⁹,2¹⁰) 14 · [2¹⁰,2¹¹) 62 · [2¹¹,2¹²) 110 · [2¹²,2¹³) 265 ·
  [2¹³,2¹⁴) 89 057 · [2¹⁴,2¹⁵) 936 · [2¹⁵,2¹⁶) 88 · [2¹⁶,2¹⁷) 63.

### (B) c hors de la boîte et hors de la bande : rien ne change
Avant 9 977, la fourmi (départ blanc) ne visite que x ∈ [−19,29], y ∈ [−22,22]. Si c est hors de [−150,150]²,
l'évolution jusqu'à 9 977 est celle du départ blanc ; les conditions F1–F4 du certificat ne lisent que des cases
proches de la fourmi, et la condition Z ne lit c que si c est dans la bande Z de l'autoroute (diagonale
x + y = j, j ∈ [−28,−18], vers (−2,+2) en y vers le bas). Hors de cette bande : certifié à 9 977. ∎

### (C) c loin dans la bande : 22 classes, lemme de translation
Loin, les cases de la bande sont c = (j−k, k), j ∈ [−28,−18], k grand ; une période de l'autoroute décale de
d = (−2,+2), donc c et c+d ont la même issue décalée de 104 pas : **22 classes** (j, parité de k) = les 22
collisions de R-16. Mesures (toutes certifiées) : k = 100…400 pas à pas (3 311) et k = 150…1 150 tous les 10 (2 222) :
le pas certifié vaut exactement **cert(k₀) + 52 (k − k₀)** pour 21 classes (même chaos, retardé), et
**+ 104 (k − k₀)** pour la classe du **demi-tour** (j = −19, k pair) : l'autoroute repart sur sa propre trace,
revient au germe de départ, y refait du chaos et repart à 90° (direction (−2,−2)). Direction finale constante dans
chaque classe.

**Lemme de translation (esquisse, À RELIRE).** Soit X_k la configuration avec c = (j−k,k). Pour t ≥ 9 977
avant l'impact, X_{k+2} au temps t+104 coïncide avec X_k au temps t translatée de d, sauf dans une zone fixe
G près du germe (la trace entre les deux est périodique). Après l'impact, les deux évolutions restent égales
(translatées) tant que la fourmi ne lit pas G ; et la bande Z du certificat final ne rencontre pas G. Pour les
21 classes sans demi-tour, tout se passe à une distance de G qui croît avec k (la fourmi reste du côté de
l'impact, la nouvelle autoroute part à 90° ou tout droit) : une vérification à k₀ suffit, par récurrence sur k.
Pour le demi-tour, la fourmi revient sur la trace (périodique) jusqu'à G : l'arrivée au germe est la même pour
tout k (décalée de 2 × 52 pas par unité de k), puis l'autoroute finale part à 90°, loin de la case c.
Ce qui reste à écrire proprement : la zone G exacte et la vérification « la fourmi ne lit pas G » à k₀ = 100.

## Ce que ça apprend sur les collisions (R-16 relu)
- 21 issues sur 22 partent en **terrain neuf** : l'autoroute qui sort est certifiable aussitôt.
- 1 issue (demi-tour) part **sur la trace** : non certifiable tant qu'elle roule dessus ; dans un monde fini,
  elle revient forcément au début de la trace (germe ou collision précédente). C'est le seul mécanisme qui
  ramène la fourmi en arrière : **c'est l'obstacle principal pour un théorème « épars » à plusieurs îlots**.

## Suite (É2, séances suivantes)
1. Écrire G et vérifier « la fourmi ne lit pas G » (rend (C) complet).
2. Deux cases noires loin l'une de l'autre et de l'origine : automate fini des « sites » (germe, 22 types de
   collision), transitions = demi-tour qui revient à un site ; montrer qu'il n'y a pas de ping-pong infini.
3. Îlots de 2 cases (R-24, 1 683 paires) puis rayon ≤ 2.

Commandes : `data/c1.in` (généré par python, voir journal R-72) ; `fourmi -T 8000000 -cert -lot < c1.in` ;
classes loin : `far.in`, `gap.in`.
