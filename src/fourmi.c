// fourmi.c — MOTEUR UNIQUE du projet (remplace bestiaire2 / explore / hw / full pour les campagnes).
// Grille carrée (lettres L R N U, q = longueur du mot) ou hexagonale (préfixe "H:" puis N R1 R2 U L2 L1).
// n fourmis jouées l'une après l'autre, cases de départ colorées, grille INFINIE (table de hachage),
// positions entières, AUCUNE fourmi retirée.
//
// Conventions : carré 0=H(0,-1) 1=D(+1,0) 2=B(0,+1) 3=G(-1,0), y vers le bas ; R = +1 quart de tour.
//   hexa (axiales) 0=E(1,0) 1=SE(0,1) 2=SO(-1,1) 3=O(-1,0) 4=NO(0,-1) 5=NE(1,-1).
// Situation = "REGLE|x,y,D;x,y,D|x,y;x,y,c"  (D = H D B G ou chiffre ; c = couleur, 1 par défaut).
//
// Usage : ./fourmi [-T pas] [-img f.pgm] "RL|0,0,H;40,0,G|"   une situation (+ image de la fin)
//         ./fourmi [-T pas] -lot < situations.txt     une situation par ligne
// Sortie (une ligne) : situation|ISSUE|SIGNATURE|t|détails
//   ISSUE : CYCLE (exact : l'état complet revient à l'état de départ, preuve par réversibilité)
//           AUTOROUTES (toutes les fourmis en autoroute confirmée) / MIXTE (une partie) / INDECIS (aucune)
//   Autoroute confirmée : période P ≤ 20000 tenue sur ≥ 20 P ET ≥ t/4 pas (écarte les bords de losange).
//   SIGNATURE : C<P> ou liste triée A<P>(dx,dy)x<k> (k fourmis groupées : même P, même déplacement, < 64 cases),
//     déplacement ramené par rotation (carré : dx>0, dy>=0 ; hexa : q>0, r>=0), + N<k> fourmis non classées.
//   détails : par fourmi P,dx,dy,début (début au sens de bestiaire2) ; taille de la boîte visitée.
// Une simulation finie ne prouve pas un comportement infini (sauf CYCLE).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXA 128
#define PMAX 20000

typedef struct { uint64_t *k; uint8_t *cur, *ini; uint64_t cap, n; } Grid;
static Grid g;
static long diff;                                  // nb de cases dont la couleur diffère de la couleur de départ
static uint64_t KEY(long x, long y){ return ((uint64_t)(uint32_t)(x + 0x40000000) << 32) | (uint32_t)(y + 0x40000000); }
static uint64_t hsh(uint64_t k){ k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; return k; }
static void g_init(uint64_t cap){ g.cap = cap; g.n = 0; g.k = calloc(cap, 8); g.cur = calloc(cap, 1); g.ini = calloc(cap, 1); }
static void g_free(void){ free(g.k); free(g.cur); free(g.ini); }
static uint64_t g_slot(uint64_t k);
static void g_grow(void){
  Grid o = g; g_init(o.cap * 2);
  for (uint64_t i = 0; i < o.cap; i++) if (o.k[i]) { uint64_t s = g_slot(o.k[i]); g.cur[s] = o.cur[i]; g.ini[s] = o.ini[i]; }
  free(o.k); free(o.cur); free(o.ini);
}
static uint64_t g_slot(uint64_t k){                // renvoie l'emplacement (créé blanc si absent)
  uint64_t m = g.cap - 1, s = hsh(k) & m;
  while (g.k[s]) { if (g.k[s] == k) return s; s = (s + 1) & m; }
  if (2 * (g.n + 1) > g.cap) { g_grow(); return g_slot(k); }
  g.k[s] = k; g.n++; return s;
}

