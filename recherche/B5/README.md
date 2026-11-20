# B5 — Carré 5×5 : toute configuration mène à l'autoroute 104 (calcul exhaustif exact)

## Énoncé
**B5.** Fourmi RL classique. Pour toute configuration de cases noires contenue dans un carré 5×5, la fourmi étant
sur n'importe quelle case du carré avec n'importe quel cap, la fourmi finit par construire l'autoroute de période 104,
pour toujours.

Conventions (= `recherche/autoroute/ant_controle.c`) : x à droite, y en haut, cap 0 = haut, 1 = droite, 2 = bas,
3 = gauche ; blanc → droite, noir → gauche, puis inverser la case et avancer. Masque : bit i ↔ case (i mod 5, i div 5),
coin bas-gauche du carré en (0,0).

## Symétrie (réduction au cap « haut »)
Soit ρ le quart de tour horaire autour du centre (2,2) du carré : ρ(x,y) = (2 + (y−2), 2 − (x−2)), et R(u,v) = (v,−u)
sa partie linéaire (R envoie le cap h sur h+1). ρ est une isométrie directe : elle conserve « tourner à droite / à
gauche » ; donc si l'état (grille C, position a, cap h) donne en un pas (C', a', h'), l'état (C∘ρ⁻¹, ρ(a), h+1) donne
en un pas (C'∘ρ⁻¹, ρ(a'), h'+1) : toute trajectoire est envoyée sur une trajectoire (autoroute 104 ↦ autoroute 104,
même instant de certificat, le lemme R-83 étant invariant par isométrie). ρ envoie le carré {0..4}² sur lui-même.
Enfin, pour un état de cap h, ρ⁻ʰ en donne l'unique image de cap 0 = haut. ⇒ il suffit de traiter le cap haut :
25 positions × 2²⁵ coloriages = 838 860 800 cas.

## Méthode (programme `b5.c`)
1. **Feuille = lemme du certificat** (R-83, `recherche/autoroute/E1_certificat.md`), p = 104. À l'instant s on prend
   V, Pv, Pa dans l'histoire réelle des 104 pas suivants (le jeu « à blanc » est le jeu réel pendant p pas), on teste
   F1–F4, puis **Z dans la boîte « carré entier ∪ toutes les cases visitées jusqu'à l'instant courant »** (hors de cette
   boîte tout est blanc ; les cases du carré non encore lues peuvent être noires et sont donc dans la boîte).
   Un instant s n'est testé que si les couleurs lues sur [s, s+104) et [s+104, s+208) coïncident (condition
   nécessaire : un certificat en s rend la suite lue périodique dès s) ; le test se fait sur l'état exact à s
   (on défait les pas s..t−1). On obtient le **premier** instant certifié.
2. **Arbre de choix.** Les 25 cases du carré sont inconnues, tout le reste est blanc. À la première lecture d'une case
   inconnue : branche blanc puis noir, retour arrière par journal (position de chaque pas, on re-retourne les cases).
   Si le certificat est vrai sauf qu'une case de Z est inconnue (aucune case de Z n'est noire connue) : on branche sur
   cette case (blanc : on reteste ; noir : échec à cet instant). Ainsi chaque coloriage compatible avec une feuille a
   exactement l'instant de certificat de la feuille. Une feuille prouve 2^(nb d'inconnues restantes) coloriages.
   Pas de certificat avant Tmax = 5·10⁶ pas (ou bord de la grille 2048²) → feuille NON RÉSOLUE (listée).
3. **Comptage** : par position, somme des 2^(inconnues) des feuilles = 2²⁵ exactement.
4. **Découpage / reprise** : chaque position est coupée en 64 sous-arbres (les 6 premiers choix imposés, `b5 arbre
   5 X Y PREFIXE TMAX`) ; une feuille rencontrée avant la fin du préfixe n'est comptée que dans le sous-arbre dont les
   bits restants sont 0. Un fichier par sous-arbre (`data/B5/jobs/pXY_PREFIXE.res`), sauté s'il existe déjà.

## Reproduire
```
cd recherche/B5 && gcc -O3 -march=native -o b5 b5.c && gcc -O2 -o ant_controle_b5 ant_controle_b5.c
python3 -c "import random; r=random.Random(20261119)
for _ in range(100000): print(r.randrange(5), r.randrange(5), r.getrandbits(25))" > ../../data/B5/echantillons.txt
./lance.sh 5000000          # 1 600 sous-arbres, tous les cœurs, reprise automatique
python3 agrege.py           # positions/pos_XY.txt, tableau.md, nonresolus.txt, comptage exact
./controles.sh              # contrôles croisés (a), (b), (c)
```
`ant_controle_b5.c` = copie de `recherche/autoroute/ant_controle.c` avec un seul ajout : le mode `lotpos`
(fourmi en (AX,AY) au lieu de (0,0)) ; la fonction de simulation n'est pas modifiée.

