# É2 — Collisions et configurations éparses (S1, 18-11-2026) — 1re étape : UNE case noire

## Théorème T1 (une case noire n'importe où)
Fourmi RL en (0,0), cap H, grille blanche sauf **une** case noire c ∈ ℤ² quelconque.
Alors la fourmi construit l'autoroute 104 pour toujours.

Statut : **DÉMONTRÉ** pour (A), (B) et (C) sauf UNE classe de positions lointaines (le « demi-tour » :
c = (−19−k, k), k pair ≥ 100), qui reste **OBSERVÉE** (k ≤ 1 150, toutes certifiées) ; preuve prévue ci-dessous.
Calcul exact + certificat pour 90 601 + 3 311 + 2 222 positions.

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

**Lemme de translation (21 classes : DÉMONTRÉ).** Notations (y vers le bas) : d = (−2,+2), p(x,y) = −x + y
(p(d) = 4), B(t) = départ blanc, X_k = départ blanc + case c_k = (j−k, k).
1. Comme B est certifié dès 9 977, a_B(t+104) = a_B(t) + d pour t ≥ 9 977. L'ensemble
   D = {e : B(t+104)(e) ≠ B(t)(e−d)} ne dépend donc pas de t ≥ 9 977 (les deux configurations basculent la même
   case à chaque pas). D ⊂ A₁ ∪ (A₀+d) (A₀, A₁ = cases touchées avant 9 977, 10 081) ⇒ **p ≤ 25 sur D**.
2. Avant l'impact, X_k(t) = B(t) + {c_k} ; donc X_{k+2}(t+104) et X_k(t) translatée de d ne diffèrent que sur D.
3. Couplage : tant que la fourmi de X_k (translatée de d) ne lit pas de case de D, X_{k+2}(t+104) = X_k(t) + d
   hors de D (récurrence pas à pas : même case lue, même couleur, même bascule). Si en plus la bande Z_k du
   certificat translatée de d évite D, X_{k+2} est certifiée à cert_k + 104 avec la même direction.
4. Condition suffisante, stable par récurrence (p augmente de 4 à chaque translation) : **min p sur les positions
   de la fourmi de X_{k₀} entre l'impact et cert + 104 > 25 − 4**, et la direction finale d' a p(d') ≥ 0
   (alors toute la bande Z a p ≥ ce min). Elle se vérifie une fois, à k₀ = 100 et 101, et vaut alors pour tout k ≥ k₀.
5. Vérification (`./ant pmin J K T`, 2ᵉ moteur) : pour les 21 classes, min p entre **157 et 225** > 21 : **OK**.
   Directions finales (2,2), (−2,−2), (−2,2) : p(d') ∈ {0, 0, 4} ≥ 0. ∎
   Classe du demi-tour (−19, k pair) : min p = −39 (la fourmi revient au germe) : ce couplage ne suffit pas.

**Demi-tour : plan de preuve (séance suivante).** (a) Lemme du certificat « sur fond périodique, horizon fini » :
mêmes F1, F2, F4, et à la place de F3/Z, « pour 1 ≤ k ≤ K et v ∈ V avec v+d ∉ V : C(a+kd+v) = Pv(v) » ⇒ la
fourmi recopie sa période K fois (même récurrence). La trace de B est périodique (certificat R-70), donc la
fourmi qui fait demi-tour roule dessus jusqu'au germe. (b) Deuxième couplage, sans translation, entre
X_{k+2} au temps s+208 et X_k au temps s (même position du « rouleur » au milieu de la trace) : ils ne
diffèrent que près du site d'impact (p grand) ; vérifier à k₀ = 100 que la suite (germe, chaos, autoroute
(−2,−2)) reste à p plus petit.

## Ce que ça apprend sur les collisions (R-16 relu)
- 21 issues sur 22 partent en **terrain neuf** : l'autoroute qui sort est certifiable aussitôt.
- 1 issue (demi-tour) part **sur la trace** : non certifiable tant qu'elle roule dessus ; dans un monde fini,
  elle revient forcément au début de la trace (germe ou collision précédente). C'est le seul mécanisme qui
  ramène la fourmi en arrière : **c'est l'obstacle principal pour un théorème « épars » à plusieurs îlots**.

## Suite (É2, séances suivantes)
1. Demi-tour : lemme « fond périodique, horizon fini » + 2ᵉ couplage (rend T1 complet).
2. Deux cases noires loin l'une de l'autre et de l'origine : automate fini des « sites » (germe, 22 types de
   collision), transitions = demi-tour qui revient à un site ; montrer qu'il n'y a pas de ping-pong infini.
3. Îlots de 2 cases (R-24, 1 683 paires) puis rayon ≤ 2.

Commandes : `data/c1.in` (généré par python, voir journal R-72) ; `fourmi -T 8000000 -cert -lot < c1.in` ;
classes loin : `far.in`, `gap.in`.
