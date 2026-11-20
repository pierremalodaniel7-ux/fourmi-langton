// balaye.c — balayage massif des règles L/R (grille carrée, 1 fourmi, départ blanc, (0,0), cap H).
// Grille infinie par tuiles 64x64 allouées à la demande (zone ±65 536). Entiers exacts.
// Pour chaque règle lue sur stdin (une par ligne) : simule jusqu'à MAXPAS et classe :
//   B  cycle exact (retour à l'état initial complet : PREUVE de périodicité)
//   V  autoroute (cap périodique de période P tenu >= 3P pas, déplacement != 0) ;
//      cert=1 si le certificat exact (voir certif()) PROUVE l'autoroute infinie
//   E  sortie de la zone ±65 536 sans autoroute détectée
//   G  croissance sans autoroute (C/S/X décidés ensuite par tri à partir des mesures)
// Usage : ./balaye MAXPAS < regles.txt > sortie.csv
// Colonnes : regle,q,classe,pas,P,dx,dy,debut,cert,t_cert,boxw,boxh,ratio,ngram,noirs,sym,symok,symtest,ms
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#define TS 64
#define NT 2048            /* tuiles par côté -> 131 072 cases */
#define HALF (NT*TS/2)
#define HB (1<<22)         /* tampon circulaire des caps */
#define HM (HB-1)
static unsigned char *tile[NT*NT];
static int alloc_list[NT*NT]; static int nalloc;
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static int q, turn[64];
static unsigned char hb[HB];          /* caps */
static unsigned char tb[HB];          /* lettres lues (0=L,1=R) */
static int out_of_zone;

static inline unsigned char *cell(int x,int y){
  int X=x+HALF, Y=y+HALF;
  if(X<0||Y<0||X>=NT*TS||Y>=NT*TS){ out_of_zone=1; static unsigned char dummy; dummy=0; return &dummy; }
  int ti=(Y/TS)*NT+(X/TS);
  if(!tile[ti]){ tile[ti]=calloc(TS*TS,1); alloc_list[nalloc++]=ti; }
  return &tile[ti][(Y%TS)*TS+(X%TS)];
}
static inline int peek(int x,int y){
  int X=x+HALF, Y=y+HALF;
  if(X<0||Y<0||X>=NT*TS||Y>=NT*TS) return 0;
  int ti=(Y/TS)*NT+(X/TS); if(!tile[ti]) return 0;
  return tile[ti][(Y%TS)*TS+(X%TS)];
}
static void reset(void){ for(int i=0;i<nalloc;i++){ free(tile[alloc_list[i]]); tile[alloc_list[i]]=0; } nalloc=0; out_of_zone=0; }

typedef struct { int x,y,d; long t; long nonwhite; int bx0,bx1,by0,by1; } St;
static inline void step(St*s){
  unsigned char*c=cell(s->x,s->y); int v=*c;
  int r=turn[v]; s->d=(s->d+(r?1:3))&3;
  int nv=v+1; if(nv==q) nv=0; if(v==0) s->nonwhite++; if(nv==0) s->nonwhite--;
  *c=nv; s->x+=DX[s->d]; s->y+=DY[s->d]; s->t++;
  hb[s->t&HM]=s->d; tb[s->t&HM]=r;
  if(s->x<s->bx0)s->bx0=s->x; if(s->x>s->bx1)s->bx1=s->x; if(s->y<s->by0)s->by0=s->y; if(s->y>s->by1)s->by1=s->y;
}
static void init(St*s){ memset(s,0,sizeof *s); }

/* Certificat exact (preuve d'autoroute infinie).
   État à t1 = f0 (grille), fourmi (p,d). On joue P pas : cases visitées S, nombre de visites n(c).
   Si la fourmi est en p+D avec le même cap, et si pour toute c de S et tout k>=0 :
      f0(c+(k+1)D) + sum_{i=1..k+1} n(c+iD) == f0(c)  (mod q)
   alors la période k+1 rejoue la période 0 translatée de (k+1)D, pour tout k (récurrence) :
   l'autoroute est infinie. Au-delà de la boîte, les termes sont constants : vérification finie. */
