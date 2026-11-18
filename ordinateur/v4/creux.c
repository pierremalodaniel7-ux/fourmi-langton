/* creux.c — moteur à GRILLE CREUSE (table de hachage : seules les cases touchées sont stockées), 18/11.
   Indépendant de trapL*, fourmi.c, sim.py, engine.js. Règles carrées L/R/N/U, q couleurs, n fourmis jouées dans l'ordre.
   Entrée : une ligne par situation « REGLE|x,y,C;...|x,y[,c];... T ». Caps H D B G (0..3), y vers le bas.
   Sortie : une ligne par situation : « cases=<nb cases touchées> » puis pour chaque fourmi « dx,dy,ms,md »
   dx,dy = déplacement sur les 18 derniers tours ; ms = min(x+y), md = min(x-y) sur les 18 dernières positions. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static uint64_t *K; static unsigned char *V; static size_t cap, used;
static inline uint64_t key(int x,int y){return (((uint64_t)(uint32_t)x<<32)|(uint32_t)y)^0x8000000080000000ULL;} /* (-1,-1) ne doit pas valoir EMPTY */
static inline size_t hsh(uint64_t k){k^=k>>33;k*=0xff51afd7ed558ccdULL;k^=k>>33;k*=0xc4ceb9fe1a85ec53ULL;k^=k>>33;return (size_t)k;}
#define EMPTY 0xFFFFFFFFFFFFFFFFULL
static void init(size_t c){cap=c;used=0;K=malloc(cap*8);V=calloc(cap,1);memset(K,0xFF,cap*8);}
static unsigned char *slot(uint64_t k);
static void grow(void){size_t oc=cap;uint64_t*OK=K;unsigned char*OV=V;init(oc*2);
  for(size_t i=0;i<oc;i++) if(OK[i]!=EMPTY){*slot(OK[i])=OV[i];} free(OK);free(OV);}
static unsigned char *slot(uint64_t k){
  if(used*10>cap*7) grow();
  size_t i=hsh(k)&(cap-1);
  while(K[i]!=EMPTY){ if(K[i]==k) return &V[i]; i=(i+1)&(cap-1);}
  K[i]=k; V[i]=0; used++; return &V[i];
}
int main(void){
  static char line[1<<20];
  while(fgets(line,sizeof line,stdin)){
    char *p1=strchr(line,'|'); if(!p1) continue; *p1=0; char *rule=line;
    char *p2=strchr(p1+1,'|'); if(!p2) continue; *p2=0; char *as=p1+1; char *rest=p2+1;
    char *sp=strrchr(rest,' '); long T=atol(sp+1); *sp=0; char *cs=rest;
    int q=strlen(rule), turn[16]; for(int i=0;i<q;i++) turn[i]= rule[i]=='R'?1: rule[i]=='L'?3: rule[i]=='U'?2:0;
    int n=0, nmax=4096; int *ax=malloc(nmax*4),*ay=malloc(nmax*4),*ad=malloc(nmax*4);
    for(char *t=strtok(as,";");t;t=strtok(NULL,";")){int x,y;char c; if(sscanf(t," %d,%d,%c",&x,&y,&c)==3){
      ax[n]=x;ay[n]=y;ad[n]= c=='H'?0: c=='D'?1: c=='B'?2: c=='G'?3: c-'0'; n++;}}
    init(1<<16);
    for(char *t=strtok(cs,";");t;t=strtok(NULL,";")){int x,y,c=1; int k=sscanf(t," %d,%d,%d",&x,&y,&c); if(k>=2) *slot(key(x,y))=c%q;}
    int *x18=malloc(n*4),*y18=malloc(n*4),*ms=malloc(n*4),*md=malloc(n*4);
    for(int i=0;i<n;i++){ms[i]=md[i]=2147483647;}
    for(long t=0;t<T;t++){
      for(int i=0;i<n;i++){
        unsigned char *c=slot(key(ax[i],ay[i]));
        ad[i]=(ad[i]+turn[*c])&3; *c=(*c+1)%q; ax[i]+=DX[ad[i]]; ay[i]+=DY[ad[i]];
      }
      if(t==T-19) for(int i=0;i<n;i++){x18[i]=ax[i];y18[i]=ay[i];}
      if(t>=T-18) for(int i=0;i<n;i++){int s=ax[i]+ay[i],d=ax[i]-ay[i]; if(s<ms[i])ms[i]=s; if(d<md[i])md[i]=d;}
    }
    size_t nz=0; for(size_t i=0;i<cap;i++) if(K[i]!=EMPTY && V[i]) nz++;
    printf("cases=%zu noires=%zu",used,nz);
    for(int i=0;i<n;i++) printf(" %d,%d,%d,%d",ax[i]-x18[i],ay[i]-y18[i],ms[i],md[i]);
    printf("\n"); fflush(stdout);
    free(K);free(V);free(ax);free(ay);free(ad);free(x18);free(y18);free(ms);free(md);
  }
  return 0;
}