## Validation (étape 0)
| Test | Résultat |
|---|---|
| 3×3, coin, cap haut : arbre vs brut, masque par masque | 512/512 identiques (instant + dérive), 499 feuilles, partition exacte |
| 4×4 : arbre vs brut | 65 536/65 536 identiques, 60 850 feuilles |
| 4×4 : arbre vs `src/fourmi -cert` (moteur indépendant, grille hachée) | 65 536/65 536 instants identiques |
| 4×4 : somme des 8 sous-arbres (préfixe 3) | 60 850 feuilles, poids 65 536, max 133 984 = arbre complet |
| T(3) | 51 277 (masque 221) |
| T(4) | 133 984 (masque 32972) |
| 5×5 masque 11433907 | 351 374 = référence |

**Écarts avec les références 3×3 = 51 377 et 4×4 = 134 065.** Nos valeurs 51 277 et 133 984 sont égales aux débuts
R-82 (ant_controle) et aux CERT de `src/fourmi`. Avec `fourmi -c0 t` on a listé les instants certifiés après le début :
décalages 0–68, 81–94, 100–110, … (les phases 69–80 et 95–99 échouent sur F2–F4, comme les 17 phases de R-83).
51 377 = début + 100 et 134 065 = début + 81 sont exactement les débuts de plages certifiées qui suivent un trou :
le vérificateur indépendant a commencé sa recherche après le premier instant certifiable (dans un trou) et a donné le
premier certificat **après son point de départ**. Le premier certificat est bien 51 277 / 133 984 (certifié par deux
programmes). Pour le masque 5×5 11433907 il est parti assez tôt : accord exact (351 374).

