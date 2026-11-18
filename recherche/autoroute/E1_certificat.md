# É1 — Lemme du certificat d'autoroute (S1, 18-11-2026)

## Idée en une image
```
   chaos derrière          fourmi        devant : bande Z, toute blanche
   ░░▓░▓▓░░▓▓   ▓▓▓▓▓[V]→ → → → → → → → →  (V+d)(V+2d)(V+3d)…
```
Si la fenêtre V lue pendant une période contient « le bon motif » et que la bande devant est blanche,
la fourmi ne lit plus jamais que ce qu'elle a elle-même écrit : elle recopie la période pour toujours.

## Notations
Une fourmi (règle quelconque, grille carrée ou hexagonale), configuration C_t, position a_t, cap h_t, couleur 0 = blanc.
À l'instant t, on joue p pas « à blanc » depuis l'état courant. On note, **relativement à a_t** :
- V = ensemble des cases lues pendant ces p pas (fini, |V| ≤ p) ;
- Pv(v) = couleur de a_t+v à l'instant t, Pa(v) = sa couleur après les p pas (v ∈ V) ;
- d = a_{t+p} − a_t (déplacement), et la condition de cap h_{t+p} = h_t.

## Énoncé (lemme du certificat)
Si les conditions finies suivantes sont vraies :
- **F1** h_{t+p} = h_t et d ≠ 0 ;
- **F2** pour v ∈ V avec v+d ∈ V : Pa(v+d) = Pv(v) ;
- **F3** pour v ∈ V avec v+d ∉ V : Pv(v) = 0 ;
- **F4** V est convexe le long de d : si v ∈ V et v+md ∈ V (m ≥ 2), alors v+kd ∈ V pour 0 < k < m ;
- **Z** toutes les cases de la bande Z = ⋃_{k≥1} (a_t+V+kd) \ (a_t+V) sont blanches à l'instant t ;

alors pour tout k ≥ 0 : a_{t+kp} = a_t + kd, h_{t+kp} = h_t, et la suite des couleurs lues est périodique de
période p à partir de t. **La fourmi construit l'autoroute (période p, dérive d) pour toujours.**

## Démonstration (récurrence sur les périodes)
Posons t_k = t + kp, A_k = a_t + kd et Z_k = ⋃_{j>k}(a_t+V+jd) \ (A_k+V). Invariant I_k :
(i) a_{t_k} = A_k, h_{t_k} = h_t ; (ii) C_{t_k}(A_k+v) = Pv(v) pour v ∈ V ; (iii) les cases de Z_k sont blanches à t_k.

- **I_0** : (i), (ii) par définition de Pv, (iii) c'est l'hypothèse Z.
- **I_k ⇒ I_{k+1}**. La fourmi ne lit que des cases ; tant que les couleurs lues sont celles du jeu « à blanc »,
  elle refait exactement les mêmes pas. Par (i)-(ii), elle part du même cap avec le même contenu sur A_k+V :
  pendant p pas elle refait le jeu à blanc décalé de kd, ne touche que A_k+V, et finit en A_k+d = A_{k+1} avec
  le cap h_t (F1) ; A_k+V contient alors Pa. D'où (i).
  (ii) Soit v ∈ V, c = A_{k+1}+v. Si v+d ∈ V, c = A_k+(v+d) contient Pa(v+d) = Pv(v) (F2). Sinon, c ∉ A_k+V
  n'a pas été touchée ; c ∈ Z_k donc blanche, et Pv(v) = 0 (F3).
  (iii) Soit c ∈ Z_{k+1} : c ∈ a_t+V+jd (j ≥ k+2) et c ∉ A_{k+1}+V. Si c ∉ A_k+V, alors c ∈ Z_k : blanche et non
  touchée. Si c ∈ A_k+V, posons w = c−a_t−jd ∈ V : w+(j−k)d ∈ V avec j−k ≥ 2, donc par F4 w+(j−k−1)d ∈ V,
  c'est-à-dire c ∈ A_{k+1}+V : contradiction. ∎

Remarques. (1) Le lemme vaut pour toute règle à une fourmi (pas seulement RL). (2) Z est infinie, mais pour une
configuration initiale finie, tout ce qui est hors de la boîte « support initial ∪ cases visitées » est blanc :
on ne vérifie que la partie de Z dans cette boîte (vérification finie). (3) Le lemme est une condition
suffisante ; pour l'autoroute 104 de RL, F1–F4 passent dans 87 phases sur 104 (les 17 autres échouent sur
F2–F4) : en pratique le certificat est trouvé au plus quelques dizaines de pas après le début de l'autoroute.
(4) Une configuration certifiée à l'instant t est donc **DÉMONTRÉE** : « la fourmi construit l'autoroute
pour toujours à partir de t » (preuve = lemme + calcul fini exact jusqu'à t).

## Implémentation
`src/fourmi -cert "…"` (une fourmi) : si une autoroute est détectée, cherche le premier instant certifié à partir
du début détecté moins p, et écrit `CERT t |V|=…` (ou `NONCERT`). Avec `-cert`, le moteur ne s'arrête plus
sur une autoroute non certifiée (avant : arrêt à 16 384 alors qu'un obstacle attendait la fourmi plus loin).
`-c0 T` : chercher le certificat à partir de T. Code : fonction `certifie()` de `src/fourmi.c`.

## Tests
| Test | Résultat |
|---|---|
| Départ blanc | CERT 9 977, |V| = 40 → **DÉMONTRÉ** : autoroute 104 pour toujours dès 9 977 |
| Départ blanc, `-c0 t` pour t = 9 977…10 080 | 87 phases certifiées sur 104 |
| 122 positions d'obstacle 1 case, `-c0 9977` (sans `-cert` en arrêt) | les 22 cases touchées → NONCERT à 9 977 (refus correct), 100 autres → CERT 9 977 |
| les mêmes avec `-cert -T 600000` | 122/122 certifiées ; 22 débuts = ceux de `ant obst` (21 à +1 pas, 1 à +3) ; demi-tour j=−19 : CERT 84 878 |
| 512 configs 3×3 | 512/512 certifiées, max 51 277 = T(3) |
