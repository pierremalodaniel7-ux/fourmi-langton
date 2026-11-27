# T2 — calcul dans une boucle qui tourne seule (27-11) — rapport de travail

Branche claude/t2-boucle-calcul (reprise : la branche existait, = main, dernier commit 08:54 UTC, > 30 min). Journal :
recherche/regles/s2_horloge/journal.md (R-513 et suivants). Heures en UTC.

## Fait (statuts)
- R-513 OBSERVÉ (négatif) : une horloge triangle ne survit à AUCUN décalage d'un seul vaisseau (34 080 machines, 0 CYCLE).
- R-514 DÉMONTRÉ (calcul exact) + VÉRIFIÉ : règle de compensation δh + rot120(δa) = 0 ; la taille de l'horloge reste libre.
- R-515 OBSERVÉ (négatif) : deux horloges différentes, même période, même centre : 0 interaction qui referme (191 262 machines).
- R-516 VÉRIFIÉ (2 moteurs) : « étoile décalée » (horloge + image par rotation 180° autour d'un autre point) : 316 machines propres.
- R-517 OBSERVÉ (négatif) : hexagramme + 3e train : 89 691 machines, 0 vrai cycle.
- R-518 AFFIRMÉ (argument) : ce qu'il faut pour un diviseur par 2 dans une machine 3-symétrique ; 0 trouvé.
- R-519 DÉMONTRÉ (sous hypothèse) : une porte sur un seul côté d'une horloge n'est jamais absorbée ; obstacles pour R-337.

## Heures réelles
- 10:55 reprise, oracle make test OK ; lecture rapport S2 + titres du journal S2.
- 11:00-11:05 t2_portes.py / t2_regulier.py : portes des 96 hexagrammes (R-512) : aucune droite à passages réguliers et issue variable.
- 11:05-11:10 t2_tolere.py (R-513) ; t2_absorbe.py, t2_compense.py (R-514), ≈ 2 min de calcul.
- 11:14-11:24 bihorloge.py k = 1 puis k = 0 (R-515), ≈ 10 min (2 cœurs).
- 11:25-11:31 etoile180.py (R-516), ≈ 6 min ; 11:32-11:40 hexa3.py (R-517), ≈ 3 min ; e180_anal + hx.py.
- 11:40-11:55 R-518, R-519 (arguments) ; journal.

## Ce qui reste
- Objectif 1 (R-337 dans la boucle) : OUVERT ; obstacles R-514, R-519 (porte sur les 3 côtés + porte compensatrice sur les impairs).
- Objectif 2 (diviseur par 2 causal) et 3 (accumulateur) : OUVERTS (R-518). Piste en cours : pixel posé EN AVAL d'une porte variable.

## En 10 lignes (L1)
Une horloge = 6 vaisseaux qui tournent sur un triangle et reviennent exactement au départ.
Le demi-additionneur pousse les vaisseaux d'une ou deux cases de côté. On a essayé : pousser UN vaisseau d'une horloge la casse toujours.
Le calcul exact dit pourquoi : à chaque tiers, le décalage de l'horaire doit être annulé par celui de l'anti-horaire (tourné de 120°).
Et la taille du triangle n'y change rien (c'est pour ça qu'il existe des horloges de toutes tailles).

Nouveau : une 2e famille de machines « deux horloges qui s'échangent des vaisseaux » (étoile décalée, 316) ; mais aucune porte ne divise
une horloge régulière par 2 : il faudrait deux vaisseaux par tiers sur le même côté, ce qui casse toujours.

avancement : 25 % de l'objectif