typedef struct { int64_t key; int n; } KN;
static int cmpk(const void*a,const void*b){ int64_t x=((KN*)a)->key, y=((KN*)b)->key; return x<y?-1:x>y; }
static inline int64_t K(int x,int y){ return ((int64_t)(x+HALF)<<20)|(int64_t)(y+HALF); }
static KN*kn; static int nkn;
static int nof(int x,int y){ int64_t k=K(x,y); int lo=0,hi=nkn-1; while(lo<=hi){int m=(lo+hi)/2; if(kn[m].key==k) return kn[m].n; if(kn[m].key<k) lo=m+1; else hi=m-1;} return 0; }
static int certif(long t1,long P){
  reset(); St s; init(&s);
  while(s.t<t1){ step(&s); if(out_of_zone) return 0; }
  int px=s.x,py=s.y,pd=s.d;
  KN*v=malloc(sizeof(KN)*P); int *vx=malloc(sizeof(int)*P), *vy=malloc(sizeof(int)*P);
  for(long i=0;i<P;i++){ vx[i]=s.x; vy[i]=s.y; v[i].key=K(s.x,s.y); v[i].n=1; step(&s); }
  int ok=1, Dx=s.x-px, Dy=s.y-py;
  if(out_of_zone||s.d!=pd||(Dx==0&&Dy==0)) ok=0;
  qsort(v,P,sizeof(KN),cmpk); nkn=0;
  for(long i=0;i<P;i++){ if(nkn&&v[nkn-1].key==v[i].key) v[nkn-1].n++; else v[nkn++]=v[i]; }
  kn=v;
  int bx0=s.bx0-1,bx1=s.bx1+1,by0=s.by0-1,by1=s.by1+1;
  for(int j=0;ok&&j<nkn;j++){
    int cx=(int)(kn[j].key>>20)-HALF, cy=(int)(kn[j].key&0xFFFFF)-HALF;
    int f0c=((peek(cx,cy)-kn[j].n)%q+q)%q;
    long sum=0;
    for(long k=0;;k++){
      int x=cx+(int)(k+1)*Dx, y=cy+(int)(k+1)*Dy;
      int nn=nof(x,y); sum+=nn;
      int f1=peek(x,y); int f0=((f1-nn)%q+q)%q;
      if((f0+sum)%q!=f0c){ ok=0; break; }
      if(x<bx0||x>bx1||y<by0||y>by1) break;
    }
  }
  free(v); free(vx); free(vy); return ok;
}

static long distinct_ngrams(long t){ /* nb de 20-grammes distincts des lettres lues sur les 2^20 derniers pas */
  static unsigned char *bits=0; if(!bits) bits=malloc(1<<17);
  memset(bits,0,1<<17); long w=t<(1<<20)?t:(1<<20); if(w<40) return 0;
  unsigned g=0; long cnt=0;
  for(long i=t-w+1;i<=t;i++){ g=((g<<1)|tb[i&HM])&0xFFFFF; if(i>=t-w+20){ if(!(bits[g>>3]&(1<<(g&7)))){bits[g>>3]|=1<<(g&7);cnt++;} } }
  return cnt;
}

