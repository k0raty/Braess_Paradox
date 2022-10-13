# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:25:33 2022

@author: anton
"""

import numpy as np
import random as rd

"""
Fichier gérant toute requêtes relatives aux graphes.
Deux manières de créer un graphe aléatoire. 
Cf documentation de chaque fonction pour plus de précision.
"""

class graph():
    """
    G              : Matrice d'adjacence du graph'
    n              : Nombre de sommets du graphe  # Doit être supérieur à 4
    m              : Poids maximal de chaque route
    p              : Proportion de routes inexistantes  VOIR CONDITIONS CONSEILLEES CI DESSOUS.  # Arrondi au centième près
    t              : Nombre maximal d'itérations # Doit être un multiple de 24.
    Poids_Max      : Poids maximum pour la fermeture automatique
    Fermeture_Auto : Active ou non la fermeture automatique
    Ouverture_Auto : Active ou non l' ouverture automatique
    Temps_Pause    : Temps de pause entre deux itérations automatiques.
    """
    
    Moy_Jour = 0
    Liste_Moyennes_Graphe  = []
    def __init__(self,G = np.array([]), n = 6, m = 809 ,p = None ,t = 96 , Fermeture_Auto = False, Ouverture_Auto = False , Poids_Max = 809 ,Temps_Pause = 1 ):
        
        """ 
        CONDITIONS SUR p            Validation du critère
        p = 0 pour n = 3            OK
        p = 0 pour n = 4            OK
        p = 1/10 pour n = 5         OK
        p = 1/2 pour n = 10         p = 7/15, c'est OK
        p = 3/4 pour n = 20         p = 68/95 = 0.71, c'est OK
        p ---> 1 quand n ---> 1     OK
        """
        
        self.n = n
        self.m = m
        self.t = t
        self.Fermeture_Auto = Fermeture_Auto 
        self.Ouverture_Auto = Ouverture_Auto
        self.Poids_Max= Poids_Max
        self.Temps_Pause = Temps_Pause
    
        if p == None :
            self.p=int(100*((n-3)*(n-4)) / (n*(n-1))) / 100
        else : self.p = p
        
        if len(G) == 0 :
            self.G = self.Verif_Graphe(self.n,self.p)
        else : self.G = G
        
        self.Liste_Position = self.t*[len(self.G)*[len(self.G)*[self.t*[0]]]] #Pour les plot
        self.Files_Attente = self.Liste_Files_Attente(self.G)
    def Crea_Graphe_Alea(self,n,p):
        """ 
        Création d'un graphe carré, aléatoire et symétrique.
        n : "Taille du graphe".
        p : "Proportion approximative de 0 dans le graphe".
        """
        G = np.zeros((n,n))
        
        for i in range(n):
            for j in range(i):
                a = rd.randint(1,100)
                if a > 100*p:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def Verif_Graphe(self,n,p):
        """
        Vérifie que le graphe est conforme pour tester le paradoxe.
        """
        v = False
        while v == False:
            v = True
            G = self.Crea_Graphe_Alea(n,p)
            for i in range(n):
                s = 0
                for j in range(n):
                    s = s + G[i][j]
                if s < 3:
                    v = False
        return G
    
    ### Matrices d'adjacence associées au graphe
    
    def Crea_Matrice_Poids(self,G,Liste_Route):
        """
        Création de la matrice des poids des routes associée au graphe.
        """
        Matrice_Poids = np.zeros((len(G),len(G)))
        
        for u in range(len(G)):
            for v in range(len(G)):
                if Liste_Route[u][v] != {}:
                    Matrice_Poids[u][v] = 0.1*int(10*Liste_Route[u][v]['Poids']) #afin d'avoir le poids à la décimal près
        return Matrice_Poids
    
    
    def Crea_Matrice_Longueur(self,G,Liste_Route):
        """
        Création de la matrice des longueurs des routes associée au graphe.
        """
        Matrice_Longueur = np.zeros((len(G),len(G)))
        
        for u in range(len(G)):
            for v in range(len(G)):
                if Liste_Route[u][v] != {}:
                    Matrice_Longueur[u][v] = int(Liste_Route[u][v]['Longueur'])
        return Matrice_Longueur
        
        
    def Crea_Matrice_Cardinal(self,G,Liste_Route):
        """
        Création de la matrice des cardinaux des routes associée au graphe.
        """
        Matrice_Cardinal = np.zeros((len(G),len(G)))
        
        for u in range(len(G)):
            for v in range(len(G)):
                if Liste_Route[u][v] != {}:
                    Matrice_Cardinal[u][v] = int(Liste_Route[u][v]['Cardinal'])
        return Matrice_Cardinal
        
        
    def Crea_Matrice_Etat(self,G,Liste_Route):
        """
        Création de la matrice des états des routes associée au graphe.
        """
        Matrice_Etat =  np.zeros((len(G),len(G)))
        
        for u in range(len(G)):
            for v in range(len(G)):
                if Liste_Route[u][v] != {}:
                    Matrice_Etat[u][v] = Liste_Route[u][v]['Etat']
        return Matrice_Etat
    
    def Liste_Files_Attente(self,G):
        """
        Initialise les files d'attentes à chque sommet.
        """
        
        
        Files_Attente=[]
        
        for i in range(len(G)):
            Files_Attente.append([])
            for j in range(len(G)):
                Files_Attente[i].append([])
        return Files_Attente

    

    