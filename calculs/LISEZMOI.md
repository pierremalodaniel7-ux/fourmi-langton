# Calculs longs sur GitHub Actions

Le forfait Claude se paie en texte lu et écrit, pas en temps de calcul. Les gros balayages
(plus de 10 min) tournent donc sur les machines de GitHub, gratuitement (dépôt public, 4 cœurs, 6 h max par lancement).

Lancer un calcul :
1. Écrire `calculs/a_lancer/NOM.sh` (bash). Les moteurs sont déjà compilés (`src/fourmi`, `recherche/regles/fourmi_r`).
   Variables fournies : `$OUT` (dossier où écrire les résultats), `$NPROC` (nombre de cœurs).
   Le script doit écrire lui-même un RÉSUMÉ court dans `$OUT/resume.txt` (≤ 50 lignes) ; les gros fichiers bruts restent hors du dépôt (> 1 Mo : ne pas les écrire dans $OUT).
2. `git add`, commit, push (n'importe quelle branche). Le calcul démarre tout seul.
3. Plus tard : `git pull` puis lire `calculs/resultats/NOM/resume.txt` et `FINI` (code de sortie, durée).
   Ne pas attendre activement : soit continuer autre chose, soit finir la session et laisser la suivante lire le résultat.

Un script déjà fait (dossier avec FINI) n'est pas relancé. Pour relancer : nouveau nom.
Suivre l'avancement : onglet « Actions » du dépôt sur GitHub, ou `gh run list -w calcul` si `gh` est disponible.
