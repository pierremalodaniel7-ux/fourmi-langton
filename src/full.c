// full.c — système COMPLET (aucune fourmi retirée), grille infinie par table de hachage, positions entières.
// ./full T DT "fourmis" "cases" [NIDS]
//   Affiche tous les DT pas : position, période et déplacement de chaque fourmi (historique des caps).
//   NIDS = liste "i,j,...:T1:P" : vérifie que les fourmis i,j,... (1-based) ET les cases de leur zone
//   sont dans le même état aux instants T1 et T1+P et T1+2P (comparaison exacte case par case dans la boîte de la zone).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
typedef struct { uint64_t *k; uint8_t *v; uint64_t cap,n; } Grid;
static inline uint64_t KEY(int x,int y){ return ((uint64_t)(uint32_t)(x+0x40000000)<<32)|(uint32_t)(y+0x40000000); }
static inline uint64_t H64(uint64_t a){ a^=a>>33; a*=0xff51afd7ed558ccdULL; a^=a>>33; a*=0xc4ceb9fe1a85ec53ULL; a^=a>>33; return a; }
static void g_init(Grid*g,uint64_t c){ g->cap=c; g->n=0; g->k=calloc(c,8); g->v=calloc(c,1); }
static uint8_t* g_slot(Grid*g,uint64_t key);
static void g_grow(Grid*g){ Grid h; g_init(&h,g->cap*2); for(uint64_t i=0;i<g->cap;i++) if(g->k[i]) *g_slot(&h,g->k[i])=g->v[i]; free(g->k); free(g->v); *g=h; }
static uint8_t* g_slot(Grid*g,uint64_t key){ if(g->n*2>g->cap) g_grow(g); uint64_t m=g->cap-1,i=H64(key)&m;
  while(g->k[i]&&g->k[i]!=key) i=(i+1)&m; if(!g->k[i]){g->k[i]=key; g->n++; g->v[i]=0;} return &g->v[i]; }
static inline int g_get(Grid*g,int x,int y){ uint64_t key=KEY(x,y),m=g->cap-1,i=H64(key)&m; while(g->k[i]){ if(g->k[i]==key) return g->v[i]&1; i=(i+1)&m; } return 0; }
#define HW 16384
typedef struct { int x,y,d; long t; uint8_t h[HW]; } Ant;
static Ant A[16]; static int n;
static int per(Ant*a,int*dx,int*dy){ long L=a->t<HW?a->t:HW; for(int p=1;p<=3000;p++){ if((long)p*5>L) break; int ok=1;
    for(long i=0;i<(long)p*4;i++) if(a->h[(a->t-1-i)%HW]!=a->h[(a->t-1-i-p)%HW]){ok=0;break;}
    if(ok){ int X=0,Y=0; for(int i=0;i<p;i++){int d=a->h[(a->t-1-i)%HW]; X+=DX[d];Y+=DY[d];} *dx=X;*dy=Y; return p; } } return 0; }
int main(int c,char**v){ long T=atol(v[1]),DT=atol(v[2]); Grid g; g_init(&g,1<<20);
  char*s=strdup(v[3]),*tk; for(tk=strtok(s,";");tk;tk=strtok(NULL,";")){ int x,y; char d[4]; if(sscanf(tk," %d,%d,%1s",&x,&y,d)==3){ memset(&A[n],0,sizeof(Ant)); A[n].x=x;A[n].y=y;A[n].d=d[0]=='H'?0:d[0]=='D'?1:d[0]=='B'?2:3; n++; } }
  if(c>4){ s=strdup(v[4]); for(tk=strtok(s,";");tk;tk=strtok(NULL,";")){int x,y; if(sscanf(tk," %d,%d",&x,&y)==2) *g_slot(&g,KEY(x,y))=1;} }
  int nid[16],nn=0; long T1=-1,P=0; if(c>5){ char*q=strdup(v[5]); char*a=strtok(q,":"); char*b=strtok(NULL,":"); char*cc=strtok(NULL,":"); T1=atol(b); P=atol(cc);
    for(char*z=strtok(a,",");z;z=strtok(NULL,",")) nid[nn++]=atoi(z)-1; }
  // zone du nid : boîte des positions des fourmis du nid pendant [T1, T1+P)
  int bx0=1<<30,bx1=-(1<<30),by0=1<<30,by1=-(1<<30); int S1x[16],S1y[16],S1d[16]; uint8_t*snap=NULL; long W=0,H=0;
  for(long t=1;t<=T;t++){
    for(int i=0;i<n;i++){ Ant*a=&A[i]; uint8_t*sl=g_slot(&g,KEY(a->x,a->y)); int col=*sl&1; a->d=(a->d+(col?3:1))&3; *sl^=1; a->x+=DX[a->d]; a->y+=DY[a->d]; a->h[a->t%HW]=a->d; a->t++; }
    if(nn&&t>=T1&&t<T1+P) for(int k=0;k<nn;k++){ Ant*a=&A[nid[k]]; if(a->x<bx0)bx0=a->x; if(a->x>bx1)bx1=a->x; if(a->y<by0)by0=a->y; if(a->y>by1)by1=a->y; }
    if(nn&&(t==T1+P||t==T1+2*P||t==T1+3*P)){
      if(t==T1+P){ W=bx1-bx0+3; H=by1-by0+3; snap=malloc(W*H); for(long y=0;y<H;y++) for(long x=0;x<W;x++) snap[y*W+x]=g_get(&g,bx0-1+x,by0-1+y);
        for(int k=0;k<nn;k++){S1x[k]=A[nid[k]].x;S1y[k]=A[nid[k]].y;S1d[k]=A[nid[k]].d;} printf("nid : boite %ldx%ld relevee a T1+P=%ld\n",W,H,t); }
      else { long diff=0; for(long y=0;y<H;y++) for(long x=0;x<W;x++) if(snap[y*W+x]!=g_get(&g,bx0-1+x,by0-1+y)) diff++;
        int same=1; for(int k=0;k<nn;k++) if(S1x[k]!=A[nid[k]].x||S1y[k]!=A[nid[k]].y||S1d[k]!=A[nid[k]].d) same=0;
        printf("nid a t=%ld : fourmis %s, cases differentes dans la boite : %ld -> %s\n",t,same?"identiques":"DIFFERENTES",diff,(same&&!diff)?"OK":"ECHEC"); } }
    if(DT&&t%DT==0){ printf("t=%ld",t); for(int i=0;i<n;i++){ int dx=0,dy=0,p=per(&A[i],&dx,&dy); printf(" | %d:(%d,%d) p%d(%d,%d)",i+1,A[i].x,A[i].y,p,dx,dy);} printf("\n"); } }
  return 0; }
