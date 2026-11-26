#!/usr/bin/env python3
"""R-309 Densité de trace : cases non blanches laissées par période (germe, 200 et 400 périodes)."""
import json, subprocess
from banc import launcher, sit
G = json.load(open('data/germes_regles.json'))
for rule, g in G.items():
    a, c = launcher(g); n = []
    for k in (200, 400):
        out = subprocess.run(['./fourmi_r', '-T', str(k * g['P']), '-x', '-dump', '-lot'], input=sit(rule, [a], c) + '\n', capture_output=True, text=True).stdout
        d = [l for l in out.splitlines() if l.startswith('DUMP')][0].split('|')[2]
        n.append(len([x for x in d.split(';') if x]))
    print(f"{rule}\tP={g['P']}\tgerme={len(g['cases'])}\tcases(200P)={n[0]}\tcases(400P)={n[1]}\tpar période={(n[1]-n[0])/200:.2f}")
