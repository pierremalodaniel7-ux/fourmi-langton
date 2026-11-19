/* b5.c — B5 : arbre de choix exhaustif exact pour la fourmi RL classique dans un carré n×n.
   Conventions (= ant_controle.c) : x à droite, y en HAUT, cap 0 = haut, 1 = droite, 2 = bas, 3 = gauche ;
   blanc (0) -> tourne à droite, noir (1) -> tourne à gauche, puis on inverse la case et on avance.
   Masque : bit i <-> case (i mod n, i div n), coin bas-gauche du carré en (0,0).

   Arbre : les n² cases du carré sont INCONNUES (valeur 2), tout le reste est blanc. À la première lecture
   d'une case inconnue on branche (blanc puis noir) ; un journal (positions de chaque pas) permet d'annuler.
   Feuille : premier instant s où le lemme du certificat (R-83, E1_certificat.md) est vrai pour p = 104.
   Candidat s seulement si les couleurs lues sur [s, s+p) et [s+p, s+2p) coïncident (condition nécessaire :
   un certificat en s rend la suite lue périodique dès s). Le certificat en s se teste sur l'état exact à s
   (on défait les pas s..t-1), avec V, Pv, Pa tirés de l'histoire réelle (le jeu « à blanc » = le jeu réel
   pendant p pas). Z est vérifiée dans la boîte « carré entier ∪ toutes les cases visitées jusqu'à t » ;
   hors de cette boîte tout est blanc. Une case de Z noire connue -> échec ; sinon une case de Z inconnue ->
   on branche dessus (blanc : on reteste ; noir : échec à cet instant). Ainsi, pour CHAQUE coloriage
   complet compatible avec une feuille, le premier instant certifié est exactement celui de la feuille.
   Une feuille prouve 2^(nb d'inconnues restantes) coloriages.

   Usage :
     b5 arbre N AX AY PREFIXE TMAX [echantillons]   sous-arbre dont les premiers choix suivent PREFIXE
                                                    ('-' = vide ; ex. 0110). Résumé sur stdout.
     b5 brut  N AX AY TMAX [masque]                  sans arbre : tous les masques (ou un seul) -> "m t"
     b5 feuilles N AX AY TMAX                        arbre complet, une ligne par feuille (validation)
   Échantillons : fichier de lignes "AX AY MASQUE" ; pour ceux de cette position et compatibles avec le
   préfixe, on écrit "ECH ax ay masque t profondeur" (t de la feuille qui contient le masque).
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define P 104
#define W 2048
#define OFF (W/2)
#define MARGE 8
static uint8_t g[W*W];                 /* 0 blanc, 1 noir, 2 inconnue */
static uint32_t *HP; static uint8_t *HT, *HH;   /* histoire : position (indice), couleur lue, cap avant le pas */
static int dx[4]={0,1,0,-1}, dy[4]={1,0,-1,0};
static long TMAX;
static int N, AX, AY;
static inline uint32_t IDX(int x,int y){ return (uint32_t)(y+OFF)*W + (uint32_t)(x+OFF); }
static inline int IX(uint32_t i){ return (int)(i%W)-OFF; }
static inline int IY(uint32_t i){ return (int)(i/W)-OFF; }

/* état courant */
static long t; static int x, y, h; static int bx0,bx1,by0,by1; static long runlen;
static uint64_t pas_total=0;

