# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:42:24 2022

@author: anton
### Creation des blocs

Les blocs sont identifiés par (k,i,j)=(instant de départ, sommet de départ, sommet d'arrivée)

"""

import random as rd
from utils import Repartition_Temporelle, Dijkstra

class block():
    
    Moy_Bloc = 0
    Liste_Moyennes_Blocs = []
    def __init__(self,G,Liste_Route,t):
        
        self.Liste_Bloc = self.Crea_Liste_Bloc(G,Liste_Route,t)
        
    def Crea_Bloc(self,G,Liste_Route,k,i,j):  #Liste_Ville en paramètre
        """
        Création du bloc kij.
        Card_Min : "Nombre de véhicules min possible d'un bloc"
        Card_Max : "Nombre de véhicules max possible d'un bloc"
        Le choix du nombre de véhicules dans le bloc peut être aléatoire, ou alors déterminé en fonction de ce qu'il s'est passé à l'itération précédente (nombre de gens sortis du graphe), voir de l'attractivité des villes alentours et de la population des villes si on veut vraiment complexifier. Ici c'était simplement aléatoire.
        """
        Card_Min = 0
        Card_Max = 100
        Rep_Temps = Repartition_Temporelle(k)
        
        Bloc = {}
        
        if i != j:
            Bloc['Identifiant'] = (k,i,j)
            Bloc['Cardinal'] = 15*int(rd.randint(Card_Min,Card_Max)*Rep_Temps) 
            Bloc['Chemin'] = Dijkstra(G,Liste_Route,i,j)
            Bloc['Route'] = 0
            Bloc['Position'] = 0
            Bloc['Vitesse'] = 0
            Bloc['Etat'] = 0
        return Bloc
    
    
    def Crea_Liste_Bloc(self,G,Liste_Route,t):
        """
        Création de la liste des dictionnaires des blocs. 
        t est le nombre d'itérations.
        """
        Liste_Bloc = []
        
        for k in range(t):
            Liste_Bloc.append([])
            for i in range(len(G)):
                Liste_Bloc[k].append([])
                for j in range(len(G)):
                    Bloc = self.Crea_Bloc(G,Liste_Route,k,i,j)
                    Liste_Bloc[k][i].append(Bloc)
        return Liste_Bloc
        
        
    def Prolongement_Liste_Bloc(self,G,Liste_Route,Liste_Bloc,t):
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
    
