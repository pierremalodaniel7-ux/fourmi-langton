// gate.c — banc C pour les portes (règle RL, grille 4096², fourmis jouées dans l'ordre).
// Entrée : une ligne par situation "fourmis|cases T" (format du projet, caps H D B G).
// Sortie par fourmi : dx,dy (déplacement sur 104 pas, tenu 8 périodes) , voie u=x-y et v=x+y (min sur la dernière période),
// début de l'autoroute finale, ou "X" si pas d'autoroute 104. Bord touché => "BORD".
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 8192
#define O 4096
static unsigned char G[W*W];
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(){
  static char line[1<<20];
  int *px=malloc(sizeof(int)*16*2000001), *py=malloc(sizeof(int)*16*2000001);
  while(fgets(line,sizeof line,stdin)){
    int ax[64],ay[64],ad[64],n=0; long T=0; char *bar=strchr(line,'|'); if(!bar) continue; *bar=0;
    char *rest=bar+1; char *sp=strrchr(rest,' '); T=atol(sp+1); *sp=0;
    for(char *t=strtok(line,";");t;t=strtok(NULL,";")){char c; if(sscanf(t," %d,%d,%c",&ax[n],&ay[n],&c)==3){ad[n]=c=='H'?0:c=='D'?1:c=='B'?2:3;n++;}}
    memset(G,0,sizeof G);
    for(char *t=strtok(rest,";");t;t=strtok(NULL,";")){int x,y; if(sscanf(t," %d,%d",&x,&y)==2) G[(y+O)*W+x+O]^=1;}
    if((long)T*n>32000000)T=32000000/n; int bord=0; long t;
    for(t=0;t<T&&!bord;t++) for(int i=0;i<n;i++){
      int k=(ay[i]+O)*W+ax[i]+O; ad[i]=(ad[i]+(G[k]?3:1))&3; G[k]^=1; ax[i]+=DX[ad[i]]; ay[i]+=DY[ad[i]];
      if(ax[i]<-O+2||ax[i]>O-3||ay[i]<-O+2||ay[i]>O-3) bord=1;
      px[t*n+i]=ax[i]; py[t*n+i]=ay[i]; }
    if(bord){printf("BORD %ld\n",t);fflush(stdout);continue;}
    for(int i=0;i<n;i++){
      long e=T-1; int dx=px[e*n+i]-px[(e-104)*n+i], dy=py[e*n+i]-py[(e-104)*n+i]; int ok=(abs(dx)==2&&abs(dy)==2);
      for(long s=e;ok&&s>e-8*104;s--) if(px[s*n+i]-px[(s-104)*n+i]!=dx||py[s*n+i]-py[(s-104)*n+i]!=dy) ok=0;
      if(!ok){printf("X ");continue;}
      long s=e; while(s-104>=0 && px[s*n+i]-px[(s-104)*n+i]==dx && py[s*n+i]-py[(s-104)*n+i]==dy) s--;
      // voie : x-y (ou x+y) est constant le long de l'autoroute à phase près ; on prend le min sur 1 période
      int u=1<<30,v=1<<30; for(long r=e-103;r<=e;r++){int uu=px[r*n+i]-py[r*n+i],vv=px[r*n+i]+py[r*n+i]; if(uu<u)u=uu; if(vv<v)v=vv;}
      int lane = (dx*dy>0)? u : v;   // autoroute ↘/↖ : x-y constant ; ↙/↗ : x+y constant
      printf("%d,%d,%d,%ld ",dx,dy,lane,s-104+1); }
    printf("\n"); fflush(stdout);
  }
}
