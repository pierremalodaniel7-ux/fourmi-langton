# É2 — Collisions et configurations éparses (S1, 18-11-2026) — 1re étape : UNE case noire

## Théorème T1 (une case noire n'importe où)
Fourmi RL en (0,0), cap H, grille blanche sauf **une** case noire c ∈ ℤ² quelconque.
Alors la fourmi construit l'autoroute 104 pour toujours.

Statut : **DÉMONTRÉ** (calcul exact fini + lemmes écrits ci-dessous ; preuve à faire relire par un humain).
Les 22 classes lointaines sont traitées : 21 par translation, le demi-tour par double couplage.
Calcul exact + certificat pour 90 601 + 3 311 + 2 222 positions.

### (A) c ∈ [−150,150]² : calcul exhaustif
90 601 configurations, toutes **certifiées** (`fourmi -cert`, lemme R-83). Temps de calcul : ≈ 100 s sur 2 cœurs.
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

**Demi-tour (classe j = −19, k pair) : double couplage — DÉMONTRÉ.** p = −x+y, d = (−2,+2), D comme ci-dessus (p ≤ 25).
Dans X_k, après l'impact la fourmi repart en arrière (dérive −d) en roulant sur sa trace : le « rouleur ».
Soit s un instant où le rouleur est au milieu de la trace, W la fenêtre lue pendant [s, s+104), L = min p de la
fourmi sur [impact, s). Conditions finies vérifiées à k₀ = 100 (`./ant uturn -19 100 150 79678`) :
- **U1** p > 21 sur [impact, s+104] (le couplage par translation de l'étape 3 tient jusqu'à s+104) : min 146 ;
- **U2** a(s+104) = a(s) − d, même cap, et le contenu de la fenêtre se recopie : X(s+104) sur a(s)−d+W = X(s) sur a(s)+W (|W| = 41) ;
- **U3** min p sur [s, s+104] ≥ L − 4 : 147 ≥ 147 ;
- **U4** après s+104, toute case lue pour la première fois depuis s est dans {p < L} (2 542 lectures) ; et la bande Z de
  l'autoroute finale (−2,−2) (p(d') = 0) est dans {p < L} : max p = −7 < 151.

Preuve. Par U1 et le couplage par translation, X_{k+2}(s+208) = X_k(s+104) + d hors de D ; avec U2 le rouleur de
X_{k+2} est en a(s) au temps s+208, même cap, et la fenêtre a(s)+W y a le même contenu que dans X_k(s).
Les cases de {p < L} n'ont été touchées, dans X_k avant s et dans X_{k+2} avant s+208, que par l'autoroute de
départ blanc (U3 : les positions translatées restent à p ≥ L) : elles sont identiques. Par U4, à partir de là
les deux fourmis lisent les mêmes couleurs : X_{k+2} refait exactement X_k, décalée de 208 pas, **sans translation**,
jusqu'au certificat (dont la bande Z est dans {p < L}). Les conditions U1–U4 se transmettent de k à k+2
(L ne diminue pas, mêmes lectures), d'où tout k pair ≥ 100. Prédiction cert(k+2) = cert(k) + 208 : vérifiée
(79 678, 79 886, 80 094 pour k = 100, 102, 104, et pente 104 par unité de k jusqu'à 1 150). ∎
Robustesse : U1–U4 passent aussi pour s pris à p* = 120, 90, 70.

## Ce que ça apprend sur les collisions (R-16 relu)
- 21 issues sur 22 partent en **terrain neuf** : l'autoroute qui sort est certifiable aussitôt.
- 1 issue (demi-tour) part **sur la trace** : non certifiable tant qu'elle roule dessus ; dans un monde fini,
  elle revient forcément au début de la trace (germe ou collision précédente). C'est le seul mécanisme qui
  ramène la fourmi en arrière : **c'est l'obstacle principal pour un théorème « épars » à plusieurs îlots**.

## Suite (É2, séances suivantes)
1. Faire relire T1 (A, B, C) par un humain ; l'écrire en note courte.
2. Deux cases noires loin l'une de l'autre et de l'origine : automate fini des « sites » (germe, 22 types de
   collision), transitions = demi-tour qui revient à un site ; montrer qu'il n'y a pas de ping-pong infini.
3. Îlots de 2 cases (R-24, 1 683 paires) puis rayon ≤ 2.

Commandes : `data/c1.in` (généré par python, voir journal R-85) ; `fourmi -T 8000000 -cert -lot < c1.in` ;
classes loin : `far.in`, `gap.in`.

