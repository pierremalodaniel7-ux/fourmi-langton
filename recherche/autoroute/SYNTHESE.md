---
title: "Conjecture de l'autoroute — note de synthèse (séances S1 à S9, 18/19-11-2026)"
---

# Conjecture de l'autoroute : ce qui est démontré (S1–S9, 18/19-11-2026)

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
| Germes | Toutes les configurations de ≤ 3 cases dans [−5,5]², de 4 cases dans [−4,4]², de 5 cases dans [−3,3]² (fourmi en 0, cap H) | 288 100 + 1 581 580 + 1 712 304 certifiées | R-105, R-108, R-110 |
| Germe R-20 | Le bout d'autoroute de 11 cases est certifié dès le pas 0 | 1 config | R-105 |
| Rebours | Le passé d'une configuration = le futur de la même grille, fourmi retournée (a − dir(h), cap h+2). Donc « autoroute à rebours pour tout décor fini » ⇔ conjecture | calcul direct, 60/60 contrôles | R-107 (sans doute connu) |

Partiel : boîtes 5×5 (fourmi au coin, cap H), les masques [0, 12 400 000) sont certifiés (S9), transitoire max 351 374 (R-118).

### Observations chiffrées (OBSERVÉ, pas démontré)

| | Énoncé | Données | Réf. |
|---|---|---|---|
| Records | record(n) = plus long transitoire d'une boîte n×n ; record(n+1) ≥ record(n) (recopie au coin) ; record(5) ≥ 351 374 (exhaustif partiel, S9), donc record(n) ≥ 351 374 pour n ≥ 5 ; la montée de colline ne fait pas mieux (8×8 : 220 334) | T(3) = 51 277, T(4) = 133 984 exacts | R-84, R-101, R-111, R-118 |
| Statistique | Pas certifié médian 5×5 dans [2 048, 4 096) ; 15 % ≥ 8 192 ; aucune corrélation entre nombre de cases noires et log(transitoire) (r² ≈ 0) | 6,8 M boîtes | R-104 |
| Boucle gelée | Sur l'autoroute nue, la boucle gelée L(t) est périodique (104), 34 valeurs, max 152 | calcul exact | R-102 (VÉRIFIÉ) |
| C-L | Si L(t) imite la suite de l'autoroute nue pendant 104 pas, une autoroute suit ; hors autoroute, imitation ≤ 89 pas | ≈ 74 300 configurations | R-103 |
| Germes | Transitoire minimal à k cases : 9 977, 310, 162, 126, 67 (k=4, dans [−4,4]²), 62 (k=5, [−3,3]²), …, 0 (k=11, germe R-20) | | R-105, R-108, R-110 |
| Ping-pong | Glouton « case la plus proche qui renverse l'autoroute » : 8 renversements, puis plus de case renversante à < 400 demi-périodes | 8 cases, certifié à 136 818 | R-109 |


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

## 3 bis. La contre-attaque (É7)

**S9 : autoroute × vieille trace (R-112 à R-115).** Une autoroute qui percute la trace d'une vieille autoroute (200 périodes,
4 orientations, tous les décalages utiles : 328 configurations) construit toujours une autoroute certifiée (2ᵉ moteur d'accord
328/328). En perpendiculaire : 8 classes (traverse, « relais » qui longe la trace et prolonge la vieille autoroute, remontée jusqu'au
germe de la trace, demi-tour), indépendantes de la longueur et du point de croisement loin des bouts (R-113) ; de face, l'issue ne
dépend que de P mod 12 (R-115). Une vieille trace se comporte donc comme un « site » de plus. Germes : 6 à 9 cases dans [−2,2]²
toutes démontrées (R-114). T6 rendu reproductible (R-116) ; T7 (C) lancé : 53/484 bases complètes (R-119).

Pas de décor fini qui occupe la fourmi indéfiniment. Le seul mécanisme de retour vu dans T1–T6 est le **demi-tour** (une case
sur la bande renvoie l'autoroute sur sa trace jusqu'au site précédent) ; le nombre de traversées est fini et fixé par la classe.
Le glouton R-109 s'épuise au 9ᵉ renversement. Détails : `E7_contre_attaque.md`.

