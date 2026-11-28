#!/bin/bash
# R-723 bis (29/11) : relance de r723_ecran2 (raté : numpy absent sur GitHub).
# R-723 (objectif 2 de REPRISE) : démo intégrée 2 pas à l'écran (2 pas + effacements + 8 ports de lecture, LECT=1), 256 états.
# 1) moteur C à tC (deux_pas_long.py C) ; 2) hx.py pas à pas (tA, tA2 + lectures, tB, tC) sur les 256 états en $NPROC tranches.
# Si faux : pour chaque pixel, le premier état faux et ce qui est lu au lieu de l'attendu. Test local : PETIT=1 (hx sur 2 états).
set -u
RACINE=$PWD; T4=$RACINE/recherche/regles/s4_ecran/t4; S3=$RACINE/recherche/regles/s3_pas; T0=$(date +%s); BUDGET=${BUDGET:-18900}
PETIT=${PETIT:-0}; NPROC=${NPROC:-$(nproc)}; export PETIT NPROC; OUT=$(cd "$OUT" && pwd); export LECT=1
W=$(mktemp -d); DD=$T4/data_deux_pas; mkdir -p "$DD"
# numpy (absent du python système de GitHub) : pip (PEP 668 contourné), sinon apt
python3 -c "import numpy" 2>/dev/null || python3 -m pip install -q --user --break-system-packages numpy \
  || python3 -m pip install -q --user numpy || sudo apt-get install -y -q python3-numpy