## Deux cases loin (S1, 1re exploration) — OBSERVÉ (chaque configuration calculée est DÉMONTRÉE individuellement)
1re case : les 22 classes à k = 100/101 ; 2e case : 122 positions (décalage −30…30, deux parités) à 200 cases
devant la nouvelle autoroute. **2 684/2 684 certifiées** (`data/two.in`, `fourmi -T 30000000 -cert`, < 30 s).
Chaque nouvelle autoroute a aussi exactement 22 cases « touchables » (484 doubles collisions). Retard maximal dû
à la 2e case : 198 026 pas (1re case −119,100 = le demi-tour, puis demi-tour au 2e site). Aucun « ping-pong »
infini dans ces 484 cas. Prochaine étape : écrire l'automate des sites (germe + 22 types) et ses transitions
par demi-tour, et le démontrer avec les mêmes couplages.

## Théorème T2 : un îlot de 2 cases voisines (côté ou coin), n'importe où — DÉMONTRÉ (à faire relire)
Fourmi (0,0) cap H + deux cases noires {c, c+e}, e ∈ {(1,0),(0,1),(1,1),(1,−1)}, c quelconque.
- (A) c ∈ [−150,150]² : **362 404/362 404 certifiées** (≈ 5 min sur 2 cœurs). Plus court : {(−2,−1),(−1,0)}
  certifié dès **197** ; plus long : {(−29,11),(−29,12)} à **117 736**. 350 203 certifiées dès 9 977.
