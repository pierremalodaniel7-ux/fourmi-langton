// drop.c — passagers sur une trace. ./drop TB "fourmis" "cases" PER [S=60000]
// 1) les fourmis construisent pendant TB pas ; constructeurs = fourmis de période PER ; on les fige.
// 2) fenêtre = cases touchées par les constructeurs pendant [TB/2, TB/2+PER) ; candidats = ces cases et voisines (rayon 2) × 4 caps.
// 3) chaque candidat roule seul S pas ; « passager » = périodique, déplacement parallèle à la trace, reste à < 40 de la ligne.
#include "ant.h"
static const char CAP[]="HDBG";
int main(int c,char**v){ long TB=atol(v[1]); int PER=atoi(v[4]); long S=c>5?atol(v[5]):60000;
  Ant A[16]; int n=0; char*s=strdup(v[2]),*tok; for(tok=strtok(s,";");tok;tok=strtok(NULL,";")){char d[4]; memset(&A[n],0,sizeof(Ant)); sscanf(tok," %d,%d,%1s",&A[n].x,&A[n].y,d); A[n].d=pdir(d); n++;}
  Grid g; g_init(&g,1<<23); s=strdup(v[3]); for(tok=strtok(s,";");tok;tok=strtok(NULL,";")){int x,y; if(sscanf(tok," %d,%d",&x,&y)==2) g_set(&g,x,y,1);}
  int ncand=0; static int CX[200000],CY[200000]; Grid mark; g_init(&mark,1<<16); Grid tr; g_init(&tr,1<<20); int cons[16]={0},ux=0,uy=0,ox=0,oy=0;
  for(long t=1;t<=TB;t++){ for(int i=0;i<n;i++){ if(t>TB/2&&t<=TB/2+PER&&cons[i]) for(int a=-2;a<=2;a++)for(int b=-2;b<=2;b++){ uint8_t*f=g_slot(&mark,KEY(A[i].x+a,A[i].y+b)); if(!*f){*f=1; CX[ncand]=A[i].x+a; CY[ncand++]=A[i].y+b;} }
      if(cons[i]||t<=TB/2) g_set(&tr,A[i].x,A[i].y,1); a_step(&g,&A[i]); }
    if(t==TB/2){ for(int i=0;i<n;i++){int dx,dy,p=a_period(&A[i],700,20,&dx,&dy); cons[i]=(p==PER); if(cons[i]){ux=dx;uy=dy;ox=A[i].x;oy=A[i].y;} printf("fourmi %d periode %d (%d,%d)%s\n",i+1,p,dx,dy,cons[i]?" constructeur":"");} } }
  printf("trace : direction (%d,%d) ; %d candidats x 4 caps\n",ux,uy,ncand);
  static int LX[2000000],LY[2000000]; int hist[2000][3]={0}; // [période][sens +/-] ; compte
  for(int k=0;k<ncand;k++) for(int d=0;d<4;d++){ Ant a; memset(&a,0,sizeof a); a.x=CX[k]; a.y=CY[k]; a.d=d; int ok=0,p=0,dx=0,dy=0;
    for(long t=0;t<S;t++){ LX[t]=a.x; LY[t]=a.y; a_step(&g,&a); }
    p=a_period(&a,700,20,&dx,&dy); long cr=(long)(a.x-ox)*uy-(long)(a.y-oy)*ux; double dist=fabs((double)cr)/sqrt(ux*ux+uy*uy);
    int inter=0; for(long t=S-2*p;t<S&&p;t++) if(g_get(&tr,LX[t],LY[t])) inter++;
    if(p&&(dx||dy)&&(long)dx*uy==(long)dy*ux&&dist<40&&inter) ok=1;
    if(ok){ int sens=(dx*ux+dy*uy)>0; if(p<2000){ if(!hist[p][sens]) printf("  passager periode %d dep (%d,%d) %s : fourmi %d,%d,%c\n",p,dx,dy,sens?"meme sens":"sens inverse",CX[k],CY[k],CAP[d]); hist[p][sens]++; } }
    for(long t=S-1;t>=0;t--){ uint8_t*f=g_slot(&g,KEY(LX[t],LY[t])); *f^=1; } }
  for(int p=0;p<2000;p++) for(int s2=0;s2<2;s2++) if(hist[p][s2]) printf("periode %d %s : %d candidats\n",p,s2?"meme sens":"sens inverse",hist[p][s2]);
}
