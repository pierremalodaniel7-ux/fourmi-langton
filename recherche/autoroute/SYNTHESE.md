---
title: "Conjecture de l'autoroute — note de synthèse (séances S1 à S5, 18-11-2026)"
---

# Conjecture de l'autoroute : ce qui est démontré (S1–S5, 18-11-2026)

*Note de travail pour relecture. Fourmi RL classique, fourmi en (0,0) cap haut, y vers le bas, norme max(|x|, |y|).
Tous les énoncés « DÉMONTRÉ » reposent sur un calcul exact fini et sur les lemmes écrits ci-dessous ; ils restent
**à faire relire par un humain**.*

## 1. L'outil : le certificat d'autoroute (R-83)

Si, à un instant t, les 104 pas suivants « à blanc » lisent une fenêtre V et reviennent au même cap avec un déplacement d ≠ 0,
si le motif se recopie (F2), si les cases neuves sont blanches (F3), si V est convexe le long de d (F4), et si la bande
⋃(V + kd) ∖ V est blanche, alors la fourmi construit l'autoroute pour toujours. La preuve est une récurrence sur les
périodes. La vérification est finie, car au-delà de la boîte « support initial ∪ cases visitées » tout est blanc.
Implémenté dans `src/fourmi -cert`. Exemple : le départ blanc est démontré dès 9 977.

## 2. Les théorèmes

| | Énoncé | Calcul | Réf. |
|---|---|---|---|
| Boîtes | Boîtes 3×3 et 4×4 (fourmi au coin, cap haut) : toutes les configurations | 512 + 65 536 certifiées ; T(3) = 51 277, T(4) = 133 984 | R-84 |
| T1 | Départ blanc + **une case noire n'importe où** | 90 601 proches + 22 classes lointaines | R-85 à R-87 |
| T2 | + **un îlot de 2 cases voisines** n'importe où | 362 404 + 128 classes | R-76 |
| T3 | + **un îlot de 3 cases en L ou en ligne** n'importe où | 246 072 + 228 classes | R-78 |
| T4 | + **tout îlot contenu dans un carré 3×3** (400 formes) n'importe où | 1 813 428 + 76 000 + 15 200 classes | R-80, R-81, R-92 |
| T5 | Une configuration C₀ déjà certifiée + une case noire n'importe où (exemple traité : l'îlot 3×3 le plus lent) | 39 429 + 22 classes | R-90 |
| T6 | **Deux cases noires éparses** : \|c₁\|, \|c₂\| ≥ 417 et \|c₁ − c₂\| ≥ 545 ⇒ autoroute pour toujours | 683 080 cas proches, 484/484 paires de classes lointaines | R-93 à R-98 |

Partiel : boîtes 5×5, les 6 000 000 premières configurations (sur 33,5 M) sont certifiées, transitoire max 209 637.

## 3. La méthode pour « loin » : les couplages

Un îlot posé loin dans la bande de l'autoroute, à la distance k, a pour tout k ≥ k₀ la même histoire qu'à k₀, au temps près.

- **Phase 0 (translation)** : X(k+2) au temps t+104 est X(k) au temps t, translaté d'une période d. Les deux mondes diffèrent
  seulement sur un ensemble fixe D près du germe (p = −x+y ≤ 25). Le couplage dure tant que la fourmi lit des cases de p > 21.
- **Changement de repère** : quand la fourmi repart sur sa propre trace (un « rouleur » périodique), le bon repère devient
  l'identité près du germe, puis de nouveau la translation près du site, etc. À chaque changement, on prouve que les deux
  mondes coïncident sur un ensemble explicite : la fenêtre, p < L ou p > H, les diagonales jamais touchées, et la règle
  « un pas de translation » fermée par chaînes.
- **Récurrence** : toutes les conditions se vérifient sur X(k₀) seul et se transmettent de k à k+2.
- **Deux cases** : récurrence en la 2e distance (base = blanc + c₁), puis en la 1re distance, puis un **lemme de transport**
  qui relie les deux (R-95, R-96), et son « dual » pour les 2 paires où la récurrence en k₁ utilise la règle (R-98).

Écrit en détail : `recherche/autoroute/E2b_couplage.md`. Vérificateurs : `ant multi` (conditions), `ant deux` (simule
X(k) et X(k+2) et compare pas à pas : 768 + 484 cas, tous exacts).

## 4. Ce qu'il faut relire en priorité

1. Lemme 3 de `E2b_couplage.md` (changement de repère), surtout le point 2 corrigé en S4 (R-92) : les cases hors des diagonales
   touchées valent la même chose dans un repère identité, mais pas dans un repère translation.
2. La fermeture des ensembles d'accord dans le passage k₀+2 → k₀+4 (argumentée, pas écrite case par case).
3. Le lemme de transport et son dual (R-95, R-96, R-98) et l'assemblage de T6 (énumération des cas).
4. Le code de `ant multi` (`recherche/autoroute/ant_controle.c`) : 4 failles trouvées et corrigées en relisant (R-89, R-92,
   test Z pour NS impair, HV[−2]). Aucune n'a changé un résultat, mais c'est un signe qu'il faut une relecture extérieure.

## 5. Nouveauté

Littérature consultée (`deja_connu.md`, plus 2 recherches web le 18/11) : la conjecture générale est ouverte. Le seul résultat
général connu est que la trajectoire n'est jamais bornée (Bunimovich–Troubetzkoy, Cohen–Kong). Rien trouvé sur des familles
infinies de configurations démontrées, comme « une case noire n'importe où ». L'idée du certificat (autoroute + devant blanc ⇒
pour toujours) est sans doute connue de façon informelle.

## 6. Prochaines étapes

Trois cases éparses (même schéma, base = blanc + c₁ + c₂) ; terminer le 5×5 ; une
relecture humaine des preuves avant toute diffusion.
