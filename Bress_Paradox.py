####  LE PARADOXE DE BRAESS ET SES APPLICATIONS  ####

### Introduction :

#============================================================================#
#----------------------------------------------------------------------------#
#                                   TIPE                                     #
#----------------------------------------------------------------------------#
#                               Antony Davi                                  #
#                      Guillaume Gautier de La Plaine                        #
#                              Roman Rousseau                                #
#                                                                            #
#----------------------------------------------------------------------------#
#                              VERSION 11.0                                  #
#                                                                            #
# o Version la plus aboutie en terme d'exécution pure.                       #
#                                                                            #
# o Toute la simulation ainsi que l'affichage d'une interface Homme/Machine  #
#   fonctionnent correctement.                                               #
#                                                                            #
# o Les valeurs sont pour la plupart choisies de manière aléatoire.          #
#                                                                            #
# o Les seules variables à modifier sont celles dans les deux avant-dernières# 
#   cellules, "Paramètres d'affichage" et "Paramètres de simulation". A voir.#
#                                                                            #
# o Remasterisée sous forme de classe par Antony Davi                        #
#                                                                            #
#----------------------------------------------------------------------------#
#============================================================================#


"""
Par soucis de clarté, les noms des variables (discrètes et globales) sont homogénéisées dans toutes les fonctions.

n                   : Taille du graphe;
Graph.p                   : Proportion de routes inexistantes;
Graph.G                   : Matrice d'adjacence du graphe;
Graph.t                   : Nombre maximal d'itérations;
Graph.Poids_Max           : Poids maximum pour la fermeture automatique si activée;
Graph.Fermeture_Auto      : Active ou non la fermeture automatique;
Graph.Ouverture_Auto      : Active ou non l' ouverture automatique;

City.Liste_Ville*        : Liste des influences des villes, pour une répartition spatiale du traffic;
Rep_Temps*          : Liste de la répartition temporelle du traffic;

Road.Liste_Route*        : Liste des informations sur chaque route;
Epaisseur_Min       : Epaisseur minimale d'une route;
Epaisseur_Max       : Epaisseur maximale d'une route;
(u,v)               : Couple (depart, arrivée) identifiant une route;
Longueur_Min        : Longueur minimale d'une route;
Longueur_Max        : Longueur maximale d'une route;

Block.Liste_Bloc*         : Listge des informations sur chaque bloc de véhicules;
Card_Min            : Cardinal minimum de chaque bloc;
Card_Max            : Cardinal maximum de chaque bloc;
Graph.Matrice_Poids*      : Matrice d'adjacence du graphe, contenant les poids de chaque route;
Graph.Matrice_Cardinal*   : Matrice d'adjacence du graphe, contenant le nombre de personnes sur chaque route;
Graph.Matrice_Etat*       : Matrice d'adjacence du graphe, contenant l'état de chaque route, ouverte ou fermée;
Graph.Matrice_Longueur*   : Matrice d'adjacence du graphe, contenant la longueur de chaque route;

Liste_Moyennes*     : Liste des moyennes des poids sur une simulation.

* : Variables écrasées puis renouvelées à chaque simulation.
"""


### Modules utilisés :

import math
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import networkx as nx
import time

from mpl_toolkits.mplot3d import Axes3D
from tkinter import * 
from copy import deepcopy

#Import 

#utils
from utils import *

#graph_tools
from graph_tools import graph

