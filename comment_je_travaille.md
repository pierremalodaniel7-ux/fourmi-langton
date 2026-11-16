# Comment Claude travaille sur ce projet (16-11-2026)

## En une image
```
toi : "explore …"  ──►  je lis etat.md + CLAUDE.md (pas tout le journal)
                        │
                        ▼
              gen.py fabrique N situations ──► src/fourmi (2 cœurs, en tâche de fond, tranches de ~5 min)
                        │
                        ▼
              tri.py : résumé + morceaux INCONNUS (absents de connus.txt)   ← je ne lis QUE ça
                        │
                        ▼
              revérification du plus petit exemple à 4 000 000 de pas
                        │
                ┌───────┴────────┐
          disparaît          reste
       (transitoire)      ─► germe + image + fiche PDF + journal + connus.txt
                        │
                        ▼
              commit + push, puis réponse courte
```

## Ce qu'il faut savoir
- **Je ne calcule que pendant que je prépare ma réponse.** Quand je réponds, les calculs en cours s'arrêtent
  quelques minutes après. D'où le budget en minutes et le travail par tranches.
- **Machine** : 2 cœurs. Mesuré le 16-11 : 950 situations de 10 à 100 fourmis, 400 000 pas max, en 5 min 40 s.
- **Ce qui me coûte de la mémoire de travail (« contexte »)** : lire de longs fichiers ou de longues sorties.
  D'où les règles : etat.md d'une page, `grep` dans journal.md, seulement le résumé de tri.py.
- **Ce qui est exact / ce qui ne l'est pas** : un CYCLE détecté par `./fourmi` est exact (retour à l'état de
  départ). Une autoroute reste une OBSERVATION (simulation finie), même confirmée à 4 M pas.
- **Les N<k>** (fourmis encore en mouvement non classé à la fin) ne sont pas des découvertes : souvent des nids,
  des losanges ou des fourmis encore en interaction. Je ne donne que leur fréquence.
- **Les pièges que je surveille** : bords de grille, fourmis retirées, bords de losange (périodes 2, 3, 4, 10),
  tronçons d'autoroute transitoires (d'où la revérification à 4 M pas).
- **Je ne compte pas mes tokens** : je n'ai pas de compteur. Je peux donner des durées (horloge) et le nombre
  de situations calculées.

## Pour m'utiliser au mieux
1. Donne le budget (minutes) et la forme du résultat, comme dans ta dernière demande : c'est idéal.
2. Garde `connus.txt` à jour : c'est lui qui fait que je ne te présente que du nouveau.
3. Pour une vraie nuit de calcul, lance `outils/campagne.sh` sur ta machine (Claude Code) : plus de cœurs,
   et pas d'arrêt quand je réponds ; je n'aurai qu'à lire les résumés.
