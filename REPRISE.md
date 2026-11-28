# REPRISE — à lire en premier (1 page, mise à jour à la fin de chaque session)

But final : la « fourmi dans la fourmi » en hexa R2L2 = la petite fourmi RL sur le tore 2×2 (8 bits),
calculée pas après pas par des vaisseaux R2L2, affichée sur l'écran 2×2, et qui tourne seule.
Acquis (dans main) : portes, fusion R-403, additionneurs, mémoire, horloges, pixel qui clignote (R-502),
pas complet réutilisable (R-616/617), écran 2×2 et 4×4 (R-707, R-711), écran branché sur 1 pas (R-715).

| # | Objectif ouvert | Branche | Où ça en est | Prochaine action |
|---|---|---|---|---|
| 1 | Enchaîner N pas, taille linéaire (8 bits) | claude/t1-deux-pas | greffe = ×4 par pas (R-621) ; copie + routage linéaire pour h0 seul (R-622/623) ; h1'' 2 pas VÉRIFIÉ 256/256 (C) + 16/16 hx (R-624, 28/11) | étendre copie + routage aux 8 bits : script chain8_descente À FINIR (options SIDES=+- FANK=100,400 FDT=2.4,3.2 → routage toujours impossible, 1 000 000 conflits) |
| 2 | Deux pas de suite à l'écran | claude/t4-ecran-fourmi | 1 pas OK (R-715) ; boucles longues (R-720), port de lecture (R-722) ; démo 2 pas R-723 : calcul de nuit raté (numpy absent), relancé 29/11 (r723_ecran2b) | lire calculs/resultats/r723_ecran2b/resume.txt |
| 3 | Un calcul dans une machine qui tourne seule | claude/t2-boucle-calcul (PR n°16) | règle de compensation R-514 ; porte d'un seul côté jamais absorbée (R-519) ; diviseur par 2 causal R-521 ; horloge qui ralentit, vaisseaux porteurs de bit (R-522) | lancés 28/11 : `t2_porte_x0x1` (branche claude/jour-28-11-t2_porte_x0x1, X0 ET X1) et `t2_div4` (claude/jour-28-11-t2_div4, 2e couche sur les 60 machines 504) → lire calculs/resultats/<nom>/resume.txt ; « un seul CYCLE » = candidat à vérifier (X1 peut juste casser) ; data/t2 se régénère en ≈ 2 min |
| 4 | Reboucler le pas (fourmi dans fourmi qui tourne) | — | dépend de 1, 2, 3 | version A : constants qui arrivent de loin en file |

Calculs longs : `calculs/LISEZMOI.md` (GitHub Actions). Journal : `journal.md` (grep « R-6 », « R-5 », « R-7 »).

Inventaire 28/11 (préparation, rien d'autre lancé) — utilité / coût d'écriture :
- LANCÉS : porte X0/X1 (obj. 3, utile, script = t2_sym2.py BIT=both) ; diviseur par 4 en cascade (R-522 + 2e couche, BASE=, cherche P = 2 016).
- À FINIR : copie + routage 8 bits (chainN.py 'pos' / '7', descente sur $NPROC graines) : options à revoir (FDT trop grand ? garder REAL=1).
- ÉCARTÉ : compteur R-507 sur l'écran R-707 : les horloges n'émettent aucun vaisseau (R-521/522), rien pour piloter le démux ; R-507 a déjà ses 2 pixels.
- Base : calcul.yml installe numpy/matplotlib/pillow et met une croix rouge si un FINI a code ≠ 0 (après enregistrement).
- Outils : calculs/run_t2.py + commun_t2.sh (régénère data/t2) ; outils_r.lot utilise $NPROC.
