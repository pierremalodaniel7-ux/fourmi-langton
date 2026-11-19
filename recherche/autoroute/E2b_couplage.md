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
Avec le lemme 1, le couplage dure tant que X_k lit des cases de p > 21 (condition C1 ; en général p > MPD − 4, MPD = max p sur D).

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
   pendant la phase i−1 (L_i ≤ min p sur [s_{i−1}, s_i) et ≤ min p sur [s_i, s_i+104] + 4) ; **et (correctif S10, R-122)
   L_i ≤ pI = min p sur les cases de l'îlot** : pour i = 1, « égales au début de la phase » vient de ce que les deux mondes ne
   diffèrent, en repère identité, que sur l'îlot (et la trace de la phase 0, à grand p) — il faut donc que l'îlot soit hors de {p < L₁} ;
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

## Généralisations utilisées (S3–S4)
- **Base quelconque** C₀ (au lieu du départ blanc) dont l'autoroute est certifiée à T0 avec la dérive d : remplacer 9 977 par T0,
  B par l'évolution de C₀, D par {c : C₀(t+104)(c) ≠ C₀(t)(c−d)} ⊂ cases touchées avant T0+104 ∪ cases de C₀ (et leurs
  translatées par d), MPD = max p sur cet ensemble. Les cases de C₀ sont identiques dans les deux mondes : elles comptent dans
  Δ_i seulement pour i pair (repère translation) — c'est le correctif R-92.
- **Rotation** : la règle RL commute avec les rotations d'un quart de tour ; on pivote la configuration (et le cap initial de
  la fourmi) pour ramener la dérive de la base à d.
- **Îlot** : ses cases bougent (de d) entre X_k et X_{k+2} ; en repère identité elles diffèrent donc d'un monde à l'autre,
  c'est pourquoi leurs diagonales sont toujours dans Δ_i (d conserve x+y).

## Relecture S5
Relu en entier après R-89, R-92 et R-95/96. Cohérent avec le code de `ant multi` (bases, Δ, règle, L/H, fenêtres, Z selon la
direction). Points encore délicats : la fermeture des ensembles S_i par le décalage de repère (passage k₀+2 → k₀+4), argumentée
mais pas écrite case par case ; l'attribution des acceptations dans les appels récursifs de `agree` (NS ≥ 2) pour le décompte
« règle » de R-96 (seule une paire NS = 2 est concernée, et elle reste OBSERVÉE).

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

## S5 — Lemme de transport : double récurrence « deux cases loin » (R-95)
Notations : c₁ dans une classe de T1 à la distance k₁ (le long de d) ; d₂ = direction de l'autoroute qui sort du 1er site ;
c₂ = c₁ + r₀ + m·d₂ (m ≥ m₀). X(k₁, m) = blanc + {c₁, c₂}.
- (a) m → m+1 à k₁ = k₀ fixé : prouvé en R-93 (base W = blanc + c₁(k₀), `multi` avec BASE/T0/H0). Ses repères relient
  X(k₀, m+1) et X(k₀, m) : sur chaque segment, la position de la fourmi est soit la même (repère identité), soit translatée
  de d₂ (repère translation), avec un décalage de temps fixe, jusqu'au certificat.
- (b) k₁ → k₁+2 à m fixé : îlot {c₁, c₂} déplacé en bloc de d ; condition NS = 0 de `multi` : (C1) p > 21 sur les positions
  après l'impact, (Z) fenêtre finale : p > 21 si la direction finale n'est pas −d, diagonales hors de celles de D sinon.
