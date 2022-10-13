# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 01:00:32 2022

@author: anton
"""
from utils import Temps_Trajet, Dijkstra
from copy import deepcopy
import sys

### Code principal
def Fermeture_Route_Auto(Graph,Road):
    
    if Graph.Fermeture_Auto == True :
        
        Graph.Matrice_Poids = Graph.Crea_Matrice_Poids(Graph.G,Road.Liste_Route)
        Graph.Matrice_Etat = Graph.Crea_Matrice_Etat(Graph.G,Road.Liste_Route)
        
        n = len(Graph.Matrice_Poids)
        
        for i in range(n):
            for j in range(n):
                if Graph.Matrice_Poids[i,j] > Graph.Poids_Max:
                    Road.Liste_Route[i][j]['Etat'] = 0
                    Graph.Matrice_Etat[i][j] = Road.Liste_Route[i][j]['Etat']


def main(Graph,Road,Block,car,e):
    """
    Code principal qui assure l'évolution du circuit routier.
    """
    m=0
    nompasadequat=0
    
    #L=[]
    Fermeture_Route_Auto(Graph,Road)
    for k in range(len(Block.Liste_Bloc)):  # On va évaluer chaque bloc
        for i in range(len(Graph.G)):  
            for j in range(len(Graph.G)):
                
                if Block.Liste_Bloc[k][i][j] != {}:
                   
                    if k == e :
                        Block.Liste_Bloc[k][i][j]['Etat'] = 1
                        
                    if Block.Liste_Bloc[k][i][j]['Etat'] == 1:
                        
                        # Calcul de différentes Moyennes.
                        Block.Moy_Bloc = Block.Moy_Bloc + Temps_Trajet(Graph.Matrice_Poids, Block.Liste_Bloc[k][i][j])
                        m=m+1
                        
                        nompasadequat = nompasadequat + Block.Liste_Bloc[k][i][j]['Cardinal']
                        car.Moy_Vehi = car.Moy_Vehi + Temps_Trajet(Graph.Matrice_Poids, Block.Liste_Bloc[k][i][j]) * Block.Liste_Bloc[k][i][j]['Cardinal']
                        
                        
                        # On localise la route sur laquelle il se situe :
                        (u,v) = Block.Liste_Bloc[k][i][j]['Chemin'][Block.Liste_Bloc[k][i][j]['Route']]
                        
                        if Block.Liste_Bloc[k][i][j]['Position'] == 0:
                            if Road.Liste_Route[u][v]['Etat'] == 0:
                                
                                (a,b) = Block.Liste_Bloc[k][i][j]['Chemin'][-1]
                                Block.Liste_Bloc[k][i][j]['Chemin'] = Dijkstra(Graph.G,Road.Liste_Route,u,b)
                                Block.Liste_Bloc[k][i][j]['Route'] = 0
                                (u,v) = Block.Liste_Bloc[k][i][j]['Chemin'][Block.Liste_Bloc[k][i][j]['Route']]
                            if Block.Liste_Bloc[k][i][j]['Cardinal']+Road.Liste_Route[u][v]['Flux'][0]+Road.Liste_Route[u][v]['Flux'][1]+Road.Liste_Route[u][v]['Flux'][2]+Road.Liste_Route[u][v]['Flux'][3]>Road.Liste_Route[u][v]['Capacité']*Road.Liste_Route[u][v]['Coefficient']:
                                Block.Liste_Bloc[k][i][j]['Etat']=0
                                Graph.Files_Attente[u][v].append(Block.Liste_Bloc[k][i][j])
                            else:
                                Block.Liste_Bloc[k][i][j]['Vitesse'] = Road.Liste_Route[u][v]['Longueur']/Road.Liste_Route[u][v]['Poids']
                            
                                Road.Liste_Route[u][v]['Cardinal'] = Road.Liste_Route[u][v]['Cardinal'] + Block.Liste_Bloc[k][i][j]['Cardinal']
                                Road.Liste_Route[u][v]['Flux'][0]= Road.Liste_Route[u][v]['Flux'][0] + Block.Liste_Bloc[k][i][j]['Cardinal']
                            
                            
                            
                            
                        
                        # S'étant déplacé pendant l'itération antérieure, on identifie sa nouvelle position :
                   
                        Block.Liste_Bloc[k][i][j]['Position'] = Block.Liste_Bloc[k][i][j]['Position'] + (Block.Liste_Bloc[k][i][j]['Vitesse'] / Road.Liste_Route[u][v]['Longueur'])*(24/Graph.t)
                
                        
                        
                        if Block.Liste_Bloc[k][i][j]['Position'] >= 1: # Si sa position est plus grande que 1, il est arrivé sur la prochaine route :
                    
                            """ On retire sa population de la pop de l'ancienne route """
                            Road.Liste_Route[u][v]['Cardinal'] = Road.Liste_Route[u][v]['Cardinal'] - Block.Liste_Bloc[k][i][j]['Cardinal']
                           
                        
                            if Block.Liste_Bloc[k][i][j]['Route'] < len(Block.Liste_Bloc[k][i][j]['Chemin']) - 1: # Si il reste du chemin :
                            
                                """ L'indice de la route sur laquelle il est est itéré de 1 """
                                Block.Liste_Bloc[k][i][j]['Route'] = Block.Liste_Bloc[k][i][j]['Route'] + 1
                                Block.Liste_Bloc[k][i][j]['Position'] = 0
                            

                            else: 
                            # Si c'était sa dernière route, alors le bloc est arrivé à destination, on le désactive :
                                Block.Liste_Bloc[k][i][j]['Etat'] = 0
            
    
    Block.Moy_Bloc = Block.Moy_Bloc / m
    car.Moy_Vehi = car.Moy_Vehi / nompasadequat

    for u in range(0,len(Road.Liste_Route)):
        for v in range(0,len(Road.Liste_Route)):
            if Road.Liste_Route[u][v]!= {}:                 
                o=Road.Liste_Route[u][v]['Prop sat']
                q=Road.Liste_Route[u][v]['Capacité']
                r=Road.Liste_Route[u][v]['Sensibilité']
                p=Road.Liste_Route[u][v]['Flux'][3]+Road.Liste_Route[u][v]['Flux'][2]+Road.Liste_Route[u][v]['Flux'][1]+Road.Liste_Route[u][v]['Flux'][0]
                Road.Liste_Route[u][v]['Poids'] = Road.Liste_Route[u][v]['Longueur']*(1/Road.Liste_Route[u][v]['Vitesse max'])*(1+o*(p/q)**r)
                Road.Liste_Route[u][v]['Flux'][3]=Road.Liste_Route[u][v]['Flux'][2]                            
                Road.Liste_Route[u][v]['Flux'][2]=Road.Liste_Route[u][v]['Flux'][1]
                Road.Liste_Route[u][v]['Flux'][1]=Road.Liste_Route[u][v]['Flux'][0] 
                Road.Liste_Route[u][v]['Flux'][0]=0
                h=deepcopy(len(Graph.Files_Attente[u][v]))
                for r in range(h):
                    if Graph.Files_Attente[u][v][r]['Cardinal']+Road.Liste_Route[u][v]['Flux'][0]+Road.Liste_Route[u][v]['Flux'][1]+Road.Liste_Route[u][v]['Flux'][2]+Road.Liste_Route[u][v]['Flux'][3]<=Road.Liste_Route[u][v]['Capacité']*Road.Liste_Route[u][v]['Coefficient']:
                            w=Graph.Files_Attente[u][v][r]['Identifiant'][0]
                            x=Graph.Files_Attente[u][v][r]['Identifiant'][1]
                            c=Graph.Files_Attente[u][v][r]['Identifiant'][2]
                            Block.Liste_Bloc[w][x][c]['Vitesse'] = Road.Liste_Route[u][v]['Longueur']/Road.Liste_Route[u][v]['Poids']
                            Road.Liste_Route[u][v]['Cardinal'] = Road.Liste_Route[u][v]['Cardinal']+Graph.Files_Attente[u][v][r]['Cardinal']
                            Graph.Matrice_Cardinal[u,v]=Graph.Matrice_Cardinal[u,v]+Graph.Files_Attente[u][v][r]['Cardinal']
                            Road.Liste_Route[u][v]['Flux'][0]=Road.Liste_Route[u][v]['Flux'][0]+Graph.Files_Attente[u][v][r]['Cardinal']
                            Block.Liste_Bloc[w][x][c]['Position'] = (Graph.Files_Attente[u][v][r]['Vitesse'] / Road.Liste_Route[u][v]['Longueur'])*(24/Graph.t)
                            Block.Liste_Bloc[w][x][c]['Etat'] = 1
                            Graph.Files_Attente[u][v][r]=0
                                
                                
                    else:
                        break
                Graph.Files_Attente[u][v]=[i for i in Graph.Files_Attente[u][v] if i !=0]
   