# Test : vérifie que les deux moteurs tournent sur GitHub.
{
echo "test d'installation du $(date -u +%F)"
echo "coeurs : $NPROC"
./src/fourmi "RL|0,0,H|" | head -3
./recherche/regles/fourmi_r -h 2>&1 | head -2
} > "$OUT/resume.txt"
cat "$OUT/resume.txt"
# relance du test
