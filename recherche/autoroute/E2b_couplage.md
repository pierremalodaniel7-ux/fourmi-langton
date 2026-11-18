# É2b — Couplage multiple : preuve écrite (S3, 18-11-2026)

But : montrer qu'un îlot I posé loin dans la bande de l'autoroute (position k le long de la bande) a, pour tout
k ≥ k₀, la même histoire qu'à k₀, au temps près et à translation près. Sert à T1–T4 (R-85 à R-87, R-76, R-78, R-80, R-81).

## Notations (y vers le bas)
- d = (−2,+2) : déplacement de l'autoroute de départ par période (104 pas). p(x,y) = −x+y, p(d) = 4. d conserve x+y.
- X_k = départ blanc + îlot I_k = I_{k₀} + ((k−k₀)/2)·d (k et k₀ de même parité). B = départ blanc seul.
- D = {c : B(t+104)(c) ≠ B(t)(c−d)}, indépendant de t ≥ 9 977 ; p ≤ 25 sur D.
- Pour un monde X et un instant t : a_X(t) position, h_X(t) cap, X(t) configuration.

## Lemme 1 (couplage)
Soient deux mondes X, Y, des instants t, t', un vecteur v ∈ {0, d}. Si h_Y(t') = h_X(t), a_Y(t') = a_X(t) + v et si
Y(t')(c+v) = X(t)(c) pour toute c d'un ensemble S, alors, tant que chaque case lue par X pour la première fois depuis t
est dans S, on a pour tout n : a_Y(t'+n) = a_X(t+n) + v, même cap, même couleur lue, et Y(t'+n)(c+v) = X(t+n)(c) sur
S ∪ {cases touchées par X depuis t}.
*Preuve* : récurrence sur n ; la fourmi ne dépend que de la couleur lue ; une case déjà touchée depuis t a la même
histoire dans les deux mondes. ∎

## Lemme 2 (phase 0 : translation)
Pour t ≥ 9 977 avant l'impact, X_{k+2}(t+104)(c+d) = X_k(t)(c) pour c ∉ D−d, et les fourmis sont couplées (v = d).
*Preuve* : X_k(t) = B(t) ∪ I_k, X_{k+2}(t+104) = B(t+104) ∪ (I_k + d), définition de D, et B est certifié dès 9 977. ∎
Avec le lemme 1, le couplage dure tant que X_k lit des cases de p > 21 (condition C1).

## Lemme 3 (changement de repère)
Supposons le couplage du repère i−1 (décalage τ_{i−1} = 104·i, translation v_{i−1}) valable jusqu'à s_i + 104, et :
- (rouleur) a_k(s_i+104) = a_k(s_i) + u (u = −d si i impair, +d si i pair), même cap, et la fenêtre W_i (cases lues sur
  [s_i, s_i+104)) se recopie : X_k(s_i+104)(c+u) = X_k(s_i)(c) pour c ∈ a_k(s_i)+W_i.

Alors avec τ_i = τ_{i−1} + 104 et v_i = v_{i−1} + u (v₀ = d ; donc v alterne : 0, d, 0, …), les fourmis sont couplées au repère i
aux instants s_i (X_k) et s_i + τ_i (X_{k+2}), et les configurations coïncident (à v_i près) sur l'ensemble S_i suivant :
1. la fenêtre a_k(s_i)+W_i ;
2. les cases hors des diagonales Δ_i (x+y des positions de X_k sur [9 977, s_i+104] et de l'îlot) : jamais touchées après 9 977
   dans aucun des deux mondes. Repère identité (i impair) : elles valent donc la même chose (même germe). Repère translation
   (i pair) : il faut en plus qu'elles évitent D, d'où Δ_i ⊇ diagonales de D pour i pair (correctif S4, R-92) ;
3. (i impair) p < L_i, et accord de la phase i−2 (pour i ≥ 3) : ces cases n'ont été touchées dans aucun des deux mondes
   pendant la phase i−1 (L_i ≤ min p sur [s_{i−1}, s_i) et ≤ min p sur [s_i, s_i+104] + 4) ;
   (i pair) p > H_i (max p sur [s_{i−1}, s_i+104]), et c+d ∉ D pour i = 2, accord de la phase i−2 sinon ;
4. règle « un pas » : c telle que c+u ne soit pas touchée sur [s_i, s_i+104), X_k(s_i)(c+u) = X_k(s_i)(c), c+u dans
   l'accord du repère i−1 à l'instant s_i+104 (et c aussi, pour la récurrence), et c+u ∈ S_i (fermeture par chaîne :
   la chaîne c, c+u, c+2u… avance en p de ∓4 et finit dans 3). Concrètement : c−d vers le germe (i impair), c+d vers le site.
*Preuve de 4* (Y = X_{k+2}) : Y(s_i+τ_i)(c+v_i) = Y((s_i+104)+τ_{i−1})((c+u)+v_{i−1}) car v_i = v_{i−1} + u ;
par le couplage i−1 à l'instant s_i+104 (c+u y est dans l'accord), cela vaut X_k(s_i+104)(c+u) = X_k(s_i)(c+u)
(non touchée sur [s_i, s_i+104)) = X_k(s_i)(c). Les points 1–3 se prouvent de même (fenêtre : recopie ; 2 : jamais touchées ; 3 : non touchées pendant
la phase i−1 dans les deux mondes, et égales au début de cette phase par l'accord i−2). ∎

## Théorème (récurrence sur k)
Si, pour X_{k₀} : C1, les rouleurs aux s_i, toutes les premières lectures de la phase i (jusqu'à s_{i+1}+208, ou jusqu'au
certificat + 104 pour la dernière) dans S_i, et la bande Z du certificat final dans S_NS (règle selon la direction finale),
alors X_{k₀+2} est certifiée à cert(k₀) + 104·(NS+1)… et satisfait les mêmes conditions ; donc tout X_k, k ≥ k₀ de même
parité, construit l'autoroute pour toujours.
*Preuve* : lemmes 1–3 de proche en proche donnent le couplage jusqu'au certificat ; le lemme du certificat (R-83)
s'applique à X_{k₀+2} car la fenêtre et Z coïncident. Pour passer à k₀+4 : X_{k₀+2} a les mêmes s_i (+τ), les mêmes
fenêtres, et les ensembles S_i(k₀+2) contiennent S_i(k₀) aux cases utiles, parce que tous les critères (p, Δ, chaînes)
sont fermés par le décalage de repère et s'évaluent sur des cases où les deux mondes coïncident. ∎

## Contrôles
- `ant multi` vérifie exactement ces conditions sur X_{k₀} (NS = 0 : `pmin` ; NS = 1 : `uturn` ; NS = 2 : `triple2`).
- `ant deux` (R-88) simule X_{k₀} et X_{k₀+2} et confirme le couplage pas à pas : 768/768 cas.
- Prédictions cert(k) affines (pente 52·(NS+1)) : vérifiées jusqu'à k = 2 000 sur 262 classes (R-80).

## Points à relire en priorité
Le point 3 pour i ≥ 3 (accord de la phase i−2) et la fermeture des ensembles d'accord par le décalage (passage k₀+2 → k₀+4).

## Correctif S3 (R-89) : direction finale −d en phase 0
Pour NS = 0 (translation pure), la bande Z de l'autoroute finale doit éviter D après translation. Si la direction finale
est −d, p décroît le long de Z : on exige que les diagonales x+y de la fenêtre finale ne soient pas celles de D
(D ⊂ cases touchées avant T0+104 ∪ cases de la base, sur leurs diagonales). Sinon (p non décroissant) : p > MPD−4.
