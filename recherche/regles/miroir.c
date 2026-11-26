// miroir.c (nuit 26/11) — OUTIL DE RECHERCHE hexa R2L2 (pas un moteur du projet : toute trouvaille est revérifiée avec
// fourmi_r et hx.py). Même convention que fourmi_r : axiales, caps 0=E 1=SE 2=SO 3=O 4=NO 5=NE, blanc -> +2, noir -> +4,
// fourmis jouées l'une après l'autre dans l'ordre de la liste, grille infinie simulée par un tableau 2048² (on vérifie les bords).
//
// Modes :
//  ./miroir enum NA BOX NC TMAX [seed nb]   : oscillateurs (cycles exacts) à NA fourmis, fourmi 0 en (0,0), les autres dans [-BOX,BOX]²,
//                                     0..NC cases dans [-2,2]² ; TMAX pas max ; seed/nb : tirage au hasard de nb configurations.
//                                     Sortie : OSC p na | situation   (une par orbite distincte à translation/rotation près)
//  ./miroir tir D T < oscillateurs    : chaque oscillateur reçoit un vaisseau de chaque direction r (6), chaque voie, chaque phase,
//                                     ordre « vaisseau en dernier » puis « en premier ». Sortie : lignes MIR / TRA / DEC + résumé.
//  ./miroir reuse NV < lignes MIR      : rejoue chaque miroir avec NV vaisseaux successifs, espacements s = 20..20+p+8 périodes.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 2048
#define O 1024
#define MA 64
static uint8_t g[N * N], tm[N * N];
static int *touch; static long nt = 0, tcap = 0;
static const int DX[6] = {1, 0, -1, -1, 0, 1}, DY[6] = {0, 1, 1, 0, -1, -1}, KK[2] = {2, 4};
typedef struct { int x, y, h; } Ant;
static int oob = 0;
static inline void mark(int i){ if (!tm[i]) { tm[i] = 1; if (nt == tcap) { tcap = tcap ? 2 * tcap : 1 << 16; touch = realloc(touch, tcap * sizeof(int)); } touch[nt++] = i; } }
static inline void step(Ant *a, int n){
  for (int k = 0; k < n; k++) {
    int i = (a[k].y + O) * N + a[k].x + O; int c = g[i];
    a[k].h = (a[k].h + KK[c]) % 6; g[i] = c ^ 1; mark(i);
    a[k].x += DX[a[k].h]; a[k].y += DY[a[k].h];
    if (a[k].x < -O + 4 || a[k].x > O - 4 || a[k].y < -O + 4 || a[k].y > O - 4) { oob = 1; a[k].x = 0; a[k].y = 0; }
  }
}
static void clear(void){ for (long k = 0; k < nt; k++) { g[touch[k]] = 0; tm[touch[k]] = 0; } nt = 0; }
static void setc(int x, int y){ int i = (y + O) * N + x + O; g[i] = 1; mark(i); }
static void rot(int *x, int *y, int r){ for (int k = 0; k < ((r % 6) + 6) % 6; k++) { int t = *x; *x = -*y; *y = t + *y; } }
static int hd(int dx, int dy){ int s = dx + dy; return (abs(dx) + abs(dy) + abs(s)) / 2; }
// ---- vaisseau : 48 phases (cap, cases noires relatives) ----
typedef struct { int h, nc, cx[8], cy[8]; } Ph;
static Ph PH[48]; static int PAX[48], PAY[48];
static int cmpi2(const void *a, const void *b){ const int *p = a, *q = b; return p[0] != q[0] ? p[0] - q[0] : p[1] - q[1]; }
static void ships(void){
  for (int r = 0; r < 6; r++) {
    int cx = 1, cy = 0; rot(&cx, &cy, r);
    Ant a = {0, 0, (4 + r) % 6}; setc(cx, cy);
    for (int ph = 0; ph < 8; ph++) {
      Ph *P = &PH[r * 8 + ph]; P->h = a.h; P->nc = 0; int tmp[16]; PAX[r * 8 + ph] = a.x; PAY[r * 8 + ph] = a.y;
      for (long k = 0; k < nt; k++) if (g[touch[k]]) { int x = touch[k] % N - O, y = touch[k] / N - O; tmp[2 * P->nc] = x - a.x; tmp[2 * P->nc + 1] = y - a.y; P->nc++; }
      qsort(tmp, P->nc, 2 * sizeof(int), cmpi2);
      for (int j = 0; j < P->nc; j++) { P->cx[j] = tmp[2 * j]; P->cy[j] = tmp[2 * j + 1]; }
      step(&a, 1);
    }
    clear();
  }
}
// identifie un vaisseau : fourmi a + cases noires à distance <= 3 ; renvoie r*8+ph ou -1 ; nb = nb de cases utilisées
static int ship_id(Ant a, int *nb){
  int tmp[64], n = 0;
  for (int dy = -3; dy <= 3; dy++) for (int dx = -3; dx <= 3; dx++) if (hd(dx, dy) <= 3) {
    int i = (a.y + dy + O) * N + a.x + dx + O; if (g[i]) { if (n < 30) { tmp[2 * n] = dx; tmp[2 * n + 1] = dy; } n++; } }
  *nb = n; if (n > 8) return -1;
  qsort(tmp, n, 2 * sizeof(int), cmpi2);
  for (int k = 0; k < 48; k++) { if (PH[k].h != a.h || PH[k].nc != n) continue; int ok = 1;
    for (int j = 0; j < n; j++) if (PH[k].cx[j] != tmp[2 * j] || PH[k].cy[j] != tmp[2 * j + 1]) { ok = 0; break; }
    if (ok) return k; }
  return -1;
}
// ---- situations ----
static int parse(const char *s, Ant *a, int *na, int *cx, int *cy, int *nc){
  const char *p = strchr(s, '|'); if (!p) return 0; p++;
  *na = 0; *nc = 0;
  while (*p && *p != '|') { int x, y, h, m; if (sscanf(p, "%d,%d,%d%n", &x, &y, &h, &m) != 3) break; a[*na].x = x; a[*na].y = y; a[*na].h = h; (*na)++; p += m; if (*p == ';') p++; }
  if (*p == '|') p++;
  while (*p && *p != '\n' && *p != '|') { int x, y, m; if (sscanf(p, "%d,%d%n", &x, &y, &m) != 2) break; cx[*nc] = x; cy[*nc] = y; (*nc)++; p += m; if (*p == ',') { int c; sscanf(p, ",%d%n", &c, &m); p += m; } if (*p == ';') p++; }
  return 1;
}
static void psit(FILE *f, Ant *a, int na, int *cx, int *cy, int nc){
  fprintf(f, "H:R2L2|"); for (int k = 0; k < na; k++) fprintf(f, "%s%d,%d,%d", k ? ";" : "", a[k].x, a[k].y, a[k].h);
  fprintf(f, "|"); for (int k = 0; k < nc; k++) fprintf(f, "%s%d,%d", k ? ";" : "", cx[k], cy[k]); }
