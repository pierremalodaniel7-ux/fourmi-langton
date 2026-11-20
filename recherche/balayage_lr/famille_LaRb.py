#!/usr/bin/env python3
"""Teste la conjecture LᵃRᵇ sur regles_lr.csv :
 b=1, a>=3 : P = 16a+4 (connu) ; b impair >=3, a >= b-1 : P = 16(a+b)-20 ou sa moitié ; b pair : pas d'autoroute."""
import csv, os, re
H = os.path.dirname(os.path.abspath(__file__))
rows = {r["regle"]: r for r in csv.DictReader(open(os.path.join(H, "regles_lr.csv")))}
ok = bad = 0; lines = []
for w, r in sorted(rows.items(), key=lambda x: (len(x[0]), x[0])):
    m = re.fullmatch(r"(L+)(R+)", w)
    if not m: continue
    a, b = len(m.group(1)), len(m.group(2)); cl = r["classe"]; P = int(r["periode"] or 0)
    if b == 1 and a >= 3: pred = {16*a+4}
    elif b % 2 == 1 and b >= 3 and a >= b-1: F = 16*(a+b)-20; pred = {F, F//2}
    elif b % 2 == 0: pred = None
    else: pred = "?"
    if pred == "?": tag = "hors conjecture"
    elif pred is None: tag = "OK" if cl != "V" else "CONTRE-EX"
    else: tag = "OK" if (cl == "V" and P in pred) else "CONTRE-EX"
    if tag == "OK": ok += 1
    elif tag == "CONTRE-EX": bad += 1
    lines.append(f"{w:18s} a={a:2d} b={b:2d} {cl} P={P:5d} début={r['debut']:>8s} cert={'oui' if r['t_certificat'] else 'non'} {tag}"
                 + (f" (moitié)" if cl == "V" and pred not in (None, '?') and P == min(pred) and len(pred) > 1 else ""))
open(os.path.join(H, "famille_LaRb.txt"), "w").write("\n".join(lines) + f"\nconformes {ok}, contre-exemples {bad}\n")
print("\n".join(l for l in lines if "CONTRE" in l or "hors" in l)); print("conformes", ok, "contre-exemples", bad)
