#!/usr/bin/env python3
"""Découpe un export texte du Drive (plusieurs programmes à la suite) en vrais fichiers.
Repères reconnus :  « ===== nom.c ===== »,  une ligne qui ne contient que « nom.c »,  « Code nom.c (…) ».
Le texte en prose entre deux programmes est retiré (C : on coupe après la dernière accolade fermante ;
Python : on coupe au premier double saut de ligne suivi de prose).
Usage : python3 outils/decoupe.py FICHIER [DOSSIER=src]"""
import re, sys, pathlib

lignes = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").split("\n")
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "src"); out.mkdir(exist_ok=True)
NOM = r"([A-Za-z0-9_]+\.(?:c|h|py|sh))"
reperes = [re.compile(rf"^\\?=+\s*{NOM}\s*\\?=+\s*$"), re.compile(rf"^{NOM}\s*$"), re.compile(rf"^Code {NOM}\b")]
blocs, nom, cur = [], None, []
for l in lignes:
    l = re.sub(r"\\([=#<>_\[\]*`])", r"\1", l)          # échappements du Drive
    l = re.sub("[\ue000-\uf8ff\u200b\ufeff]", "", l).replace("\u00a0", " ")  # marques de bloc de code Google Docs
    m = next((r.match(l) for r in reperes if r.match(l)), None)
    if m:
        if nom: blocs.append((nom, cur))
        nom, cur = m.group(1), []
    elif nom: cur.append(l)
if nom: blocs.append((nom, cur))
vus = {}
for nom, cur in blocs:
    if nom.endswith((".c", ".h")):
        fin = max((i for i, l in enumerate(cur) if l.rstrip().endswith("}") or l.startswith("#endif")), default=len(cur) - 1)
        cur = cur[:fin + 1]
    else:
        while cur and (not cur[-1].strip() or re.match(r"^[A-ZÀ-Ý][^=():]*$", cur[-1]) and not cur[-1].startswith(("#", "import"))):
            cur.pop()
    if nom in vus:                                    # même nom deux fois : garder les deux
        vus[nom] += 1; nom = nom.replace(".", f"_{vus[nom]}.")
    else: vus[nom] = 1
    (out / nom).write_text("\n".join(cur).strip("\n") + "\n", encoding="utf-8")
    print(f"{nom}: {len(cur)} lignes")