/* symétrie du motif (couleurs égales) autour du centre de la boîte des cases non blanches */
static int *vis_x,*vis_y; static long nvis, capvis;
static int symtest(void){
  int x0=1<<30,x1=-(1<<30),y0=1<<30,y1=-(1<<30); long nw=0;
  for(long i=0;i<nvis;i++){ int x=vis_x[i],y=vis_y[i]; if(peek(x,y)){ nw++; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
  if(nw<8) return 0;
  long cx=x0+x1, cy=y0+y1; int mask=0;
  for(int w=0;w<6;w++){
    int ok=1;
    for(long i=0;i<nvis&&ok;i++){ int X=vis_x[i],Y=vis_y[i]; int c=peek(X,Y); if(!c) continue;
      long u=2L*X-cx, vv=2L*Y-cy, a,b;
      switch(w){case 0:a=-u;b=vv;break; case 1:a=u;b=-vv;break; case 2:a=vv;b=u;break; case 3:a=-vv;b=-u;break; case 4:a=-u;b=-vv;break; default:a=-vv;b=u;}
      if((a+cx)&1||(b+cy)&1){ok=0;break;}
      if(peek((int)((a+cx)/2),(int)((b+cy)/2))!=c) ok=0; }
    if(ok) mask|=1<<w;
  }
  return mask; /* bits : 0 miroir |, 1 miroir -, 2 diag, 3 antidiag, 4 centrale 180, 5 rotation 90 */
}

static void buildvis(void){ nvis=0;
  for(int a=0;a<nalloc && nvis<capvis;a++){ int ti=alloc_list[a]; int TX=(ti%NT)*TS-HALF, TY=(ti/NT)*TS-HALF;
    for(int k=0;k<TS*TS && nvis<capvis;k++) if(tile[ti][k]){ vis_x[nvis]=TX+k%TS; vis_y[nvis]=TY+k/TS; nvis++; } } }
int main(int argc,char**argv){
  long maxs=atol(argv[1]); long Pmax=argc>2?atol(argv[2]):600000;
  char rule[128];
  capvis=4000000; vis_x=malloc(sizeof(int)*capvis); vis_y=malloc(sizeof(int)*capvis);
  while(scanf("%127s",rule)==1){
    clock_t c0=clock();
    q=strlen(rule); for(int i=0;i<q;i++) turn[i]=rule[i]=='R';
    reset(); St s; init(&s); nvis=0;
    char cls='G'; long P=0,start=0; int Dx=0,Dy=0, cert=0; long tcert=0;
    long box1m=0, box2m=0; long nextchk=65536, nextsym=1000; int symmask_or=0, symok=0, symtest_n=0, symall=63;
    while(s.t<maxs){
      step(&s);
      if(out_of_zone){ cls='E'; break; }
      if(s.nonwhite==0 && s.x==0 && s.y==0 && s.d==0){ cls='B'; break; }
      if(s.x==0&&s.y==0&&s.t>=nextsym){ nextsym=s.t+s.t/3+1000; buildvis(); int mm=symtest(); symtest_n++; if(mm){symok++; symmask_or|=mm;} }
      if(s.t==maxs/2) box1m=(s.bx1-s.bx0>s.by1-s.by0?s.bx1-s.bx0:s.by1-s.by0)+1;
      if(s.t>=nextchk){
        nextchk+=65536;
        long w=s.t<HB-8?s.t:HB-8;
        for(long p=1;3*p<=w && p<=Pmax;p++){
          long hold=3*p<30000?30000:3*p; if(hold+p>w) break;
          long i=0; while(i<hold && hb[(s.t-i)&HM]==hb[(s.t-i-p)&HM]) i++;
          if(i<hold) continue;
          int ddx=0,ddy=0; for(long j=0;j<p;j++){ int d=hb[(s.t-j)&HM]; ddx+=DX[d]; ddy+=DY[d]; }
          if(ddx==0&&ddy==0) continue;
          long st=s.t-3*p; long lim=s.t-w+p; while(st>lim && hb[st&HM]==hb[(st+p)&HM]) st--;
          P=p; Dx=ddx; Dy=ddy; start=st; cls='V'; break;
        }
        if(cls=='V') break;
      }
    }
    long steps=s.t; int bw=s.bx1-s.bx0+1, bh=s.by1-s.by0+1;
    box2m=bw>bh?bw:bh; long nw=s.nonwhite;
    long ng=(cls=='G'||cls=='E')?distinct_ngrams(s.t):0;
    if(cls=='G'){ buildvis(); int m=symtest(); symtest_n++; if(m){symok++; symmask_or|=m;} }
    if(cls=='V'){
      long T=steps; long tries[4]={start, start+P, start+(T-start)/2, T-P};
      for(int i=0;i<4&&!cert;i++){ long t1=tries[i]; if(t1<0) t1=0; if(certif(t1,P)){cert=1;tcert=t1;} }
    }
    double ratio=box1m?(double)box2m/box1m:0;
    double ms=1000.0*(clock()-c0)/CLOCKS_PER_SEC;
    printf("%s,%d,%c,%ld,%ld,%d,%d,%ld,%d,%ld,%d,%d,%.3f,%ld,%ld,%d,%d,%d,%.0f\n",
      rule,q,cls,steps,P,Dx,Dy,start,cert,tcert,bw,bh,ratio,ng,nw,symmask_or,symok,symtest_n,ms);
    fflush(stdout);
  }
  return 0;
}
