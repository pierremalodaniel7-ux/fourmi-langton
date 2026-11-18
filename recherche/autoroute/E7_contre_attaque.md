# É7 — Contre-attaque : un décor fini peut-il occuper la fourmi indéfiniment ? (S8, 18-11-2026)

Réponse de cette séance : **pas de construction** ; voici ce qui bloque et ce qu'on a mesuré.

## 1. Ce qui est impossible (connu)
- Trajectoire bornée : impossible pour toute configuration finie (Bunimovich–Troubetzkoy 1992). Un décor fini ne peut donc pas
  « enfermer » la fourmi ; il faudrait l'occuper en l'emmenant de plus en plus loin sans autoroute.
- La dynamique inverse n'aide pas : le passé d'une configuration est le futur de la fourmi retournée (R-107) ; « autoroute à
  rebours pour tout décor fini » est équivalent à la conjecture.

## 2. Les seuls mécanismes de retour qu'on ait vus (T1–T6)
Le **demi-tour** : une case sur la bande renvoie l'autoroute sur sa propre trace jusqu'au site précédent (germe ou collision),
qui peut la renvoyer à son tour (classes « aller-retour » de T4 : jusqu'à 4 traversées). Dans tous les cas démontrés, le nombre
de traversées est **fini et fixé par la classe** (pente 52·(NS+1)), et l'autoroute finit par partir en terrain neuf.

## 3. Expérience « ping-pong le plus court » (`outils/pingpong.py`)
À chaque étape, on ajoute la case la plus proche, devant la fourmi au moment du certificat, qui renverse la direction finale.
| étape | case ajoutée | distance (demi-périodes) | certifié | boîte des cases |
|---|---|---|---|---|
| 1 | (−11,−4) | 1 | 15 199 | 11 |
| 2 | (26,−13) | 1 | 18 785 | 26 |
| 3 | (7,28) | 1 | 36 485 | 28 |
| 4 | (47,30) | 1 | 43 678 | 47 |
| 5 | (−13,25) | 1 | 55 755 | 47 |
| 6 | (46,−1) | 1 | 81 382 | 47 |
| 7 | (−18,56) | 2 | 79 188 | 56 |
| 8 | (67,−45) | 25 | 136 818 | 67 |
| 9 | — | aucun demi-tour à < 400 demi-périodes (décalage ±12) | — | — |
Remarque : la case est posée là où était la fourmi au certificat ; elle peut modifier tout le chaos précédent (étape 7 : le
certificat recule). Chaque étape est une nouvelle configuration, toutes certifiées (8 cases : 136 818 pas).
Conclusion : renverser la fourmi coûte une case par renversement et une boîte qui grandit ; la méthode gloutonne s'arrête vite.
Ce n'est pas une preuve d'impossibilité.

## 4. Ce qu'il faudrait pour une vraie construction
Un mécanisme **auto-entretenu** (la fourmi fabrique elle-même les miroirs qui la renvoient, comme le rectangle croissant de
Lutfalla pour LLRRRL). Pour RL, les seules structures auto-construites observées sont l'autoroute et le « rouleur » qui roule sur
sa trace et s'arrête au site précédent (R-74, R-81). Aucune ne se reconstruit plus loin. Piste non explorée : chercher, parmi les
issues de collision « autoroute × trace » (R-25), une issue qui renvoie une autoroute vers un site qu'elle vient elle-même de créer.
