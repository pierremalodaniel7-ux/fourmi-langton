#!/usr/bin/env python3
"""suivi.py fichier_chaine.json [idx] [pas] : suit chaque sonde (fourmi 0 = dernière impulsion) d'une chaîne de bascule,
position toutes les `pas` étapes (moteur Python moteur2.py)."""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../bascule'))
from moteur2 import charge, pas
H=json.load(open(sys.argv[1])); h=H[int(sys.argv[2]) if len(sys.argv)>2 else -1]; P=int(sys.argv[3]) if len(sys.argv)>3 else 1000
turn,ants,noir=charge(h['situation']); n=len(ants)
for t in range(h['T']+1):
    if t%P==0: print(t, len(noir), ' '.join(f'{a[0]},{a[1]}' for a in ants))
    if t<h['T']: pas(turn,ants,noir,range(n))
