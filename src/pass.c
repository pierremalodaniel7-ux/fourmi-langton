// pass.c — recherche au hasard de « passagers » : 2 fourmis dans la même direction, périodes différentes, proches.
// ./pass NFOURMIS NCASESMAX ESSAIS GRAINE [R=6] [PAS=400000]
#include "ant.h"
static uint64_t rs; static inline uint32_t rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (uint32_t)rs; }
static const char CAP[]="HDBG";
int main(int c,char**v){ int na=atoi(v[1]),nc=atoi(v[2]); long E=atol(v[3]); rs=atol(v[4])*2654435761ULL+1;
  int R=c>5?atoi(v[5]):6; long T=c>6?atol(v[6]):400000; Grid g; g_init(&g,1<<20);
  Ant A[8]; int x0[8],y0[8],d0[8],px[8],py[8];
  for(long e=0;e<E;e++){ g_clear(&g); int k=rnd()%(nc+1);
    for(int i=0;i<na;i++){ memset(&A[i],0,sizeof(Ant)); A[i].x=x0[i]=rnd()%(2*R+1)-R; A[i].y=y0[i]=rnd()%(2*R+1)-R; A[i].d=d0[i]=rnd()%4; }
    for(int j=0;j<k;j++){ px[j]=rnd()%(2*R+1)-R; py[j]=rnd()%(2*R+1)-R; g_set(&g,px[j],py[j],1); }
    int found=0;
    for(long t=1;t<=T&&!found;t++){ for(int i=0;i<na;i++) a_step(&g,&A[i]);
      if(t%8192) continue;
      int p[8],dx[8],dy[8]; for(int i=0;i<na;i++) p[i]=a_period(&A[i],700,20,&dx[i],&dy[i]);
      for(int i=0;i<na&&!found;i++) for(int j=0;j<na&&!found;j++)
        if(i!=j&&p[i]&&p[j]&&p[i]<p[j]&&(dx[i]||dy[i])&&(long)dx[i]*dy[j]==(long)dy[i]*dx[j]&&dx[i]*dx[j]>=0&&dy[i]*dy[j]>=0
           &&abs(A[i].x-A[j].x)+abs(A[i].y-A[j].y)<300){
          found=1; printf("t=%ld rapide %d(%d,%d) lent %d(%d,%d) | fourmis \"",t,p[i],dx[i],dy[i],p[j],dx[j],dy[j]);
          for(int q=0;q<na;q++) printf("%s%d,%d,%c",q?";":"",x0[q],y0[q],CAP[d0[q]]);
          printf("\" points \""); for(int q=0;q<k;q++) printf("%s%d,%d",q?";":"",px[q],py[q]); printf("\"\n"); fflush(stdout); } } }
  return 0; }
