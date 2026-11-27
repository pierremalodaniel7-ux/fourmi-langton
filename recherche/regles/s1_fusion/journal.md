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

## R-404 CROISEMENT : deux vaisseaux libres ne s'influencent que s'ils passent à distance ≤ 1 (≤ 2 s'ils sont parallèles) — DÉMONTRÉ (calcul exhaustif) (croisement.py, paralleles.py, croisement_demo.py)
Toutes les géométries relatives proches de 2 vaisseaux de directions différentes (r = 1 … 5, tau, v modulo u, 2 ordres : 1 880, R-333) :
distance minimale des trajectoires libres 0 : 232 / 240 interagissent ; 1 : 184 / 360 ; 2, 3, 4, 5, 6 : 0 / 256 chacune (croisement EXACT :
chaque fourmi suit pas à pas sa trajectoire libre). Au-delà de 6 : transparent exact (R-333). Aucun « vrai choc » ne rend les deux trajectoires
libres (0 échange). 416 géométries interdites en tout (64, 96, 96, 96, 64 pour r = 1 … 5). Parallèles (même direction, [−8, 8]², 8 phases,
2 ordres) : distance 2 : 4 / 296 interagissent ; ≥ 3 : 0. Conséquence : à contresens, deux routes ne se gênent que si la somme de leurs voies
est dans [−3, 1] (au lieu de « ≤ 6 voies » utilisé jusqu'ici, trop prudent).
⇒ Un croisement n'a besoin d'AUCUN constant : il suffit que les deux signaux ne passent pas à ≤ 1 l'un de l'autre. Démonstration
réutilisable (croisement_demo.py) : directions 0 et 1 (60°), puis 0 et 2 (120°), fourmis à distance 2 au plus près : 4 cas justes, 2 moteurs ;
2 usages 16/16 ; 20 usages (3 graines + 20 × (1,1)) 20/20, superposition exacte, 2 moteurs ; certificat (distance entre usages 117 + 200 (j−1),
resp. 17 + 100 (j−1)).
Certificat fin (cert_fin.py) : condition « distance ≥ 7, ou les deux fourmis libres et ≥ 3 / ≥ 2 », sur toute la droite des temps, + argument de
parité (couleur = parité des passages) ⇒ superposition exacte. Contrôle : la fusion R-403 passe (libres à 7, non libres ≥ 180).

## (vague 2, 27/11, début 00:41 UTC) Piste « relais » de la vague 1 (add2_fusion.py) : 0 réussite — OBSERVÉ ; cause trouvée : ORDRE DE JEU
Vague 1 : 1 010 relais (fusions R-402) × placements → « 16 cas : sale » à chaque fois. Vague 2 : même chose avec les fusions R-403 et
l'entrée de l'étage 1 par A, B ou c (add2_relais.py, relais 0 … 400 : 10 800 essais sales). Diagnostic (diverge.py) : les fourmis sont
jouées l'une après l'autre, et dans R-349 la pièce A joue APRÈS K3, K2, B ; en posant HA0 avant l'étage 1, la fourmi qui porte c0 joue
avant les pièces qu'elle rencontre ⇒ autre dynamique au contact. (Pour la piste relais, les 16 cas sales venaient aussi de relais qui
ne font que décaler c0 de quelques voies : l'étage 1 retombe alors presque sur HA0.)

## R-405 ADDITIONNEUR 2 BITS RÉUTILISABLE (a1a0 + b1b0 → c1 s1 s0) — VÉRIFIÉ (2 moteurs, 20 usages) (add2_perm.py, add2_final.py)
Idée : a + b + c est symétrique ⇒ la retenue c0 du demi-additionneur R-337 entre dans l'additionneur complet R-349 par sa pièce A
(même direction 2 que c0 : rotation 0), pas par c (R-350 : K2 parallèle à c traverse la porte de HA0). compose.attach (étage 1 posé pour
que A suive EXACTEMENT c0), glissé de D périodes ; le bloc HA0 joue À LA PLACE de la pièce A dans l'ordre de R-349 (sinon 15/16).
Balayage D = 0 … 400 (pas 10) : pièce A → 16/16 pour TOUT D ≥ 10 (39/39) ; pièce B (rotation 2) → 12/16 au mieux.
Retenu D = 20 : 8 pièces seulement, ordre de jeu : c(étage 1, entrée b1) « 74,−8,2 », K3' « −38,56,4 », K2' « 80,−4,4 », B' (entrée a1)
« −22,40,4 », puis HA0 : K3 « −16,16,4 », K2 « 62,−24,4 », B (b0) « 0,0,4 », A (a0) « 30,−56,0 » (cases : add2_final.json).
Sorties au temps 9 000 : s0 sur (0,0,2218,0) ou (0,0,2250,0) ; s1 sur (0,18,2188,0), (2,−29,2163,0), (4,8,2108,2) ; c1 sur
(0,19,2187,0), (0,19,2187,7), (2,−30,2168,1) (« un vaisseau sur l'une des positions »).
16/16 justes, propres (0 case hors vaisseaux), 2 moteurs identiques ; 2 usages (k = 200) : 256/256 couples en superposition exacte ;
20 usages dans UNE simulation : graines 0, 1, 2, 20 × (1,1,1,1), alterné : 20/20 chaque fois, superposition exacte, 2 moteurs identiques.
PIÈGE : fourmi_r a MAXA = 128 et IGNORE sans message les fourmis suivantes (20 × 1111 = 160 fourmis → faux échec « 0/20, 2 moteurs
différents »). s1_fusion/fourmi_r512 (même source, MAXA = 512) + big.py ; à signaler dans le dépôt commun.
La fusion R-403 n'a pas été nécessaire pour 2 bits (elle servira à rendre c1 « une seule route » pour enchaîner un 3e bit).
Commande : python3 s1_fusion/add2_final.py 20 5   (depuis recherche/regles/)

## R-406 CROISEMENTS dans un vrai circuit (l'additionneur R-405) — OBSERVÉ (16 cas) + R-404 (croisement_add2 : croise_add2.py)
Dans R-405, 50 paires (fourmi de l'étage 0, fourmi de l'étage 1) ont des CHEMINS qui se coupent (même case, instants différents) sans
jamais être à moins de 2 au même instant : ex. B' (entrée a1) coupe le chemin de B (étage 0) à 467 pas d'écart (distance min 40) ;
K3' coupe K3, K2 et B. Par R-404 ce sont des croisements transparents ; le circuit est juste 16/16 et 20/20 avec eux.
Commande : python3 s1_fusion/croise_add2.py 20
