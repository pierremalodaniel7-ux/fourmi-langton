#!/bin/bash
# R-624 (objectif 1 de REPRISE) : vérifier h1'' (2 pas, 8 bits) sur 256/256 états, moteur C, puis hx.py (option py) sur 16 cas.
# Si des cas sont faux ou sales : descente de placement (chain_h1b.py, REALOBJ=1, MULT=1, comme R-620) sur $NPROC graines,
# 3 meilleurs placements dans $OUT, revérification du meilleur sur 256.
# Test local : PETIT=1 (2 cas C, 1 cas py) ; FORCE=1 force la descente ; BUDGET=secondes.
set -u
RACINE=$PWD; S=$RACINE/recherche/regles/s3_pas; T0=$(date +%s); BUDGET=${BUDGET:-18900}   # 5 h 15
PETIT=${PETIT:-0}; FORCE=${FORCE:-0}; NPROC=${NPROC:-$(nproc)}; OUT=$(cd "$OUT" && pwd)
W=$(mktemp -d); mkdir -p "$S/data"
sed 's/#define MAXA 128/#define MAXA 4096/' "$RACINE/recherche/regles/fourmi_r.c" > "$W/fr_big.c"
gcc -O2 -w -o "$S/fourmi_r_big" "$W/fr_big.c" || { echo "VERDICT : ÉCHEC — compilation fourmi_r_big" > "$OUT/resume.txt"; exit 1; }
reste() { echo $(( BUDGET - $(date +%s) + T0 )); }
ETAPE="départ"; echo "$ETAPE" > "$W/etape"
resume() {   # réécrit $OUT/resume.txt à partir des fichiers d'étape (appelé toutes les 10 min et à la fin)
  python3 - "$W" "$OUT" "$(( $(date +%s) - T0 ))" <<'EOF'
import sys, re, glob, os, json
W, OUT, dt = sys.argv[1], sys.argv[2], int(sys.argv[3])
def tot(pat):
    n = s = f = m = mm = 0; lines = []
    for fn in sorted(glob.glob(os.path.join(W, pat))):
        for l in open(fn):
            x = re.search(r"(\d+) cas, (\d+) sales, (\d+) faux, 2 moteurs (\d+)/(\d+)", l)
            if x: a = list(map(int, x.groups())); n += a[0]; s += a[1]; f += a[2]; m += a[3]; mm += a[4]; lines.append(l.strip()[:150])
    return n, s, f, m, mm, lines
etape = open(os.path.join(W, 'etape')).read().strip()
c = tot('c_*.txt'); p = tot('p_*.txt'); v = tot('v_*.txt')
desc = []
for fn in sorted(glob.glob(os.path.join(W, 'desc_*.log'))):
    l = [x.strip() for x in open(fn) if x.strip()]
    if l: desc.append(f"  {os.path.basename(fn)} : {l[-1][:120]}")
fin = etape.startswith('fin')
if fin and 'VERDICT' in etape: v1 = etape.split('|', 1)[1]
else: v1 = f"VERDICT : PARTIEL — C {c[0]-c[1]-c[2]}/{c[0]} justes et propres, py {p[3]}/{p[4]} identiques (en cours : {etape})"
L = [v1, f"durée {dt} s ; étape : {etape}",
     f"moteur C, placement h1pp_param.json : {c[0]} cas, {c[1]} sales, {c[2]} faux",
     f"hx.py (py) : {p[0]} cas, {p[1]} sales, {p[2]} faux, 2 moteurs identiques {p[3]}/{p[4]}"]
if desc: L += ["descente (chain_h1b REALOBJ=1 MULT=1) :"] + desc[:12]
if v[0]: L.append(f"revérification du meilleur placement (C) : {v[0]} cas, {v[1]} sales, {v[2]} faux")
L += ["détail des tranches C :"] + ["  " + x for x in c[5][:16]] + ["détail py :"] + ["  " + x for x in p[5][:8]]
open(os.path.join(OUT, 'resume.txt'), 'w').write('\n'.join(L[:50]) + '\n')
EOF
}
( while sleep 600; do resume; done ) & VEILLE=$!
etape() { ETAPE="$1"; echo "$1" > "$W/etape"; echo "$(date -u +%T) $1"; resume; }
cd "$S"
verif_c() {   # $1 = fichier de placement, $2 = préfixe des sorties ; 256 cas en K tranches
  local K=16; [ "$PETIT" = 1 ] && K=128
  local P=$(( NPROC / 2 )); [ $P -lt 1 ] && P=1
  local J; J=$(seq 0 $((K-1))); [ "$PETIT" = 1 ] && J="0"
  echo "$J" | xargs -P $P -I{} sh -c "python3 h1pp_check.py '$1' {}/$K > '$W/$2_{}.txt' 2>&1"
}
etape "C sur 256 états"; verif_c h1pp_param.json c
etape "py sur 16 cas"
NPY=16; [ "$PETIT" = 1 ] && NPY=1
seq 0 $((NPY-1)) | xargs -P "$NPROC" -I{} sh -c "python3 h1pp_check.py h1pp_param.json \$(( {} * 16 ))/256 py > '$W/p_{}.txt' 2>&1"
read NC SC FC NP SP FP MP MMP < <(python3 - "$W" <<'EOF'
import sys, re, glob, os
def tot(pat):
    t = [0]*5
    for fn in glob.glob(os.path.join(sys.argv[1], pat)):
        for l in open(fn):
            x = re.search(r"(\d+) cas, (\d+) sales, (\d+) faux, 2 moteurs (\d+)/(\d+)", l)
            if x: t = [a + int(b) for a, b in zip(t, x.groups())]
    return t
c, p = tot('c_*.txt'), tot('p_*.txt'); print(c[0], c[1], c[2], p[0], p[1], p[2], p[3], p[4])
EOF
)
NATT=256; [ "$PETIT" = 1 ] && NATT=2
if [ "$FORCE" != 1 ] && [ "$NC" = "$NATT" ] && [ "$SC$FC$SP$FP" = "0000" ] && [ "$MP" = "$MMP" ] && [ "$NP" -gt 0 ]; then
  etape "fin|VERDICT : OK — $NC/$NC justes et propres (moteur C), py $MP/$MMP identiques et justes"