**Lemme de transport.** Si (b) vaut à (k₀, m) avec NS = 0 et si p(d₂) ≥ 0 (d₂ = d ou d₂ ⟂ d), alors (b) vaut à (k₀, m+1),
sauf dans un cas : direction finale −d et d₂ ⟂ d avec des diagonales qui se rapprochent de celles de D.
*Preuve.* Par (a), les positions de X(k₀, m+1) après l'impact sont les images de celles de X(k₀, m) : identiques, ou
translatées de d₂ (p augmente de p(d₂) ≥ 0). Donc le min de p ne diminue pas (C1). La fenêtre finale est l'image de l'ancienne
(même direction finale) : p ne diminue pas ; d₂ = d conserve les diagonales ; si d₂ ⟂ d, les diagonales bougent de ±4 par
pas, donc il suffit qu'elles soient déjà du côté où elles s'éloignent de D. ∎
**Théorème (R-95).** Pour les 454 paires de classes où (b) vaut à la base avec NS = 0 et où le lemme s'applique :
pour tout k₁ ≥ k₀ (même parité) et tout m ≥ m₀, X(k₁, m) construit l'autoroute pour toujours.
*Preuve.* Par récurrence sur m (lemme), (b) vaut à (k₀, m) pour tout m ≥ m₀ ; puis, à m fixé, la récurrence (b) donne tout k₁. ∎
Contrôle indépendant : cert(k₀+40, m₀+10) prédit par les deux pentes, calculé directement : 40/40 exacts.

### Extension (R-96) : récurrence (b) avec changement de repère, sans la règle « un pas »
Si la vérification (b) passe avec NS ≥ 1 en n'acceptant les lectures que par p, par la fenêtre ou « hors Δ » (jamais par la
règle « un pas », dont les couleurs pourraient changer avec m), elle se transporte aussi de m à m+1 :
- G1 (c₁ = demi-tour, d₂ ⟂ d, c₂ fixe quand k₁ varie : base blanc + c₂) : avant s₁ rien ne dépend de m ; après, les lectures
  près de c₂ sont translatées de d₂ (p inchangé ; leurs diagonales, vers −800, sont sous celles de Δ₁ et s'en éloignent de
  4 par pas) ; les autres sont identiques. Z : même règle, mêmes conclusions.
- G2 (d₂ = d, la fourmi revient du 2e site au 1er puis au germe) : les lectures près de c₂ n'ont lieu qu'en phase 0 (p croît
  de 4 par pas : C1 tient) ; après le changement de repère de (a), les positions sont identiques ; L ne diminue pas ; Δ₁ est
  inchangé (d conserve les diagonales).

### Transport dual (R-98) : les 2 dernières paires
Si (b) est prouvée à m₀ seulement (même avec la règle « un pas »), elle couple X(k₁+2, m₀) et X(k₁, m₀) pour tout k₁. On
transporte alors la vérification (a) (récurrence en m, base W(k₁) = blanc + c₁) le long de k₁ par les repères de (b), à
condition que (a) n'utilise pas la règle. Les repères de (b) sont des translations de d (p +4, diagonales conservées) ou
l'identité. La borne MPD de W augmente au plus de 4 ; L_a augmente de 4 sur les segments translatés ; les ensembles {p < L}
ne font que grandir ; la fenêtre et Z suivent.
- c₁ = (−127,100), classe de c₂ en NS = 2 pour (b) : (a) en NS = 1, p* = 300, règle 0 ; le changement de repère de (a)
  (p ≤ 300) a lieu pendant la phase translation de (b) (dont le changement est à p ≤ 100).
- c₁ = (−119,100) (demi-tour), c₂ = (−401,−409) : (a) en NS = 1, p* = 90, règle 0 ; toutes les lectures de (a) après c₂ ont
  lieu dans la phase identité de (b) (après le passage au germe) : identiques pour tout k₁.
Puis, pour chaque k₁, la récurrence (a) donne tous les m ≥ m₀. Contrôle : 6/6 prédictions exactes (k₁ + 20…80, m + 0…30).

## S10 — Esquisse : transport à deux étages pour trois cases (T7) — À RELIRE, NON DÉMONTRÉ
Notations : c₁ = classe de T1 à k₁ (le long de d) ; c₂ = c₁ + r₀ + m·d₂ ; c₃ = c₂ + s₀ + m₃·d₃ (d₂, d₃ : directions des autoroutes qui
sortent du 1er et du 2e site). X(k₁, m, m₃) = blanc + {c₁, c₂, c₃}. Trois récurrences vérifiées avec `multi` puis `deux` :
- (C) m₃ → m₃+1 à (k₀, m₀) : base blanc + c₁ + c₂ (R-117, R-119, R-123) ; ses repères relient X(k₀,m₀,m₃+1) et X(k₀,m₀,m₃) :
  positions identiques ou translatées de d₃, décalage de temps fixe.