static int M, q, turn[64], DX[6], DY[6];
static const int sqx[4] = {0,1,0,-1}, sqy[4] = {-1,0,1,0}, hxx[6] = {1,0,-1,-1,0,1}, hxy[6] = {0,1,1,0,-1,-1};
static int n, ax[MAXA], ay[MAXA], ad[MAXA], x0[MAXA], y0_[MAXA], d0[MAXA];
static uint8_t *hist[MAXA]; static long T = 1L << 21, histcap = 0;
static long P[MAXA], deb[MAXA]; static int ddx[MAXA], ddy[MAXA];
static long bx0, bx1, by0, by1;
static const char *img = NULL;                     // -img fichier.pgm : image de la grille à la fin
static void image(void){                           // gris clair = case visitée blanche, noir = couleur ≠ 0, gris = fourmi
  long w = bx1 - bx0 + 3, h = by1 - by0 + 3, sc = 1; while (w / sc > 1000 || h / sc > 1000) sc++;
  long W = w / sc + 1, H = h / sc + 1; uint8_t *px = malloc(W * H); memset(px, 255, W * H);
  for (uint64_t i = 0; i < g.cap; i++) if (g.k[i]) {
    long x = (long)(g.k[i] >> 32) - 0x40000000, y = (long)(uint32_t)g.k[i] - 0x40000000;
    long X = (x - bx0 + 1) / sc, Y = (y - by0 + 1) / sc; if (X < 0 || Y < 0 || X >= W || Y >= H) continue;
    uint8_t v = g.cur[i] ? (uint8_t)(80 - 80 * g.cur[i] / q) : 225; if (v < px[Y * W + X]) px[Y * W + X] = v; }
  for (int i = 0; i < n; i++) { long X = (ax[i] - bx0 + 1) / sc, Y = (ay[i] - by0 + 1) / sc;
    if (X >= 0 && Y >= 0 && X < W && Y < H) px[Y * W + X] = 140; }
  FILE *f = fopen(img, "wb"); if (f) { fprintf(f, "P5\n%ld %ld\n255\n", W, H); fwrite(px, 1, W * H, f); fclose(f); }
  free(px);
}

static int parse_rule(const char *r){
  q = 0;
  if (!strncmp(r, "H:", 2)) { M = 6; memcpy(DX, hxx, sizeof hxx); memcpy(DY, hxy, sizeof hxy);
    for (const char *p = r + 2; *p; ) {
      if (*p == 'N') { turn[q++] = 0; p++; } else if (*p == 'U') { turn[q++] = 3; p++; }
      else if (*p == 'R' && p[1]) { turn[q++] = p[1] - '0'; p += 2; } else if (*p == 'L' && p[1]) { turn[q++] = 6 - (p[1] - '0'); p += 2; }
      else return 0; }
  } else { M = 4; memcpy(DX, sqx, sizeof sqx); memcpy(DY, sqy, sizeof sqy);
    for (const char *p = r; *p; p++) { if (*p=='R') turn[q++]=1; else if (*p=='L') turn[q++]=3; else if (*p=='U') turn[q++]=2; else if (*p=='N') turn[q++]=0; else return 0; } }
  return q >= 1;
}
static int cap_of(const char *s){ switch (*s) { case 'H': return 0; case 'D': return 1; case 'B': return 2; case 'G': return 3; default: return atoi(s); } }

static void canon(int *dx, int *dy){                // rotation jusqu'à dx>0, dy>=0 (carré) / q>0, r>=0 (hexa)
  for (int i = 0; i < M; i++) { if (*dx > 0 && *dy >= 0) return;
    int a = *dx, b = *dy; if (M == 4) { *dx = -b; *dy = a; } else { *dx = -b; *dy = a + b; } }
}
static void detect(long t, int i){                  // cherche une autoroute confirmée pour la fourmi i au temps t
  uint8_t *h = hist[i];
  for (long p = 1; p <= PMAX && 20 * p <= t; p++) {
    long j; for (j = t; j > t - 3 * p; j--) if (h[j] != h[j - p]) break;
    if (j > t - 3 * p) continue;
    long k = t; while (k - p >= 1 && h[k] == h[k - p]) k--;
    long L = t - k;                                 // longueur de la queue périodique
    if (L < 20 * p || L < t / 4) return;
    int dx = 0, dy = 0; for (long s = t - p + 1; s <= t; s++) { dx += DX[h[s]]; dy += DY[h[s]]; }
    if (!dx && !dy) return;
    P[i] = p; deb[i] = k - p + 1 > 0 ? k - p + 1 : 0; ddx[i] = dx; ddy[i] = dy; return;
  }
}

