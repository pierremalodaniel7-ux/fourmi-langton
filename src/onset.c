// onset.c — début exact (au sens de bestiaire2) de l'autoroute de chaque fourmi : ./onset T "fourmis" "cases"
// Joue T pas (système complet, table de hachage), puis pour chaque fourmi : plus petite période p<=3000 répétée 3 fois à la fin,
// et premier pas à partir duquel la suite des caps est p-périodique jusqu'à T.
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
int main(int c,char**v){ long T=atol(v[1]); int n=0,X[16],Y[16],D[16]; Grid g; g_init(&g,1<<20);
  char*s=strdup(v[2]),*tk; for(tk=strtok(s,";");tk;tk=strtok(NULL,";")){ char d[4]; if(sscanf(tk," %d,%d,%1s",&X[n],&Y[n],d)==3){ D[n]=d[0]=='H'?0:d[0]=='D'?1:d[0]=='B'?2:3; n++; } }
  if(c>3){ s=strdup(v[3]); for(tk=strtok(s,";");tk;tk=strtok(NULL,";")){int x,y; if(sscanf(tk," %d,%d",&x,&y)==2) *g_slot(&g,KEY(x,y))=1;} }
  uint8_t*h[16]; for(int i=0;i<n;i++) h[i]=malloc(T+1);
  for(long t=1;t<=T;t++) for(int i=0;i<n;i++){ uint8_t*sl=g_slot(&g,KEY(X[i],Y[i])); int col=*sl&1; D[i]=(D[i]+(col?3:1))&3; *sl^=1; X[i]+=DX[D[i]]; Y[i]+=DY[D[i]]; h[i][t]=D[i]; }
  for(int i=0;i<n;i++){ long P=0; for(long p=1;p<=3000&&4*p<T;p++){ long j; for(j=T;j>T-3*p;j--) if(h[i][j]!=h[i][j-p]) break; if(j==T-3*p){P=p;break;} }
    long deb=-1; int dx=0,dy=0; if(P){ long j=T; while(j-P>=1&&h[i][j]==h[i][j-P]) j--; deb=j-P+1>0?j-P+1:0; for(long k=T-P+1;k<=T;k++){dx+=DX[h[i][k]];dy+=DY[h[i][k]];} }
    printf("fourmi %d : periode %ld deplacement (%d,%d) debut %ld fin (%d,%d)\n",i+1,P,dx,dy,deb,X[i],Y[i]); }
  printf("cases noires %ld (cases touchees %ld)\n",0L,(long)g.n); }