/* certificat en s = t-2P. Retour : 1 certifié, 0 non, 2 besoin de la case *zc (inconnue, dans Z). */
static uint32_t vmark[W*W/1]; static uint32_t stamp=0; static uint8_t vid[W*W];
static int certifie(long s, uint32_t *zc, int *ddx_out, int *ddy_out){
  /* V depuis l'histoire réelle */
  static uint32_t V[P]; static uint8_t pv[P], pa[P]; int nv=0;
  if(++stamp==0){ memset(vmark,0,sizeof vmark); stamp=1; }
  for(long u=s; u<s+P; u++){ uint32_t c=HP[u];
    if(vmark[c]!=stamp){ vmark[c]=stamp; vid[c]=(uint8_t)nv; V[nv]=c; pv[nv]=HT[u]; pa[nv]=HT[u]; nv++; }
    pa[vid[c]]^=1; }
  int sx=IX(HP[s]), sy=IY(HP[s]);
  int ex=IX(HP[s+P]), ey=IY(HP[s+P]);
  int Dx=ex-sx, Dy=ey-sy;
  if(HH[s+P]!=HH[s] || (Dx==0&&Dy==0)) return 0;                       /* F1 */
  long dI=(long)Dy*W+Dx;
  for(int i=0;i<nv;i++){ uint32_t c=(uint32_t)((long)V[i]+dI);
    if(vmark[c]==stamp){ if(pa[vid[c]]!=pv[i]) return 0; }               /* F2 */
    else if(pv[i]!=0) return 0; }                                         /* F3 */
  for(int i=0;i<nv;i++) for(int m=2;m<=2*P;m++){                         /* F4 */
    int cx=IX(V[i])+m*Dx, cy=IY(V[i])+m*Dy;
    if(abs(cx-sx)>P+1||abs(cy-sy)>P+1) break;
    if(vmark[IDX(cx,cy)]==stamp)
      for(int k=1;k<m;k++) if(vmark[IDX(IX(V[i])+k*Dx,IY(V[i])+k*Dy)]!=stamp) return 0; }
  /* Z : couleurs à l'instant s -> défaire les pas s..t-1 */
  for(long u=t-1;u>=s;u--) g[HP[u]]^=1;
  int res=1; uint32_t first_unk=0; int has_unk=0;
  for(int i=0;i<nv && res;i++){
    int cx=IX(V[i]), cy=IY(V[i]);
    for(int k=1;;k++){ cx+=Dx; cy+=Dy;
      if(cx<bx0||cx>bx1||cy<by0||cy>by1) break;      /* rayon sorti de la boîte convexe : n'y revient pas */
      uint32_t c=IDX(cx,cy); if(vmark[c]==stamp) continue;
      if(g[c]==1){ res=0; break; }
      if(g[c]==2 && !has_unk){ has_unk=1; first_unk=c; } } }
  for(long u=s;u<t;u++) g[HP[u]]^=1;
  if(!res) return 0;
  if(has_unk){ *zc=first_unk; return 2; }
  *ddx_out=Dx; *ddy_out=Dy; return 1;
}

/* pile de choix */
typedef struct { long t; int x,y,h,bx0,bx1,by0,by1; long runlen; uint32_t cell; int kind; int col; int fixe; } Frame;
static Frame st[64]; static int dep;

/* résultats */
static long nfeuilles=0, nnonres=0; static uint64_t poids=0, poids_nonres=0, poids_autre=0;
static long tmax_cert=-1, tmin_cert=-1; static uint64_t mask_max=0, known_max=0; static int dep_max=0;
static long hist[40];
static FILE *fnonres; static int verbeux=0;
/* échantillons */
static int nech=0; static uint64_t *ech; static long *ech_t; static int *ech_d;
static int *lst[66]; static int nlst[66];   /* échantillons compatibles avec les choix st[0..d-1] */
static void filtre(int d){ /* recalcule lst[d+1] à partir de lst[d] et du choix st[d] */
  if(!nech) return; uint32_t c=st[d].cell; int i=IY(c)*N+IX(c); int b=st[d].col; int k=0;
  for(int j=0;j<nlst[d];j++){ int e=lst[d][j]; if((int)((ech[e]>>i)&1)==b) lst[d+1][k++]=e; } nlst[d+1]=k; }

static void masque_feuille(uint64_t *val, uint64_t *known){
  *val=0; *known=0;   /* valeurs initiales = couleurs affectées dans la pile */
  for(int d=0;d<dep;d++){ uint32_t c=st[d].cell; int i=(IY(c))*N+IX(c); *known|=1ULL<<i; if(st[d].col) *val|=1ULL<<i; }
}

static void feuille(int certifiee, long tc, int Dx, int Dy, const char *pref, int lpref){
  /* feuille avant la fin du préfixe : ne la compter qu'une fois (bits restants du préfixe = 0) */
  for(int d=dep; d<lpref; d++) if(pref[d]!='0') return;
  uint64_t w=1ULL<<(N*N-dep), val, known; masque_feuille(&val,&known);
  if(verbeux) printf("F %llu %llu %ld %d %d %d\n",(unsigned long long)known,(unsigned long long)val,certifiee?tc:-1,dep,Dx,Dy);
  for(int j=0;j<nlst[dep];j++){ int e=lst[dep][j]; ech_t[e]=certifiee?tc:-1; ech_d[e]=dep; }
  if(!certifiee){ nnonres++; poids_nonres+=w;
    if(fnonres) fprintf(fnonres,"NONRES %d %d known=%llu val=%llu t=%ld\n",AX,AY,(unsigned long long)known,(unsigned long long)val,tc);
    return; }
  nfeuilles++; poids+=w;
  if(!((Dx==2||Dx==-2)&&(Dy==2||Dy==-2))) poids_autre+=w;
  if(tc>tmax_cert){ tmax_cert=tc; mask_max=val; known_max=known; dep_max=dep; }
  if(tmin_cert<0||tc<tmin_cert) tmin_cert=tc;
  int b=0; long v=tc; while(v>1){v>>=1;b++;} hist[b]++;
}

