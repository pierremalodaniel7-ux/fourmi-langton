# Fourmis de Langton généralisées — dépôt de travail (Pierre-Malo, Octave, Claude)

Ce dépôt est la RÉFÉRENCE de travail (code, journal, pistes). Le Drive et les docs du projet Claude
sont des archives. Tutoiement, français, réponses courtes, exemple ou schéma d'abord.

## Avant toute tâche : poser des questions (demande de Pierre-Malo, 16/11)
Quand il demande de faire quelque chose (explorer, chercher, construire…), poser d'abord 2 à 4 questions
courtes (AskUserQuestion) pour être sûr de ce qu'il veut : objectif, périmètre (règles, nb de fourmis, cases),
durée / budget, forme du résultat. Puis reformuler en une ligne et lancer. Exception : mots-clés simples (point, vérifie).

## Démarrage d'une session (dans cet ordre, rien de plus)
1. Lire `etat.md` (une page). Ne lire `journal.md` que par recherche ciblée : `grep -n "R-14" journal.md`.
2. `make -C src` puis `make -C src test` (oracle : 18 tests, quelques secondes) avant toute campagne.
3. Ne jamais recopier un fichier entier dans la conversation : `head`, `grep`, `wc`, résumés.

## Outils (ne pas réécrire de moteur : modifier ceux-ci)
- `src/fourmi` = MOTEUR UNIQUE (carré/hexa, q couleurs, n fourmis, cases, grille infinie, rien n'est retiré,
  cycle exact, autoroutes confirmées, groupes). `./fourmi "RL|0,0,H;40,0,G|"` ou `./fourmi -lot < fichier`.
- `outils/campagne.sh NOM PAS [options gen.py]` : génère (gen.py), calcule sur les 2 cœurs, trie.
- `outils/tri.py data/NOM.out` : résumé + morceaux INCONNUS (absents de `connus.txt`). Ne lire que ça.
- Vérifier une trouvaille : `./fourmi -T` plus grand, puis `cyc` / `nav` / `full` (anciens programmes) si besoin.
- Limite actuelle : les fourmis restantes après le départ d'autoroutes (N<k>, souvent des nids) ne sont pas
  encore classées exactement.

## Conventions
Grille carrée, y vers le bas, caps 0=H 1=D 2=B 3=G, RL (blanc → droite), fourmis jouées l'une après
l'autre (≠ synchrone de Golly / Fatès-Chevrier). Formats « x,y,D ; … » et cases « x,y ; … ».
Positions en entiers, jamais en flottants. Statuts : VÉRIFIÉ / OBSERVÉ / AFFIRMÉ / FAUX / OUVERT.
Une simulation finie ne prouve jamais un comportement infini.

## Règles d'écriture
- Journal : AJOUTER à la fin de `journal.md` (ID, énoncé, statut, commande, source). Ne pas réécrire.
- `etat.md` : mettre à jour seulement les lignes qui changent.
- Littérature : consulter `deja_connu.md` AVANT toute recherche web ; y ajouter ce qu'on a cherché.
- Nouveauté (choix de Pierre-Malo, 16/11) : ne pas monter de campagne sur un thème déjà connu. Vérifier le thème
  dans `deja_connu.md` (puis 1 ou 2 recherches courtes si absent) AVANT de lancer. Une trouvaille déjà connue :
  l'expliquer brièvement pour comprendre, la noter avec sa source, et passer à autre chose.
- Gros fichiers de résultats (CSV > 1 Mo) : dans `data/` (ignoré par git) ; ne garder que les résumés.
- Commit court en français après chaque étape utile, puis push.

## Pièges déjà rencontrés (ne pas recommencer)
- Grille de taille fixe : la fourmi touche le bord → fausses autoroutes / tronçons (R-08, R-11).
- Retirer une fourmi partie loin fausse les passagers qui la suivent (R-26) : revérifier dans le système complet.
- Période 2, 3, 4 ou 10 au bord d'un losange = fourmi qui longe le bord, pas une autoroute.
- Je m'arrête de calculer quand je réponds : annoncer la durée, ou travailler par étapes.
