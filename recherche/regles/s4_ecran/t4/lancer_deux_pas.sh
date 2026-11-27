#!/bin/bash
# R-720 : moteur C (256 états à tC) puis hx.py (256 états, 4 lectures) en 2 processus parallèles
cd "$(dirname "$0")/.."
timeout 1500 python3 t4/deux_pas_long.py C > t4/data_deux_pas/c.log 2>&1
(timeout 2400 python3 t4/deux_pas_long.py hx 2 129 > t4/data_deux_pas/hx_a.log 2>&1 &)
timeout 2400 python3 t4/deux_pas_long.py hx 129 256 > t4/data_deux_pas/hx_b.log 2>&1
