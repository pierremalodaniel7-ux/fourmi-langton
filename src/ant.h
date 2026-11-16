// ant.h — fourmis RL multiples, grille par table de hachage, positions entières.
// Convention du projet : 0=H(0,-1) 1=D(+1,0) 2=B(0,+1) (y vers le bas, comme engine.js) 3=G(-1,0), R=+1.
// Pas d'une fourmi : c=couleur(x) ; d+=tour[c] ; couleur^=1 ; x+=dir(d). Fourmis 1,2,… l'une après l'autre.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
typedef struct { uint64_t *k; uint8_t *v; uint64_t cap, n; } Grid;
static inline uint64_t KEY(int x,int y){ return ((uint64_t)(uint32_t)(x+0x40000000)<<32)|(uint32_t)(y+0x40000000); }
static inline uint64_t H64(uint64_t a){ a^=a>>33; a*=0xff51afd7ed558ccdULL; a^=a>>33; a*=0xc4ceb9fe1a85ec53ULL; a^=a>>33; return a; }
static void g_init(Grid*g,uint64_t cap){ g->cap=cap; g->n=0; g->k=calloc(cap,8); g->v=calloc(cap,1); }
static void g_free(Grid*g){ free(g->k); free(g->v); }
static void g_clear(Grid*g){ memset(g->k,0,g->cap*8); memset(g->v,0,g->cap); g->n=0; }
static uint8_t* g_slot(Grid*g,uint64_t key);
static void g_grow(Grid*g){ Grid h; g_init(&h,g->cap*2); for(uint64_t i=0;i<g->cap;i++) if(g->k[i]) *g_slot(&h,g->k[i])=g->v[i]; g_free(g); *g=h; }
static uint8_t* g_slot(Grid*g,uint64_t key){
  if(g->n*2>g->cap) g_grow(g);
  uint64_t m=g->cap-1, i=H64(key)&m;
  while(g->k[i] && g->k[i]!=key) i=(i+1)&m;
  if(!g->k[i]){ g->k[i]=key; g->n++; }
  return &g->v[i];
}
static inline uint8_t g_get(Grid*g,int x,int y){ uint64_t key=KEY(x,y),m=g->cap-1,i=H64(key)&m; while(g->k[i]){ if(g->k[i]==key) return g->v[i]; i=(i+1)&m;} return 0; }
static inline void g_set(Grid*g,int x,int y,uint8_t c){ *g_slot(g,KEY(x,y))=c; }
static int g_black(Grid*g){ int n=0; for(uint64_t i=0;i<g->cap;i++) if(g->k[i]&&g->v[i]) n++; return n; }


// détection d'autoroute par fourmi : historique des caps
#define W 16384
typedef struct { int x,y,d; uint8_t hist[W]; long t; int frozen; } Ant;
static int TURN[2]={1,3}; // RL
static inline void a_step(Grid*g,Ant*a){
  uint8_t *s=g_slot(g,KEY(a->x,a->y)); uint8_t c=*s;
  a->d=(a->d+TURN[c])&3; *s=c^1; a->x+=DX[a->d]; a->y+=DY[a->d];
  a->hist[a->t%W]=a->d; a->t++;
}
// plus petite période p (2..pmax) répétée K fois, avec déplacement non nul ; 0 sinon
static int a_period(Ant*a,int pmax,int K,int*dx,int*dy){
  if(a->t<W) return 0;
  for(int p=2;p<=pmax;p++){ if((long)p*(K+1)>W) break; int ok=1;
    for(int i=0;i<p*K&&ok;i++) if(a->hist[(a->t-1-i)%W]!=a->hist[(a->t-1-i-p)%W]) ok=0;
    if(ok){ int X=0,Y=0; for(int i=0;i<p;i++){int d=a->hist[(a->t-1-i)%W]; X+=DX[d]; Y+=DY[d];}
      *dx=X;*dy=Y; return p; } }
  return 0;
}
static int pdir(const char*s){ return s[0]=='H'?0:s[0]=='D'?1:s[0]=='B'?2:3; }
