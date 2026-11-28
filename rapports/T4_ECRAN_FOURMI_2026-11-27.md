# Rapport T4 — l'écran de la fourmi (27/11, session sans Pierre-Malo)

Heures réelles en UTC. Branche claude/t4-ecran-fourmi (existait, identique à main, dernier commit 08:54 → reprise, personne dessus).
Fichiers : recherche/regles/s4_ecran/t4/ ; journal : recherche/regles/s4_ecran/journal.md (R-714 à R-723).
Choix notés (sans questions) : un pixel par sortie de case (pas de démux : chaque case a déjà son vaisseau) ; les entrées du 2e pas
sont posées à la main (s1 = R-61(s0)) : le bouclage sortie → entrée est la mission T2 ; lecture par « port dédié » (une droite de tir
par pixel) plutôt que par démux (R-712/R-713 négatifs).

## Tranches (UTC)
- 10:55–11:00 : reprise, tests 19/19, lecture des rapports S3/S4.
- 11:00–11:05 : R-715 écran branché sur le pas (256/256, 2 moteurs) ; R-716 balayages effacement / remplissage.
- 11:05–11:15 : R-717 (boucle à 2 chocs : impossible) ; R-718 boucles à 3 chocs (4 pixels, 256/256 chacun, 1 usage).
- 11:12–11:35 : R-719 deux pas avec boucles courtes : pas 2 faux, cause trouvée (retour de face avec l'usage 2).
- 11:35–12:05 : R-720 boucles longues (outil de conflits géométriques, pré-tests, 4 pixels).
- 12:00–12:15 : R-721 chocs sélectifs ; R-722 ports de lecture (4 pixels × 2 lectures).
- 12:07– : calculs longs R-720 (moteur C, 256 états) puis R-723 (démo complète, C + hx.py, 256 états).

## Résultats (statuts)
| ID | Énoncé | Statut |
|---|---|---|
| R-715 | écran 2×2 sur les 4 sorties de cases du pas R-617 : 256/256, hx.py = C sur 64 | VÉRIFIÉ |
| R-716 | aucune écriture à 1 vaisseau n'est idempotente (effacer / remplir à l'aveugle impossible) | VÉRIFIÉ (balayage) |
| R-717 | boucle d'effacement à 2 chocs : u ≡ 0 mod 3 toujours, R' demande 1 ou 2 mod 3 | OBSERVÉ (calcul exact) |
| R-718 | boucle à 3 chocs vers RST3 : 4 pixels, 256/256 chacun (1 usage) | OBSERVÉ (moteur C) |
| R-719 | 2 pas avec boucles courtes : pas 2 faux (choc de face avec l'usage 2) | OBSERVÉ (2 moteurs sur l'exemple) |
| R-720 | boucles longues vers RST2 (écran allumé ≈ tout l'intervalle) | OBSERVÉ (4 états/pixel), complet → R-723 |
| R-721 | 16 chocs propres deviennent transparents si le signal a 3 pas de retard | VÉRIFIÉ (2 moteurs) |
| R-722 | port de lecture dédié, neutre (phase conservée), réutilisable : 4 pixels × 2 lectures | OBSERVÉ (hx.py, pixel seul) |
| R-723 | démo complète : 2 pas + effacements + 8 lectures, 256 états | en cours |

## Chiffres
- Situations : 256 états × (1 pas : 1 ; 2 pas : 1 simulation par état, jusqu'à t = 397 574). Pré-tests : quelques centaines de petites simulations.
- Temps de calcul : 1 pas, 256 états, moteur C 5 s ; 2 pas, 256 états, moteur C ≈ 15 min ; hx.py ≈ 15–18 s par état à t = 397 574
  (plus rapide que le moteur C en option -x à cette longueur).

## Ce qui a raté
- Boucles à 2 chocs (R-717) ; boucles courtes pour 2 pas (R-719) ; horloges à 60° du front des sorties (toujours un débris voisin) ;
  1er filtre géométrique trop strict (des croisements à distance 1 sont propres) ; bug de prédiction (fermeture Python) dans
  ecran_deux_pas.py, corrigé ; un fichier de 8 Mo poussé par erreur (t4/boucle_geo.json), retiré du dépôt (copie dans data/).

## Ce qui reste
- Fin de R-723 (chiffres), bestiaire 34, germes, Drive, PR.
- Plus de 2 pas : il faudrait des horloges par pas (pas de difficulté nouvelle) ; bouclage sortie → entrée (T2).
- Écran compact (les 4 pixels sont à des milliers de cases les uns des autres, sur 4 routes parallèles).

## En 10 lignes (L1)
(à écrire à la fin)

avancement : 80 % de l'objectif
