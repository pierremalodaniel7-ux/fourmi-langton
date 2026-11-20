#!/usr/bin/env python3
"""Énumère les règles L/R à balayer : mots primitifs (pas w^k), au moins un L et un R,
un seul représentant par paire L<->R (celui qui commence par L). Usage : regles_lr.py QMIN QMAX"""
import sys, itertools
def primitif(w):
    n=len(w); return all(w!=w[:d]*(n//d) for d in range(1,n) if n%d==0)
a,b=int(sys.argv[1]),int(sys.argv[2])
for q in range(a,b+1):
    for t in itertools.product("LR",repeat=q-1):
        w="L"+"".join(t)
        if "R" in w and primitif(w): print(w)