static void arbre(const char *pref){
  int lpref=(int)strlen(pref); if(!strcmp(pref,"-")) lpref=0;
  memset(g,0,sizeof g);
  for(int i=0;i<N*N;i++) g[IDX(i%N,i/N)]=2;
  t=0; x=AX; y=AY; h=0; bx0=0; bx1=N-1; by0=0; by1=N-1; runlen=0; dep=0;
  int verif=0;   /* 1 : refaire le test de certificat à l'instant t (reprise sur une case de Z) */
  for(;;){
    /* ---- avance jusqu'à une feuille ---- */
    int fin=0, certok=0, Dx=0, Dy=0;
    while(!fin){
      if(verif){ verif=0;
        if(runlen>=P){ uint32_t zc; int r=certifie(t-2*P,&zc,&Dx,&Dy);
          if(r==1){ fin=1; certok=1; break; }
          if(r==2){ Frame *f=&st[dep++]; f->t=t; f->x=x; f->y=y; f->h=h; f->bx0=bx0; f->bx1=bx1; f->by0=by0; f->by1=by1;
            f->runlen=runlen; f->cell=zc; f->kind=1; f->fixe=dep-1<lpref; f->col=f->fixe?pref[dep-1]-'0':0;
            g[zc]=(uint8_t)f->col; filtre(dep-1); verif=1; continue; } }
      }
      if(t>=TMAX || x<-OFF+MARGE||x>OFF-MARGE||y<-OFF+MARGE||y>OFF-MARGE){ fin=1; certok=0; break; }
      uint32_t c=IDX(x,y); uint8_t col=g[c];
      if(col==2){ Frame *f=&st[dep++]; f->t=t; f->x=x; f->y=y; f->h=h; f->bx0=bx0; f->bx1=bx1; f->by0=by0; f->by1=by1;
        f->runlen=runlen; f->cell=c; f->kind=0; f->fixe=dep-1<lpref; f->col=f->fixe?pref[dep-1]-'0':0;
        g[c]=(uint8_t)f->col; col=g[c]; filtre(dep-1); }
      HP[t]=c; HT[t]=col; HH[t]=(uint8_t)h;
      h = col ? (h+3)&3 : (h+1)&3; g[c]^=1; x+=dx[h]; y+=dy[h];
      if(x<bx0)bx0=x; if(x>bx1)bx1=x; if(y<by0)by0=y; if(y>by1)by1=y;
      if(t>=P){ if(HT[t]==HT[t-P]) runlen++; else runlen=0; }
      t++; pas_total++;
      if(runlen>=P) verif=1;
    }
    feuille(certok, certok? t-2*P : t, Dx, Dy, pref, lpref);
    /* ---- retour arrière ---- */
    for(;;){
      if(dep==0) return;
      Frame *f=&st[dep-1];
      for(long u=t-1;u>=f->t;u--) g[HP[u]]^=1;     /* défaire les pas */
      t=f->t; x=f->x; y=f->y; h=f->h; bx0=f->bx0; bx1=f->bx1; by0=f->by0; by1=f->by1; runlen=f->runlen;
      if(!f->fixe && f->col==0){ f->col=1; g[f->cell]=1; filtre(dep-1); verif=(f->kind==1); break; }
      g[f->cell]=2; dep--;
      if(f->fixe && dep<lpref){ /* on remonte dans le préfixe : fin du sous-arbre */ return; }
    }
  }
}

