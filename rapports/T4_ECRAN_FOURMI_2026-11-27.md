# Rapport T4 — l'écran de la fourmi (27/11, session sans Pierre-Malo)

Heures réelles en UTC. Branche claude/t4-ecran-fourmi (existait déjà, identique à main, dernier commit 08:54 : reprise).
Fichiers : recherche/regles/s4_ecran/t4/ ; journal : recherche/regles/s4_ecran/journal.md (R-714 à R-7xx).
Choix notés (sans questions) : un pixel par sortie de case (pas de démux, chaque case a déjà son vaisseau) ; les vaisseaux d'entrée
du 2e pas sont posés à la main (état s1 = R-61(s0)), le bouclage sortie → entrée est la mission T2.

## Tranches
- 10:55–11:00 : reprise, tests 19/19, lecture des rapports S3/S4.
- 11:00–11:05 : R-715 écran branché sur le pas (256/256, 2 moteurs) ; R-716 balayages effacement/remplissage.
- 11:05–11:15 : R-717 (boucle à 2 chocs : impossible, u ≡ 0 mod 3), R-718 boucles à 3 chocs (4 pixels, 256/256 chacun).
- 11:12– : R-719 deux pas de suite (simulation 256 états, T = 397 574) ; R-720 boucle longue.

## Résultats (statuts)
| ID | Énoncé | Statut |
|---|---|---|
| R-715 | écran 2×2 sur les 4 sorties de cases du pas R-617 : 256/256, hx.py = C sur 64 | VÉRIFIÉ |
| R-716 | aucune écriture à 1 vaisseau n'est idempotente (effacer/remplir à l'aveugle impossible) | VÉRIFIÉ (balayage) |
| R-717 | boucle d'effacement à 2 chocs 0→4→2 vers RST2 : u ≡ 0 mod 3 toujours, R' demande 1 ou 2 | OBSERVÉ (calcul exact, 2 catalogues) |
| R-718 | boucle à 3 chocs 0→4→2→3 vers RST3 : trouvée pour les 4 pixels, 256/256 chacun (moteur C) | OBSERVÉ (1 moteur) |
| R-719 | 2 pas de suite à l'écran | en cours |

## Ce qui reste
- R-719 lecture C (T = 397 574) et 2e moteur ; R-720 boucle longue (écran allumé presque tout l'intervalle) ; images ; tâche 3 (lecture).

## En 10 lignes (L1)
(à écrire)

avancement : 35 % de l'objectif
