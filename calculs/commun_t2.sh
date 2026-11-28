set -u
R=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd); OUT=$(cd "$OUT" && pwd); cd "$R/recherche/regles"; export NPROC=${NPROC:-2}
T0=$(date +%s); BUDGET=18900   # 5 h 15
[ -f fourmi_r ] || gcc -O2 -w -o fourmi_r fourmi_r.c
if [ ! -s ../../data/t2/conversions_effet.json ]; then   # data/ absent sur GitHub : régénéré (≈ 2 min sur 4 cœurs)
  python3 s2_horloge/tbascule.py 1 && python3 s2_horloge/tbascule.py 2 && python3 s2_horloge/tb_filtre.py || { echo "VERDICT : ÉCHEC — régénération data/t2" > "$OUT/resume.txt"; exit 2; }
fi