static void run(char *line){
  char buf[16384]; strncpy(buf, line, sizeof buf - 1); buf[sizeof buf - 1] = 0;
  char *nl = strpbrk(buf, "\r\n"); if (nl) *nl = 0;
  if (!buf[0] || buf[0] == '#') return;
  char *f1 = strchr(buf, '|'); if (!f1) { printf("%s|ERREUR|format|0|\n", buf); return; }
  *f1++ = 0; char *f2 = strchr(f1, '|'); if (f2) *f2++ = 0; else f2 = "";
  if (!parse_rule(buf)) { printf("%s|ERREUR|regle|0|\n", buf); return; }
  g_init(1 << 16); diff = 0; n = 0;
  char tmp[16384]; strcpy(tmp, f1);
  for (char *s = strtok(tmp, ";"); s && n < MAXA; s = strtok(NULL, ";")) {
    while (*s == ' ') s++; if (!*s) continue;
    char *c1 = strchr(s, ','), *c2 = c1 ? strchr(c1 + 1, ',') : 0; if (!c2) continue;
    x0[n] = ax[n] = atoi(s); y0_[n] = ay[n] = atoi(c1 + 1); while (c2[1] == ' ') c2++; d0[n] = ad[n] = cap_of(c2 + 1) % M; n++; }
  strcpy(tmp, f2);
  for (char *s = strtok(tmp, ";"); s; s = strtok(NULL, ";")) {
    char *c1 = strchr(s, ','); if (!c1) continue; char *c2 = strchr(c1 + 1, ',');
    int col = c2 ? atoi(c2 + 1) : 1; uint64_t sl = g_slot(KEY(atoi(s), atoi(c1 + 1)));
    g.cur[sl] = g.ini[sl] = (uint8_t)(((col % q) + q) % q); }
  if (histcap < T + 1) { for (int i = 0; i < MAXA; i++) { free(hist[i]); hist[i] = malloc(T + 1); } histcap = T + 1; }
  for (int i = 0; i < n; i++) { P[i] = 0; hist[i][0] = ad[i]; }
  bx0 = bx1 = ax[0]; by0 = by1 = ay[0];
  long t, next = 4096; int cyc = 0;
  for (t = 1; t <= T; t++) {
    for (int i = 0; i < n; i++) {
      uint64_t s = g_slot(KEY(ax[i], ay[i])); int c = g.cur[s];
      ad[i] = (ad[i] + turn[c]) % M;
      int nc = c + 1 == q ? 0 : c + 1;
      diff += (nc != g.ini[s]) - (c != g.ini[s]);
      g.cur[s] = nc; ax[i] += DX[ad[i]]; ay[i] += DY[ad[i]]; hist[i][t] = ad[i];
      if (ax[i] < bx0) bx0 = ax[i]; if (ax[i] > bx1) bx1 = ax[i]; if (ay[i] < by0) by0 = ay[i]; if (ay[i] > by1) by1 = ay[i];
    }
    if (!diff) { int ok = 1; for (int i = 0; i < n; i++) if (ax[i] != x0[i] || ay[i] != y0_[i] || ad[i] != d0[i]) { ok = 0; break; }
      if (ok) { cyc = 1; break; } }
    if (t == next || t == T) { next *= 2; int all = 1;
      for (int i = 0; i < n; i++) { P[i] = 0; detect(t, i); if (!P[i]) all = 0; }   // tout revérifier : une autoroute peut casser
      // arrêt anticipé seulement si aucune paire ne peut encore se rencontrer :
      // même vitesse (groupe) ou en train de s'éloigner (r·w > 0, w = vitesse relative)
      for (int i = 0; all && i < n; i++) for (int j = i + 1; all && j < n; j++) {
        long wx = (long)ddx[j] * P[i] - (long)ddx[i] * P[j], wy = (long)ddy[j] * P[i] - (long)ddy[i] * P[j];
        long rx = ax[j] - ax[i], ry = ay[j] - ay[i];
        if (wx == 0 && wy == 0) { if (labs(rx) + labs(ry) > 128) all = 0; }   // même vitesse mais loin : attendre
        else if (rx * wx + ry * wy <= 0) all = 0;
        // parallèles, même sens, vitesses différentes : l'une roule sur la trace de l'autre (passager,
        // navette R-19) et peut faire demi-tour au bout de la trace → ne pas conclure, aller jusqu'à T
        else if ((long)ddx[i] * ddy[j] == (long)ddy[i] * ddx[j] && (long)ddx[i] * ddx[j] + (long)ddy[i] * ddy[j] > 0) all = 0; }
      if (all) break; }
  }
  if (t > T) t = T;
  printf("%s|%s|%s|", buf, f1, f2);
  if (img) image();
  if (cyc) { printf("CYCLE|C%ld|%ld|boite %ldx%ld\n", t, t, bx1 - bx0 + 1, by1 - by0 + 1); g_free(); return; }
  // groupes : même P, même déplacement, à moins de 64 cases
  int grp[MAXA], ng = 0, nc = 0; for (int i = 0; i < n; i++) grp[i] = -1;
  char sig[MAXA][48]; int ns = 0;
  for (int i = 0; i < n; i++) { if (!P[i]) { nc++; continue; } if (grp[i] >= 0) continue;
    grp[i] = ng; int k = 1;
    long G = P[i];                                  // période du groupe = ppcm des périodes (même vitesse)
    for (int j = i + 1; j < n; j++) if (P[j] && grp[j] < 0
        && (long)ddx[j] * P[i] == (long)ddx[i] * P[j] && (long)ddy[j] * P[i] == (long)ddy[i] * P[j]
        && labs((long)ax[j] - ax[i]) < 64 && labs((long)ay[j] - ay[i]) < 64) {
      grp[j] = ng; k++; long a = G, b = P[j]; while (b) { long r = a % b; a = b; b = r; } G = G / a * P[j]; }
    int cx = (int)(ddx[i] * (G / P[i])), cy = (int)(ddy[i] * (G / P[i])); canon(&cx, &cy);
    snprintf(sig[ns++], 48, "A%ld(%d,%d)x%d", G, cx, cy, k); ng++; }
  for (int a = 0; a < ns; a++) for (int b = a + 1; b < ns; b++) if (strcmp(sig[a], sig[b]) > 0) { char z[48]; strcpy(z, sig[a]); strcpy(sig[a], sig[b]); strcpy(sig[b], z); }
  printf("%s|", nc == n ? "INDECIS" : nc ? "MIXTE" : "AUTOROUTES");
  for (int a = 0; a < ns; a++) printf("%s%s", a ? "+" : "", sig[a]);
  if (nc) printf("%sN%d", ns ? "+" : "", nc);
  printf("|%ld|", t);
  for (int i = 0; i < n; i++) if (P[i]) printf("%ld,%d,%d,%ld ", P[i], ddx[i], ddy[i], deb[i]); else printf("- ");
  printf("boite %ldx%ld fin", bx1 - bx0 + 1, by1 - by0 + 1);
  for (int i = 0; i < n; i++) printf(" %d,%d", ax[i], ay[i]);
  printf("\n"); g_free();
}

int main(int argc, char **argv){
  int lot = 0; char *one = NULL;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "-T") && i + 1 < argc) T = atol(argv[++i]);
    else if (!strcmp(argv[i], "-img") && i + 1 < argc) img = argv[++i];
    else if (!strcmp(argv[i], "-lot")) lot = 1; else one = argv[i]; }
  setvbuf(stdout, NULL, _IOLBF, 0);
  if (one) run(one);
  if (lot) { static char line[16384]; while (fgets(line, sizeof line, stdin)) run(line); }
  if (!one && !lot) { fprintf(stderr, "usage : ./fourmi [-T pas] \"RL|0,0,H|\"  ou  ./fourmi -lot < fichier\n"); return 1; }
  return 0;
}
