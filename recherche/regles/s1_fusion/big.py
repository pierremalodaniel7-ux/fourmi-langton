"""S1 : fourmi_r est limité à 128 fourmis (MAXA, les suivantes sont IGNORÉES sans message). fourmi_r512 = même source, MAXA = 512.
patch() fait utiliser fourmi_r512 par fa_lib.lotdump (et donc circuit.check_multi / check_cases)."""
import os, subprocess, threading, fa_lib, circuit
EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fourmi_r512')
def lotdump(lines, T, ncpu=2):
    parts = [lines[i::ncpu] for i in range(ncpu)]; res = [None] * ncpu
    def w(k):
        o = subprocess.run([EXE, '-T', str(T), '-x', '-dump', '-lot'], input='\n'.join(parts[k]) + '\n', capture_output=True, text=True).stdout
        res[k] = [l for l in o.splitlines() if l.startswith('DUMP')]
    th = [threading.Thread(target=w, args=(k,)) for k in range(ncpu)]; [t.start() for t in th]; [t.join() for t in th]
    out = [None] * len(lines)
    for k in range(ncpu):
        for j, l in enumerate(res[k]): out[k + j * ncpu] = fa_lib.parse_dump(l)
    return out
def patch():
    fa_lib.lotdump = lotdump; circuit.lotdump = lotdump