// cases noires actuelles (triées)
static int blacks(int *xy, int max){ int n = 0; for (long k = 0; k < nt; k++) if (g[touch[k]]) { if (n < max) { xy[2 * n] = touch[k] % N - O; xy[2 * n + 1] = touch[k] / N - O; } n++; }
  if (n <= max) qsort(xy, n, 2 * sizeof(int), cmpi2); return n; }
// ---- orbite d'un oscillateur ----
#define PMAXO 4096
#define CMAX 256
typedef struct { int p, na, nc[PMAXO]; Ant *a; int *c; int cxm, cym; } Orb;   // a[ph*na+k], c[ph*CMAX*2 + ...]
static int orbit(Ant *a0, int na, int *cx, int *cy, int nc, int pmax, Orb *o){
  // simule seul jusqu'au retour EXACT à l'état de départ (réversible : bornée <=> périodique)
  clear(); oob = 0; for (int k = 0; k < nc; k++) setc(cx[k], cy[k]);
  Ant a[MA]; memcpy(a, a0, na * sizeof(Ant));
  int ini[2 * CMAX]; int ni = blacks(ini, CMAX); if (ni > CMAX) return 0;
  if (o) { o->na = na; o->a = malloc((size_t)pmax * na * sizeof(Ant)); o->c = malloc((size_t)pmax * CMAX * 2 * sizeof(int)); }
  for (int t = 0; t < pmax; t++) {
    if (o) { memcpy(o->a + t * na, a, na * sizeof(Ant)); int n = blacks(o->c + (size_t)t * CMAX * 2, CMAX); if (n > CMAX) return 0; o->nc[t] = n; }
    step(a, na); if (oob) return 0;
    for (int k = 0; k < na; k++) if (abs(a[k].x) > 40 || abs(a[k].y) > 40) return 0;
    int same = 1; for (int k = 0; k < na; k++) if (a[k].x != a0[k].x || a[k].y != a0[k].y || a[k].h != a0[k].h) { same = 0; break; }
    if (same) { int tmp[2 * CMAX]; int n = blacks(tmp, CMAX); if (n == ni && !memcmp(tmp, ini, 2 * n * sizeof(int))) { if (o) o->p = t + 1; return t + 1; } }
  }
  return 0;
}
// empreinte canonique (translation, phase, rotation) d'une orbite, pour éliminer les doublons
static uint64_t hst(Ant *a, int na, int *c, int nc){
  int mx = 1 << 30, my = 1 << 30; for (int k = 0; k < na; k++) { if (a[k].x < mx) mx = a[k].x; if (a[k].y < my) my = a[k].y; }
  for (int k = 0; k < nc; k++) { if (c[2 * k] < mx) mx = c[2 * k]; if (c[2 * k + 1] < my) my = c[2 * k + 1]; }
  uint64_t h = 1469598103934665603ULL; int v[3 * MA]; int idx[MA];
  for (int k = 0; k < na; k++) idx[k] = k;
  // fourmis triées (on ignore l'identité pour l'empreinte)
  for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) { Ant *p = &a[idx[i]], *q = &a[idx[j]]; if (p->x > q->x || (p->x == q->x && (p->y > q->y || (p->y == q->y && p->h > q->h)))) { int t = idx[i]; idx[i] = idx[j]; idx[j] = t; } }
  for (int k = 0; k < na; k++) { v[3 * k] = a[idx[k]].x - mx; v[3 * k + 1] = a[idx[k]].y - my; v[3 * k + 2] = a[idx[k]].h; }
  for (int k = 0; k < 3 * na; k++) { h ^= (uint64_t)(v[k] + 1000); h *= 1099511628211ULL; }
  h ^= 77777; h *= 1099511628211ULL;
  for (int k = 0; k < nc; k++) { h ^= (uint64_t)(c[2 * k] - mx + 1000); h *= 1099511628211ULL; h ^= (uint64_t)(c[2 * k + 1] - my + 1000); h *= 1099511628211ULL; }
  return h;
}
static uint64_t canon(Orb *o){
  uint64_t best = ~0ULL; Ant a[MA]; int c[2 * CMAX];
  for (int r = 0; r < 6; r++) for (int t = 0; t < o->p; t++) {
    for (int k = 0; k < o->na; k++) { a[k] = o->a[t * o->na + k]; rot(&a[k].x, &a[k].y, r); a[k].h = (a[k].h + r) % 6; }
    int nc = o->nc[t]; for (int k = 0; k < nc; k++) { c[2 * k] = o->c[(size_t)t * CMAX * 2 + 2 * k]; c[2 * k + 1] = o->c[(size_t)t * CMAX * 2 + 2 * k + 1]; rot(&c[2 * k], &c[2 * k + 1], r); }
    qsort(c, nc, 2 * sizeof(int), cmpi2);
    uint64_t h = hst(a, o->na, c, nc); if (h < best) best = h; }
  return best;
}
static void orb_free(Orb *o){ free(o->a); free(o->c); }
// ---- table de hachage des empreintes ----
static uint64_t *HS; static long HC = 1 << 22;
static int hs_add(uint64_t h){ if (!h) h = 1; long i = h & (HC - 1); while (HS[i]) { if (HS[i] == h) return 0; i = (i + 1) & (HC - 1); } HS[i] = h; return 1; }
static uint64_t rng = 88172645463325252ULL; static uint64_t xr(void){ rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static void enum_mode(int NA, int BOX, int NC, int TMAX, long nb){
  HS = calloc(HC, 8); long tested = 0, found = 0;
  int W = 2 * BOX + 1, NPOS = W * W, CB = 5;   // cases dans [-2,2]²
  Ant a[MA]; int cx[8], cy[8];
  long total = 1; for (int k = 1; k < NA; k++) total *= (long)NPOS * 6; total *= 6;
  long ncfg = 1 + 25 + (NC >= 2 ? 300 : 0);
  long tot = nb ? nb : total * ncfg;
  for (long it = 0; it < tot; it++) {
    long u; int nc = 0, ok = 1;
    if (nb) { a[0].x = 0; a[0].y = 0; a[0].h = xr() % 6;
      for (int k = 1; k < NA; k++) { a[k].x = (int)(xr() % W) - BOX; a[k].y = (int)(xr() % W) - BOX; a[k].h = xr() % 6; }
      nc = (int)(xr() % (NC + 1)); for (int k = 0; k < nc; k++) { cx[k] = (int)(xr() % CB) - 2; cy[k] = (int)(xr() % CB) - 2; }
    } else {
      u = it / ncfg; long cc = it % ncfg;
      a[0].x = 0; a[0].y = 0; a[0].h = u % 6; u /= 6;
      for (int k = 1; k < NA; k++) { int pp = u % NPOS; u /= NPOS; a[k].x = pp % W - BOX; a[k].y = pp / W - BOX; a[k].h = u % 6; u /= 6; }
      if (cc == 0) nc = 0; else if (cc <= 25) { nc = 1; cx[0] = (cc - 1) % 5 - 2; cy[0] = (cc - 1) / 5 - 2; }
      else { int q = cc - 26, i, j, m = 0; for (i = 0; i < 25 && m <= q; i++) for (j = i + 1; j < 25; j++) { if (m == q) { cx[0] = i % 5 - 2; cy[0] = i / 5 - 2; cx[1] = j % 5 - 2; cy[1] = j / 5 - 2; } m++; } nc = 2; }
    }
    for (int i = 0; i < NA && ok; i++) for (int j = i + 1; j < NA; j++) if (a[i].x == a[j].x && a[i].y == a[j].y) { ok = 0; break; }
    for (int i = 0; i < nc && ok; i++) for (int j = i + 1; j < nc; j++) if (cx[i] == cx[j] && cy[i] == cy[j]) { ok = 0; break; }
    if (!ok) continue;
    tested++;
    int p = orbit(a, NA, cx, cy, nc, TMAX, NULL);
    if (!p) continue;
    Orb o; orbit(a, NA, cx, cy, nc, p + 1, &o); o.p = p;
    uint64_t h = canon(&o); orb_free(&o);
    if (hs_add(h)) { found++; printf("OSC %d %d | ", p, NA); psit(stdout, a, NA, cx, cy, nc); printf("\n"); fflush(stdout); }
  }
  fprintf(stderr, "enum NA=%d BOX=%d NC=%d : %ld configurations testées, %ld oscillateurs distincts\n", NA, BOX, NC, tested, found);
}
// ---- tir : un vaisseau sur un oscillateur ----
static Orb OB; static int ocx, ocy, orad; static uint64_t OBH;
// état final : partie proche (fourmis et cases à distance <= R du centre) comparée à l'orbite ; fourmis lointaines = vaisseaux ?
// renvoie : nombre de vaisseaux sortis (*nsh), leurs infos ; *psi = phase de l'orbite retrouvée (-1 si détruit) ; *exact = même ordre des fourmis ; *deb = cases non expliquées
typedef struct { int k, r, ph, x, y, h; } Sh;
static void analyse(Ant *a, int n, int R, int *nsh, Sh *sh, int *psi, int *exact, int *deb){
  int near[MA], nn = 0; *nsh = 0; *deb = 0; int used = 0;
  for (int k = 0; k < n; k++) {
    if (hd(a[k].x - ocx, a[k].y - ocy) <= R) near[nn++] = k;
    else { int nb; int id = ship_id(a[k], &nb); if (id < 0) { *nsh = -1; *psi = -1; return; }
      sh[*nsh].k = k; sh[*nsh].r = id / 8; sh[*nsh].ph = id % 8; sh[*nsh].x = a[k].x; sh[*nsh].y = a[k].y; sh[*nsh].h = a[k].h; (*nsh)++; used += nb; }
  }
  static int bl[2 * 4096]; int nbk = blacks(bl, 4096); if (nbk > 4096) { *psi = -1; return; }
  int cn[2 * CMAX], ncn = 0;
  for (int k = 0; k < nbk; k++) if (hd(bl[2 * k] - ocx, bl[2 * k + 1] - ocy) <= R) { if (ncn < CMAX) { cn[2 * ncn] = bl[2 * k]; cn[2 * ncn + 1] = bl[2 * k + 1]; } ncn++; }
  *deb = nbk - ncn - used;
  *psi = -1; *exact = 0;
  if (nn != OB.na || ncn > CMAX) return;
  for (int t = 0; t < OB.p; t++) {
    if (OB.nc[t] != ncn || memcmp(OB.c + (size_t)t * CMAX * 2, cn, 2 * ncn * sizeof(int))) continue;
    Ant *b = OB.a + t * OB.na; int ex = 1, ms = 1; char usedb[MA] = {0};
    for (int i = 0; i < nn; i++) { Ant *p = &a[near[i]]; if (p->x != b[i].x || p->y != b[i].y || p->h != b[i].h) ex = 0;
      int f = 0; for (int j = 0; j < nn; j++) if (!usedb[j] && p->x == b[j].x && p->y == b[j].y && p->h == b[j].h) { usedb[j] = 1; f = 1; break; }
      if (!f) { ms = 0; break; } }
    if (ms) { *psi = t; *exact = ex; return; }
  }
}
static void tir_mode(int D, int T){
  char line[8192]; long nosc = 0; long cnt[8] = {0}; long nmir = 0;
  while (fgets(line, sizeof line, stdin)) {
    char *s = strstr(line, "H:R2L2|"); if (!s) continue;
    Ant a0[MA]; int na, cx[CMAX], cy[CMAX], nc; parse(s, a0, &na, cx, cy, &nc);
    int p = orbit(a0, na, cx, cy, nc, PMAXO, NULL); if (!p) continue;
    if (nosc) orb_free(&OB);
    orbit(a0, na, cx, cy, nc, p + 1, &OB); OB.p = p; nosc++; OBH = canon(&OB);
    // centre et rayon de l'oscillateur (sur toute l'orbite)
    long sx = 0, sy = 0; for (int k = 0; k < na; k++) { sx += a0[k].x; sy += a0[k].y; } ocx = sx / na; ocy = sy / na; orad = 0;
    for (int t = 0; t < p; t++) { for (int k = 0; k < na; k++) { int d = hd(OB.a[t * na + k].x - ocx, OB.a[t * na + k].y - ocy); if (d > orad) orad = d; }
      for (int k = 0; k < OB.nc[t]; k++) { int d = hd(OB.c[(size_t)t * CMAX * 2 + 2 * k] - ocx, OB.c[(size_t)t * CMAX * 2 + 2 * k + 1] - ocy); if (d > orad) orad = d; } }
    int R = orad + 12; if (D < R + 20) D = R + 20;
    int TT = T > 8 * (2 * D + 10) ? T : 8 * (2 * D + 10); TT = (TT / 8) * 8;
    for (int ord = 0; ord < 2; ord++) for (int r = 0; r < 6; r++) {
      int dx = 1, dy = -1, ex = 1, ey = 0; rot(&dx, &dy, r); rot(&ex, &ey, r);
      for (int l = -(orad + 4); l <= orad + 4; l++) for (int ph = 0; ph < p; ph++) {
        clear(); oob = 0;
        Ant a[MA]; int n = 0;
        int sxp = ocx - D * dx + l * ex, syp = ocy - D * dy + l * ey;
        int scx = 1, scy = 0; rot(&scx, &scy, r);
        Ant sa = {sxp, syp, (4 + r) % 6};
        if (ord == 1) a[n++] = sa;
        for (int k = 0; k < na; k++) a[n++] = OB.a[ph * na + k];
        if (ord == 0) a[n++] = sa;
        for (int k = 0; k < OB.nc[ph]; k++) setc(OB.c[(size_t)ph * CMAX * 2 + 2 * k], OB.c[(size_t)ph * CMAX * 2 + 2 * k + 1]);
        setc(sxp + scx, syp + scy);
        for (int t = 0; t < TT; t++) { step(a, n); if (oob) break; }
        if (oob) { cnt[7]++; continue; }
        int nsh, psi, exact, deb; Sh sh[MA];
        // repositionner : l'oscillateur seul serait à la phase (ph + TT) % p ; on cherche n'importe quelle phase
        analyse(a, n, R, &nsh, sh, &psi, &exact, &deb);
        int expect = (ph + TT) % p, kship = ord == 1 ? 0 : na;
        if (psi < 0 && nsh == 1 && !deb) {   // l'objet restant est-il un oscillateur ? le même (déplacé / tourné) ?
          Ant b[MA]; int nb2 = 0, bx[CMAX], by[CMAX], nbc = 0; static int bl[2 * 4096]; int nbk = blacks(bl, 4096);
          for (int k = 0; k < n; k++) if (hd(a[k].x - ocx, a[k].y - ocy) <= R) b[nb2++] = a[k];
          for (int k = 0; k < nbk && nbc < CMAX; k++) if (hd(bl[2 * k] - ocx, bl[2 * k + 1] - ocy) <= R) { bx[nbc] = bl[2 * k]; by[nbc] = bl[2 * k + 1]; nbc++; }
          int sr = sh[0].r, sk = sh[0].k;
          int p2 = nb2 ? orbit(b, nb2, bx, by, nbc, PMAXO, NULL) : 0;
          if (p2) { Orb o2; orbit(b, nb2, bx, by, nbc, p2 + 1, &o2); o2.p = p2; uint64_t h2 = canon(&o2);
            // position : décalage du 1er état vs orbite d'origine (centre des fourmis)
            long qx = 0, qy = 0; for (int k = 0; k < nb2; k++) { qx += b[k].x; qy += b[k].y; }
            int same = (h2 == OBH);
            const char *ty = same ? (sr == r ? "DECT" : "MIRT") : "CONV"; cnt[same ? (sr == r ? 2 : 3) : 0]++;
            if (same && sr != r) nmir++;
            if (!same && !getenv("CONV")) { orb_free(&o2); continue; }
            printf("%s osc=%ld p=%d p2=%d ord=%d r=%d l=%d ph=%d angle=%d sortie_r=%d qui=%s na2=%d centre2=%ld,%ld centre=%d,%d | ", ty, nosc, p, p2, ord, r, l, ph,
               ((sr - r) % 6 + 6) % 6 * 60, sr, sk == kship ? "vaisseau" : "osc", nb2, nb2 ? qx / nb2 : 0, nb2 ? qy / nb2 : 0, ocx, ocy);
            psit(stdout, a0, na, cx, cy, nc); printf(" | D=%d T=%d | restant ", D, TT); psit(stdout, b, nb2, bx, by, nbc); printf("\n");
            orb_free(&o2); continue; }
        }
        int ncnear = 0; { static int bl2[2 * 4096]; int nbk2 = blacks(bl2, 4096); for (int k = 0; k < nbk2 && nbk2 <= 4096; k++) if (hd(bl2[2 * k] - ocx, bl2[2 * k + 1] - ocy) <= R) ncnear++; }
        if (nsh == n && !deb && getenv("DES")) {   // destruction propre : toutes les fourmis repartent en vaisseaux, aucune case
          printf("DES osc=%ld p=%d ord=%d r=%d l=%d ph=%d cases_restantes=%d sorties=", nosc, p, ord, r, l, ph, ncnear);
          for (int k = 0; k < nsh; k++) printf("%s%d", k ? "," : "", sh[k].r); printf(" | "); psit(stdout, a0, na, cx, cy, nc); printf(" | D=%d T=%d\n", D, TT); }
        if (psi < 0 || nsh != 1 || deb) { cnt[0]++;
          if (getenv("DIAG")) { int nn = 0; for (int k = 0; k < n; k++) if (hd(a[k].x - ocx, a[k].y - ocy) <= R) nn++;
            printf("DIAG proches=%d vaisseaux=%d", nn, nsh); for (int k = 0; k < nsh; k++) printf(" r%d%s", sh[k].r, sh[k].k == kship ? "v" : "o"); printf(" debris=%d psi=%d\n", deb, psi); }
          continue; }
        int fx = sxp + (TT / 8) * dx, fy = syp + (TT / 8) * dy;  // vaisseau non perturbé
        const char *typ;
        if (sh[0].r == r) { typ = (sh[0].x == fx && sh[0].y == fy && sh[0].h == (4 + r) % 6 && psi == expect && sh[0].k == kship) ? "TRA" : "DEC"; cnt[typ[0] == 'T' ? 1 : 2]++; if (typ[0] == 'T') continue; }
        else { typ = "MIR"; cnt[3]++; nmir++; if (psi == expect) cnt[4]++; if (exact) cnt[5]++; if (sh[0].k != kship) cnt[6]++; }
        printf("%s osc=%ld p=%d ord=%d r=%d l=%d ph=%d angle=%d sortie_r=%d qui=%s dphase=%d exact=%d | ", typ, nosc, p, ord, r, l, ph,
               ((sh[0].r - r) % 6 + 6) % 6 * 60, sh[0].r, sh[0].k == kship ? "vaisseau" : "osc", ((psi - expect) % p + p) % p, exact);
        psit(stdout, a0, na, cx, cy, nc); printf(" | D=%d T=%d\n", D, TT);
      }
    }
    fflush(stdout);
  }
  fprintf(stderr, "tir : %ld oscillateurs ; détruits/sales %ld, transparents %ld, décalés %ld, MIROIRS %ld (phase conservée %ld, identités %ld, sortie par une fourmi de l'oscillateur %ld), bord %ld\n",
          nosc, cnt[0], cnt[1], cnt[2], cnt[3], cnt[4], cnt[5], cnt[6], cnt[7]);
}
// ---- flux : NV vaisseaux sur la même voie, espacés de DL pas, sur l'oscillateur (lignes CONV/MIRT/MIR/DEC de tir) ----
static int lane(int x, int y, int r){ rot(&x, &y, -r + 6); return x + y; }
static void flux_mode(int NV, int D, int dlmin, int dln){
  char line[16384]; long ncand = 0, nok = 0;
  while (fgets(line, sizeof line, stdin)) {
    int p, ord, r, l, ph; char *q;
    if (!(q = strstr(line, " ord="))) continue; sscanf(q, " ord=%d r=%d l=%d ph=%d", &ord, &r, &l, &ph);
    char *s = strstr(line, "H:R2L2|"); if (!s) continue;
    Ant a0[MA]; int na, cx[CMAX], cy[CMAX], nc; parse(s, a0, &na, cx, cy, &nc);
    p = orbit(a0, na, cx, cy, nc, PMAXO, NULL); if (!p) continue;
    orbit(a0, na, cx, cy, nc, p + 1, &OB); OB.p = p; OBH = canon(&OB); ncand++;
    long sx = 0, sy = 0; for (int k = 0; k < na; k++) { sx += a0[k].x; sy += a0[k].y; } ocx = sx / na; ocy = sy / na; orad = 0;
    for (int t = 0; t < p; t++) { for (int k = 0; k < na; k++) { int d = hd(OB.a[t * na + k].x - ocx, OB.a[t * na + k].y - ocy); if (d > orad) orad = d; }
      for (int k = 0; k < OB.nc[t]; k++) { int d = hd(OB.c[(size_t)t * CMAX * 2 + 2 * k] - ocx, OB.c[(size_t)t * CMAX * 2 + 2 * k + 1] - ocy); if (d > orad) orad = d; } }
    int R = orad + 12, DD = D < R + 20 ? R + 20 : D;
    int dx = 1, dy = -1, ex = 1, ey = 0; rot(&dx, &dy, r); rot(&ex, &ey, r);
    int sxp = ocx - DD * dx + l * ex, syp = ocy - DD * dy + l * ey;
    for (int DL = dlmin; DL < dlmin + dln; DL++) {
      clear(); oob = 0; Ant a[MA]; int n = 0;
      int TT = 8 * (2 * DD + 10) + NV * DL;
      Ant st[MA]; int ns = 0;
      for (int i = 0; i < NV; i++) {      // vaisseau i : en retard de i*DL pas sur la même trajectoire
        long lag = (long)i * DL; long kk = (lag + 7) / 8; int j = (int)(kk * 8 - lag);   // germe recule de kk cases, avancé de j pas
        int id = r * 8 + j; int bx = sxp - (int)kk * dx, by = syp - (int)kk * dy;
        // position de la fourmi à la phase j : germe + PAX tourné ? PAX est déjà dans le repère tourné (germe tourné de r)
        st[ns].x = bx + PAX[id]; st[ns].y = by + PAY[id]; st[ns].h = PH[id].h; ns++;
        for (int c = 0; c < PH[id].nc; c++) setc(st[ns - 1].x + PH[id].cx[c], st[ns - 1].y + PH[id].cy[c]);
      }
      if (ord == 1) for (int i = 0; i < ns; i++) a[n++] = st[i];
      for (int k = 0; k < na; k++) a[n++] = OB.a[ph * na + k];
      if (ord == 0) for (int i = 0; i < ns; i++) a[n++] = st[i];
      for (int k = 0; k < OB.nc[ph]; k++) setc(OB.c[(size_t)ph * CMAX * 2 + 2 * k], OB.c[(size_t)ph * CMAX * 2 + 2 * k + 1]);
      for (int t = 0; t < TT; t++) { step(a, n); if (oob) break; }
      if (oob) continue;
      int nsh, psi, exact, deb; Sh sh[MA];
      analyse(a, n, R, &nsh, sh, &psi, &exact, &deb);
      if (nsh != NV || deb) continue;
      int r2 = sh[0].r, ok = 1, l2 = lane(sh[0].x, sh[0].y, sh[0].r), nl = 1;
      for (int k = 0; k < nsh; k++) { if (sh[k].r != r2) ok = 0; if (lane(sh[k].x, sh[k].y, sh[k].r) != l2) nl = 0; }
      if (!ok || r2 == r) continue;
      int same = psi >= 0;   // l'objet est exactement l'oscillateur de départ (même place, une phase)
      if (!same) {           // sinon : est-ce un oscillateur ? lequel ?
        Ant b[MA]; int nb2 = 0, bx[CMAX], by[CMAX], nbc = 0; static int bl[2 * 4096]; int nbk = blacks(bl, 4096);
        for (int k = 0; k < n; k++) if (hd(a[k].x - ocx, a[k].y - ocy) <= R) b[nb2++] = a[k];
        for (int k = 0; k < nbk && nbc < CMAX; k++) if (hd(bl[2 * k] - ocx, bl[2 * k + 1] - ocy) <= R) { bx[nbc] = bl[2 * k]; by[nbc] = bl[2 * k + 1]; nbc++; }
        if (!nb2 || !orbit(b, nb2, bx, by, nbc, PMAXO, NULL)) continue;
      }
      nok++;
      printf("FLUX NV=%d DL=%d angle=%d meme_voie=%d objet=%s | osc p=%d ord=%d r=%d l=%d ph=%d | ", NV, DL, ((r2 - r) % 6 + 6) % 6 * 60, nl,
             same ? "IDENTIQUE" : "autre_osc", p, ord, r, l, ph);
      psit(stdout, a0, na, cx, cy, nc); printf("\n"); fflush(stdout);
    }
    orb_free(&OB);
  }
  fprintf(stderr, "flux NV=%d : %ld candidats, %ld (candidat, espacement) où les %d vaisseaux tournent tous pareil\n", NV, ncand, nok, NV);
}
int main(int argc, char **argv){
  ships();
  if (argc >= 6 && !strcmp(argv[1], "enum")) { if (argc >= 8) rng = strtoull(argv[6], 0, 10) * 2654435761ULL + 1; enum_mode(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), argc >= 8 ? atol(argv[7]) : 0); }
  else if (argc >= 6 && !strcmp(argv[1], "flux")) flux_mode(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]));
  else if (argc >= 4 && !strcmp(argv[1], "tir")) tir_mode(atoi(argv[2]), atoi(argv[3]));
  else { fprintf(stderr, "usage : voir en-tête\n"); return 1; }
  return 0;
}