## Résultats (19-20/11)
**25/25 positions, cap haut : chaque position a ses 64 sous-arbres, somme des poids = 2²⁵ = 33 554 432 exactement,
0 non résolu (Tmax = 5·10⁶), toutes les feuilles certifiées avec une dérive (±2,±2) (autoroute 104).**
Total : 838 860 800 coloriages, 702 113 441 feuilles (83,7 % de 25·2²⁵ : la fourmi lit presque toujours tout le carré),
3,28·10¹² pas simulés (≈ 3 911 par coloriage), 35 856 s·cœur ≈ 10,0 h·cœur (≈ 9,1·10⁷ pas/s/cœur), 4 cœurs ;
temps réel : 18 h 17 – 19 h 11 (580 sous-arbres) puis 22 h 34 – 00 h 11 (1 020 sous-arbres ; le premier lancement
s'est arrêté avec la fin du tour de conversation, reprise automatique sans perte).

**T(5) = 351 374** (fourmi en (0,0) cap haut, masque 11433907) = maximum des 25 records ; par la symétrie, c'est le
plus long transitoire (premier instant certifié) pour toute position du carré et tout cap.

| position (x,y) | sous-arbres | feuilles | poids certifié | non résolus | 1er certificat max | masque du record | plus court | temps (s·cœur) |
|---|---|---|---|---|---|---|---|---|
| 0,0 | 64/64 | 28 588 484 | 33 554 432 = 2^25 | 0 | 351 374 | 11433907 | 60 | 1481 |
| 1,0 | 64/64 | 28 511 923 | 33 554 432 = 2^25 | 0 | 218 072 | 27970974 | 56 | 1456 |
| 2,0 | 64/64 | 28 366 365 | 33 554 432 = 2^25 | 0 | 234 449 | 4455031 | 48 | 1447 |
| 3,0 | 64/64 | 28 412 580 | 33 554 432 = 2^25 | 0 | 233 237 | 28372497 | 65 | 1421 |
| 4,0 | 64/64 | 28 490 693 | 33 554 432 = 2^25 | 0 | 273 825 | 7176115 | 44 | 1420 |
| 0,1 | 64/64 | 28 092 041 | 33 554 432 = 2^25 | 0 | 273 824 | 8313294 | 27 | 1414 |
| 1,1 | 64/64 | 28 367 346 | 33 554 432 = 2^25 | 0 | 233 234 | 31064756 | 46 | 1403 |
| 2,1 | 64/64 | 27 835 784 | 33 554 432 = 2^25 | 0 | 231 822 | 28799897 | 51 | 1379 |
| 3,1 | 64/64 | 27 987 883 | 33 554 432 = 2^25 | 0 | 273 823 | 7176107 | 26 | 1394 |
| 4,1 | 64/64 | 28 698 953 | 33 554 432 = 2^25 | 0 | 233 235 | 28372489 | 59 | 1506 |
| 0,2 | 64/64 | 27 520 199 | 33 554 432 = 2^25 | 0 | 219 673 | 30865118 | 52 | 1426 |
| 1,2 | 64/64 | 27 886 800 | 33 554 432 = 2^25 | 0 | 273 822 | 8313262 | 37 | 1437 |
| 2,2 | 64/64 | 27 815 144 | 33 554 432 = 2^25 | 0 | 233 232 | 31064692 | 32 | 1420 |
| 3,2 | 64/64 | 27 890 705 | 33 554 432 = 2^25 | 0 | 233 233 | 28372233 | 33 | 1428 |
| 4,2 | 64/64 | 28 063 130 | 33 554 432 = 2^25 | 0 | 231 823 | 31455345 | 24 | 1443 |
| 0,3 | 64/64 | 28 118 339 | 33 554 432 = 2^25 | 0 | 273 820 | 8312238 | 47 | 1474 |
| 1,3 | 64/64 | 28 006 839 | 33 554 432 = 2^25 | 0 | 233 230 | 6068407 | 30 | 1430 |
| 2,3 | 64/64 | 27 728 720 | 33 554 432 = 2^25 | 0 | 233 231 | 28368137 | 31 | 1408 |
| 3,3 | 64/64 | 27 421 061 | 33 554 432 = 2^25 | 0 | 231 817 | 18809847 | 34 | 1405 |
| 4,3 | 64/64 | 27 923 088 | 33 554 432 = 2^25 | 0 | 233 223 | 19336923 | 47 | 1433 |
| 0,4 | 64/64 | 28 338 524 | 33 554 432 = 2^25 | 0 | 231 811 | 18390007 | 28 | 1493 |
| 1,4 | 64/64 | 27 760 108 | 33 554 432 = 2^25 | 0 | 218 568 | 12422578 | 53 | 1421 |
| 2,4 | 64/64 | 27 778 129 | 33 554 432 = 2^25 | 0 | 273 821 | 27852140 | 48 | 1435 |
| 3,4 | 64/64 | 27 972 621 | 33 554 432 = 2^25 | 0 | 231 824 | 32742875 | 25 | 1441 |
| 4,4 | 64/64 | 28 537 982 | 33 554 432 = 2^25 | 0 | 233 236 | 31097015 | 68 | 1443 |

« plus court » = plus petit premier certificat de la position. Temps = somme des 64 sous-arbres (s·cœur).
Remarque : plusieurs records valent 273 820–273 825 ou 233 223–233 237 pour des positions différentes, avec des masques
voisins : probablement le même chaos décalé de quelques pas (non vérifié).

## Contrôles croisés (étape 3)
Voir `controles_resultats.txt`.
| Contrôle | Résultat |
|---|---|
| (a) 100 000 tirages (pos, masque) au hasard, graine 20261119 (99 997 distincts) : instant de la feuille de l'arbre vs `src/fourmi -cert` | 100 000/100 000 identiques |
| (a) mêmes tirages vs `ant_controle_b5 lotpos` (moteur de ant_controle.c, début d'autoroute) | 100 000/100 000 : autoroute détectée, début ≤ certificat (égal pour 77 472, écart max 3 pas) |
| (b) record de chaque position : arbre / `b5 brut` / `src/fourmi -cert` / ant_controle | 25/25 : mêmes instants (ant_controle : début = certificat ou −1) |
| (c) coin bas-gauche : records des 46 tranches de `resultats/box5/` (masques [0, 9,2 M)) recalculés | 46/46 identiques ; max box5 252 046 ≤ 351 374 (record hors des tranches déjà calculées) |
Durée des contrôles : 2 min 46 s (1 cœur).

## Statut
**B5 DÉMONTRÉ (sous réserve de relecture humaine du code de l'arbre, `b5.c`, fonctions `certifie` et `arbre`)** :
0 non résolu, comptages exacts (25 × 2²⁵), contrôles 100 % d'accord. La preuve = lemme R-83 (démontré) +
calcul exact fini de 838 860 800 cas + symétrie ci-dessus. Corollaire : T(5) = 351 374 exactement (le premier
certificat ; le début réel de l'autoroute peut être jusqu'à quelques pas plus tôt, cf. ant_controle).

## Estimation 6×5 (non calculé)
Rectangle 6×5 : seule la rotation d'un demi-tour le conserve ⇒ 2 caps (haut, droite) × 30 positions × 2³⁰ =
6,4·10¹⁰ cas (77 × B5). Au coût mesuré ici (4,27·10⁻⁵ s·cœur par coloriage, arbre peu efficace), ≈ 2,75·10⁶ s·cœur
≈ 765 h·cœur ≈ 8 jours sur 4 cœurs — minorant, car les transitoires grandissent avec le support. Il faudrait
d'abord gagner un facteur ≥ 10 (par ex. mémoriser les états du chaos déjà certifiés, ou partager les préfixes de
trajectoire entre positions de départ).