- (B) hors boîte et hors bande : comme T1.
- (C) loin dans la bande : 4 × 16 × 2 = **128 classes** (orientation, j ∈ [−31,−16], parité de k), mesurées pour
  k = 100…300 pas à pas (12 864 calculs) : toutes exactement affines, une seule direction par classe :
  32 non touchées (pente 0), 91 « translation » (pente 52), **5 demi-tours** (pente 104).
  Preuves à k₀ = 100/101 (`recherche/autoroute/outils/preuves_dominos.txt`, à passer à `./ant`) :
  91/91 `pmin` OK (min p entre 117 et 226 > 21) ; 5/5 `uturn` : U1–U4 OK.
  Condition en plus, trouvée ici : 3 des 5 demi-tours repartent ensuite dans la direction d'origine d (p(d') = 4 > 0) ;
  la bande finale monte alors en p et pourrait croiser le site d'impact. Mais d conserve x+y : les cases où X_k et
  X_{k+2} diffèrent sont sur les diagonales x+y du site, et la bande finale est sur d'autres diagonales
  (ex. site [0,38], bande [−42,−32]) : **disjointes** dans les 3 cas. (Pour T1, direction finale (−2,−2), p(d') = 0 : inutile.)

## Chaîne de demi-tours (S1) — OBSERVÉ (chaque configuration DÉMONTRÉE individuellement)
`outils/chaine_demitours.py 5 150` : à chaque étape, nouvelle case dans la classe demi-tour de l'autoroute finale
(repérée par la pente 208 entre k et k+2), à 150 cases au-delà de la position finale. La classe demi-tour est
**unique** à chaque étape. Résultats (pas certifié, direction finale, y vers le bas) :
| étape | cases | certifiée dès | direction |
|---|---|---|---|
| 0 | — | 9 977 | (−2,2) |
| 1 | (−287,268) | 97 150 | (−2,−2) |
| 2 | + (−827,−835) | 255 032 | (2,2) |
| 3 | + (5372,5378) | 907 088 | (−2,−2) |
| 4 | + (−23866,−23902) | 3 361 062 | (2,2) |
Chaque demi-tour ramène la fourmi au site précédent, qui la renvoie dans une direction neuve : pas de ping-pong
infini jusqu'à 4 niveaux. Étape 5 arrêtée (trop longue pour la séance). Piste pour l'automate des sites.

## Théorème T3 : îlot de 3 cases en L (4 orientations) ou en ligne (2 orientations), n'importe où — DÉMONTRÉ (à faire relire)
- (A) Boîte réduite : (B) ne demande que « îlot hors de [−60,60]² et hors de la bande », donc (A) = positions dans
  [−100,100]² ∪ bande x+y ∈ [−36,−11], y ≤ 100 : **246 072/246 072 certifiées** (≈ 4 min, 2 cœurs).
  Plus rapide : ligne {(−1,3),(0,3),(1,3)} dès **158** ; plus lent : L {(11,10),(12,10),(11,11)} à **93 138**.
- (C) 228 classes lointaines (k = 100…160, 6 954 calculs), toutes exactement affines : 76 non touchées,
  148 translations (`pmin` 148/148 OK), **4 demi-tours** (`uturn` OK avec s pris à p* = 90 : à p* ≥ 120 la fourmi
  n'est pas encore « rouleuse » pour l'un d'eux et U2/U4 échouent — choisir s quand le rouleur est formé).
  Directions finales des demi-tours : trois fois d (diagonales x+y disjointes du site : OK), une fois −d
  (repart vers le germe sur une autre diagonale ; p décroît le long de Z, donc Z ⊂ {p < L} : OK).
- Commandes : `data/tri.in`, `data/trifar.in` (python, voir journal R-78), `outils/preuves_loin.py trifar.cert`,
  `outils/preuves_trominos.txt` (à passer à `./ant`).

## S2 — Raffinement de la condition U4 et de Z (diagonales Δ)
Les cases où X_k(s) et X_{k+2}(s+208) diffèrent sont parmi les cases touchées après 9 977 (dans l'un ou l'autre
monde) et les cases de l'îlot. Comme d conserve x+y, toutes sont sur les diagonales
**Δ = {x+y des positions de X_k sur [9 977, s+104]} ∪ {x+y des cases de l'îlot}**. Donc :
- **U4'** : une case lue pour la première fois depuis s (après s+104) est sûre si p < L, ou si elle est dans la fenêtre W,
  ou si sa diagonale n'est pas dans Δ (elle est blanche dans les deux mondes).
- **Z** selon la direction finale d' : d' = +d (p croît) ⇒ toutes les diagonales de la fenêtre finale hors de Δ ;
  d' = −d ou perpendiculaire (p ne croît pas) ⇒ max p de la fenêtre finale < L.
- En S1, le test « diagonales disjointes » ne regardait que le site, pas la trace : les 10 demi-tours de T1–T3 ont été
  **revérifiés en S2 avec Δ complet : 10/10 OK** (`outils/juge_uturn.py`, `outils/cherche_s.sh`).
- Le choix de s (seuil p*) fait partie de la preuve : `cherche_s.sh` essaie p* ∈ {90, 70, 50, 110, …, 210} et garde le
  premier qui passe (le rouleur doit être formé : U2).

## S2 — Classes « aller-retour » (pente 156 et 208) : diagnostic
Exemple : îlot {(−120,101),(−118,102),(−118,103)} (classe j = −19, k impair, cases (0,0),(2,1),(2,2)).
Trace de p = −x+y : impact vers 15 000 (p ≈ 200), chaos au site jusqu'à ≈ 47 000, rouleur vers le germe (p → −36 à
57 000), le germe le **renvoie** le long de la trace (p → 242 à 67 000), nouveau chaos au site, puis autoroute à 90°
(p ≈ 160 constant). Trois traversées de la trace : pente 3 × 52 = 156. Pente 208 : quatre traversées.
Preuve à faire (« triple couplage ») : translation (site) → identité (germe) → translation (site). Le mode
`./ant triple J K CE P1 T1 P2 T2 L …` vérifie C1–C7 mais **échoue** : au 2ᵉ changement de repère, le rouleur qui
revient relit le sillage du premier rouleur, qui n'est dans aucun ensemble d'accord prouvé. Il manque le lemme
« **rouleur sur fond périodique** » : un rouleur périodique laisse un sillage invariant par translation de d, ce
qui donne l'accord sur tout le sillage. C'est la prochaine pièce à écrire ; elle servira aussi à l'automate des sites
(le germe est un site qui renvoie ou dévie les rouleurs).
**Piste précise pour S3 (triple couplage).** Ensemble d'accord au 1er changement de repère (X_k(s1) contre
X_{k+2}(s1+208)) : en plus de {p < L}, W1 et « hors Δ », toute case c ∉ D telle que
(i) c−d n'est pas touchée par X_k sur [s1, s1+104) et (ii) X_k(s1)(c−d) = X_k(s1)(c).
Justification : X_{k+2}(s1+208)(c) = X_k(s1+104)(c−d) (couplage par translation jusqu'à s1+104) = X_k(s1)(c−d) (i) = X_k(s1)(c) (ii).
Pour la récurrence k → k+2, exiger la **fermeture par chaînes** : si c entre par cette règle, c−d doit être dans
l'ensemble (règle ou base) ; la chaîne c, c−d, c−2d… descend en p de 4 par pas et finit dans {p < L}.
Même règle (avec +d) au 2ᵉ changement de repère. Tout se vérifie sur X_{k₀} seul. À coder dans `ant triple`.

## S2 — Triple couplage (classes de pente 156) : vérificateur `ant triple2` — DÉMONTRÉ sous réserve de relecture
Trois repères successifs entre X_k et X_{k+2} : translation d, décalage 104 (site) → identité, décalage 208 (germe)
→ translation d, décalage 312 (site). s1 = 1er instant après l'impact où p ≤ P1 (rouleur vers le germe) ; s2 = 1er
instant, après passage au germe (p ≤ 25), où p ≥ P2 (rouleur qui revient).
Ensembles d'accord (tous vérifiés sur X_{k₀} seul) :
- **S_G** (au temps s1) : p < L, ou fenêtre W1, ou diagonale hors Δ1, ou règle « un pas » : c ∉ D, c−d non touchée sur
  [s1, s1+104), X(s1)(c−d) = X(s1)(c), et c−d ∈ S_G (fermeture par chaîne, la chaîne descend en p jusqu'à p < L).
- **S_A2** (au temps s2) : p > Hm (Hm = max p sur [s1, s2+104]), ou fenêtre W2, ou diagonale hors Δ2, ou règle
  « un pas » vers +d : X(s2)(c+d) = X(s2)(c), c+d non touchée sur [s2, s2+104), c et c+d dans S_G ∪ {touchées sur [s1, s2]},
  et c+d ∈ S_A2 (chaîne montante jusqu'à p > Hm).
Conditions : C1 p > 21 jusqu'à s1+104 ; C2 rouleur 1 périodique (−d, même cap, fenêtre recopiée) ; C3 L ≤ min p ;
C4 lectures neuves sur [s1+104, s2+208] dans S_G ; C5 rouleur 2 périodique (+d) ; C7 lectures neuves après s2+104
dans S_A2 ; Z selon la direction finale (perpendiculaire ou +d : min p > Hm ; −d : diagonales hors Δ2).
Récurrence k → k+2 : les ensembles sont fermés par +d (base p, Δ, chaînes), et S_G(k+2) ⊇ S_G(k), S_A2(k+2) ⊇ S_A2(k)
car ils s'évaluent sur des cases où les deux mondes coïncident. Prédiction : cert(k+2) = cert(k) + 312 (pente 156) : vérifiée.
Résultat : **42/42 classes de pente 156 OK** (base k₀ = 200/201 ; k = 100…199 certifiés un par un).
Contrôle négatif : les **3 classes de pente 208** (quatre traversées) **échouent** (C7), comme attendu.
Commandes : `outils/cherche_triple.sh`, liste et paramètres dans `outils/preuves_ilots_3x3_triple.txt`.

## S2 — Vérificateur général `ant multi` (n changements de repère)
`./ant multi J K CE NS P1 … PNS offsets` : repères alternés (impair : identité vers le germe, décalage 104·(i+1) ;
pair : translation d vers le site), ensembles d'accord définis récursivement (base p < L_i ∩ accord de la phase i−2,
ou p > H_i ∩ accord de la phase i−2 ; fenêtre ; hors Δ_i ; règle « un pas » avec fermeture par chaînes, voisins
dans l'accord de la phase i−1 ou touchés pendant celle-ci). Cohérence : NS = 1 redonne les 423 demi-tours OK de
`uturn` (p* = 90) ; NS = 2 redonne les 42/42 de `triple2`. **NS = 3 : les 3 classes de pente 208 OK**
(`outils/preuves_ilots_3x3_pente208.txt`). Statut : DÉMONTRÉ **sous réserve de relecture du vérificateur** (code neuf).

## Théorème T4 : tout îlot contenu dans un carré 3×3, n'importe où — DÉMONTRÉ (sous réserve de relecture) — S2
Fourmi (0,0) cap H + un îlot I = P + t, P l'une des **400 formes** non vides de [0,2]² (à translation près), t quelconque.
- (B) Si I ne touche ni [−24,32]×[−25,25] (la fourmi blanche ne visite que [−21,29]×[−22,22] avant 10 185) ni la
  bande Z (diagonales x+y ∈ [−28,−18]) : certifié à 9 977 (argument de T1).
- (A) I touche la boîte, ou la bande avec y ≤ 100 : **1 813 428/1 813 428 certifiées** (≈ 36 min sur 2 cœurs).
  Plus rapide : {(−1,−3),(0,−3),(1,−3),(−1,−2),(−1,−1),(0,−1)} dès **142** ; plus lent : {(−56,28),(−54,28),(−54,30)} à **228 739**.
- Trou repéré en S2 (aussi présent dans T3 de S1) : 1re case à y = 99 dont seule une case à y = 101 touche la bande.
  Comblé par le calcul direct des ancres k = 90…99 : **76 000/76 000 certifiées**.
- (C) Classes lointaines (forme, j ∈ [−32,−14], parité de k) : 15 200 classes, k = 100…105 (45 600 calculs, tous certifiés).
  4 032 non touchées ; 10 678 « translation » : 10 673 `pmin` OK à k₀ = 100/101 ; 434 demi-tours : 433 OK
  (`uturn`, p* choisi par `cherche_s.sh`) ; restent 62 classes (5 `pmin` en échec, 1 demi-tour, 11 irrégulières à
  k ≤ 105, 42 de pente 156, 3 de pente 208) : **toutes calculées pour chaque k de 100 à 600 (15 530, certifiées)**,
  régulières dès k ≤ 120 ; preuves à la base k₀ = 200/201 : 12 `pmin` + 5 `uturn` OK, 42 `triple2` OK, 3 `multi` NS = 3 OK.

## S2 — Première relecture de `ant multi` (fin de séance)
Points vérifiés : bornes L_i (min sur [s_{i−1}, s_i) et min sur [s_i, s_i+104] + 4), H_i (max sur [s_{i−1}, s_i+104]) ;
fenêtres et cases touchées pendant la 1re période ; marquage des premières lectures ; limites des phases de lecture
(jusqu'à s_{i+1}+208) ; Δ_i ; règles « un pas » (c ∉ D pour i = 1, voisins dans l'accord de la phase précédente sinon) ;
profondeur de récursion bornée.
**Faille trouvée et corrigée** : pour NS impair, le test Z ne vérifiait que p < L_NS, alors que la base exige aussi
l'accord de la phase NS−2 ; test remplacé par p < L_NS et p < L_{NS−2} (suffisant). Les 3 classes de pente 208 restent OK
(L₁ = 100 ; L₃ = 64, 62, 100). Le reste de la relecture (preuve écrite du couplage multiple) : séance suivante.

## S3 — Base quelconque : « T1 relatif » (brique de l'automate des sites)
`ant multi` et `ant deux` acceptent une configuration de base C₀ (variables BASE="x,y;…" en y vers le bas, T0 = instant
de certification de son autoroute, qui doit avoir la dérive (−2,+2)). D, MPD (borne de p sur D) et les diagonales de D
sont recalculés pour C₀. Alors « C₀ + une case noire n'importe où » se traite exactement comme T1 :
(A) zone d'activité de C₀ + début de sa bande, calcul direct ; (B) ailleurs hors bande : certifié à T0 ;
(C) loin dans la bande : classes, `multi` à la base k₀.
**T5 (exemple)** : C₀ = îlot {(−56,28),(−54,28),(−54,30)} (le plus lent de T4, T0 = 228 739, MPD = 149, activité dans
[−93,62]×[−43,115], bande x+y ∈ [90,100]). (C) : 51 diagonales × k = 300…305 (306 calculs) : 22 classes touchées, toutes
de pente 52 (aucun demi-tour) ; `multi` NS = 0 : 22/22 OK ; `deux` : 22/22 couplages exacts. (A) : voir R-90.

### Plan pour deux îlots loin (pas fait)
Double récurrence : (i) k₁ fixé (base C₀ = blanc + c₁(k₁)) : T1 relatif donne c₂ partout ; (ii) k₁ → k₁+2 en déplaçant
{c₁, c₂} ensemble (îlot à grand écart, `multi` accepte des écarts quelconques). Difficulté : (ii) doit valoir pour tous
les écarts r = c₂ − c₁ ; il faut montrer que les conditions de `multi` à (k₀, r) se transportent de r à r + d₂
(couplage le long de la 2e autoroute). Si d₂ ⟂ d, p est constant le long de la 2e bande : piste prometteuse.

## S4 — Deux cases : la 1re à distance fixe (k = 100/101, ses 22 classes), la 2e n'importe où
Pour chacune des 22 positions c₁ de T1 à k = 100/101 (celles qui touchent l'autoroute), base C₀ = blanc + c₁
(T0 = son certificat). Les 13 bases dont l'autoroute tourne sont **pivotées d'un quart de tour** (fourmi au départ en
cap D, B ou G : variable H0 pour `ant`, 4e argument de `relatif.py`) pour ramener la dérive à (−2,+2).
- (C) loin dans la nouvelle bande (k₂ ≥ 400) : 22 × 22 = 484 classes, **484/484 preuves `multi`**, 484/484 couplages exacts
  (`deux`). Sur 13 bases, 1 classe demi-tour qui revient au 1er site (p* ≥ 300) ; 7 bases sans demi-tour.
- (A) zone d'activité de la base + bande jusqu'à k₂ < 400 : 9 bases non pivotées 264 470/264 470 certifiées (plus lent :
  c₁ = (−121,101), c₂ = (−144,104), 181 641) ; 13 bases pivotées : voir R-93.
- (B) ailleurs : certifié à T0.
Reste pour « deux cases loin » en général : faire varier aussi k₁ (double récurrence, cf. S3).

### S4 — Double récurrence : état
- Récurrence en k₂ à k₁ fixé : R-91/R-93 (toutes les classes, k₁ = 100/101).
- Récurrence en k₁ à écart fixé : R-94 (968 cas, tous OK). Deux paramétrages selon c₁ : îlot {c₁, c₂} déplacé en bloc
  (l'autoroute sortante bouge avec c₁), ou c₂ fixe en base (c₁ = demi-tour : l'autoroute repart du germe).
- Manque : l'uniformité (les conditions de l'une des deux récurrences doivent valoir pour toutes les valeurs de l'autre
  paramètre). Idée : exprimer les conditions de la récurrence en k₂ sur X(k₁+2, ·) à partir de X(k₁, ·) via le couplage
  en k₁ (p augmente de 4 sur les segments « translation », inchangé sur les segments « identité », diagonales conservées),
  et montrer que chaque inégalité est préservée. Point délicat : la borne MPD de la base (blanc + c₁) augmente avec k₁.

## Théorème T6 (S5) : deux cases noires éparses — DÉMONTRÉ sous réserve de relecture, sauf 2 paires de classes
Départ blanc + deux cases noires c₁, c₂ avec |c₁|, |c₂| ≥ **R = 417** et |c₁ − c₂| ≥ **D = 545** (norme max(|x|,|y|)).
Alors la fourmi construit l'autoroute 104 pour toujours — sauf peut-être si (c₁, c₂), après échange éventuel, est dans l'une
des 2 paires de classes non démontrées de R-96 (OBSERVÉES) : c₁ dans la classe du demi-tour (j = −19, k pair) avec c₂ dans la
classe de (−401,−409) ; c₁ dans la classe j = −27, k pair, avec la classe de c₂ en NS = 2.
*Preuve (cas).* Bande de départ : diagonales x+y ∈ [−28,−18] ; |c| ≥ R ⇒ hors du germe (la fourmi blanche reste dans
[−21,29]×[−22,22] avant 10 185) et, sur la bande, k ≥ 100.
1. Aucune case sur la bande de départ : certifié à 9 977 (argument (B) de T1).
2. Sinon, c₁ = la case de la bande touchée la première (k₁ ≥ 100, une des 22 classes). Base W = blanc + c₁, certifiée à T0(k₁)
   (T1). Les cases que W touche avant T0+104 sont : le germe, la bande de départ avant c₁, la zone du 1er site (translatée
   avec k₁ ; à distance < D_i ≤ 544 de c₁) et, pour la classe du demi-tour, une zone fixe près du germe (|·| ≤ 416).
   - c₂ hors de tout cela et hors de la 2e bande Z₂ : W + c₂ est certifiée à T0 (argument (B) relatif à W).
   - c₂ dans Z₂ : comme |c₂ − c₁| ≥ D (ou |c₂| ≥ R pour le demi-tour, dont Z₂ part du germe), c₂ est dans la partie lointaine
     (paramètre ≥ 400) : R-95/R-96 (double récurrence) s'applique, sauf les 2 paires ci-dessus.
   - c₂ sur la bande de départ avant c₁ : contredit le choix de c₁.
R et D calculés par `outils/epars_RD.py` (maximum sur les 22 classes). Contrôle : 300 paires tirées au hasard dans le domaine
(moitié avec c₁ sur la bande et c₂ sur des diagonales voisines) : 300/300 certifiées.
