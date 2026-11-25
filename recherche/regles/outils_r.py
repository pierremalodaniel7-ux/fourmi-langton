"""Outils communs du banc (recherche/regles) : lancer fourmi_r en lot sur 2 cœurs, lire la sortie."""
import subprocess, threading
EXE = './fourmi_r'
def lot(lines, T, opts=(), ncpu=2):
    """renvoie la liste des lignes de sortie (dans l'ordre des entrées) ; une ligne de sortie par situation (+ DUMP éventuel)."""
    lines = list(lines)
    parts = [lines[i::ncpu] for i in range(ncpu)]
    res = [None] * ncpu
    def w(k):
        out = subprocess.run([EXE, '-T', str(T), *opts, '-lot'], input='\n'.join(parts[k]) + '\n', capture_output=True, text=True).stdout
        res[k] = [l for l in out.splitlines() if not l.startswith('DUMP') and not l.startswith('ZERO')]
    th = [threading.Thread(target=w, args=(k,)) for k in range(ncpu)]
    [t.start() for t in th]; [t.join() for t in th]
    out = [None] * len(lines)
    for k in range(ncpu):
        for j, l in enumerate(res[k]): out[k + j * ncpu] = l
    return out
def parse(l):
    """-> dict issue, sig, t, ants=[(P,dx,dy,deb) ou None], fin=[(x,y)]"""
    f = l.split('|')
    d = {'issue': f[3], 'sig': f[4], 't': int(f[5])}
    det = f[6].split(' boite ')[0].split()
    det = [x for x in det if x not in ('CERT', 'NONCERT') and not x.startswith('|V|')]
    ants = []
    for x in det:
        if x == '-': ants.append(None)
        else:
            try: P, dx, dy, deb = map(int, x.split(',')); ants.append((P, dx, dy, deb))
            except ValueError: pass
    d['ants'] = ants
    fin = f[6].split(' fin ')[1].split() if ' fin ' in f[6] else []
    d['fin'] = [tuple(map(int, p.split(','))) for p in fin]
    d['boite'] = f[6].split(' boite ')[1].split(' fin')[0] if ' boite ' in f[6] else ''
    return d
SQ = [(0,-1),(1,0),(0,1),(-1,0)]; HX = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]; TR = [(1,0),(1,0),(0,1),(-1,0),(-1,0),(0,-1)]
def geo(rule):
    if rule.startswith('H:'): return HX, 6
    if rule.startswith('T:'): return TR, 6
    return SQ, 4
def ncol(rule):
    if rule.startswith('H:'): return sum(1 for c in rule[2:] if c in 'NRLU' )
    if rule.startswith('T:'): return len(rule) - 2
    return len(rule)
