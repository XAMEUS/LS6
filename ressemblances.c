#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <fcntl.h>
#include <sys/wait.h>

struct matrice{
  double **mat;
  char **fics;
  int nb_fic;
};

int liste_fichiers(char * path, char **fichiers, int nb_fic) 
{
  DIR * d;
  struct dirent *ent; 
  struct stat s;
  char * tmp;
  
  if(stat(path,&s)) exit(1) ;

  if(S_ISDIR(s.st_mode)){
    d=opendir(path);
    while((ent=readdir(d))!=NULL)
      if(strcmp(".",ent->d_name) && strcmp("..",ent->d_name)){
	tmp= malloc(sizeof(char)*(strlen(path)+strlen(ent->d_name)+2));
	sprintf(tmp,"%s/%s", path, ent->d_name);
        if ((!stat(tmp,&s)) && (S_ISDIR(s.st_mode)) ) 
	  nb_fic=liste_fichiers(tmp, fichiers, nb_fic);
	else
	  fichiers[nb_fic++] = tmp;
      }
    closedir(d);
  }
  return nb_fic;
}

void concat(char *fic1, char *fic2){
  int fd1 = open(fic1, O_RDONLY );
  int fd2 = open(fic2, O_RDONLY );
  int fd = open("temp", O_WRONLY | O_TRUNC  | O_CREAT, 0644);
  int lu;
  char buf[1024];
  while((lu = read(fd1, buf, 1024)))
    write(fd, buf, lu);
  while((lu = read(fd2, buf, 1024)))
    write(fd, buf, lu);
  close(fd1);
  close(fd2);
  close(fd);
}

int taille_zip(char *fichier, char * path, char *cmd, char *cmd_inv, char *ext){
  int f;
  struct stat s;
  char nom[1024];
  
  f = fork();
  if(f==0){
    execlp(cmd, cmd, fichier, NULL);
    printf("exec 1\n");
    exit(1);
  }
  wait(NULL);
  sprintf(nom,"%s.%s", fichier, ext);
  if(stat(nom,&s)) {printf("%s\n", fichier); perror("stat"); exit(1) ;}
  f = fork();
  if(f==0){
    execlp(cmd_inv, cmd_inv, fichier, NULL);
    printf("erreur exec\n");
    exit(1);
  }
  wait(NULL);
  return s.st_size;
}

struct matrice matrice(char **fichiers, int nb_fic, char * path, char *cmd, char *cmd_inv, char *ext){
  int i, j, f, t;
  double **m = malloc(nb_fic * sizeof(int *));
  int *tailles = calloc(nb_fic, sizeof(int));
  struct matrice sm;
  sm.nb_fic = nb_fic;

  for(i=0; i<nb_fic; i++){
    m[i] = malloc(nb_fic * sizeof(double));
    m[i][i] = -1;
  }
  for(i=0; i<nb_fic-1; i++){
    if(!tailles[i])
      tailles[i] = taille_zip(fichiers[i], path, cmd, cmd_inv, ext);
    for(j=i+1; j<nb_fic; j++){
      if(!tailles[j])
	tailles[j] = taille_zip(fichiers[j], path, cmd, cmd_inv, ext);
      concat(fichiers[i], fichiers[j]);
      t = taille_zip("temp", path, cmd, cmd_inv, ext);
      m[i][j] = fabs(tailles[i]+tailles[j]-t)/t;
      m[j][i] = m[i][j];
    }
  }
  free(tailles);
  sm.mat = m;
    
  return sm;
}

struct matrice matrice_proximite(char *path, char *cmd, char *cmd_inv, char *ext){
  char **fichiers = malloc(1000 *sizeof(char *));
  int i, nb_fic = liste_fichiers(path, fichiers, 0);
  struct matrice m = matrice(fichiers, nb_fic, path, cmd, cmd_inv, ext);

  m.fics = malloc(nb_fic * sizeof(char *));
  for(i=0; i<nb_fic; i++)
    m.fics[i] = fichiers[i];
  free(fichiers);
  return m;
}

void fichier_proximite(char *nom, char *path, char *cmd, char *cmd_inv, char *ext){
  char **fichiers = malloc(1000 *sizeof(char *));
  int nb_fic = liste_fichiers(path, fichiers, 0);
  struct matrice m = matrice(fichiers, nb_fic, path, cmd, cmd_inv, ext);
  int f = open(nom, O_WRONLY | O_TRUNC  | O_CREAT, 0644);
  int i, j;
  char buf[10000];

  for(i=0; i<nb_fic-1; i++){
    sprintf(buf, "%s\t", fichiers[i]);
    write(f, buf, strlen(buf));
  }
  sprintf(buf, "%s\n\n", fichiers[nb_fic-1]);
  write(f, buf, strlen(buf));
  
  for(i=0; i<nb_fic; i++){
    for(j=0; j<nb_fic-1; j++){
      sprintf(buf, "%f\t", m.mat[i][j]);
      write(f, buf, strlen(buf));
    }
    sprintf(buf, "%f\n", m.mat[i][nb_fic-1]);
    write(f, buf, strlen(buf));
  }
  close(f);
  for(i=0; i<nb_fic; i++)
    free(m.mat[i]);
  free(m.mat);
}

int main(){
  //struct matrice m = matrice_proximite("TestMessages", "gzip","gunzip", "gz");
  fichier_proximite("matrice_de_proximite.txt", "Messages", "gzip","gunzip", "gz");
  return 0;
}