#road_tools
from road_tools import road
#car tools
from car_tools import car
#city_tools
from city_tools import city
#block_tools
from block_tools import block
#tkinter_tools
from tkinter_tools import *
#core
from main import main

    
def Afficher(Graph):
    """
    Fonction d'affichage de la matrice des poids ; 1 élément = 1 case
    """
    tailleH=(Rapport-5)//(len(Graph.Matrice_Poids)+1)
    tailleV=(Hauteur-5)//(len(Graph.Matrice_Poids)+1)
    mat.delete(ALL)
    
    for i in range(len(Graph.Matrice_Poids)+1):
        for j in range(len(Graph.Matrice_Poids)+1):
            if i==0:
                mat.create_rectangle(j*tailleH, i*tailleV, j*tailleH+tailleH, i*tailleV+tailleV, width=1)
                mat.create_text( (2*j*tailleH+tailleH)/2, (i*tailleV+tailleV)/2, text=str(j-1) , width= tailleH-2)
            if j==0:
                mat.create_rectangle(j*tailleH, i*tailleV, j*tailleH+tailleH, i*tailleV+tailleV, width=1)
                mat.create_text( (2*j*tailleH+tailleH)/2, (2*i*tailleV+tailleV)/2, text=str(i-1) , width= tailleH-2)
            if i!= 0 and j!=0 :
                if Road.Liste_Route[i-1][j-1]!={}:
                    mat.create_rectangle(j*tailleH, i*tailleV, j*tailleH+tailleH, i*tailleV+tailleV, width=1, fill=Couleurs[Conversion(int(Graph.Matrice_Poids[i-1,j-1]/(Road.Liste_Route[i-1][j-1]['Longueur']/Road.Liste_Route[i-1][j-1]['Vitesse max'])*100))])
                mat.create_text( (2*j*tailleH+tailleH)/2, (2*i*tailleV+tailleV)/2, text=str(int(Graph.Matrice_Poids[i-1,j-1]))+ 'h'+str(int((Graph.Matrice_Poids[i-1,j-1]-int(Graph.Matrice_Poids[i-1,j-1]))*60)) , width= tailleH-2, fill='blue')
                if Road.Liste_Route[i-1][j-1]=={}:
                    mat.create_rectangle(j*tailleH, i*tailleV, j*tailleH+tailleH, i*tailleV+tailleV, width=1, fill=Couleurs[ Conversion(int(Graph.Matrice_Poids[i-1,j-1])) ]) 
                    mat.create_text( (2*j*tailleH+tailleH)/2, (2*i*tailleV+tailleV)/2, text=str((Graph.Matrice_Poids[i-1,j-1])) , width= tailleH-2, fill='blue')



def Afficher_Graphe():
    """
    Affiche le graphe avec le module NetworkX.
    """
    labels={}
    h=Graph.Matrice_Etat.shape
    Graphe_Aff = nx.DiGraph(Graph.Matrice_Etat)
    L=[] # liste contenant les arcs qui où il  y aura des flèches
    M=[] # liste contenant les arcs sans flèche
    for i in range(0,h[0]) :
        for j in range(0,h[1]):
            if (Graph.Matrice_Etat[i,j]!=0 and Graph.Matrice_Etat[j,i]==0) :
                L.append((i,j))
            if (Graph.Matrice_Etat[i,j] !=0 and Graph.Matrice_Etat[j,i]!=0): 
                M.append((i,j))
        labels[i]=i
    pos=nx.circular_layout(Graphe_Aff) # disposition circulaire 
          

    plt.clf()
    nx.draw_networkx_edges(Graphe_Aff,pos,edgelist=L,width=0,edge_color='b',alpha=0.5,arrowstyle='simple',arrowsize=25)
    nx.draw_networkx_edges(Graphe_Aff,pos,edgelist=M,width=5,edge_color='#0CE0C4',alpha=0.5,arrows=False) #couleur bleu claire


    nx.draw_networkx_nodes(Graphe_Aff,pos, node_size=500, node_color='r', node_shape='o', alpha=1.0)
    nx.draw_networkx_labels(Graphe_Aff, pos, labels, font_size=10,font_color='k',alpha=1)
    # on dessine , les traits bleu claire correspondant a des routes à double sens , en bleu foncé ce sont des routes orientées.


