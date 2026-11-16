// tr.c — suivre 2 fourmis : ./tr PAS DT "fourmis" "cases"
#include "ant.h"
int main(int c,char**v){ long T=atol(v[1]),DT=atol(v[2]); Ant A[8]; int n=0; char*s=strdup(v[3]),*tok; for(tok=strtok(s,";");tok;tok=strtok(NULL,";")){char d[4]; memset(&A[n],0,sizeof(Ant)); sscanf(tok," %d,%d,%1s",&A[n].x,&A[n].y,d); A[n].d=pdir(d); n++;}
  Grid g; g_init(&g,1<<22); if(c>4){ s=strdup(v[4]); for(tok=strtok(s,";");tok;tok=strtok(NULL,";")){int x,y; if(sscanf(tok," %d,%d",&x,&y)==2) g_set(&g,x,y,1);} }
  for(long t=1;t<=T;t++){ for(int i=0;i<n;i++) a_step(&g,&A[i]); if(t%DT==0){ printf("t=%ld",t); for(int i=0;i<n;i++){int dx,dy,p=a_period(&A[i],700,20,&dx,&dy); printf(" | %d: %d,%d p%d(%d,%d)",i+1,A[i].x,A[i].y,p,dx,dy);} printf("\n"); } } }
