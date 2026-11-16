// tipmin.c — bout d'autoroute minimal EXACT. ./tipmin [HORIZON_PERIODES=60]
// Pour chaque phase s : B_s = cases noires à T+s que la fourmi touchera après T+s. Tout germe qui donne
// l'autoroute dès le pas 0 (même trajectoire) contient B_s (la couleur lue fixe le virage) et B_s suffit.
#include "ant.h"
static const char CAP[]="HDBG";
int main(int c,char**v){ int NP=c>1?atoi(v[1]):60; long T=200000; Grid g; g_init(&g,1<<20); Ant a; memset(&a,0,sizeof a);
  for(long t=0;t<T;t++) a_step(&g,&a);
  int L=104*(NP+1); int *X=malloc(L*4),*Y=malloc(L*4),*D=malloc(L*4); uint8_t *G0=malloc(L);
  for(int i=0;i<L;i++){ X[i]=a.x; Y[i]=a.y; D[i]=a.d; G0[i]=g_get(&g,a.x,a.y); a_step(&g,&a); }
  // G0[i] = couleur au pas i de la case visitée au pas i (avant lecture)
  int best=1<<30,bs=-1;
  for(int s=0;s<104;s++){ Grid seen; g_init(&seen,1<<16); int n=0;
    for(int i=s;i<L;i++){ uint8_t *f=g_slot(&seen,KEY(X[i],Y[i])); if(*f) continue; *f=1; if(G0[i]) n++; }
    // première visite après s : la couleur lue au pas i est celle de T+s (personne d'autre ne l'a touchée entre-temps)
    if(n<best){best=n;bs=s;} if(c>2) printf("phase %d : %d cases\n",s,n); g_free(&seen); }
  printf("minimum = %d cases (phase %d). Germe : fourmi 0,0,%c ; cases :",best,bs,CAP[D[bs]]);
  Grid seen; g_init(&seen,1<<16); for(int i=bs;i<L;i++){ uint8_t *f=g_slot(&seen,KEY(X[i],Y[i])); if(*f) continue; *f=1; if(G0[i]) printf(" %d,%d ;",X[i]-X[bs],Y[i]-Y[bs]); } printf("\n");
}
