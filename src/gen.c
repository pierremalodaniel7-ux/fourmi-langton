// gen.c — fabrique un germe : joue "fourmis" "cases" pendant TB pas, ajoute la fourmi X,Y,D, écrit fourmis / points.
// ./gen TB "fourmis" "cases" "X,Y,D"
#include "ant.h"
static const char CAP[]="HDBG";
int main(int c,char**v){ long TB=atol(v[1]); Ant A[16]; int n=0; char*s=strdup(v[2]),*tok; for(tok=strtok(s,";");tok;tok=strtok(NULL,";")){char d[4]; memset(&A[n],0,sizeof(Ant)); sscanf(tok," %d,%d,%1s",&A[n].x,&A[n].y,d); A[n].d=pdir(d); n++;}
  Grid g; g_init(&g,1<<20); s=strdup(v[3]); for(tok=strtok(s,";");tok;tok=strtok(NULL,";")){int x,y; if(sscanf(tok," %d,%d",&x,&y)==2) g_set(&g,x,y,1);}
  for(long t=0;t<TB;t++) for(int i=0;i<n;i++) a_step(&g,&A[i]);
  printf("FOURMIS="); for(int i=0;i<n;i++) printf("%d,%d,%c ; ",A[i].x,A[i].y,CAP[A[i].d]); printf("%s\nPOINTS=",v[4]);
  int f=1; for(uint64_t i=0;i<g.cap;i++) if(g.k[i]&&g.v[i]){ printf("%s%d,%d",f?"":" ; ",(int)(g.k[i]>>32)-0x40000000,(int)(uint32_t)g.k[i]-0x40000000); f=0; } printf("\n"); }
