"""Lance une liste de passes t2_sym2.py (une par ligne de commande) et réécrit $OUT/resume.txt toutes les 10 min.
Usage : python3 ../../calculs/run_t2.py porte|div4"""
import os, sys, subprocess, time, json, re, threading
OUT = os.environ['OUT']; quoi = sys.argv[1]; P = os.environ.get('PETIT') == '1'; T0 = time.time(); BUD = 18900 - 600
if quoi == 'porte':
    passes = [dict(BIT='both', mode='exact', Pmax='1200', n='30'), dict(BIT='both', mode='retard', Pmax='900', n='300')]
    if P: passes = [dict(BIT='both', mode='retard', Pmax='520', n='20', NJMAX='800')]
else:
    N = len(json.load(open('s2_horloge/t2_sym_doublement504.json')))
    passes = [dict(BIT='X0', mode=m, Pmax='9999', n=n, BASE='s2_horloge/t2_sym_doublement504.json:%d' % i, TMUL='8')
              for m, n in (('exact', '30'), ('retard', '300')) for i in range(N)]
    if P: passes = passes[:2] + passes[N:N + 2]
log = []; etat = {'fini': 0, 'cle': 0, 'cycles': 0}
def resume(fin=False):
    v = 'OK' if etat['cle'] > 0 else ('ÉCHEC' if fin else 'PARTIEL')
    nom = 'poses qui lisent le bit (2 CYCLE ≠ ou 1 seul)' if quoi == 'porte' else 'machines de période 4·504 = 2 016 (diviseur par 4)'
    L = ['VERDICT : %s — %s : %d ; passes %d/%d ; %d min' % (v, nom, etat['cle'], etat['fini'], len(passes), (time.time() - T0) // 60)]
    L += log[-45:]
    open(os.path.join(OUT, 'resume.txt'), 'w').write('\n'.join(L[:50]) + '\n')
def tic():
    while True:
        time.sleep(600); resume()
threading.Thread(target=tic, daemon=True).start()
for k, p in enumerate(passes):
    if time.time() - T0 > BUD: log.append('budget atteint, passe %d non faite' % k); break
    env = dict(os.environ, **{a: b for a, b in p.items() if a not in ('mode', 'Pmax', 'n')}, OUTJ=os.path.join(OUT, 'cycles_%s_%d.json' % (quoi, k)))
    r = subprocess.run(['python3', 's2_horloge/t2_sym2.py', p['Pmax'], p['mode'], p['n']], env=env, capture_output=True, text=True,
                       timeout=max(60, BUD - (time.time() - T0)))
    if r.returncode: log.append('passe %d ERREUR : %s' % (k, r.stderr[-300:].replace('\n', ' '))); continue
    out = r.stdout; etat['fini'] += 1
    hits = json.load(open(env['OUTJ'])) if os.path.exists(env['OUTJ']) else []
    if not hits and os.path.exists(env['OUTJ']): os.remove(env['OUTJ'])
    elif os.path.getsize(env['OUTJ']) > 900000: json.dump(hits[:300], open(env['OUTJ'], 'w'))
    etat['cycles'] += len(hits)
    if quoi == 'porte':
        m = re.search(r'LECTURE poses (\d+) deux CYCLE de périodes différentes (\d+) un seul CYCLE (\d+)', out)
        if m: etat['cle'] += int(m[2]) + int(m[3])
        log.append('passe %d %s : %s' % (k, p['mode'], m[0] if m else out[-200:]))
    else:
        d4 = [h for h in hits if h['P'] == 4 * 504]
        etat['cle'] += len(d4)
        pa = re.search(r'PAIRES (.*)', out)
        log.append('passe %d %s base %s : CYCLE %d, période 2016 : %d ; %s' % (k, p['mode'], p['BASE'][-3:], len(hits), len(d4), (pa[1] if pa else '')[:120]))
    resume()
resume(fin=True); print(open(os.path.join(OUT, 'resume.txt')).read())
sys.exit(0 if etat['cle'] > 0 and etat['fini'] == len(passes) else (3 if etat['cle'] == 0 else 0))
