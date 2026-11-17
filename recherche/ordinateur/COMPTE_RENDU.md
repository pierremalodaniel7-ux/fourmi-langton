# R-39 — Ordinateur à fourmis : additionneur par modules enchaînés (16-11, soir)

**Résultat.** Un module « additionneur complet » (2 fourmis + cases) recopié n fois donne un additionneur
n bits ; la retenue passe d'une fourmi à la suivante par une autoroute. Germe livré : 4 bits, réglé sur 3+2.

## Ce qui marche (statut)
| Étape | Entrées testées | Statut |
|---|---|---|
| Module seul (c, a, b), retenue émulée | 8/8 | VÉRIFIÉ (calcul exact, fini) |
| 1 bit (module 0 seul) | 4/4 | VÉRIFIÉ |
| 2 bits (3+2 → S0 ↙ S1 ↘ K1 ↗ = 101) | 16/16 | VÉRIFIÉ |
| 3 bits | 64/64 | VÉRIFIÉ |
| 4 bits (germe livré) | 256/256 | VÉRIFIÉ + recalculé par un 2e programme (JavaScript) : 256/256 |
| 5 bits | 1024/1024 | VÉRIFIÉ (moteur C seulement) |
« Vérifié » = la direction de chaque fourmi lectrice, au pas de lecture indiqué, est juste pour toutes les
entrées (énoncé sur un temps fini ; rien n'est affirmé sur l'infini).

## Comment c'est fait
1. Retenue = autoroute ↗ sur une voie exacte (x+y et phase fixées). Un lecteur ↘ qui croise sa trace est
   décalé de 8 voies (classe de croisement trouvée parmi les 8 possibles ; 3 seulement donnent un décalage propre).
2. Lecteurs (germe R-17) arrivant par une longue voie ↙ puis tournés ↘ par une case : le retard réglable
   (950 périodes par module) laisse passer la retenue avant que le module suivant lise.
3. Arbre de cases (méthode R-37) : S bascule ↘/↙ à chaque 1 (somme = parité) ; K bascule ↘/↗ (majorité,
   une case « noire si b=0 »).
4. Aiguillage : les 3 feuilles « retenue = 1 » de K reçoivent 2 cases chacune pour sortir EXACTEMENT sur la
   même autoroute (voie x+y=220, x−y ≡ 2 mod 4). La retenue sortante = retenue entrante décalée de
   V = (1311, −1091) : c'est ce qui rend le module recopiable tel quel.

## Ce qui ne marche pas / limites
- La lecture « à la fin » est fausse dans 120/256 cas en 4 bits : une sortie ↙ finit par heurter les
  traces des modules précédents (à ~1 700 cases du module). Il faut lire chaque fourmi à son pas (fiche).
- Une entrée b_m = 0 demande une case noire (b_m = 1 : cinq cases). a_m = 1 : quatre cases.
- Germe étendu : x de −55 à 11 075, y de −10 534 à 14 ; ~420 000 pas.
- Une feuille de K a un chaos long (≈ 24 000 pas) ; ça passe mais c'est le point fragile.
- Mémoire / horloge : pas commencé (OUVERT).
- Numérotation : le Drive a des R-36 à R-38 « ordinateur » ; le journal du dépôt a un autre R-36. Ce travail est R-39.

## Déjà connu
Gajardo, Moreira, Goles, *Complexity of Langton's ant* (Discrete Appl. Math. 117, 2002) : une seule fourmi
calcule tout circuit booléen (P-difficile). Ici : autre mécanisme (plusieurs fourmis, retenue portée par
une autoroute, modules recopiables). Le principe « la fourmi calcule » n'est pas nouveau.

## Reproduire (dossier recherche/ordinateur/)
    gcc -O2 -shared -fPIC -o libmoteur.so moteur.c
    python3 construit_module.py && python3 aiguillage2.py 220 2 && python3 verif_module.py   # module (≈ 30 s)
    python3 chaine.py 4 436400 95000          # 256 entrées, ≈ 7 s
    python3 export.py                          # germe_ordinateur.json + entrees.json
    node verif_independante.js tout            # 2e programme, ≈ 32 s
Note : `aiguillage2.py` lit `module_sans_aig.json` (module avant aiguillage) et écrit `module.json`.

## Temps de calcul mesurés
Module 9 s ; aiguillage 16 s par essai (5 essais) ; 2-3-4 bits 7 s ; 5 bits 48 s ; JavaScript 4 bits 32 s.
Situations simulées : quelques milliers de petites (recherche de cases) + 1 364 germes complets (16+64+256+1024+4).
