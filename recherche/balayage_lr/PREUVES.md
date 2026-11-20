# Balayage LR — section 1 : réductions (20-11-2026)

Modèle : grille carrée, y vers le bas, caps 0=H 1=D 2=B 3=G ; règle w ∈ {L,R}^q ; à chaque pas
c = N[x] mod q, tourner selon w[c] (R = +1, L = −1), N[x]++, avancer. Départ : blanc, (0,0), cap H.

## R1. Échange L↔R = miroir — VÉRIFIÉ (preuve + calcul)
Soit σ(x,y) = (−x,y). σ fixe H et B, échange D et G, et σ∘(virage droite)∘σ = virage gauche.
Récurrence : si à l'instant t l'état de w̄ (= w échangé) est l'image par σ de l'état de w (fourmi, cap, grille),
la fourmi de w̄ lit la même couleur c, tourne de −w[c] = image du virage w[c], écrit c+1 sur la même case (image),
avance vers l'image de la case suivante. L'état initial (blanc, origine, cap H) est σ-invariant. ∎
Calcul : `verif_sec1.py`, 5 règles × 200 000 pas, trajectoires identiques au miroir près (RL, LLR, LRRL, LLRRRL, LRRRRRLLR).
Conséquence : on ne simule que les mots commençant par L ; période identique, déplacement (dx,dy) → (−dx,dy).

## R2. Mot répété w^k ≡ w — VÉRIFIÉ (preuve + calcul)
Avec u = w^k (longueur kq), u[c] = w[c mod q]. Les deux fourmis comptent les visites N[x] ; le virage de u est
u[N mod kq] = w[(N mod kq) mod q] = w[N mod q] : même virage à chaque pas, donc même trajectoire (positions, caps)
pour toujours. Seules les couleurs affichées diffèrent (N mod kq contre N mod q). ∎
Attention : un cycle exact de w (retour à N ≡ 0 mod q) n'en est pas forcément un de w^k (il faut N ≡ 0 mod kq) :
la période de cycle peut être multipliée ; les autoroutes (trajectoire) sont identiques.
Calcul : 5 règles × 200 000 pas, trajectoires identiques. On ne garde que les mots primitifs.

## R3. Une seule lettre (L^q ou R^q) : cycle trivial — VÉRIFIÉ
La fourmi tourne toujours du même côté : elle parcourt le carré de 4 cases en 4 pas, chaque case visitée une fois
tous les 4 pas. Au pas 4q chaque case a été visitée q fois (N ≡ 0 mod q), la fourmi est revenue en (0,0) cap H :
retour exact à l'état initial, période 4q (et pas avant : au pas 4j, j<q, les 4 cases valent j ≠ 0). ∎ Calcul : q = 2..16 OK.

## R4. Relations testées sans rien supposer (sur les 65 242 règles du balayage)
- (b) décalage circulaire : la règle w décalée de k (w'[c] = w[c+k]) partant du blanc = la règle w partant d'un
  fond uni de couleur k (renumérotation c ↦ c+k des couleurs) — VÉRIFIÉ (identité de renumérotation).
  Mais depuis le BLANC, w et sa rotation n'ont PAS le même comportement — FAUX en général.
  Contre-exemple : LLLR (autoroute 52) / LLRL (autoroute 384) ; LRRRR (pas d'autoroute) / RRRRL ≅ LLLLR (autoroute 68).
- (a) mot lu à l'envers : FAUX en général. Contre-exemple : LLLR (autoroute 52) / RLLL ≅ LRRR (pas d'autoroute en 2·10⁶).
- (c) complément puis envers : FAUX en général. Contre-exemple : LLLR (autoroute 52) / LRRR.
  Remarque : c'est la relation qu'on attend du renversement du temps (la fourmi est réversible), mais elle
  relie w depuis le blanc à w' depuis un AUTRE état (l'état final de w), pas depuis le blanc.
Chiffres (voir relations.md) : même classe dans ≈ 72 % des paires, mais c'est surtout « chaotique / chaotique » ;
parmi les paires où les deux règles font une autoroute, la période est la même dans 8 à 13 % des cas seulement.

## R5. Théorème des paires — DÉJÀ CONNU (Gale, Propp, Sutherland, Troubetzkoy 1995), vérifié sur les données
Classe S (motif symétrique à au moins la moitié des passages par l'origine) = EXACTEMENT les règles dont un
décalage circulaire est formé de lettres doublées (LLRR, LRRL, LLRRLL…) : 470 / 470, aucune exception
dans un sens ni dans l'autre (q ≤ 16). Symétrie trouvée : miroir d'axe horizontal (bit « miroir- »).

## R6. Certificat d'autoroute (preuve d'infinité) — DÉMONTRÉ (raisonnement) ; code `src/balaye.c`, fonction certif()
État à t1 = grille f0, fourmi (p,d). On joue P pas : S = cases visitées, n(c) = nombre de visites.
Si la fourmi revient en p + D (D ≠ 0) avec le cap d, et si pour toute c ∈ S et tout k ≥ 0
   f0(c + (k+1)D) + Σ_{i=1..k+1} n(c + iD) ≡ f0(c)   (mod q),
alors la période k+1 rejoue exactement la période 0 translatée de (k+1)D, pour tout k.
Preuve : récurrence ; si les périodes 0..k rejouent, f_{k+1}(x) = f0(x) + Σ_{j=0..k} n(x − jD), donc la couleur
lue en c+(k+1)D au début de la période k+1 vaut f0(c+(k+1)D) + Σ_{i=1..k+1} n(c+iD) ≡ f0(c) : la fourmi lit les
mêmes couleurs, fait les mêmes virages et les mêmes écritures. ∎ Au-delà de la boîte des cases touchées,
f0 = 0 et n = 0 : les termes deviennent constants, la vérification est finie.
Appliqué aux 6 768 autoroutes de la passe 1 : 6 768 certifiées (aucune autoroute observée non certifiée).

## R7. Conjecture LᵃRᵇ (OBSERVÉ, pas de preuve)
- b = 1, a ≥ 3 : autoroute P = 16a + 4, début 24a + 6 — déjà connu (Gajardo-Lutfalla-Rao 2025, famille LⁿR).
- b impair ≥ 3, a ≥ max(3, b − 1) : autoroute de période 16(a + b) − 20 ou sa moitié (moitié : (3,3), (4,5), (6,5), (9,7)).
- b pair : aucune autoroute (et souvent une boîte minuscule : L¹²RR tient dans 12×12 après 2·10⁶ pas).
- b impair, a < b − 1 : aucune autoroute observée. Exception unique à la 2e ligne : LLRRR (a=2, b=3), chaotique.
Données : famille_LaRb.txt (92 conformes, 1 exception, q ≤ 16). Les mots LᵃRᵇ, RᵃLᵇ et leurs rotations
recouvrent la même famille à miroir près.
