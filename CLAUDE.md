# Fourmis de Langton généralisées — dépôt de travail (Pierre-Malo, Octave, Claude)

Ce dépôt est la RÉFÉRENCE de travail (code, journal, pistes). Le Drive et les docs du projet Claude
sont des archives. Tutoiement, français, réponses courtes, exemple ou schéma d'abord.

## Avant toute tâche : poser des questions (demande de Pierre-Malo, 16/11)
Quand il demande de faire quelque chose (explorer, chercher, construire…), poser d'abord 2 à 4 questions
courtes (AskUserQuestion) pour être sûr de ce qu'il veut : objectif, périmètre (règles, nb de fourmis, cases),
durée / budget, forme du résultat. Puis reformuler en une ligne et lancer. Exception : mots-clés simples (point, vérifie).

## Mot-clé « continue » / recherche « autoroute » (18/11)
Si Pierre-Malo écrit « continue » ou parle de la conjecture de l'autoroute : lire
`recherche/autoroute/INSTRUCTIONS.md` puis `recherche/autoroute/ETAT.md`, et suivre ces instructions
(séance d'une heure, sans questions préalables, rapport à la fin).

## Après CHAQUE recherche : 3 documents, tous dans le Drive (demande de Pierre-Malo, 16/11)
Sans qu'il ait à le redemander, à la fin de toute recherche (explore, campagne…) :
1. **Bestiaire** (PDF, une fiche par trouvaille vérifiée : image, situation, signature, statut, commande).
   Ajouter les bêtes à `docs/sources/catalogue.json` (nouveau numéro de bestiaire = le plus grand du catalogue ET du
   dossier Bestiaires du Drive, + 1) puis générer TOI-MÊME le PDF :
   `python3 outils/mkbestiaires.py <numéro> "<titre>"` (→ `resultats/Bestiaire <n> - <titre>.pdf`). Ne pas le laisser au chat.
2. **Germes** (`germes_<date>.json`, format {dossier, nom, regle, fourmis, points, note}).
3. **Rapport de travail** : ce que j'ai fait, heures (début/fin de chaque tranche), nombre de situations,
   répartition des issues, ce qui a raté, temps de calcul ; jamais de chiffre inventé (pas de compteur de tokens).
Les déposer dans le Drive « Fourmi de Langton — recherche (Pierre-Malo) » :
- Bestiaire PDF + catalogue.json → dossier Bestiaires (id 1IJ-gddNy7VFsgFypqqBNnTxM_H6U-Z46)
- Germes → 02_Resultats (id 1ojVWJxKVWJHsud4Vfig3tmWD2OniqgtR)
- Rapport → 05_Methode (id 1TdFVPN0VJi8-PtDTSbK87yE8YhjQkUpr), en Google Doc (markdown converti)
- Ancienne version d'un fichier remplacé → 99_Archives (id 1KydgWyrPh3nC5_yFb-sL-dBU-bgYM5Ft) ; jamais de doublon.
Aussi dans le dépôt : `resultats/` + journal.md + etat.md + connus.txt, puis commit et push. S'il n'y a aucune
trouvaille, faire quand même le rapport (et le dire) ; bestiaire et germes vides ne sont pas déposés.

## Démarrage d'une session (dans cet ordre, rien de plus)
1. Lire `etat.md` (une page). Ne lire `journal.md` que par recherche ciblée : `grep -n "R-14" journal.md`.
2. `make -C src` puis `make -C src test` (oracle : 19 tests, quelques secondes) avant toute campagne.
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
