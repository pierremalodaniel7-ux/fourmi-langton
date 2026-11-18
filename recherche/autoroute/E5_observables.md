# É5 — Observables : la boucle gelée (S7, 18-11-2026)

**Boucle gelée** à l'instant t : l'orbite de la fourmi si l'on cessait de retourner les cases (même règle de virage). Cette
dynamique est une bijection sur les états (position, cap), donc l'orbite est un cycle ; L(t) = sa longueur. Outil : `ant obs`,
`ant imite` (2ᵉ moteur, `recherche/autoroute/ant_controle.c`).

## Faits mesurés
1. L(t) est toujours un multiple de 4 (cohérent avec R-03 : longueur de cycle ≡ 0 mod 4).
2. **Correction de l'acquis** « L ≤ 112 sur l'autoroute » (échantillonné tous les 20 pas) : sur l'autoroute nue loin du germe,
   L suit une suite **périodique de période 104**, avec **34 valeurs, max 152**, et la boucle reste à ≤ 11 cases (norme max) de la
   fourmi ; près du germe (t ∈ [9 977, 12 000]) L monte jusqu'à 172 ; juste après le début d'autres autoroutes, jusqu'à 4 072
   (la boucle repasse dans la tache).
3. **Pas de seuil** : pendant le chaos L descend à 4 et monte à 1 388 (départ blanc) ; 65 % des pas de chaos ont une valeur de L
   « permise » sur l'autoroute. Aucun seuil sur L ne sépare chaos et autoroute.
4. **Imitation de la suite** (bien plus fine que les valeurs) : on compte la plus longue suite de pas consécutifs où L(t) égale
   la suite périodique de l'autoroute nue (pour une phase φ). Campagne : 512 boîtes 3×3 + 3 000 4×4 + 800 5×5 + 300 6×6 aléatoires
   (4 612 configurations) : **hors des plages d'autoroute (trace périodique de période 104 pendant ≥ 104 pas, 1re période
   comprise), l'imitation dure au plus 49 pas** (pire : 6×6 m = 33008227804) ; distribution : ≤ 19 pour 99 % des cas.
   Le record 5×5 (209 637) contient une **autoroute temporaire** de 1 054 pas (t ≈ 127 800–128 852) pendant laquelle L imite la
   suite 758 pas ; hors autoroute, 22 pas au plus.
5. Après le début de l'autoroute finale, L se cale définitivement sur la suite nue entre **−4 et +623 pas** (même campagne).

6. **Configurations diverses** (`BASE=… ./ant imite 1 0 CERT`) : 300 cases uniques (T1), 150 paires de cases loin, 100 cases
   lointaines dans la bande, 150 îlots 3×3 — dont 302 avec une autoroute **temporaire** avant un choc : imitation hors plages
   d'autoroute ≤ **83 pas** ; le pire (îlot {(−28,9),(−26,10),(−28,11)}) : L continue d'imiter 83 pas **après** la cassure de
   l'autoroute (t = 10 670) — la boucle, locale, ne voit pas tout de suite le choc.

## Conjecture C-L (OBSERVÉE, 4 612 + 700 configurations + records)
Si la longueur de la boucle gelée suit exactement la suite de l'autoroute nue pendant **104 pas consécutifs**, alors la fourmi
est en train de construire une autoroute 104 (la trace des couleurs lues est périodique de période 104 à ce moment) — éventuellement
temporaire (elle peut se briser sur des débris plus loin), ou vient de la construire il y a moins de 104 pas.
Marge observée : 49 (boîtes) et 83 (après un choc) < 104 — mince ; variante plus sûre : **208 pas** (deux périodes).
Réciproque (lemme, esquisse) : sur une autoroute certifiée, dès que la fourmi est à plus de 11 cases de toute case non blanche qui
n'a pas été écrite par l'autoroute, L(t) est exactement la suite nue (la boucle ne lit que des cases à ≤ 11 de la fourmi, et elles
sont alors celles de l'autoroute nue). D'où le calage observé de −4 à +623 pas.
Intérêt : un détecteur d'autoroute **local** (il ne regarde que la boucle autour de la fourmi), différent de la périodicité de la trace.

## Nouveauté
`deja_connu.md` : rien ; 1 recherche web (« frozen loop » / invariant pour détecter l'autoroute) : rien trouvé.

## Autres observables (R-104)
- Nombre de cases noires initial : **aucune corrélation** avec le transitoire (r² ≈ 0, 5×5 et 6×6 aléatoires).
- Distribution du transitoire (6,8 M boîtes 5×5) : médiane dans [2 048, 4 096) ; 15,2 % ≥ 8 192 ; 4,8 % ≥ 16 384 ; 0,05 % ≥ 65 536.

## Lemme de calage (DÉMONTRÉ, preuve courte)
*Énoncé.* Sur l'autoroute nue loin du germe, pour chacune des 104 phases, la boucle gelée ne lit que des cases à distance ≤ 11
(norme max) de la fourmi (calcul exact, t = 20 000…20 103, valable pour toute période ultérieure par périodicité).
Soit une configuration X dont l'autoroute est certifiée à T0. Si à l'instant t ≥ T0 toutes les cases à distance ≤ 11 de la
fourmi ont, dans X, la même couleur que dans l'autoroute nue à la même phase (après translation), alors L_X(t) = L_nue(phase).
*Preuve.* La boucle gelée est déterminée pas à pas par les couleurs qu'elle lit ; par récurrence sur sa longueur, la boucle de X
lit les mêmes cases que celle de l'autoroute nue (toutes à ≤ 11), donc elle est identique. ∎
*Conséquence.* Les cases à ≤ 11 de la fourmi coïncident avec l'autoroute nue dès que la fourmi est à plus de 11 cases de toute case
écrite avant T0 ou noire au départ (devant : bande certifiée blanche ; derrière : trace écrite par l'autoroute elle-même) ;
l'autoroute avançant d'une diagonale de 2 par période, le calage arrive au plus ≈ 52·(distance + 11) pas après T0.
Observé : calage de −4 à +623 pas après le début (R-103). La conjecture C-L est la **réciproque** de ce lemme.
