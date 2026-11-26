# S1 fusion — journal (R-400+)
Début session S1 : 19:30 UTC

Session S1 (fusion / enchaînement), 26/11 soir, automatique (Pierre-Malo absent). Branche claude/s1-fusion (depuis claude/r2l2-additionneur-boucle).
Règle H:R2L2 (hexa, blanc → +120°, noir → −120°), fourmis jouées l'une après l'autre, positions entières. Moteurs : fourmi_r (C) et hx.py (Python).
Commandes à lancer depuis recherche/regles/.

## R-400 Fusion de deux signaux exclusifs avec UN constant : 1 529 fusions (UN usage) — VÉRIFIÉ (2 moteurs, temps fini) (fusion1.py, fusion1v.py)
Fusion = deux routes s1, s2 (au plus un vaisseau à la fois) → UN vaisseau sur UNE trajectoire O (même direction, voie, instant, phase),
O absente quand il n'y a aucun signal, 0 case restante. Recherche EXHAUSTIVE à 1 constant K (vaisseau direction 0) : tous les chocs
propres de R-333 (1 688), rangés modulo la symétrie σ (décaler s de 8 pas et de −d_K laisse K invariant) ; deux chocs qui émettent la
même trajectoire = fusion. 2 360 paires, 1 529 à routes distinctes, toutes revérifiées par simulation directe des 3 cas (fourmi_r)
et par hx.py (0 désaccord). Complément (fusion1b.py) : un signal qui ne touche pas K ne peut pas servir (les 1 904 sorties prolongées
en arrière passent toutes à ≤ 6 de K) ⇒ la liste est complète.

## R-401 À 1 constant, toute fusion RÉUTILISABLE est une « fusion à ombre » — DÉMONTRÉ (calcul exhaustif R-400) (fusion_reuse.py)
Sur les 1 529 : 1 516 ont une sortie qui repart à contresens sur l'axe d'une entrée (≤ 6 voies) ⇒ percutée par l'usage suivant.
Les 13 restantes sont réutilisables (2 usages 9/9, 20 usages × 3 graines 20/20, 2 moteurs, certificat : distance 99 + 100 (j − 1))
MAIS O = K décalé d'UNE voie : dans le cas « aucun signal », K passe sur la voie voisine au même instant (l'« ombre »). C'est un
codage « 2 rails » (O = x∨y, ombre = ¬(x∨y)), pas une sortie seule sur sa route.
Pourquoi (argument géométrique + invariants R-331) : la ligne de O passe par les deux points de choc P1 (s1+K) et P2 (s2+K), qui sont sur la
ligne de K ; donc O est sur l'axe de K (ombre si même sens, route de face si sens opposé) ou P1 ≈ P2 ; dans ce 2e cas toutes les lignes
passent par le même point et (I1)+(I2) forcent les directions des déchets ; ex. type (s1, s2, O) = (1, 2, 2) : le déchet de s1 + K a
forcément la direction 5, à contresens de s2, et part du point de choc, donc sur l'axe de s2.

## R-402 Ombre + 2e constant « séparateur » : 5 640 fusions… toutes encore à ombre — OBSERVÉ (fusion2.py, bases 0 et 1)
K' placé sur la route de O (17 instants, 5 directions, 81 décalages, 8 phases, 2 ordres : 2 × 74 912 placements) : 5 640 réussites à 2 usages
9/9, mais O' est toujours K' retardé de quelques pas (même voie) : l'ombre a seulement changé de constant. Critère corrigé ensuite :
« aucune sortie du cas vide parallèle à O à ≤ 6 voies ».

## R-403 FUSION PROPRE ET RÉUTILISABLE à 2 constants — VÉRIFIÉ (2 moteurs, 20 usages) ; tout nombre d'usages DÉMONTRÉ (certificat) (fusion3.py, fusion_final.py)
Idée : partir d'une fusion à 1 constant non réutilisable dont le SEUL défaut est le déchet forcé de R-401 (type (1, 2, 2)) et ajouter un
constant K' qui percute ce déchet δ périodes après sa naissance, là où s2 est déjà passé. Recherche : 17 432 placements par base,
642 réussites par base (2 usages 9/9, sans ombre, sans route de face).
Exemple retenu (fusion_verif.json, indice 0) : ordre de jeu Kp, s1, s2, K ;
 K = « −85,85,4 » + case (−84,85) (direction 0) ; Kp = « 91,−7,2 » + case (91,−8) (direction 4) ;
 s1 = « −85,1,1 » + cases (−85,0), (−85,1) (direction 1) ; s2 = « −1,−83,2 » + cases (−1,−83), (0,−84) (direction 2) ;
 O = vaisseau direction 2, voie 1, abscisse 833, phase 6 au temps 4 000 (même trajectoire exacte pour s1 et pour s2).
 Cas vide : K et Kp continuent (directions 0 et 4, rien de parallèle à O). 3 cas justes, 2 moteurs ; 2 usages 9/9 ; 20 usages dans UNE simulation :
 3 suites au hasard + 20 × s1 + 20 × s2 + alterné : 20/20, superposition exacte, 2 moteurs identiques à chaque fois.
 Certificat (circuit.certificat, j = 1 … 10) : distance minimale EXACTE entre fourmis de deux usages = 7 (> 6) pour tout écart, aucune paire de face
 (les 7 viennent de deux routes à contresens à 7 voies, qui se croisent toujours à 7) ⇒ N usages = superposition exacte pour tout N.
Commande : python3 s1_fusion/fusion_final.py s1_fusion/fusion3_122_0_2.json 0 10
