# enum.py — toutes les règles L/R de longueur q (à rotation et miroir près NON réduites : on garde tout, c'est simple)
import itertools, subprocess, sys
qmin, qmax, T = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
out = open(sys.argv[4], 'w')
for q in range(qmin, qmax + 1):
    for w in itertools.product('LR', repeat=q):
        r = ''.join(w)
        if 'L' not in r or 'R' not in r: continue
        if r != min(r[i:] + r[:i] for i in range(q)): pass  # (rotations = règles différentes, on garde)
        o = subprocess.run(['./hw2', r, '1', '1', T, '1', '0', '0', '0'], capture_output=True, text=True).stdout
        out.write(o if o else f'N|{r}\n'); out.flush()


