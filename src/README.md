# Programmes (`make` puis `make test`)

| Fichier | Rôle | Résultats |
|---|---|---|
| ant.h | moteur commun : fourmis RL, grille infinie (table de hachage) | — |
| **fourmi.c** | **moteur unique pour les campagnes (voir CLAUDE.md)** ; oracle.txt = résultats attendus | tous |
| bestiaire2.c | analyse d'une situation, toutes règles carrées / hexa (grille 4096², attention au bord) | bestiaire |
| run.c, cyc.c, tr.c, gen.c | rejouer ; cycle exact ; suivre 2 fourmis ; fabriquer un germe | R-19 à R-25 |
| tipmin.c | bout d'autoroute minimal | R-20 |
| nav.c | navettes de portée réglable | R-21 |
| drop.c, pass.c | passagers | R-22, R-23 |
| auto2.c, two.c, col.c | collisions (1 case, 2 cases, 2 autoroutes) | R-16, R-24, R-25 |
| explore.c, full.c, onset.c, lam.c + ana.py, cycpipe.py, build.py | recherche massive, nids, Lambine | R-26 à R-34 |
| hw.c, hwv.c + dirs.py, sel.py, build6.py, enum_regles.py | autoroutes par direction (hwv.c est le vérificateur) | R-35 |

Manquent (pas dans l'export) : oneh.c, exact.c, perturb.c, multi.c, ants.c, mkbestiaires.py, render.c.