else
  SECS=$(( $(reste) - 1500 )); MARGE=600; [ "$PETIT" = 1 ] && { SECS=30; MARGE=20; }
  if [ "$NC" != "$NATT" ]; then etape "C incomplet ($NC/$NATT) : descente quand même"; fi
  etape "descente $NPROC graines, $SECS s"
  if [ "$SECS" -gt 60 ] || [ "$PETIT" = 1 ]; then
    seq 1 "$NPROC" | xargs -P "$NPROC" -I{} sh -c "REALOBJ=1 MULT=1 DMAX=30000 GMAX=5000 timeout $((SECS+MARGE)) python3 chain_h1b.py \$((100+{})) $SECS h1pp_param.json > /dev/null 2>&1; cp data/chainh1b_\$((100+{})).log \"$W/desc_\$((100+{})).log\" 2>/dev/null"
  fi
  python3 - "$S/data" "$OUT" <<'EOF' > "$W/meilleurs.txt"
import sys, json, glob, os, shutil
d, out = sys.argv[1], sys.argv[2]; c = []
for fn in glob.glob(os.path.join(d, 'chainh1b_*.json')):
    b = os.path.basename(fn)
    if not b[9:-5].replace('OK_', '').replace('_r0', '').isdigit(): continue
    try: p = json.load(open(fn))
    except Exception: continue
    c.append((0 if 'OK_' in b else 1 if '_r0' in b else 2, p.get('conflits', 9999), b))
c.sort(); seen = set()
for i, (k, n, b) in enumerate([x for x in c if not (x[2] in seen or seen.add(x[2]))][:3]):
    shutil.copy(os.path.join(d, b), os.path.join(out, f'placement_{i+1}.json')); print(f'placement_{i+1}.json <- {b} (classe {k}, {n} conflits)')
EOF
  cat "$W/meilleurs.txt"
  if [ -s "$OUT/placement_1.json" ]; then
    etape "revérification de placement_1 sur 256"; verif_c "$OUT/placement_1.json" v
    read NV SV FV < <(cat "$W"/v_*.txt | grep -o "[0-9]* cas, [0-9]* sales, [0-9]* faux" | awk '{n+=$1; s+=$3; f+=$5} END {print n+0, s+0, f+0}')
    if [ "$NV" = "$NATT" ] && [ "$SV$FV" = "00" ]; then
      etape "fin|VERDICT : OK — nouveau placement_1 : $NV/$NV justes et propres (h1pp_param.json : $SC sales, $FC faux / $NC)"
    else
      etape "fin|VERDICT : ÉCHEC — h1pp_param.json : $SC sales, $FC faux / $NC ; meilleur placement : $SV sales, $FV faux / $NV"
    fi
  else
    etape "fin|VERDICT : ÉCHEC — h1pp_param.json : $SC sales, $FC faux / $NC ; py $MP/$MMP ; aucun placement trouvé"
  fi
fi
pkill -P $VEILLE 2>/dev/null; kill $VEILLE 2>/dev/null; resume
[ -s "$W/meilleurs.txt" ] && { echo "meilleurs placements :"; cat "$W/meilleurs.txt"; } >> "$OUT/resume.txt"
cat "$OUT/resume.txt"; rm -f "$S/fourmi_r_big"
