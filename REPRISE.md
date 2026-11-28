# REPRISE — à lire en premier (1 page, mise à jour à la fin de chaque session)

But final : la « fourmi dans la fourmi » en hexa R2L2 = la petite fourmi RL sur le tore 2×2 (8 bits),
calculée pas après pas par des vaisseaux R2L2, affichée sur l'écran 2×2, et qui tourne seule.
Acquis (dans main) : portes, fusion R-403, additionneurs, mémoire, horloges, pixel qui clignote (R-502),
pas complet réutilisable (R-616/617), écran 2×2 et 4×4 (R-707, R-711), écran branché sur 1 pas (R-715).

| # | Objectif ouvert | Branche | Où ça en est | Prochaine action |
|---|---|---|---|---|
| 1 | Enchaîner N pas, taille linéaire (8 bits) | claude/t1-deux-pas | greffe = ×4 par pas (R-621) ; copie + routage linéaire pour h0 seul (R-622/623) ; h1'' placé, en vérification (R-624) | finir h1'' (2 pas, 256/256), puis étendre copie + routage aux 8 bits |
| 2 | Deux pas de suite à l'écran | claude/t4-ecran-fourmi | 1 pas OK (R-715) ; boucles d'effacement courtes : échec à l'usage 2 (R-719) ; boucles longues (R-720) et port de lecture (R-722) observés | démo intégrée 2 pas (R-723) à vérifier sur 256 états |
| 3 | Un calcul dans une machine qui tourne seule | claude/t2-boucle-calcul (PR n°16) | règle de compensation R-514 ; porte d'un seul côté jamais absorbée (R-519) ; diviseur par 2 causal R-521 | porte placée des 2 côtés de l'horloge (symétrique), cycle exact |
| 4 | Reboucler le pas (fourmi dans fourmi qui tourne) | — | dépend de 1, 2, 3 | version A : constants qui arrivent de loin en file |

Calculs longs : `calculs/LISEZMOI.md` (GitHub Actions). Journal : `journal.md` (grep « R-6 », « R-5 », « R-7 »).
