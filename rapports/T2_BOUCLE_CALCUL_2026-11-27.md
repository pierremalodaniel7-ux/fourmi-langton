# T2 — calcul dans une boucle qui tourne seule (27-11) — rapport de travail

Branche claude/t2-boucle-calcul (la branche existait, = main, dernier commit 08:54 UTC, > 30 min : reprise). Journal :
recherche/regles/s2_horloge/journal.md, entrées R-513 à R-521. Heures en UTC. Aucun chiffre inventé : tous viennent des sorties de calcul.

## Fait (statuts)
- R-513 OBSERVÉ (négatif) : une horloge triangle ne survit à AUCUN décalage d'un seul vaisseau (34 080 machines, 0 CYCLE).
- R-514 DÉMONTRÉ (calcul exact) + VÉRIFIÉ : règle de compensation δh + rot120(δa) = 0 ; la taille de l'horloge reste libre.
- R-515 OBSERVÉ (négatif) : deux horloges différentes, même période, même centre : 0 interaction qui referme (191 262 machines).
- R-516 VÉRIFIÉ (2 moteurs) : « étoile décalée » (horloge + image par rotation 180° autour d'un autre point) : 316 machines propres.
- R-517 OBSERVÉ (négatif) : hexagramme + 3e train : 89 691 machines, 0 vrai cycle.
- R-518 AFFIRMÉ (argument) : ce qu'il faut pour un diviseur par 2 dans une machine 3-symétrique ; 0 trouvé (871 machines analysées).
- R-519 DÉMONTRÉ (sous hypothèse) : une porte sur un seul côté d'une horloge n'est jamais absorbée ; obstacles pour R-337.
- R-520 VÉRIFIÉ (2 moteurs, temps fini) : le bit M est DÉPHASÉ par un vaisseau qui passe exactement ; pas de vraie bascule T (0 / 1 227 096 flux).
- R-521 VÉRIFIÉ (2 moteurs, CYCLE exact) : horloge 1 131 + bit M → période 2 262 = 2 × 1 131 ; la phase de M change à chaque tour (s ← s ⊕ 1).

## Objectifs de la mission
1. R-337 dans une horloge, tous vaisseaux récupérés : NON atteint. Raisons démontrées (R-513, R-514, R-519) : une porte qui décale doit être
   présente sur les 3 côtés ET compensée sur l'anti-horaire ; R-337 ne touche que des pairs ; ses 3 droites d'entrée forment un triangle trop
   petit pour 3 horloges concentriques. (Avec une porte R-314 : déjà fait par R-512, et maintenant aussi sans symétrie commune, R-516.)
2. Diviseur par 2 causal : PARTIEL. R-521 = diviseur par 2 causé par l'horloge (pas 2 horloges indépendantes), CYCLE exact, 2 moteurs ;
   mais le « bit » est la phase de M et la bascule n'émet rien : elle ne pilote pas de 2e bascule (OUVERT).
3. Accumulateur 1 bit : PARTIEL, même machine R-521 (s ← s ⊕ 1 à chaque tour, GIF img/doublement_R521.gif) ; calculé par l'interaction
   vaisseau–bit, pas par le demi-additionneur.

## Heures réelles
- 10:55 reprise, oracle make test OK ; lecture rapport S2 + titres du journal S2.
- 11:00-11:05 t2_portes.py / t2_regulier.py : portes des 96 hexagrammes (R-512).
- 11:05-11:10 t2_tolere.py (R-513) ; t2_absorbe.py, t2_compense.py (R-514), ≈ 2 min de calcul.
- 11:14-11:24 bihorloge.py k = 1 puis k = 0 (R-515), ≈ 10 min (2 cœurs).
- 11:25-11:31 etoile180.py (R-516), ≈ 6 min ; 11:32-11:40 hexa3.py (R-517), ≈ 3 min ; e180_anal + hx.py.
- 11:40-11:44 R-518, R-519 (arguments) ; t2_pixel_aval / t2_pixel_tri (pixels en aval d'une porte : 139 386 poses, rien de concluant :
  la porte « variable » ne fait que retarder les vaisseaux, tous finissent par écrire le pixel) ; ≈ 3 min.
- 11:45-11:55 tbascule.py étapes 1-3 (508 objets, 813 600 tirs, 1 227 096 flux), ≈ 6 min ; tb_filtre, tb_hx (R-520).
- 11:56-12:07 t2_tb_horloge.py (468 000 + 78 867 poses, R-521), ≈ 5 min ; t2_tb_check, t2_classes.
- 12:08-12:13 poses « retardées » (215 910 machines, négatif) ; GIF ; bestiaire 33 (4 fiches), germes, rapport.
Calcul total ≈ 40 min sur 2 cœurs ; ≈ 3 300 000 simulations.

## Ce qui a raté
- Aucune porte d'hexagramme / d'étoile ne divise par 2 une horloge RÉGULIÈRE (R-518).
- Pixels en aval d'une porte : pas de vrai pilotage (les vaisseaux détournés reviennent tous).
- Aucune vraie bascule T (objet changé en un autre puis remis par un vaisseau identique) parmi 508 objets (R-520).
- Doublements de période « faciles » : tous triviaux (ppcm) sauf la famille 1 131 (R-521).
- Erreur corrigée : de gros fichiers JSON (bi-horloges, pixels) ont été commités puis déplacés dans data/ (ignoré) ; ils restent dans
  l'historique de la branche (≈ 25 Mo) : fusionner la PR en « squash » si possible.

## Ce qui reste
- Compteur causal à 2 étages : il faut qu'une bascule ÉMETTE (un vaisseau retardé ou décalé selon son état) ; R-514 dit comment l'horloge
  peut l'absorber (même retard sur l'horaire et l'anti-horaire du même côté, sur les 3 côtés).
- R-337 dans une boucle : 2 demi-additionneurs (pairs + impairs, tourné de 60°) sur les 3 côtés de 4 horloges : géométrie à étudier
  avec des horloges de tailles différentes (rapport ≈ 2) ou des routes non triangulaires.

## En 10 lignes (L1)
Une horloge = 6 vaisseaux qui tournent sur un triangle et reviennent exactement au départ.
Le demi-additionneur pousse les vaisseaux d'une ou deux cases de côté : on a montré que pousser UN vaisseau casse toujours l'horloge,
et le calcul exact dit pourquoi : il faut pousser aussi l'autre vaisseau du même côté, de la bonne façon (règle de compensation).
On a trouvé une nouvelle famille de machines : un triangle et son image retournée autour d'un autre point (316 machines qui reviennent).
Le résultat du jour : une horloge de 1 131 pas + le petit « bit » M ; les vaisseaux le traversent sans être abîmés,
mais ils changent sa phase (son « heure interne ») : 0 au tour 1, 18 au tour 2, 0 au tour 3…
Donc la machine ne revient qu'après 2 tours : c'est un diviseur par 2 provoqué par l'horloge elle-même (prouvé : retour exact, 2 moteurs).
Il manque encore qu'une bascule « parle » à une autre (un compteur à 2 chiffres).

avancement : 40 % de l'objectif (1 : non ; 2 et 3 : partiels)