## 4. Ce qu'il faut relire en priorité

1. Lemme 3 de `E2b_couplage.md` (changement de repère), surtout le point 2 corrigé en S4 (R-92) : les cases hors des diagonales
   touchées valent la même chose dans un repère identité, mais pas dans un repère translation.
2. La fermeture des ensembles d'accord dans le passage k₀+2 → k₀+4 (argumentée, pas écrite case par case).
3. Le lemme de transport et son dual (R-95, R-96, R-98) et l'assemblage de T6 (énumération des cas).
4. Le code de `ant multi` (`recherche/autoroute/ant_controle.c`) : 4 failles trouvées et corrigées en relisant (R-89, R-92,
   test Z pour NS impair, HV[−2]). Aucune n'a changé un résultat, mais c'est un signe qu'il faut une relecture extérieure.
5. Le certificat lui-même (`E1_certificat.md`, `src/fourmi -cert`) : tout « DÉMONTRÉ » par calcul en dépend. Le relire une fois
   suffit pour R-84, R-105, R-108, R-110, R-111 (ces résultats n'utilisent pas les couplages).
6. R-107 (rebours) : 5 lignes à vérifier à la main.

## 5. Nouveauté

Littérature consultée (`deja_connu.md`, plus 2 recherches web le 18/11) : la conjecture générale est ouverte. Le seul résultat
général connu est que la trajectoire n'est jamais bornée (Bunimovich–Troubetzkoy, Cohen–Kong). Rien trouvé sur des familles
infinies de configurations démontrées, comme « une case noire n'importe où ». L'idée du certificat (autoroute + devant blanc ⇒
pour toujours) est sans doute connue de façon informelle.

### Nouveauté, résultat par résultat (S9, 19-11)

| Résultat | Statut | Nouveauté |
|---|---|---|
| Certificat d'autoroute (R-83) | DÉMONTRÉ | principe sans doute folklore ; pas trouvé écrit |
| Boîtes 3×3, 4×4, 5×5 partiel (R-84, R-111) | DÉMONTRÉ | le dépôt GitHub evanmack45 simule le 5×5 (non relu) ; pas de preuve publiée trouvée |
| T1–T5 (une case, îlots 3×3 n'importe où) | DÉMONTRÉ, à relire | pas trouvé ; le plus proche : simulations de Gajardo–Lutfalla–Rao 2024 (1 case à distance ≤ 3) |
| T6 (deux cases éparses) | DÉMONTRÉ, à relire | pas trouvé |
| Germes ≤ 5 cases (R-105, R-108, R-110) | DÉMONTRÉ | pas trouvé |
| Rebours (R-107) | DÉMONTRÉ | sans doute connu (réversibilité de la fourmi, classique) |
| Records de transitoire (R-101, R-111, R-118) | OBSERVÉ | pas trouvé. MFCS 2026 (Etse, arXiv 2606.26677) borne le **temps d'échappement** d'un domaine fini (borne factorielle pour les carrés) : autre question (sortie du domaine, pas arrivée de l'autoroute) |
| C-L, boucle gelée (R-102, R-103) | OBSERVÉ / VÉRIFIÉ | pas trouvé |

## 6. Prochaines étapes

Relecture humaine des preuves (§4) avant toute diffusion ; trois cases éparses (T7, ≈ 8 h, plan dans `E2_epars.md`) ;
terminer le 5×5 ; germes exacts à 6–10 cases ; É7 « autoroute × trace ».

## 7. Fichiers

`E0_controle.md` (deux moteurs), `E1_certificat.md` (certificat), `E2_epars.md` et `E2b_couplage.md` (T1–T6),
`E4_transitoires.md`, `E5_observables.md`, `E6_germes.md`, `E7_contre_attaque.md` ; rapports `rapports/S1…S9` ;
résultats 5×5 `resultats/box5/`.
