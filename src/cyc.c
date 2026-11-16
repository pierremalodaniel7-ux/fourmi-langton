// cyc.c — cycle exact d'une configuration (toutes les fourmis).  ./cyc PASMAX "fourmis" ["cases"]
// Empreinte de Zobrist (grille + fourmis), points distingués (empreinte & 0x3FF == 0) ;
// une empreinte qui revient donne P candidat, puis vérification EXACTE : 2 copies, comparaison case par case.
#include "ant.h"
typedef struct { Ant A[16]; int n; Grid g; } St;
static uint64_t hz(St*s){ uint64_t h=0; for(uint64_t i=0;i<s->g.cap;i++) if(s->g.k[i]&&s->g.v[i]) h^=H64(s->g.k[i]);
  for(int i=0;i<s->n;i++) h^=H64((KEY(s->A[i].x,s->A[i].y)<<2|s->A[i].d)+0x9e37ULL*(i+1)); return h; }
static void parse(St*s,int c,char**v){ char*p=strdup(v[2]),*tok; s->n=0; g_init(&s->g,1<<20);
  for(tok=strtok(p,";");tok;tok=strtok(NULL,";")){ char d[4]; Ant*a=&s->A[s->n++]; memset(a,0,sizeof(Ant)); sscanf(tok," %d,%d,%1s",&a->x,&a->y,d); a->d=pdir(d);}
  if(c>3){ p=strdup(v[3]); for(tok=strtok(p,";");tok;tok=strtok(NULL,";")){int x,y; if(sscanf(tok," %d,%d",&x,&y)==2) g_set(&s->g,x,y,1);} } }
static void step(St*s,uint64_t*h){ for(int i=0;i<s->n;i++){ Ant*a=&s->A[i];
  *h^=H64((KEY(a->x,a->y)<<2|a->d)+0x9e37ULL*(i+1)); *h^=H64(KEY(a->x,a->y)); a_step(&s->g,a);
  *h^=H64((KEY(a->x,a->y)<<2|a->d)+0x9e37ULL*(i+1)); } }
static int same(St*a,St*b){ for(int i=0;i<a->n;i++) if(a->A[i].x!=b->A[i].x||a->A[i].y!=b->A[i].y||a->A[i].d!=b->A[i].d) return 0;
  int na=0,nb=0; for(uint64_t i=0;i<a->g.cap;i++) if(a->g.k[i]&&a->g.v[i]){ na++; int x=(int)(a->g.k[i]>>32)-0x40000000,y=(int)(uint32_t)a->g.k[i]-0x40000000; if(!g_get(&b->g,x,y)) return 0; }
  nb=g_black(&b->g); return na==nb; }
#define NS (1<<22)
int main(int c,char**v){ long T=atol(v[1]); St s; parse(&s,c,v); uint64_t h=hz(&s);
  static uint64_t HK[NS]; static long HT[NS]; int nd=0; long P=0,t0=0;
  HK[nd]=h; HT[nd++]=0; // l'état initial est toujours enregistré
  for(long t=1;t<=T;t++){ step(&s,&h);
    if((h&0x3FF)==0||t==0){ for(int j=nd-1;j>=0;j--) if(HK[j]==h){ P=t-HT[j]; t0=HT[j]; break; }
      if(P) break; if(nd<NS){HK[nd]=h;HT[nd++]=t;} }
    if(h==HK[0]){ P=t; t0=0; break; } }
  if(!P){ printf("pas de cycle avant %ld pas\n",T); return 0; }
  // vérification exacte : état à t0 et à t0+P
  St a,b; parse(&a,c,v); parse(&b,c,v); uint64_t x=0;
  for(long t=0;t<t0;t++){ step(&a,&x); step(&b,&x);} for(long t=0;t<P;t++) step(&b,&x);
  int ok=same(&a,&b); printf("candidat : periode %ld des le pas %ld  -> verification exacte : %s (%d cases noires)\n",P,t0,ok?"OUI":"NON",g_black(&a.g));
}
