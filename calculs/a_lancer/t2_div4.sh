#!/bin/bash
# Diviseur par 4 : 2e couche d'objets 3-symétriques (t2_sym2.py BASE=) sur les 60 machines 2P de R-522 (P = 504) ; on cherche la période 2 016.
# Tout est régénéré (calculs/commun_t2.sh) ; résumé toutes les 10 min ; code ≠ 0 si aucun résultat clé. PETIT=1 : test < 2 min.
source "$(dirname "$0")/../commun_t2.sh"
python3 ../../calculs/run_t2.py div4
