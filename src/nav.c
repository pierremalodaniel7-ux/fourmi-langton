// nav.c — navette de portée réglable. ./nav "fourmis" "cases" T0 RETIRE AVANCE F PASMAX
// Joue la config jusqu'à T0 ; retire la fourmi RETIRE (1-based, 0 = aucune) ; fait marcher la fourmi AVANCE seule F pas ;
// puis cherche un cycle exact (empreinte de Zobrist + vérification case par case sur 2 copies).
#include "ant.h"
typedef struct { Ant A[8]; int n; Grid g; } St;
static char *AS,*PS; static long T0,F; static int RET,AV;
static void setup(St*s){ char*p=strdup(AS),*tok; s->n=0; g_init(&s->g,1<<22);
  for(tok=strtok(p,";");tok;tok=strtok(NULL,";")){ char d[4]; Ant*a=&s->A[s->n++]; memset(a,0,sizeof(Ant)); sscanf(tok," %d,%d,%1s",&a->x,&a->y,d); a->d=pdir(d);}
  p=strdup(PS); for(tok=strtok(p,";");tok;tok=strtok(NULL,";")){int x,y; if(sscanf(tok," %d,%d",&x,&y)==2) g_set(&s->g,x,y,1);}
  for(long t=0;t<T0;t++) for(int i=0;i<s->n;i++) a_step(&s->g,&s->A[i]);
  if(RET){ for(int i=RET-1;i<s->n-1;i++) s->A[i]=s->A[i+1]; s->n--; if(AV>RET) AV--; }
  for(long t=0;t<F;t++) a_step(&s->g,&s->A[AV-1]); }
static uint64_t ah(Ant*a,int i){ return H64((KEY(a->x,a->y)<<2|a->d)+0x9e37ULL*(i+1)); }
static uint64_t hz(St*s){ uint64_t h=0; for(uint64_t i=0;i<s->g.cap;i++) if(s->g.k[i]&&s->g.v[i]) h^=H64(s->g.k[i]); for(int i=0;i<s->n;i++) h^=ah(&s->A[i],i); return h; }
static void step(St*s,uint64_t*h){ for(int i=0;i<s->n;i++){ Ant*a=&s->A[i]; *h^=ah(a,i)^H64(KEY(a->x,a->y)); a_step(&s->g,a); *h^=ah(a,i);} }
static int same(St*a,St*b){ for(int i=0;i<a->n;i++) if(a->A[i].x!=b->A[i].x||a->A[i].y!=b->A[i].y||a->A[i].d!=b->A[i].d) return 0;
  int na=0; for(uint64_t i=0;i<a->g.cap;i++) if(a->g.k[i]&&a->g.v[i]){ na++; int x=(int)(a->g.k[i]>>32)-0x40000000,y=(int)(uint32_t)a->g.k[i]-0x40000000; if(!g_get(&b->g,x,y)) return 0; }
  return na==g_black(&b->g); }
#define NS (1<<22)
int main(int c,char**v){ AS=v[1]; PS=v[2]; T0=atol(v[3]); RET=atoi(v[4]); AV=atoi(v[5]); F=atol(v[6]); long T=atol(v[7]);
  St s; setup(&s); uint64_t h=hz(&s); static uint64_t HK[NS]; static long HT[NS]; int nd=0; long P=0,t0=0; long far=0;
  for(long t=1;t<=T;t++){ step(&s,&h); for(int i=0;i<s.n;i++){ long r=labs(s.A[i].x)>labs(s.A[i].y)?labs(s.A[i].x):labs(s.A[i].y); if(r>far) far=r; }
    if(getenv("DBG")&&t%(1<<21)==0){ for(int i=0;i<s.n;i++){int dx,dy,p=a_period(&s.A[i],700,20,&dx,&dy); printf(" [%d: %d,%d p%d (%d,%d)]",i+1,s.A[i].x,s.A[i].y,p,dx,dy);} printf(" t=%ld\n",t);}
    if((h&0x3FF)==0){ for(int j=nd-1;j>=0;j--) if(HK[j]==h){P=t-HT[j];t0=HT[j];break;} if(P) break; if(nd<NS){HK[nd]=h;HT[nd++]=t;} } }
  if(!P){ printf("F=%ld : pas de cycle avant %ld pas (portee max %ld)\n",F,T,far); return 0; }
  St a,b; setup(&a); setup(&b); uint64_t x=0; for(long t=0;t<t0;t++){step(&a,&x);step(&b,&x);} for(long t=0;t<P;t++) step(&b,&x);
  printf("F=%ld : periode %ld des le pas %ld (apres T0+F) ; portee max %ld ; exact : %s\n",F,P,t0,far,same(&a,&b)?"OUI":"NON");
}
