# Gomme et bascule — nuit du 25/11/2026 (R-136 à R-142)

Résumé : (1) la gomme marche et c'est connu ; (2) une fourmi seule ne peut JAMAIS repartir en gomme sur sa propre trace
(invariant de parité) ; (3) une autre fourmi peut le faire (échange) mais, d'après une loi d'équilibre observée, la pièce
est alors toujours détruite ; (4) en revanche une BASCULE « T » existe : une pièce de 2 fourmis (+ cases) qui alterne entre
deux cycles S0 et S1 à chaque autoroute 104 qui arrive par la même ligne — vérifiée dans la simulation complète (traces
comprises), 2 moteurs.

## 1. La gomme (R-136) — VÉRIFIÉ (preuve + 2 moteurs), CONNU

État d'une fourmi = (x, h) : case x, cap h = direction de son dernier déplacement. Gomme : R(x, h) = (x − e_h, h + 2).
**Énoncé.** Règle RL (ou LR, NN, UU ; 2 couleurs). Après t pas, appliquer R, jouer t pas : grille de départ, fourmi en
R(départ) ; appliquer R encore : état de départ exact.
**Preuve (un pas, puis récurrence).** La fourmi en (x, h) lit c, prend le cap h' = h + t_c, retourne la case, va en
y = x + e_h'. Gommée : R(y, h') = (x, h' + 2).
- Cas blanc (c = 0, t_0 = +1) : h' = h + 1 ; gommée, elle est en x, devenue NOIRE, cap h + 3 ; noir → gauche : cap h + 2 ;
  x redevient BLANCHE ; elle va en x + e_{h+2} = x − e_h. Nouvel état R(x, h). ✔
- Cas noir (c = 1, t_1 = −1) : h' = h − 1 ; gommée : en x, devenue BLANCHE, cap h + 1 ; blanc → droite : cap h + 2 ;
  x redevient NOIRE ; elle va en x − e_h. Nouvel état R(x, h). ✔
Donc S∘R∘S = R (S = un pas) : chaque pas joué après la gomme défait le pas d'avant.
**Pour quelles règles.** 2 couleurs, virages t_0, t_1 : il faut t_0 + t_1 ≡ 0 (mod 4) → RL, LR, NN, UU (RR, LL : non ;
RR testé : cycle 4). 3 couleurs ou plus (LLR…) : impossible avec la même règle (une fourmi fait c → c + 1, défaire demande
c + 1 → c). Hexagonal 2 couleurs si t_0 + t_1 ≡ 0 (mod 6) (H:R1L1 et H:R2L2 testés : effacé).
**Plusieurs fourmis.** Un tour = S_{n−1}∘…∘S_0 ; son inverse = R∘(S_0∘S_1∘…∘S_{n−1})∘R : gommer TOUTES les fourmis et
jouer dans l'ordre INVERSE. Sans inverser l'ordre : faux dès que les fourmis se touchent.
**Vérifications.** `src/fourmi -gomme t -T 2t+10` et `moteur2.py` (Python) : départ blanc t = 10, 500, 11 000, 10⁵, 10⁶ →
EFFACE au pas 2t ; germe R-20, t = 1 040, 104 000, 1 040 000 → effacé, germe intact ; 3 fourmis + 1 case : effacé (ordre
inversé), 892 cases fausses sans inverser l'ordre ; 0,0,H ; 40,0,G : 488 cases fausses sans inverser.
**Connu** : réversibilité de la fourmi / des « flipping rotators » ; Tsukiji & Hagiwara, Algorithms 4(1), 2011 : « the
reverse of a walking course is defined by reversing the order of the coloring changes and reversing the ants' moves ».

## 2. Pas de gomme pour une fourmi seule (R-137) — DÉMONTRÉ

I = (x + y + h) mod 2 ne change jamais (à chaque pas x + y change de ±1 et h de ±1 ; c'est la classe de R-09).
R change I (x + y de ±1, h de 2). Donc une fourmi n'est JAMAIS dans l'état R d'un de ses états passés : aucune pièce de
cases (taille, forme, couleurs quelconques) ne renvoie une autoroute en mode gomme sur sa propre trace.
Contrôle : 22 + 2 574 pièces de 1 et 2 cases → 0 retour ; les 141 « demi-tours » longent la trace (elle double).
Seule issue : l'ÉCHANGE — une autre fourmi, de l'autre classe, repart en gomme.

## 3. Gomme par échange (R-138) — OBSERVÉ / VÉRIFIÉ sur échantillon (2 moteurs)

Montage : germe R-20 à L ≈ 200 cases (50 périodes) d'une pièce = petit cycle (boîte ≤ 7×7), toutes phases et voies utiles.
Critère : la fenêtre x ∈ [35,75], y ∈ [−75,−35] (entre L/4 et 3L/4 de la trace) redevient entièrement blanche (20 000 pas).
- 2 fourmis (2 049 cycles, 501 370 essais) : 8 152 gommes ; 300/300 tirées au hasard : pièce détruite (une fourmi part).
- 4 fourmis (1 000 premiers des 3 978 cycles, 903 776 essais) : 15 825 gommes ; 15 825/15 825 : pièce détruite (987 « restées
  dans la boîte » à 20 000 pas éclatent ensuite en autoroutes).
- 10/10 gommes rejouées par moteur2.py : fenêtre blanche, positions finales identiques.
La gomme est souvent « décalée d'une période » : elle efface toute la trace mais abîme le germe source (28 cases).

## 4. Loi d'équilibre (R-139) — OBSERVÉ (conjecture), pas trouvée dans la littérature

**Conjecture : dans un cycle (RL), il y a autant de fourmis de chaque classe.**
Données : 0 cycle sur 2 213 888 configurations 3+1 (4 fourmis dans [−3,3]², T = 20 000) ; 0 sur 200 000 pour chacun de :
3 fourmis (2:1, avec ou sans case), 4 fourmis 3:1 + 1 case, 5 fourmis 3:2, 6 fourmis 4:2 (avec ou sans case) ; témoins
équilibrés : 2:2 + 1 case 6 123 cycles / 200 000, 3:3 292 et 308 / 200 000 ; catalogue : 47 cycles, tous équilibrés
(1:1, 2:2, 3:3, 4:4, 6:6). Ce qui est démontré : au moins une de chaque classe (R-09 ; au coin du domaine visité les
visites alternent entre les 2 classes — argument noté dans le rapport).
**Conséquence (si la loi est vraie).** Un échange fait passer la pièce de (k, k) à (k + 1, k − 1) : elle ne peut plus être
un cycle, donc (R-44) elle ne reste pas bornée. Avec R-137 : AUCUNE pièce bornée ne renvoie une autoroute en gomme en
restant intacte. La bascule « par gomme » demandée est donc impossible en RL (et la gomme elle-même impossible en LLR).

## 5. La bascule T (R-140) — VÉRIFIÉ (simulation complète, 2 moteurs, temps fini)

Idée compatible avec la loi : l'autoroute ne revient pas, elle repart (même classe) ; la pièce passe d'un cycle S0 à un
cycle S1. Recherche : 19 936 déviations « pièce intacte » (2 fourmis) → 15 257 résidus changés, dont 1 668 petits cycles
(393 orbites S1) ; 2e tir idéalisé (autoroute neuve) sur chaque S1 : 521 368 essais → 16 retours exacts à S0.
Test honnête (les 2 autoroutes dans la même simulation, germes sur des voies voisines de la même ligne, la 2e partie plus
loin) : 11/16 → 3 bascules physiquement distinctes, retour à S0 EN PLACE.
Meilleure : pièce 572 de cycles2.json (RL|0,0,D;−1,−2,G|0,3 : 2 fourmis + 1 case, période 24), S1 = cycle de période 28 (2 fourmis + 8 cases) — voir README / bestiaire.
Chronologie (moteur Python) : S0 jusqu'au pas ≈ 6 100, S1 dès 6 200, S0 dès 8 400 (la 2e autoroute arrive en roulant
sur la trace de la 1re), puis S0 jusqu'à la fin. Impulsions suivantes : voir README.md.
