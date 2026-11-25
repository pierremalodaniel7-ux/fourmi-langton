#!/usr/bin/env python3
"""Tableau comparatif règle × (fil, déviation, croisement, réutilisation, gomme) à partir des fichiers data/ du banc.
Sortie : resumes/tableau.md + resumes/tableau.json"""
import json, os, glob
G = json.load(open('data/germes_regles.json'))
fil = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open('data/fil_resume.txt')}
trace = {l.split('\t')[0]: l.split('\t')[-1].split('=')[1].strip() for l in open('data/trace.txt')}
def gomme(r):
    if r.startswith('H:'):
        m = {'N':0,'R1':1,'R2':2,'U':3,'L2':4,'L1':5}; s = r[2:]; K = []
        while s:
            for k in ('R1','R2','L1','L2','N','U'):
                if s.startswith(k): K.append(m[k]); s = s[len(k):]; break
        M = 6
    else: K = [{'L':3,'R':1,'N':0,'U':2}[c] for c in r]; M = 4
    return len(K) == 2 and (K[0] + K[1]) % M == 0
def J(p):
    try: return json.load(open(p))
    except Exception: return None
rows = []
for r, g in G.items():
    f = r.replace(':', '_')
    b = J(f'data/banc_{f}.json') or {}
    mi = J(f'data/miroirs_{f}.json'); mu = J(f'data/murs_{f}.json'); co = J(f'data/collisions_{f}.json'); rc = J(f'data/reuse_chocs_{f}.json')
    fl = fil.get(r)
    pct = round(100 * int(fl[2].split()[1]) / int(fl[1]), 1) if fl else None
    b1 = b.get('b1_1case', {}); b2 = b.get('b2_2cases', {}); b3 = b.get('b3_trace') or {}
    dirs = set()
    for x in (b1, b2):
        dirs |= {k for k in x.get('dirs', {}) if k != '0'}
    if mi:
        for k in mi['issues']:
            t = eval(k)
            if t[0] == 'propre' and t[1] not in (0, None): dirs.add(str(t[1]))
    defl1 = sum(v for k, v in b1.get('dirs', {}).items() if k != '0')
    reuse_obst = sum(1 for x in (mi or {}).get('reuse', []) if x['m'] == 10 and x['reutilisable'])
    n_obst = sum(1 for x in (mi or {}).get('reuse', []) if x['m'] == 10)
    ct = sum(v for k, v in (co or {}).get('cat', {}).items() if k.endswith("'T')"))
    cx = sum(v for k, v in (co or {}).get('cat', {}).items() if k.endswith("'X')"))
    cn = (co or {}).get('n', 0)
    libre = b.get('d_reutilisation', {}).get('libre_m10', {})
    lib_ok = bool(libre) and libre['B'][0] == 'propre' and libre['B'][1] == 0 and libre['B'][2] == libre['solo'][2]
    rc_s = (rc or {}).get('stat', {}); rc_ok = rc_s.get("(100, True)", 0); rc_n = (rc or {}).get('devies', 0)
    rows.append(dict(regle=r, P=g['P'], germe=len(g['cases']), debut_blanc=g['debut_blanc'] if g['depart'].endswith('|0,0,0|') else None,
        pct_petits=pct, trace=trace.get(r), gomme=gomme(r),
        dev1=f"{b1.get('propre')}/{b1.get('n')}", dev1_devie=defl1, chaos1=b1.get('chaos_med'), dev2=f"{b2.get('propre')}/{b2.get('n')}",
        trace_B=f"{b3.get('B_propre')}/{b3.get('n')}", nb_dirs=len(dirs),
        crois_T=f"{ct}/{cn}", crois_X=cx, lane_libre=lib_ok, miroir_reutil=f"{reuse_obst}/{n_obst}", choc_reutil=f"{rc_ok}/{rc_n}"))
json.dump(rows, open('resumes/tableau.json', 'w'), indent=1)
H = ['regle','P','germe','debut_blanc','pct_petits','trace','dev1','dev1_devie','chaos1','dev2','trace_B','nb_dirs','crois_T','crois_X','lane_libre','miroir_reutil','choc_reutil','gomme']
with open('resumes/tableau.md', 'w') as o:
    o.write('| ' + ' | '.join(H) + ' |\n|' + '---|' * len(H) + '\n')
    for x in rows: o.write('| ' + ' | '.join(str(x[h]) for h in H) + ' |\n')
print(open('resumes/tableau.md').read())