def Iteration():
    """
    Permet d'itérer par le bouton le code principal et d'afficher les listes des routes et des blocs à chaque étape
    """
    global J 
    global e
    global d 
    global Q2
    global Graph
    global Block
    global Car
    
    if Q2 == 1:
        
        main(Graph,Road,Block,car,e)
        e = e+1
        Graph.Matrice_Poids = Graph.Crea_Matrice_Poids(Graph.G,Road.Liste_Route)
        Afficher(Graph)
        Graph.Matrice_Cardinal = Graph.Crea_Matrice_Cardinal(Graph.G,Road.Liste_Route)
        Graph.Matrice_Etat = Graph.Crea_Matrice_Etat(Graph.G,Road.Liste_Route)
        
        print()
        print()
        
        print("Etape ", e)       
        
        print("Jour", d, ", ", int(((e-1)-Graph.t*(d-1))//(Graph.t/24)), "h", int(((e-1)-Graph.t*(d-1))%(Graph.t/24)*60/(Graph.t/24)))
        print()
        print()
        
        print("-------------")
        print("Moyenne des poids des routes : ")
        Liste_Files_Attente_Route_1_0.append(len(Graph.Files_Attente[1][0]))
        Liste_Files_Attente_Route_1_2.append(len(Graph.Files_Attente[1][2]))
        Liste_Files_Attente_Route_1_3.append(len(Graph.Files_Attente[1][3]))
        Liste_Files_Attente_Route_1_4.append(len(Graph.Files_Attente[1][4]))
        Liste_Files_Attente_Route_1_5.append(len(Graph.Files_Attente[1][5]))
        Liste_Files_Attente_Route_2_0.append(len(Graph.Files_Attente[2][0]))
        Liste_Files_Attente_Route_2_1.append(len(Graph.Files_Attente[2][1]))
        Liste_Files_Attente_Route_2_3.append(len(Graph.Files_Attente[2][3]))


        
        Graph.Liste_Moyennes_Graphe.append(Moyenne_Poids_Divergente(Graph.Matrice_Poids))
        Graph.Moy_Jour = Graph.Moy_Jour + Moyenne_Poids_Divergente(Graph.Matrice_Poids)
        a=Moyenne_Poids_Divergente(Graph.Matrice_Poids)
        print( str(int(a)) +'h'+ str( int((a-int(a))*60) ))
        print()
        
        print("-------------")
        print("Moyenne des temps de trajet des Blocs : ")
        Block.Liste_Moyennes_Blocs.append(Block.Moy_Bloc)
        print(str(int(Block.Moy_Bloc)) +'h'+ str( int((Block.Moy_Bloc-int(Block.Moy_Bloc))*60) ))
        print()
        
        print("-------------")
        print("Moyenne des temps de trajet des Véhicules : ")
        Car.Liste_Moyennes_Vehicules.append(Car.Moy_Vehi)
        print(str(int(Car.Moy_Vehi)) +'h'+ str( int((Car.Moy_Vehi-int(Car.Moy_Vehi))*60) ))
        print()
        f=0
        for u in range(0,len(Graph.G)):
            for v in range(0,len(Graph.G)):
                if Road.Liste_Route[u][v] != {}:
                    f+=Road.Liste_Route[u][v]['Cardinal']
        Liste_Population.append(f)
        
        Liste_Route_Flux_1_0.append(Road.Liste_Route[1][0]['Flux'][0]+Road.Liste_Route[1][0]['Flux'][1]+Road.Liste_Route[1][0]['Flux'][2]+Road.Liste_Route[1][0]['Flux'][3])
        
        Liste_Route_Cardinal_1_0.append(Road.Liste_Route[1][0]['Cardinal'])
        Vitesse_Moyenne_Route_1_0.append(Road.Liste_Route[1][0]['Longueur']/Road.Liste_Route[1][0]['Poids'])
        Liste_Route_Poids_1_0.append(Road.Liste_Route[1][0]['Poids'])
        Liste_Route_Flux_1_2.append(Road.Liste_Route[1][2]['Flux'][0]+Road.Liste_Route[1][2]['Flux'][1]+Road.Liste_Route[1][2]['Flux'][2]+Road.Liste_Route[1][2]['Flux'][3])
        
        Liste_Route_Cardinal_1_2.append(Road.Liste_Route[1][2]['Cardinal'])
        Vitesse_Moyenne_Route_1_2.append(Road.Liste_Route[1][2]['Longueur']/Road.Liste_Route[1][2]['Poids'])
        Liste_Route_Poids_1_2.append(Road.Liste_Route[1][2]['Poids'])
        Liste_Route_Flux_1_3.append(Road.Liste_Route[1][3]['Flux'][0]+Road.Liste_Route[1][3]['Flux'][1]+Road.Liste_Route[1][3]['Flux'][2]+Road.Liste_Route[1][3]['Flux'][3])
        
        Liste_Route_Cardinal_1_3.append(Road.Liste_Route[1][3]['Cardinal'])
        Vitesse_Moyenne_Route_1_3.append(Road.Liste_Route[1][3]['Longueur']/Road.Liste_Route[1][3]['Poids'])
        Liste_Route_Poids_1_3.append(Road.Liste_Route[1][3]['Poids'])
        Liste_Route_Flux_1_4.append(Road.Liste_Route[1][4]['Flux'][0]+Road.Liste_Route[1][4]['Flux'][1]+Road.Liste_Route[1][4]['Flux'][2]+Road.Liste_Route[1][4]['Flux'][3])
        
        Liste_Route_Cardinal_1_4.append(Road.Liste_Route[1][4]['Cardinal'])
        Vitesse_Moyenne_Route_1_4.append(Road.Liste_Route[1][4]['Longueur']/Road.Liste_Route[1][4]['Poids'])
        Liste_Route_Poids_1_4.append(Road.Liste_Route[1][4]['Poids'])
        Liste_Route_Flux_1_5.append(Road.Liste_Route[1][5]['Flux'][0]+Road.Liste_Route[1][5]['Flux'][1]+Road.Liste_Route[1][5]['Flux'][2]+Road.Liste_Route[1][5]['Flux'][3])
        
        Liste_Route_Cardinal_1_5.append(Road.Liste_Route[1][5]['Cardinal'])
        Vitesse_Moyenne_Route_1_5.append(Road.Liste_Route[1][5]['Longueur']/Road.Liste_Route[1][5]['Poids'])
        Liste_Route_Poids_1_5.append(Road.Liste_Route[1][5]['Poids'])
        Liste_Route_Flux_2_0.append(Road.Liste_Route[2][0]['Flux'][0]+Road.Liste_Route[2][0]['Flux'][1]+Road.Liste_Route[2][0]['Flux'][2]+Road.Liste_Route[2][0]['Flux'][3])
        
        Liste_Route_Cardinal_2_0.append(Road.Liste_Route[2][0]['Cardinal'])
        Vitesse_Moyenne_Route_2_0.append(Road.Liste_Route[2][0]['Longueur']/Road.Liste_Route[2][0]['Poids'])
        Liste_Route_Poids_2_0.append(Road.Liste_Route[2][0]['Poids'])
        Liste_Route_Flux_2_1.append(Road.Liste_Route[2][1]['Flux'][0]+Road.Liste_Route[2][1]['Flux'][1]+Road.Liste_Route[2][1]['Flux'][2]+Road.Liste_Route[2][1]['Flux'][3])
        
        Liste_Route_Cardinal_2_1.append(Road.Liste_Route[2][1]['Cardinal'])
        Vitesse_Moyenne_Route_2_1.append(Road.Liste_Route[2][1]['Longueur']/Road.Liste_Route[2][1]['Poids'])
        Liste_Route_Poids_2_1.append(Road.Liste_Route[2][1]['Poids'])
        Liste_Route_Flux_2_3.append(Road.Liste_Route[2][3]['Flux'][0]+Road.Liste_Route[2][3]['Flux'][1]+Road.Liste_Route[2][3]['Flux'][2]+Road.Liste_Route[2][3]['Flux'][3])
        
        Liste_Route_Cardinal_2_3.append(Road.Liste_Route[2][3]['Cardinal'])
        Vitesse_Moyenne_Route_2_3.append(Road.Liste_Route[2][3]['Longueur']/Road.Liste_Route[2][3]['Poids'])
        Liste_Route_Poids_2_3.append(Road.Liste_Route[2][3]['Poids'])
        print()
        print()
        print("Fin de l'étape ", e)
        print()
        print()
        print()
        print()
    
    if e/d == Graph.t:
        print()
        print()
        print("Exécution terminée.")
        print()
        Graph.Moy_Jour = Graph.Moy_Jour/Graph.t
        Liste_Moyenne_Poids_Route.append(Graph.Moy_Jour)

        print("Moyenne des poids sur la journée complète :", Graph.Moy_Jour)
        Graph.Moy_Jour = 0
       
        d = d+1
        Prolongement_Liste_Bloc(Graph.G,Road.Liste_Route,Block.Liste_Bloc,Graph.t)
   

def Iteration_Auto():

    global Graph
    global Road
    global e
    global d
    while e/max((d-1),1) !=Graph.t :
       # time.sleep(Graph.Temps_Pause)
        Iteration()
        Graph.Matrice_Poids=Graph.Crea_Matrice_Poids(Graph.G,Road.Liste_Route)
        Afficher(Graph)
    
    if Q2=="non" or Q2=="Non":
        return None

def Afficher_Moyennes():
    
    global Graph
    global Block
    global Car
    X0=[i for i in range(len(Graph.Liste_Moyennes_Graphe))]
    X1=[i for i in range(len(Block.Liste_Moyennes_Blocs))]
    X2=[i for i in range(len(Car.Liste_Moyennes_Vehicules))]
    plt.plot(X0,Graph.Liste_Moyennes_Graphe,'-b', label="Moyenne Graphe")
    plt.plot(X1,Block.Liste_Moyennes_Blocs,'-r', label="Moyenne Blocs")
    plt.plot(X2,Car.Liste_Moyennes_Vehicules,'-g', label="Moyenne Véhicules")
    plt.xlabel("Etapes (de 15 minutes)")
    plt.ylabel("Temps en Heure")
    plt.legend()


def Afficher_Courbes():
    """
    Affichages des differentes courbes nécessaires à la compréhension de la circulation
    Passer par matplotlib pour les afficher correctement :
        Sur spyder : Préférence -> IPython_Console -> Graphics -> Automatic

    Returns
    -------
    None.

    """
    global e 
    global Graph
    global d
    
    print(d)
    if (d<2) :
        return print("Veuillez terminer une journée complète ")
    if (e/(d-1) == Graph.t):
        plt.clf()
        T = [i for i in range(0,Graph.t)]
       
        H=[]
        for i in range(0,len(Liste_Moyenne_Poids_Route)):
            H=H +Graph.t*[Liste_Moyenne_Poids_Route[i]]
        X4= [(15*i)/60 for i in range(0,len(Liste_Route_Flux_1_0))]
        Limite_1_0=[Road.Liste_Route[1][0]['Capacité']]*len(X4)
        LimiteTemps_1_0=len(X4)*[Road.Liste_Route[1][0]['Longueur']/Road.Liste_Route[1][0]['Vitesse max']]
        plt.subplot(221)
        plt.plot(X4,Liste_Route_Flux_1_0, "g-", label="Flux(1,0)")
        plt.plot(X4,Liste_Route_Cardinal_1_0, "g-", label="Population(1,0)",linewidth=4)
        plt.plot(X4,Liste_Route_Flux_1_2, "b-", label="Flux(1,2)")
        plt.plot(X4,Liste_Route_Cardinal_1_2, "b-", label="Population(1,2)",linewidth=4)
     
        plt.plot(X4,Limite_1_0,"r--",label="Capacité de (1,0)")
        plt.title("Flux et population sur une route en fonction du temps")
        plt.xlabel("temps en heure ")
        plt.ylabel("en individu")
        plt.legend()
        plt.subplot(223)
        LimiteVitesse_1_0=[Road.Liste_Route[1][0]['Vitesse max']]*len(X4)
        plt.plot(X4,Vitesse_Moyenne_Route_1_0,"g-",label="Vitesse (1,0)")
        plt.plot(X4,LimiteVitesse_1_0,"g--",label="Vitesse max (1,0)")
        plt.plot(X4,Vitesse_Moyenne_Route_1_2,"b-",label="Vitesse(1,2)")
       
        plt.title("Vitesse du véhicule")
        plt.ylim(0, 140);
        plt.legend()
        plt.subplot(322)
        plt.plot(X4,Liste_Route_Poids_1_0,"g-",label="Temps(1,0)")
        plt.plot(X4,Liste_Route_Poids_1_2,"b-",label="Temps(1,2)")
       
    
        plt.plot(X4,LimiteTemps_1_0,"r--",label="Temps optimal(1,0)")
        plt.ylim(0,maxListe(Liste_Route_Poids_1_0+H+Liste_Route_Poids_1_2+Liste_Route_Poids_1_3+Liste_Route_Poids_1_4+Liste_Route_Poids_1_5+Liste_Route_Poids_2_1+Liste_Route_Poids_2_3))
        plt.plot(X4,H,"b--",label="Moyenne sur une journée")
        plt.title("Temps de trajet en fonction du temps")
        plt.legend()
        plt.subplot(324)
        plt.plot(X4,Liste_Files_Attente_Route_1_0,"g:o",label="Nombre de bloc (1,0) ")
        plt.plot(X4,Liste_Files_Attente_Route_1_2,"b:o",label="Nombre de bloc (1,2) ")
       
        plt.legend()
        plt.title("Nombre de bloc dans la file en fonction du temps")
        plt.subplot(326)
        plt.plot(X4,Liste_Population,"b-",label="Nombre de personnes ")
        plt.legend()
        plt.title("Nombre de personnes sur le graphe")
      
        plt.show()
    else : print("Veuillez terminer une journée complète ")
    
def Ouverture_Route_Manuelle():
    """
    Fonction d'ouverture manuelle de route, sur l'IHM.
    """
    i = depart.get()
    j = arrivee.get()
    print()
    print()
    print("Ouverture de la route de", i, "vers", j)
    print()
    print()
    
    Road.Liste_Route[i][j]['Etat'] = 0
    Graph.Matrice_Etat[i][j] = Road.Liste_Route[i][j]['Etat']
    
    


def Fermeture_Route_Manuelle():
    """
    Fonction de fermeture manuelle de route, sur l'IHM.
    """
    i = depart.get()
    j = arrivee.get()
    if Road.Liste_Route[i][j]=={}:
        print('Impossible, cette route est inexistante')
    else:
        print()
        print()
        print("Fermeture de la route de", i, "vers", j)
        print()
        print()
    
        Road.Liste_Route[i][j]['Etat'] = 0
        Graph.Matrice_Etat[i][j] = Road.Liste_Route[i][j]['Etat']

    



##### Paramètres d'affichage
"""
Ceci est une des deux seules zones à modifier par l'utilisateur, en fonction des paramètres qu'il souhaite.
"""

# Dimensions, pour modifier la taille de l'afficheur.
Longueur = 950
Hauteur = 695
Rapport = (Longueur-300)    # NE PAS MODIFIER


# Autres matrices
GA = np.array([[0,3,0,5,0,1],[3,0,25,0,4,0],[0,2,0,0,4,12],[5,0,0,0,2,7],[0,3,7,11,0,0],[5,0,9,8,0,0]]) # Graphe utilisé

GA1 = np.array([[0,1,1,1,0,1],[1,0,1 ,1,1,1],[1,1,0,1,0,0 ],[1,1,1,0,1,1],[0,1,0,1 ,0,0],[1,1,0,1,0,0]])

GB = np.array([[0,0,0,1,0,0],[1,0,0,0,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[0,1,0,0,0,0],[0,0,1,0,0,0]]) # Non sym

GC = np.array([[0,1,0,3,0,0],[0,0,0,25,1,0],[0,0,0,0,0,1],[0,0,2,0,0,0],[0,0,0,0,0,1],[0,0,0,0,0,0]]) # Non sym + pt isolé

GD = np.array([[0,1,0],[1,0,1],[1,0,1]]) # Petit + non sym + boucle

GE = np.array([[2,4,4,6,3,7],[8,6,3,9,2,1],[5,7,9,8,5,2],[1,4,7,8,5,9],[7,6,4,2,1,6],[2,5,8,2,6,4]]) # f-connexe + boucles
GE1 = np.ones([6,6])
GE2 = np.array([[0,4,4,6,3,7],[8,0,3,9,2,1],[5,7,0,8,5,2],[1,4,7,0,5,9],[7,6,4,2,0,6],[2,5,8,2,6,0]]) # E sans boucles

GF = np.array([[0,1,1,1,0,0],[1,0,0,0,0,0],[1,0,0,0,1,0],[1,0,0,0,0,1],[0,0,1,0,0,0],[0,0,0,1,0,0]]) # Arbre
GF2 = np.array([[0,1,1,0,0,0],[1,0,0,1,1,0],[1,0,0,0,0,1],[0,1,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0]]) #Tas

GH = np.array([[0,1,0,1,0,0],[0,0,1,0,1,0],[0,0,0,0,0,1],[0,0,1,0,1,0],[0,0,0,0,0,1],[0,0,0,0,0,0]]) # Sommet isolé
GH2 = np.array([[0,1,0,1,0,0,0,0],[0,0,1,0,1,0,0,0],[0,0,0,0,0,0,1,1],[0,0,1,0,1,0,0,0],[0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0]]) # Graph.G + deux sommets

GK = np.array([[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,0,0,0,0]]) # "fil"
GK3 = np.array([[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[1,0,0,0,0,0]]) # "cercle"

GM = np.array([[0,0,1,0],[0,0,1,1],[1,1,0,1],[0,1,1,0]])

GZ = np.zeros((15,15))
"""
G10=np.array([ 0.,  1.,  1.,  1.,  0.,  1.,  1.,  1.,  1.,  0.],
       [ 1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
       [ 1.,  1.,  0.,  1.,  0.,  0.,  1.,  0.,  0.,  0.],
       [ 1.,  1.,  1.,  0.,  0.,  1.,  0.,  0.,  0.,  1.],
       [ 0.,  1.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.],
       [ 1.,  1.,  0.,  1.,  0.,  0.,  0.,  0.,  1.,  0.],
       [ 1.,  1.,  1.,  0.,  1.,  0.,  0.,  1.,  1.,  0.],
       [ 1.,  1.,  0.,  0.,  1.,  0.,  1.,  0.,  0.,  1.],
       [ 1.,  1.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
       [ 0.,  1.,  0.,  1.,  0.,  0.,  0.,  1.,  0.,  0.]])
"""
# Couleurs. L'utilisateur peut modifier cette liste à ses risques et Graph.périls.
"""
SI MODIFICATION: Tant que le nombre de couleurs dans cette liste reste le Graph.même, pas de poblème d'exécution. Si le nombre de couleurs change, modifier adéquatement la fonction 'Conversion'
"""
Couleurs = ['grey1', 'grey2', 'grey3', 'grey4', 'grey5', 'grey6', 'grey7', 'grey8', 'grey9', 'grey10', 'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19', 'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28', 'grey29', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37', 'grey38', 'grey39', 'grey40', 'grey41', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47', 'grey48', 'grey49', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56', 'grey57', 'grey58', 'grey59', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65', 'grey66', 'grey67', 'grey68', 'grey69', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74', 'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey80', 'grey81', 'grey82', 'grey83', 'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey90', 'grey91', 'grey92', 'grey93', 'grey94', 'grey95', 'grey96', 'grey97', 'grey98', 'grey99']
Couleurs.reverse()


##### Paramètres de simulation :


x = 0
y = 0


## Script IHM

#Q1 = input("Démarrer ? ")
Q1="oui"
if Q1 == "Oui" or Q1 == "oui" or Q1 == "OUI":
    e = 0  # Indice de l'étape
    d = 1  # Indice de la journée
    Q2 = 1
    print()
    print("Initialisation")
    print()
    print("Graphe :")
    print()
   
    Liste_Population                =[] #pour les plot
    Liste_Moyenne_Poids_Route             = []
    Liste_Moyenne_Poids_1_0         = []  # Pour les plot
    Liste_Route_Flux_1_0           = []  # Pour les plot
    Liste_Route_Cardinal_1_0        = []  # Pour les plot
    Liste_Route_Poids_1_0           = []  # Pour les plot
    Vitesse_Moyenne_Route_1_0       = []  # Pour les plot
    Liste_Files_Attente_Route_1_0   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_1_0   = []  #Pour les plot
    Liste_Moyenne_Poids_1_2         = []  # Pour les plot
    Liste_Route_Flux_1_2           = []  # Pour les plot
    Liste_Route_Cardinal_1_2        = []  # Pour les plot
    Liste_Route_Poids_1_2           = []  # Pour les plot
    Vitesse_Moyenne_Route_1_2       = []  # Pour les plot
    Liste_Files_Attente_Route_1_2   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_1_2   = []  #Pour les plot
    Liste_Route_Flux_1_3           = []  # Pour les plot
    Liste_Route_Cardinal_1_3        = []  # Pour les plot
    Liste_Route_Poids_1_3           = []  # Pour les plot
    Vitesse_Moyenne_Route_1_3       = []  # Pour les plot
    Liste_Files_Attente_Route_1_3   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_1_3   = []  #Pour les plot
    Liste_Route_Flux_1_4           = []  # Pour les plot
    Liste_Route_Cardinal_1_4        = []  # Pour les plot
    Liste_Route_Poids_1_4           = []  # Pour les plot
    Vitesse_Moyenne_Route_1_4       = []  # Pour les plot
    Liste_Files_Attente_Route_1_4   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_1_4   = []  #Pour les plot
    Liste_Route_Flux_1_5           = []  # Pour les plot
    Liste_Route_Cardinal_1_5        = []  # Pour les plot
    Liste_Route_Poids_1_5           = []  # Pour les plot
    Vitesse_Moyenne_Route_1_5       = []  # Pour les plot
    Liste_Files_Attente_Route_1_5   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_1_5   = []  #Pour les plot
    Liste_Route_Flux_1_5           = []  # Pour les plot
    Liste_Route_Cardinal_1_5        = []  # Pour les plot
    Liste_Route_Poids_1_5           = []  # Pour les plot
    Vitesse_Moyenne_Route_1_5       = []  # Pour les plot
    Liste_Files_Attente_Route_1_5   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_1_5   = []  #Pour les plot
    Liste_Route_Flux_2_0           = []  # Pour les plot
    Liste_Route_Cardinal_2_0        = []  # Pour les plot
    Liste_Route_Poids_2_0           = []  # Pour les plot
    Vitesse_Moyenne_Route_2_0       = []  # Pour les plot
    Liste_Files_Attente_Route_2_0   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_2_0   = []  #Pour les plot
    Liste_Route_Flux_2_1           = []  # Pour les plot
    Liste_Route_Cardinal_2_1        = []  # Pour les plot
    Liste_Route_Poids_2_1           = []  # Pour les plot
    Vitesse_Moyenne_Route_2_1       = []  # Pour les plot
    Liste_Files_Attente_Route_2_1   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_2_1   = []  #Pour les plot
    Liste_Moyenne_Poids_2_3         = []  # Pour les plot
    Liste_Route_Flux_2_3           = []  # Pour les plot
    Liste_Route_Cardinal_2_3        = []  # Pour les plot
    Liste_Route_Poids_2_3           = []  # Pour les plot
    Vitesse_Moyenne_Route_2_3       = []  # Pour les plot
    Liste_Files_Attente_Route_2_3   = []  #Pour les plot
    Liste_Moyenne_Poids_Route_2_3   = []  #Pour les plot
    

    
    #Definition des objets
    Graph = graph(GA1) #Si GA1 n'est pas renseigné , création d'une matrice automatiquement. Les plots ne fonctionneront pas forcément car les routes peuvent ne pas exister.
    print(Graph.G)
    Car = car()
    City = city(Graph.G)
    Road = road(Graph.G)
    Block = block(Graph.G,Road.Liste_Route,Graph.t)
    n= Graph.n


    for k in range(0,96):
        for i in range(0, len(Graph.G)):
            for j in range(0,len(Graph.G)):
                if i!=j :
                    Block.Liste_Bloc[k][i][j]['Cardinal']=10*Block.Liste_Bloc[k][i][j]['Cardinal']
    
    Graph.Matrice_Longueur            = Graph.Crea_Matrice_Longueur(Graph.G,Road.Liste_Route)
    Graph.Matrice_Poids               = Graph.Crea_Matrice_Poids(Graph.G,Road.Liste_Route)
    Graph.Matrice_Cardinal            = Graph.Crea_Matrice_Cardinal(Graph.G,Road.Liste_Route)
    Graph.Matrice_Etat                = Graph.Crea_Matrice_Etat(Graph.G,Road.Liste_Route)
    
    #Print
    print()
    print()
    
    print("Moyenne des poids des routes : ")
    print(Moyenne_Poids_Divergente(Graph.Matrice_Poids))
    print()
    
    #Afficheur#
    
    Afficheur = Tk()
    Afficheur.title("Afficheur TIPE")
    Afficheur['bg'] = 'bisque'
    Afficheur.geometry(str(Longueur)+'x'+str(Hauteur)+'+0+0')

    P1 = PanedWindow(Afficheur, handlesize=6, showhandle=False, sashrelief='sunken')
    P1.pack(fill='both')


    # Zonage de l'afficheur
    Matrice = LabelFrame(P1, text="Matrice", borderwidth=2,relief=RAISED, labelanchor="n", width=Rapport, height=Hauteur-5)
    Interface = LabelFrame(P1, text="Interface", borderwidth=2,relief=RAISED, labelanchor="n", width=70, height=Hauteur-5)
    OnOff = LabelFrame(Interface, text="OnOff", borderwidth=2,relief=RAISED, labelanchor="n", width=160, height=200)
    OnOff.pack(side = BOTTOM, padx = 5, pady = 5)


    # Boutons de l'interface
    Quest = Button(Interface, bitmap = 'question', command = Information)
    Quest.pack(side = TOP, padx = 5, pady = 5)
    
    Next = Button(Interface, text = 'Suivant ->', command = Iteration)
    Next.pack(side = TOP, padx = 5, pady = 5)

    Quit = Button(Interface, text = 'Quitter', command = Afficheur.destroy)
    Quit.pack(side = TOP, padx = 5, pady = 5)

    AffGraphe = Button(Interface, text = 'Graphe', command = Afficher_Graphe)
    AffGraphe.pack(side = TOP,padx = 5,pady = 5)
    
    Ite_Auto = Button(Interface, text='Journée entière', command = Iteration_Auto)
    Ite_Auto.pack(side = TOP, padx = 5, pady = 5)
    
    AffCourbe = Button(Interface, text = 'Courbes', command = Afficher_Courbes )
   
    AffCourbe.pack(side = TOP,padx = 5,pady = 5)
    
    AffMoyenne = Button(Interface, text = 'Moyennes', command = Afficher_Moyennes )
    
    AffMoyenne.pack(side = TOP,padx = 5,pady = 5)

    # Sous interface de fermeture de route:
    depart= IntVar()
    ChampDep = Entry(OnOff, textvariable= depart, bg ='white', fg='blue')
    ChampDep.pack(side = TOP, padx = 5, pady = 5)
    
    arrivee= IntVar()
    ChampArr = Entry(OnOff, textvariable= arrivee, bg ='white', fg='blue')
    ChampArr.pack(side = TOP, padx = 5, pady = 5)
    
    FR = Button(OnOff, text = 'Fermer!', command = Fermeture_Route_Manuelle)
    FR.pack(side = BOTTOM, padx = 5, pady = 5)

    OU = Button(OnOff, text = 'Ouvrir!', command = Ouverture_Route_Manuelle)
    OU.pack(side = BOTTOM, padx = 5, pady = 5)
    

    # Affichage de la matrice
    mat = Canvas(Matrice, width=Rapport-5, height=Hauteur-10, bg='white')
    mat.pack()
    Afficher(Graph)
    P1.add(Matrice)
    
    #Affichage de l'interface
    P1.add(Interface)
    
    #Affichage l'afficheur
    Afficheur.mainloop()
    
