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

## Résultats
(à compléter à la fin du calcul : voir `tableau.md`)