python3 -c "import numpy; print('numpy', numpy.__version__)"
( cd "$T4" && python3 -c "import sys; sys.path.insert(0, '$S3'); import deux_pas_long" ) > "$W/imp.txt" 2>&1 || { echo "VERDICT : ÉCHEC — import de deux_pas_long impossible : $(tail -n 1 "$W/imp.txt")" > "$OUT/resume.txt"; cat "$W/imp.txt"; exit 1; }
sed 's/#define MAXA 128/#define MAXA 4096/' "$RACINE/recherche/regles/fourmi_r.c" > "$W/fr_big.c"
gcc -O2 -w -o "$S3/fourmi_r_big" "$W/fr_big.c" || { echo "VERDICT : ÉCHEC — compilation fourmi_r_big" > "$OUT/resume.txt"; exit 1; }
echo "départ" > "$W/etape"
resume() {
  python3 - "$DD" "$OUT" "$(( $(date +%s) - T0 ))" "$(cat "$W/etape")" "$T4" <<'EOF'
import sys, os, json, glob
DD, OUT, dt, etape, T4 = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
sys.path.insert(0, T4); sys.argv = ['x']
import deux_pas_long as M   # predict, CASES, TC… (le bloc __main__ ne tourne pas)
envs = M.STEP.cases(); L = []
c = None
fc = os.path.join(DD, 'c_tC_lect.json')
if os.path.exists(fc):
    c = json.load(open(fc))['res']; cj = sum(v['juste'] for v in c.values()); cp = sum(v['propre'] for v in c.values())
hx = {}
N = 2 if os.environ.get('PETIT') == '1' else 256; NP = int(os.environ['NPROC'])
for fn in [os.path.join(DD, f'hx_lect_{j * N // NP}_{(j + 1) * N // NP}.json') for j in range(NP)]:   # seulement les tranches de ce calcul
    if not os.path.exists(fn): continue
    try: hx.update({int(k): v for k, v in json.load(open(fn))['res'].items()})
    except Exception: pass
lect = ('tA', 'tA2', 'tB', 'tC')
ok_hx = sum(1 for v in hx.values() if all(v[k]['juste'] and v[k]['propre'] for k in lect) and v['sorties_usage2'])
fin = etape.startswith('fin')
if c is not None and len(hx) == N and cj == cp == 256 and ok_hx == N: v1 = f"VERDICT : OK — {N}/{N} justes et propres (hx, 4 lectures + 8 ports), C {cj}/256 justes"
elif fin and ((c is not None and (cj < 256 or cp < 256)) or ok_hx < len(hx)): v1 = f"VERDICT : ÉCHEC — hx {ok_hx}/{len(hx)} justes et propres, C {cj if c else '?'}/256 justes"
else: v1 = f"VERDICT : PARTIEL — hx {ok_hx}/{len(hx)} justes et propres (sur {N}), C {(str(cj) + '/256 justes, ' + str(cp) + ' propres') if c else 'pas fini'}"
L += [v1, f"durée {dt} s ; étape : {etape}"]
if c is not None: L.append(f"moteur C à tC = {M.TC} : {cj}/256 justes, {cp}/256 propres ; empreintes distinctes {len({v['empreinte'] for v in c.values()})}")
if hx:
    for k in lect: L.append(f"hx {k} : justes {sum(v[k]['juste'] for v in hx.values())}/{len(hx)}, propres {sum(v[k]['propre'] for v in hx.values())}/{len(hx)}")
    L.append(f"hx sorties du pas 2 (usage 2) justes : {sum(v['sorties_usage2'] for v in hx.values())}/{len(hx)}")
    if c is not None: L.append(f"C et hx même état final (empreinte) : {sum(1 for i, v in hx.items() if str(i) in c and c[str(i)]['empreinte'] == v['empreinte'])}/{len(hx)}")
    # premier état faux par pixel et par lecture : lu / attendu
    T = dict(tA=M.TA, tA2=M.TA2, tB=M.TB, tC=M.TC); first = {}
    for i in sorted(hx):
        v = hx[i]
        for k in lect:
            for nm in M.CASES:
                want = list(M.predict(envs[i], nm, T[k])); got = v[k]['lu'][nm]
                if got != want and (nm, k) not in first: first[(nm, k)] = (i, got, want)
        for p, (a, b) in v.get('lectures', {}).items():
            if a != b and ('port ' + p, 'tA2') not in first: first[('port ' + p, 'tA2')] = (i, a, b)
    if first:
        L.append("premiers états faux (pixel, lecture : état n°, lu → attendu) :")
        L += [f"  {nm} {k} : n° {i}, lu {g} au lieu de {w}" for (nm, k), (i, g, w) in sorted(first.items())][:30]
    else: L.append("aucun pixel faux dans les états hx calculés")
if c is not None and cj < 256:
    bad = [int(i) for i, v in c.items() if not v['juste']]; L.append(f"C faux (tC) : {len(bad)} états, premiers {sorted(bad)[:12]}")
    for nm in M.CASES:
        b = [i for i in sorted(bad) if c[str(i)]['lu'][nm] != list(M.predict(envs[i], nm, M.TC))]
        if b: L.append(f"  C {nm} : premier faux n° {b[0]}, lu {c[str(b[0])]['lu'][nm]} au lieu de {list(M.predict(envs[b[0]], nm, M.TC))} ({len(b)} états)")
open(os.path.join(OUT, 'resume.txt'), 'w').write('\n'.join(L[:50]) + '\n')
# résultats compacts (< 1 Mo) : par état, (juste, propre) aux 4 lectures + sorties + empreinte
json.dump(dict(C={k: [v['juste'], v['propre'], v['empreinte']] for k, v in (c or {}).items()},
               hx={i: [[v[k]['juste'], v[k]['propre']] for k in lect] + [v['sorties_usage2'], v['empreinte'], v.get('lectures', {})] for i, v in hx.items()}),
          open(os.path.join(OUT, 'r723.json'), 'w'))
EOF
}
etape() { echo "$1" > "$W/etape"; echo "$(date -u +%T) $1"; resume; }
( while sleep 600; do resume; done ) & VEILLE=$!
cd "$T4"
etape "moteur C à tC, 256 états"
TC_MAX=$(( BUDGET - 1800 )); [ "$PETIT" = 1 ] && TC_MAX=20
timeout $TC_MAX python3 -c "
import sys, runpy; sys.path.insert(0, '$S3'); sys.path.insert(0, '$T4')
import s3lib; s3lib.run_c.__defaults__ = ($NPROC,)
sys.argv = ['deux_pas_long.py', 'C']; runpy.run_path('deux_pas_long.py', run_name='__main__')" 2>&1 | tail -3
etape "hx.py sur 256 états, $NPROC tranches"
N=256; [ "$PETIT" = 1 ] && N=2
RESTE=$(( BUDGET - $(date +%s) + T0 - 300 ))
seq 0 $((NPROC-1)) | xargs -P "$NPROC" -I{} sh -c "i0=\$(( {} * $N / $NPROC )); i1=\$(( ({} + 1) * $N / $NPROC )); [ \$i1 -gt \$i0 ] && timeout $RESTE python3 deux_pas_long.py hx \$i0 \$i1 > /dev/null 2>&1; true"
etape "fin"
pkill -P $VEILLE 2>/dev/null; kill $VEILLE 2>/dev/null; resume; cat "$OUT/resume.txt"; rm -f "$S3/fourmi_r_big"