int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"voir l'en-tête\n"); return 1; }
  if(!strcmp(argv[1],"arbre")||!strcmp(argv[1],"feuilles")){
    int fe=!strcmp(argv[1],"feuilles");
    N=atoi(argv[2]); AX=atoi(argv[3]); AY=atoi(argv[4]);
    const char *pref = fe ? "-" : argv[5]; TMAX=atol(fe?argv[5]:argv[6]);
    verbeux=fe; fnonres=stdout;
    HP=malloc(sizeof(uint32_t)*(TMAX+2*P+8)); HT=malloc(TMAX+2*P+8); HH=malloc(TMAX+2*P+8);
    if(!fe && argc>7){ FILE *fe2=fopen(argv[7],"r"); int a,b; unsigned long long m; ech=malloc(8*200000);
      int lp=strcmp(pref,"-")?(int)strlen(pref):0; (void)lp;
      while(fscanf(fe2,"%d %d %llu",&a,&b,&m)==3) if(a==AX&&b==AY) ech[nech++]=m;
      fclose(fe2); ech_t=malloc(sizeof(long)*(nech+1)); ech_d=malloc(sizeof(int)*(nech+1));
      for(int e=0;e<nech;e++){ ech_t[e]=-2; ech_d[e]=-1; }
      for(int d=0;d<66;d++) lst[d]=malloc(sizeof(int)*(nech+1));
      for(int e=0;e<nech;e++) lst[0][e]=e; nlst[0]=nech; }
    clock_t c0=clock(); arbre(pref); double sec=(double)(clock()-c0)/CLOCKS_PER_SEC;
    for(int e=0;e<nech;e++) if(ech_t[e]!=-2) printf("ECH %d %d %llu %ld %d\n",AX,AY,(unsigned long long)ech[e],ech_t[e],ech_d[e]);
    printf("RES N=%d pos=%d,%d pref=%s feuilles=%ld poids=%llu nonres=%ld poids_nonres=%llu poids_autre_derive=%llu "
           "tmax=%ld masque_max=%llu connues_max=%llu prof_max=%d tmin=%ld pas=%llu sec=%.2f\n",
      N,AX,AY,pref,nfeuilles,(unsigned long long)poids,nnonres,(unsigned long long)poids_nonres,(unsigned long long)poids_autre,
      tmax_cert,(unsigned long long)mask_max,(unsigned long long)known_max,dep_max,tmin_cert,(unsigned long long)pas_total,sec);
    printf("HIST"); for(int b=0;b<40;b++) printf(" %ld",hist[b]); printf("\n");
    return 0;
  }
  if(!strcmp(argv[1],"brut")){
    /* même moteur, aucune inconnue : chaque masque séparément (arbre à préfixe = masque complet impossible
       car l'ordre des cases dépend du chemin) -> on met toutes les cases connues */
    N=atoi(argv[2]); AX=atoi(argv[3]); AY=atoi(argv[4]); TMAX=atol(argv[5]);
    HP=malloc(sizeof(uint32_t)*(TMAX+2*P+8)); HT=malloc(TMAX+2*P+8); HH=malloc(TMAX+2*P+8);
    uint64_t m0=0, m1=1ULL<<(N*N); if(argc>6){ m0=strtoull(argv[6],0,10); m1=m0+1; }
    for(uint64_t m=m0;m<m1;m++){
      for(int i=0;i<N*N;i++) g[IDX(i%N,i/N)]=(m>>i)&1;
      t=0; x=AX; y=AY; h=0; bx0=0; bx1=N-1; by0=0; by1=N-1; runlen=0; long tc=-1; int Dx=0,Dy=0;
      while(t<TMAX && x>-OFF+MARGE&&x<OFF-MARGE&&y>-OFF+MARGE&&y<OFF-MARGE){
        uint32_t c=IDX(x,y); uint8_t col=g[c]; HP[t]=c; HT[t]=col; HH[t]=(uint8_t)h;
        h=col?(h+3)&3:(h+1)&3; g[c]^=1; x+=dx[h]; y+=dy[h];
        if(x<bx0)bx0=x; if(x>bx1)bx1=x; if(y<by0)by0=y; if(y>by1)by1=y;
        if(t>=P){ if(HT[t]==HT[t-P]) runlen++; else runlen=0; } t++;
        if(runlen>=P){ uint32_t zc; if(certifie(t-2*P,&zc,&Dx,&Dy)==1){ tc=t-2*P; break; } } }
      printf("%llu %ld %d %d\n",(unsigned long long)m,tc,Dx,Dy);
      for(long u=0;u<t;u++) g[HP[u]]=0; for(int i=0;i<N*N;i++) g[IDX(i%N,i/N)]=0;
    }
    return 0;
  }
  return 1;
}
