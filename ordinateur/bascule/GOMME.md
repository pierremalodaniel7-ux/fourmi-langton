# Gomme et bascule — nuit du 25/11/2026

## 1. La gomme (R-140)

**Énoncé.** Règle RL (ou LR, NN, UU ; 2 couleurs). Notons l'état d'une fourmi (x, h) : case x, cap h = direction de son
dernier déplacement. Gomme : R(x, h) = (x − e_h, h + 2). Si on applique R à la fourmi après t pas, puis qu'on joue t pas,
la grille redevient celle du départ et la fourmi est en R(état de départ). Appliquer R encore : état de départ exact.

**Preuve (un pas suffit, puis récurrence).** Un pas : la fourmi en (x, h) lit la couleur c de x, prend le cap h' = h + t_c,
retourne la case (c → 1 − c), va en x + e_h'. Elle est en (y, h') avec y = x + e_h'. Gommée : R(y, h') = (x, h' + 2).
- Cas blanc (c = 0, t_0 = +1 = droite) : h' = h + 1. Gommée elle est en x (maintenant NOIRE) avec le cap h + 3.
  Noir → gauche : cap h + 3 − 1 = h + 2 ; la case redevient BLANCHE ; elle va en x + e_{h+2} = x − e_h.
  Nouvel état (x − e_h, h + 2) = R(x, h). ✔
- Cas noir (c = 1, t_1 = −1) : h' = h − 1. Gommée : en x (maintenant BLANCHE) avec le cap h + 1. Blanc → droite :
  cap h + 2 ; la case redevient NOIRE ; elle va en x − e_h. Nouvel état R(x, h). ✔

Donc S∘R∘S = R (S = un pas), d'où (S∘R)^t... : après la gomme, chaque pas défait exactement le pas d'avant.
Condition générale (2 couleurs, virages t_0, t_1) : t_0 + t_1 ≡ 0 (mod 4) → RL, LR, NN, UU. RR et LL : NON (vérifié : RR
cycle 4, pas d'effacement). 3 couleurs ou plus (LLR…) : IMPOSSIBLE avec la même règle (la fourmi ne fait qu'avancer les
couleurs c → c+1 ; défaire demande c+1 → c). L'hexagonal à 2 couleurs marche si t_0 + t_1 ≡ 0 (mod 6) (H:R1L1, H:R2L2 testés).

**Plusieurs fourmis.** Un tour = S_{n−1}∘…∘S_0. Son inverse = R∘(S_0∘S_1∘…∘S_{n−1})∘R : gommer TOUTES les fourmis et
jouer dans l'ordre INVERSE (n−1 d'abord). Sans inverser l'ordre : faux dès que les fourmis interagissent.

**Vérifications (2 moteurs).** `src/fourmi -gomme t -T 2t+10` (nouvelle option) et `ordinateur/bascule/moteur2.py` (Python) :
départ blanc t = 10, 500, 11 000, 10⁵, 10⁶ → grille redevenue blanche (EFFACE au pas 2t) ; autoroute 104 du germe R-20 :
t = 1 040, 104 000, 1 040 000 → effacée, germe intact ; 3 fourmis + 1 case : effacé avec ordre inversé, 892 cases fausses
sans inverser l'ordre (Python) ; 0,0,H ; 40,0,G : 488 cases fausses sans inverser l'ordre.
**Connu** : c'est la réversibilité de la fourmi (Lorentz lattice gas « flipping rotators » ; Tsukiji & Hagiwara 2011,
Algorithms 4(1) : « the reverse of a walking course is defined by reversing the order of the coloring changes and reversing
the ants' moves »). Statut : VÉRIFIÉ (preuve + 2 moteurs), CONNU.

## 2. Pourquoi aucune pièce de cases ne renvoie une fourmi seule en gomme (R-141)

**Invariant (déjà R-09).** I = (x + y + h) mod 2 ne change jamais : à chaque pas, x + y change de ±1 ET h change de ±1.
**Or R change I** : R(x, h) = (x − e_h, h + 2) : x + y change de ±1, h de 2. Donc une fourmi n'est JAMAIS, à aucun instant,
dans l'état R(un de ses états passés). Conséquence : quelle que soit la pièce de cases (taille quelconque, couleurs
quelconques), une autoroute 104 ne repart jamais en mode gomme exact sur sa propre trace. Le « demi-tour » de T1 est un
ROULEUR qui longe la trace (vérifié : sur les 141 demi-tours à 2 cases, la trace double au lieu de s'effacer).
Statut : DÉMONTRÉ (preuve de 2 lignes) ; contrôle : 22 + 2 574 pièces de 1 et 2 cases → 0 retour.

**Ce qui reste possible : l'ÉCHANGE.** Une AUTRE fourmi, de la classe I opposée, peut se trouver en R(état de la sonde).
La pièce doit donc contenir une fourmi de l'autre classe (le Tourniquet en a une de chaque) : la sonde est capturée,
une fourmi de la pièce repart en gomme. C'est l'objet de la recherche à fourmis (§3).

**Bascule gratuite (théorème, R-142).** Si un état Z (autoroute qui arrive, pièce S0) devient au temps T l'état R(Z'_t),
où Z'_t = Z_t avec la pièce remplacée par S1 (trace effacée, pièce changée), alors, en jouant le système retourné, une
autoroute neuve qui arrive sur la pièce R(S1) repart en gomme et laisse R(S0). Pour une pièce de cases seules R(S) = S :
toute « gomme changée » serait automatiquement une bascule S0 → S1 → S0. (Sans objet pour les cases seules, §2 ; pour les
pièces à fourmis, R retourne aussi les fourmis de la pièce et l'ordre de jeu.)