- (M) m → m+1 à k₀, îlot {c₂, c₃} en bloc, base blanc + c₁ (R-124) ; repères : identité ou translation de d₂.
- (K) k₁ → k₁+2, îlot {c₁, c₂, c₃} en bloc (R-124).
**Énoncé visé.** Si (M) vaut à (k₀, m₀, m₃₀) avec NS = 0 et d₃ ∈ {d₂, ⟂ d₂}, et si (K) vaut à (k₀, m₀, m₃₀) avec NS = 0 et
d₂, d₃ ∈ {d, ⟂ d} (avec la règle des diagonales de transport.py quand la direction finale est −d), alors X(k₁, m, m₃) construit
l'autoroute pour toujours pour tous k₁ ≥ k₀, m ≥ m₀, m₃ ≥ m₃₀ (mêmes parités).
**Schéma.** (1) Lemme de transport de R-95 appliqué avec les repères de (C) : (M) vaut à (k₀, m₀, m₃) pour tout m₃ (les positions sont
translatées de d₃, et p₂ — la coordonnée le long de d₂ — ne diminue pas si d₃ = d₂ ou ⟂ d₂) ; la récurrence (M) donne alors tout m.
(2) Même lemme avec les repères de (C) puis de (M) : (K) vaut à (k₀, m, m₃) pour tous m, m₃ (p le long de d ne diminue pas si d₂, d₃ ∈
{d, ⟂ d}) ; la récurrence (K) donne tout k₁. (3) Point à vérifier (leçon de R-122) : les cases de l'îlot bougent aussi (c₃ de d₃,
c₂ et c₃ de d₂) ; leur p ne diminue pas sous les mêmes hypothèses, donc la borne L ≤ pI de `multi` se transporte.
Décompte des triplets qui remplissent les hypothèses : 3 123 / 3 564 (R-127). Contrôle indépendant : R-126 (300/300 prédictions).
À faire : rédiger (1)–(3) en détail, traiter les variantes « c₃ fixe » (R-124) et le transport dual (R-98) pour les 441 autres.

## S11 — Transport à deux étages (T7) : preuve détaillée — DÉMONTRÉ sous réserve de relecture
Remplace l'esquisse S10 ci-dessus.

**Notations.** y vers le bas ; pour une direction e d'autoroute, p_e(c) = ⟨c, e⟩/2 (pour e = d = (−2,2) : p = −x+y, comme plus haut).
c₁ = c₁⁰ + ((k₁−k₀)/2)·d ; c₂ = c₁ + r₀ + ((m−m₀)/2)·d₂ ; c₃ = c₂ + s₀ + ((m₃−m₃₀)/2)·d₃ (d₂, d₃ : dérives des autoroutes qui sortent
du 1er et du 2e site ; c₂ − c₁ et c₃ − c₂ ne dépendent que de m et m₃). X(k₁, m, m₃) = blanc + {c₁, c₂, c₃}.
Trois récurrences, chacune de la forme du « Théorème (récurrence sur k) » avec une base et un îlot :
- (C) en m₃, base W₂ = blanc + {c₁, c₂} à (k₀, m₀) (pivotée pour que d₃ devienne d), îlot {c₃} ;
- (M) en m, base W₁ = blanc + c₁(k₀) (pivotée : d₂ devient d), îlot {c₂, c₃} déplacé en bloc de d₂ ;
- (K) en k₁, base blanc, îlot {c₁, c₂, c₃} déplacé en bloc de d.

