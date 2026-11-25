#!/bin/bash
# pipeline.sh NOM CYFILE : recherche complète de bascules T (idéalisées puis honnêtes) sur toutes les orbites de CYFILE.
# 1) tirs sur S0 (flux.sh) 2) déviations « pièce intacte » 3) résidus S1 (dev.py) 4) liste S1 (s1list.py) 5) tirs sur S1
# 6) résidus S2 7) retours à S0 (toggle.py) 8) test honnête (honnete.py). Tout dans data/bascule/NOM_*.
set -e; N=$1; CYF=$2; D=$(cd $(dirname $0); pwd); O=$D/../../data/bascule; cd $D
n=$(python3 -c "import json;print(len(json.load(open('$CYF'))))")
echo "$(date +%T) $n orbites"
CY=$CYF ./flux.sh ${N}_a 0 $n 20000 -8,-8,14,14 2>/dev/null
filtre() { python3 - "$1" "$2" <<'PY'
import sys
out=open(sys.argv[2],'w'); n=0
for l in open(sys.argv[1]):
    f=l.rstrip().split('|')
    if len(f)<5 or f[2]!='MIXTE': continue
    try: pts=[tuple(map(int,p.split(',')[:2])) for p in f[4].split(' fin ')[1].split()]
    except Exception: continue
    det=f[4].split(' boite')[0].split()
    if det[0]=='-' or det[0].startswith('104,-2,2,') or len(pts)<3: continue
    if all(-15<=x<=22 and -15<=y<=22 for x,y in pts[1:]) and not(-30<=pts[0][0]<=40 and -30<=pts[0][1]<=40) and all(d=='-' for d in det[1:]):
        out.write(l); n+=1
print(n,'déviations pièce intacte')
PY
}
filtre $O/${N}_a.res $O/${N}_a_dev.res
split -n l/4 -d $O/${N}_a_dev.res $O/${N}_ap
for p in $O/${N}_ap0?; do CY=$CYF python3 dev.py $p > $p.json & done; wait
cat $O/${N}_ap0?.json > $O/${N}_a.json; rm $O/${N}_ap0?*
S1F=cyclesS1_$N.json python3 s1list.py $O/${N}_a.json
m=$(python3 -c "import json;print(len(json.load(open('cyclesS1_$N.json'))))")
CY=cyclesS1_$N.json ./flux.sh ${N}_b 0 $m 20000 -8,-8,14,14 2>/dev/null
filtre $O/${N}_b.res $O/${N}_b_dev.res
split -n l/4 -d $O/${N}_b_dev.res $O/${N}_bp
for p in $O/${N}_bp0?; do CY=cyclesS1_$N.json python3 dev.py $p > $p.json & done; wait
cat $O/${N}_bp0?.json > $O/${N}_b.json; rm $O/${N}_bp0?*
CY=$CYF S1F=cyclesS1_$N.json HITS=$O/${N}_hits.json python3 toggle.py $O/${N}_b.json | head -3
CY=$CYF S1F=cyclesS1_$N.json python3 honnete.py $O/${N}_hits.json 60 200 | tail -1
echo "$(date +%T) fini"
