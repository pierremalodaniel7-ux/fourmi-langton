#!/bin/bash
# Objectif 3 : porte 3-symétrique autour de l'horloge (R-514/R-522) qui LIT un bit : chaque pose en X0 ET en X1 (t2_sym2.py BIT=both).
# Tout est régénéré (calculs/commun_t2.sh) ; résumé toutes les 10 min ; code ≠ 0 si aucun résultat clé. PETIT=1 : test < 2 min.
source "$(dirname "$0")/../commun_t2.sh"
python3 ../../calculs/run_t2.py porte
