#!/bin/sh
# 2e passe du banc (outcome corrigé : « propre » ne dépend plus de l'issue globale), chocs, miroirs-oscillateurs
while pgrep -f "sh -c python3 banc.py" > /dev/null; do sleep 5; done
python3 banc.py $(cat data/regles_germes.txt) > data/banc_resume2.txt 2>&1
for r in $(cat data/regles_germes.txt); do python3 collisions.py $r 3; done > data/collisions_resume.txt 2>&1
for r in RL LLR LLLR LLLLR H:R2N H:UN H:R2UL2 H:R2R2L2 H:R2L1R1 H:R2R1R1; do python3 cycles2.py $r; python3 osc_miroir.py $r 3 30 10,60,2520; done > data/osc_resume.txt 2>&1
echo FINI >> data/osc_resume.txt
