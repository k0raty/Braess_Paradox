# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:24:06 2022

@author: anton
###Petites fonctions utiles

"""
import numpy as np

def maxListe(L):
    m=0
    for i in range(0,len(L)):
        if L[i]>m:
            m=L[i]
    return m

def Repartition_Temporelle(k):
    """
    Détermine la proportion de véhicules qui vont démarrer à chaque itération. Ne renvoie que sa valeur pour l'itération k.
    """
    
    """L06=[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]   #24'*[20] s'écrit aussi
    L69=[21,23,26,30,36,42,49,57,67,77,88,100]
    L910=[100,100,100,100]   #4*[100]
    L1013=deepcopy(L69)
    L1013.reverse()
    L1316=[20,23,29,38,50,50,50,50,38,29,23,20]
    L1623=L69+L910+L1013
    L2324=[20,20,20,20]     #4*[20]
    
    L=L06+L69+L910+L1013+L1316+L1623+L2324"""
    
    L = [5,5,5,5, 5,5,5,5, 5,5,5,5, 6,7,8,9, 10,10,10,10, 16,23,31,40, 50,61,73,86, 100,100,100,100, 86,73,61,50, 40,31,23,16, 15,19,22,25, 25,24,22,20, 20,22,24,25, 25,22,19,15, 16,23,31,40, 50,61,73,86, 100,100,100,100, 86,73,61,50, 40,31,23,16, 10,10,10,10, 9,8,7,6, 5,5,5,5, 5,5,5,5, 5,5,5,5]
    
    Rep_Temps=[i/100 for i in L]
    
    return Rep_Temps[k]

def Morphing_Liste(L):
    """
    Transforme une liste d'éléments en une liste de couples de 2 éléments
    """
    E = []
    
    for i in range(len(L)-1):
        E.append((L[i],L[i+1]))
    return E

### Calcul des moyennes

def Moyenne_Poids_Divergente(Matrice_Poids):
    """
    Calcul de la moyenne des poids sur le graphe
    c : "Nombre de routes existentes (1 sens)"
    """
    n = len(Matrice_Poids)
    c = 0
    s = 0
    for u in range(n):
        for v in range(n):
            if Matrice_Poids[u][v] != 0:
                s = s + Matrice_Poids[u][v]
                c = c+1
    return s/c


def Moyenne_Poids_Convergente(Matrice_Poids):
    """
    Calcul de la moyenne des poids sur le graphe en ne comptant pas les routes qui divergent
    n*(n-1) : "Nombre de routes à 1 sens"
    """
    n = len(Matrice_Poids)
    s = 0
    for u in range(n):
        for v in range(n):
            if Matrice_Poids[u][v] <= 809:
                s = s + Matrice_Poids[u][v]
    return s/(n*(n-1))


def Moyenne_Longueur(Matrice_Longueur):
    """
    Calcul de la moyenne des longueurs sur le graphe
    n*(n-1) : "Nombre de routes à 1 sens"
    """
    n = len(Matrice_Longueur)
    s = 0
    for u in range(n):
        for v in range(u):
            s = s + 2*Matrice_Longueur[u][v]
    return s/(n*(n-1))


def Cardinal_Total(Matrice_Cardinal):
    """
    Calcul du nombre de véhicule sur le graphe en entier
    """
    n = len(Matrice_Cardinal)
    s = 0
    for u in range(n):
        for v in range(n):
            s = s+Matrice_Cardinal[u][v]
    return s


def Temps_Trajet(Matrice_Poids:np.ndarray, Bloc):
    """
    Retourne le temps de trajet restant du bloc 'Bloc'.
    """
    
    Temps=0
    Chemin_Restant=[ Bloc['Chemin'][i] for i in range(Bloc['Route'],len(Bloc['Chemin'])) ]
    
    for i in Chemin_Restant:
        Temps = Temps + Matrice_Poids[i[0],i[1]]
    
    return Temps

def Prolongement_Liste_Bloc(G,Liste_Route,Liste_Bloc,t):
    """
    Permet d'ajouter à la liste des blocs les blocs de la nouvelle journée
    """
    N = len(Liste_Bloc)
    
    for k in range(t):
        Liste_Bloc.append([])
        for i in range(len(G)):
            Liste_Bloc[N+k].append([])
            for j in range(len(G)):
                Liste_Bloc[N+k][i].append([])
                Liste_Bloc[N+k][i][j] = {}
                if i != j:
                    Liste_Bloc[N+k][i][j]['Identifiant'] = (N+k,i,j)
                    Liste_Bloc[N+k][i][j]['Cardinal'] = 0 + Liste_Bloc[k][i][j]['Cardinal']
                    Liste_Bloc[N+k][i][j]['Chemin'] = Dijkstra(G,Liste_Route,i,j)
                    Liste_Bloc[N+k][i][j]['Route'] = 0
                    Liste_Bloc[N+k][i][j]['Position'] = 0
                    Liste_Bloc[N+k][i][j]['Vitesse'] = 0
                    Liste_Bloc[N+k][i][j]['Etat'] = 0


#Dijkstra

def Dijkstra(G,Liste_Route,u,v):
    """
    Calcule le chemin le plus court entre u et v
    """
    L = []
    n = len(G)
    for i in range(n):
        L.append([False,999999,-1])                          # True et False : l'état fixé du sommet
    
    L[u][0] = True
    L[u][1] = 0     
    courant = u
    nombre_fixe = 1
    
    while nombre_fixe < n:
        avisiter = []                                        # Liste de tous les sommets non fixés
        for i in range(0,len(L)):
            if L[i][0] == False:
                avisiter.append(i)
        
        for i in avisiter:                                   # Comparaison du nouveau et de l'ancien poids de i
            if Liste_Route[courant][i] != {}:
                if (Liste_Route[courant][i]['Longueur']/Liste_Route[courant][i]['Vitesse max']) > 0 and Liste_Route[courant][i]['Etat'] == 1:
                    ancien_poids = L[i][1]
                    nouveau_poids = L[courant][1] + (Liste_Route[courant][i]['Longueur']/Liste_Route[courant][i]['Vitesse max'])
                
                    if nouveau_poids < ancien_poids :
                        L[i][2] = courant
                        L[i][1] = nouveau_poids
        
        indice_mini = avisiter[0]
        
        for i in avisiter:
            if L[i][1] < L[indice_mini][1] :
                indice_mini = i
        
        #On fixe le sommet choisi ci-dessus, et on se prépare pour une éventuelle nouvelle boucle
        courant = indice_mini 
        L[courant][0] = True
        nombre_fixe = nombre_fixe+1
        
    Chemin = [v]
    predecesseur = v
    
    while predecesseur != u:
        predecesseur = L[predecesseur][2]
        Chemin.append(predecesseur)
        
    Chemin.reverse()
    
    s = L[v][1]                                                # s est le poids total du chemin
    
    #print("le chemin à suivre est ", chemin, " et son poids total vaut ", s)
    return Morphing_Liste(Chemin)

