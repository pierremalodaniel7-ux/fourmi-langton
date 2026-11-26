#!/usr/bin/env python3
"""aretes.py : dans un cycle exact, compte pour chaque arête les passages dans chaque sens. Observation (R-139 bis) :
flux net nul sur chaque arête (⇒ autant de pas de chaque classe ⇒ loi d'équilibre). Usage : aretes.py fichier.json [max] | cat (situations de cycle)"""
import sys, json, collections
from moteur2 import charge, pas
def test(sit,p):
    turn,an,no=charge(sit); n=len(an); F=collections.Counter()
    for t in range(p):
        old=[(a[0],a[1]) for a in an]; pas(turn,an,no,range(n))
        for i in range(n): F[(old[i],(an[i][0],an[i][1]))]+=1
    return all(F[(u,v)]==F[(v,u)] for (u,v) in F)
if __name__=='__main__':
    L=json.load(open(sys.argv[1])); mx=int(sys.argv[2]) if len(sys.argv)>2 else 10**9; ok=0; k=0
    for c in L[:mx]:
        k+=1; ok+=test(c['situation'],c['periode'])
    print(sys.argv[1],':',ok,'/',k,'cycles à flux nul sur chaque arête')
