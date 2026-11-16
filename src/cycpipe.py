# cycpipe.py — pour chaque type de cycle (CYCn P / NIDk P) trouvé, analyse 1 à 2 représentants avec exploreY
# et regroupe par « orbite » (invariants : P, cases du cycle, noires min/max, composantes).
# Usage : python3 cycpipe.py SORTIE.json fichiers...
import sys, subprocess, collections, json, re
out = sys.argv[1]; filt = sys.argv[2]; files = sys.argv[3:]
reps = collections.defaultdict(list)
for fn in files:
    for L in open(fn):
        p = L.rstrip('\n').split('|')
        if len(p) < 5: continue
        fam, sig, f, c, info = p
        m = re.search(r'(CYC\d+|NID\d+)(?: |:)P=(\d+)', sig)
        if not m: continue
        key = (m.group(1), int(m.group(2)))
        if not key[0].startswith(filt): continue
        if len(reps[key]) < 2: reps[key].append((fam, sig, f, c))
        else: reps[key].append(None) if False else None
cnt = collections.Counter()
for fn in files:
    for L in open(fn):
        m = re.search(r'(CYC\d+|NID\d+)(?: |:)P=(\d+)', L)
        if m: cnt[(m.group(1), int(m.group(2)))] += 1
res = []
import random
random.seed(1)
keys = list(reps)
sel = set(sorted(keys, key=lambda k: -k[1])[:25]) | set(sorted(keys, key=lambda k: -cnt[k])[:25]) | set(random.sample(keys, min(120, len(keys))))
for key in sorted(sel):
    lst = reps[key][:1]
    for fam, sig, f, c in lst:
        T = str(max(400000, key[1] * 3 + 200000))
        r = subprocess.run(['./exploreY', 'Y', '1', '1', T, f.replace(' ', ''), c.replace(' ', '')], capture_output=True, text=True, timeout=600).stdout
        a = [l for l in r.splitlines() if l.startswith('ANALYSE')]
        if not a: continue
        d = dict(kv.split('=', 1) for kv in re.findall(r'(\w+=\S+)', a[0]))
        comps = re.search(r'[(.*?)]', a[0]).group(1)
        res.append({'type': key[0], 'P': key[1], 'freq': cnt[key], 'fam': fam, 'sig': sig, 'fourmis': f, 'cases': c,
                    'cases_cycle': int(d['cases_du_cycle']), 'boite': d['boite'], 'nmin': int(d['noires_min']), 'nmax': int(d['noires_max']),
                    'composantes': int(d['composantes']), 'comps': comps, 'brut': a[0]})
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=0)
print(len(reps), 'types,', len(res), 'analyses')
