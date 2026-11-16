# ana.py — tri des sorties d'explore : classes de signatures, rares et « hors liste connue ».
# Usage : python3 ana.py runs/*.txt
import sys, re, collections
CONNU = {'1p104(2,2)', 'G2p104(2,2)', 'G3p104(2,2)', 'G4p104(2,2)', 'G2p102(3,5)', '1p108(2,2)', '1p100(2,2)', '1p388(6,10)',
         'G4p12(2,0)', 'G4p52(2,0)', 'G4p24(2,0)', 'G2p96(2,0)', 'G4p16(4,0)', 'G4p48(4,0)'}
ARTEFACT = re.compile(r'^(G?\d+)?p(0|2|10|12)\((0,0|1,1|2,2)\)$')   # bords de losange / sorties non périodiques
def toks(sig): return [t for t in sig.split() if t and not t.startswith('[')]
stats = collections.Counter(); ex = {}
for fn in sys.argv[1:]:
    for L in open(fn):
        p = L.rstrip('\n').split('|')
        if len(p) < 5: continue
        fam, sig, f, c, info = p
        s2 = re.sub(r'P=\d+', 'P=*', sig)
        if sig.startswith('CYC'):
            k=sig.split()[0]; stats[k]+=1
            if k not in ex: ex[k]=(fam,sig,f,c,info)
            continue
        for t in toks(sig):
            if t.startswith('s:'): continue
            if t.startswith('NID') or t.startswith('CYC'): k = t.split(':')[0].split(' ')[0]
            else: k = t
            stats[k] += 1
            if k not in ex: ex[k] = (fam, sig, f, c, info)
        if sig.startswith('CYC'):
            n = int(sig[3:].split()[0])
            stats['CYC%d' % n] += 0
print('== tokens ==')
for k, v in stats.most_common():
    tag = 'connu' if k in CONNU else ('artefact' if ARTEFACT.match(k) else ('cycle/nid' if k.startswith(('CYC', 'NID')) else 'NOUVEAU?'))
    print(f'{v:8d}  {k:22s} {tag:10s} ex: {ex[k][0]} | {ex[k][2]} | {ex[k][3][:60]}')
