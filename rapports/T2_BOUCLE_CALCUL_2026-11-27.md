# T2 — calcul dans une boucle qui tourne seule (27-11) — rapport de travail

Branche claude/t2-boucle-calcul (reprise : la branche existait, = main, dernier commit 08:54 UTC, > 30 min). Journal :
recherche/regles/s2_horloge/journal.md (R-513 et suivants). Heures en UTC.

## Fait (statuts)
- R-513 OBSERVÉ (négatif) : une horloge triangle ne survit à AUCUN décalage d'un seul vaisseau (34 080 machines, 0 CYCLE).
- R-514 DÉMONTRÉ (calcul exact) + VÉRIFIÉ : règle de compensation δh + rot120(δa) = 0 ; la taille de l'horloge reste libre.

## Heures réelles
- 10:55 reprise, oracle make test OK ; lecture rapport S2 + titres du journal S2.
- 11:00-11:05 t2_portes.py / t2_regulier.py : portes des 96 hexagrammes (R-512) : aucune droite à passages réguliers et issue variable.
- 11:05-11:10 t2_tolere.py (R-513) ; t2_absorbe.py, t2_compense.py (R-514), ≈ 2 min de calcul.

## Ce qui reste
- Objectif 1 (R-337 dans la boucle) : il faut une 2e porte qui compense sur le vaisseau impair (R-514).
- Objectif 2 (diviseur par 2 causal) et 3 (accumulateur) : OUVERTS.

## En 10 lignes (L1)
Une horloge = 6 vaisseaux qui tournent sur un triangle et reviennent exactement au départ.
Le demi-additionneur pousse les vaisseaux d'une ou deux cases de côté. On a essayé : pousser UN vaisseau d'une horloge la casse toujours.
Le calcul exact dit pourquoi : à chaque tiers, le décalage de l'horaire doit être annulé par celui de l'anti-horaire (tourné de 120°).
Et la taille du triangle n'y change rien (c'est pour ça qu'il existe des horloges de toutes tailles).

avancement : 15 % de l'objectif
