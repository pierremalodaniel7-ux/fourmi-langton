#!/usr/bin/env python3
"""Découpe un fichier .txt du Drive (« =================== nom.c =================== » entre chaque
programme) en vrais fichiers dans src/.  Usage : python3 outils/decoupe.py fichier.txt [dossier]"""
import re, sys, pathlib

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "src")
out.mkdir(exist_ok=True)
# Le Drive échappe parfois les caractères (\= \# \< \> \_ \[ \]) : on les rétablit.
src = re.sub(r"\\([=#<>_\[\]*`])", r"\1", src)
parts = re.split(r"^=+\s*([\w./-]+)\s*=+\s*$", src, flags=re.M)
for nom, corps in zip(parts[1::2], parts[2::2]):
    (out / nom).write_text(corps.strip("\n") + "\n", encoding="utf-8")
    print(f"{nom}: {corps.count(chr(10))} lignes")
