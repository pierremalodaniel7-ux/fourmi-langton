// run.c — rejouer une configuration.  ./run PAS "x,y,D;..." ["x,y;..."]
// Affiche, pour chaque fourmi, la première détection d'autoroute (période, déplacement) et l'état final.
#include "ant.h"
int main(int c,char**v){
  long T=atol(v[1]); Ant A[64]; int n=0; char *s=strdup(v[2]),*tok;
  for(tok=strtok(s,";");tok;tok=strtok(NULL,";")){ char d[4]; memset(&A[n],0,sizeof(Ant)); sscanf(tok," %d,%d,%1s",&A[n].x,&A[n].y,d); A[n].d=pdir(d); n++; }
  Grid g; g_init(&g,1<<20);
  if(c>3){ char*p=strdup(v[3]); for(tok=strtok(p,";");tok;tok=strtok(NULL,";")){int x,y; if(sscanf(tok," %d,%d",&x,&y)==2) g_set(&g,x,y,1);} }
  int seen[64]={0};
  for(long t=1;t<=T;t++){ for(int i=0;i<n;i++) a_step(&g,&A[i]);
    if(t%4096==0) for(int i=0;i<n;i++){ int dx,dy,p=a_period(&A[i],700,20,&dx,&dy);
      if(p!=seen[i]){ printf("t=%ld fourmi %d : periode %d dep (%d,%d) pos (%d,%d)\n",t,i+1,p,dx,dy,A[i].x,A[i].y); seen[i]=p; } } }
  for(int i=0;i<n;i++) printf("fin fourmi %d : (%d,%d) cap %d\n",i+1,A[i].x,A[i].y,A[i].d);
  printf("cases noires %d\n",g_black(&g));
}
