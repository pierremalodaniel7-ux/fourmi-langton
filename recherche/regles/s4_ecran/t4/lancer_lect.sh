#!/bin/bash
# R-723 : attend la fin du calcul C en cours, puis moteur C (256 états, tC, avec lectures) et hx.py (256 états, 4 lectures + lectures de pixels)
cd "$(dirname "$0")/.."
while pgrep -f "deux_pas_long.py C" > /dev/null; do sleep 20; done
LECT=1 timeout 1700 python3 t4/deux_pas_long.py C > t4/data_deux_pas/c_lect.log 2>&1
(LECT=1 timeout 2700 python3 t4/deux_pas_long.py hx 0 128 > t4/data_deux_pas/hx_lect_a.log 2>&1 &)
LECT=1 timeout 2700 python3 t4/deux_pas_long.py hx 128 256 > t4/data_deux_pas/hx_lect_b.log 2>&1