**Lemme T (transport d'une condition NS = 0).** Soit (R) l'une des récurrences (M) ou (K), de direction e (e = d₂ pour (M), d pour (K)),
et (Q) une récurrence vérifiée (pour tout ν ≥ ν₀) qui fait varier un paramètre ν, dont les repères relient X(ν+1) et X(ν) par
des positions identiques ou translatées de f (f = d₃ pour (C), d₂ pour (M)), avec p_e(f) ≥ 0. Si les conditions de (R) avec NS = 0
valent pour X(ν), elles valent pour X(ν+1), sauf peut-être si la direction finale est −e, f ⟂ e, et les diagonales de la fenêtre
finale se déplacent vers celles de D_e.
*Preuve.* Les conditions de (R) avec NS = 0 sont : (C1) toute position de la fourmi après le premier contact avec l'îlot de (R) a
p_e > MPD_e − 4 ; (Z) la fenêtre finale est dans l'accord de la phase 0 : p_e > MPD_e − 4 si la direction finale n'est pas −e, sinon
ses diagonales évitent celles de D_e. (Avec NS = 0 il n'y a ni repère identité ni borne L : le correctif R-122 ne joue pas.)
Par (Q), chaque position de X(ν+1) est l'image d'une position de X(ν) (avant l'arrivée de (Q) sur son propre îlot les deux mondes sont
identiques ; ensuite repère identité ou translation de f ; les pas « en plus » de la phase 0 sont des translatés de pas de l'autoroute
de la base de (Q)). Le premier contact avec l'îlot de (R) a lieu avant que (Q) ne distingue les deux mondes (l'îlot de (R) contient
celui de (Q), et c₁ — resp. c₂ — est touchée avant c₃). Donc min p_e ne diminue pas (p_e(f) ≥ 0) : (C1) passe. La fenêtre finale de
X(ν+1) est l'image de celle de X(ν), avec la même direction finale : p_e ne diminue pas ; si f = e les diagonales sont conservées ; si
f ⟂ e elles bougent de ±4 par pas, d'où l'exception. Enfin les ensembles D_e et MPD_e ne dépendent que de la base de (R), qui ne
dépend pas de ν. ∎

**Théorème T7-loin.** Pour une classe de triplets (classe de c₁ à k₀, de c₂ à m₀, de c₃ à m₃₀) telle que :
(i) (C) vaut (preuve `multi` recoupée par `deux`) ; (ii) (M) vaut à (k₀, m₀, m₃₀) avec NS = 0 et d₃ ∈ {d₂, ⟂ d₂} (avec la règle des
diagonales si d₃ ⟂ d₂ et direction finale −d₂) ; (iii) (K) vaut à (k₀, m₀, m₃₀) avec NS = 0 et d₂, d₃ ∈ {d, ⟂ d} (même règle) ;
alors pour tous k₁ ≥ k₀, m ≥ m₀, m₃ ≥ m₃₀ de mêmes parités, X(k₁, m, m₃) construit l'autoroute pour toujours.
*Preuve.* (a) Par (C), X(k₀, m₀, m₃) est certifiée pour tout m₃ ≥ m₃₀. (b) Lemme T avec (R) = (M), (Q) = (C) : (M) vaut à
(k₀, m₀, m₃) pour tout m₃ ; puis le théorème de récurrence appliqué à (M) donne la certification de X(k₀, m, m₃) pour tout m, et
ses repères (translation de d₂) pour tout (m, m₃). (c) Lemme T avec (R) = (K), (Q) = (C) : (K) vaut à (k₀, m₀, m₃) pour tout m₃ ;
puis avec (Q) = (M) (repères de l'étape b, f = d₂) : (K) vaut à (k₀, m, m₃) pour tous m, m₃ ; le théorème de récurrence appliqué à
(K) donne tout k₁. ∎
Points à relire : l'affirmation « le premier contact avec l'îlot de (R) précède toute différence créée par (Q) » (vraie si la fourmi
touche c₁ puis c₂ avant c₃, ce qui est le cas dans les triplets construits à partir des bases T7) ; l'usage des repères de (M) pour tous
(m, m₃) à l'étape (c), qui demande que la preuve de (M) à (k₀, m, m₃) soit elle aussi à NS = 0 (conséquence du lemme T et de la
récurrence : les conditions se transmettent telles quelles).
Application : `outils/transport7.py` (S10) vérifie exactement (ii) et (iii) ; (i) par `audit_t7c.sh`.
