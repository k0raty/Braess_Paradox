# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:32:38 2022

@author: 
    
Les routes sont identifiées par uv (depart/arrivée).
    

"""
import random as rd
import numpy as np

class road():
    
    def __init__(self,G):
        self.Liste_Route  = self.Crea_Liste_Route(G)
        
    def Calcul_Epaisseur(self,G,Epaisseur_Min,Epaisseur_Max):
        return rd.randint(Epaisseur_Min,Epaisseur_Max) * int(50 * np.exp(np.log(2.5)/np.log(2) * np.log(len(G)/22)))/100
    
    
    def Crea_Route(self,G,u,v):
        """
        Création de la route Ruv.
        Epaisseur_Min : "Epaisseur min possible d'une route"
        Epaisseur_Max : "Epaisseur max possible d'une route"
        L'épaisseur ne doit pas trop varier d'une route à l'autre.
        Cardinal : "Nombre de véhicules sur la route"
        """
        
        Route = {}
        
        if G[u][v] != 0:
            Route['Identifiant'] = (u,v)
            Route['Longueur'] = 0
            Route['Cardinal'] = 0
            Route['Poids'] = 0
            Route['Epaisseur'] = rd.randint(2, 4)
            if Route['Epaisseur'] ==2:
                Route['Prop sat']= 0.41
                Route['Sensibilité']=4
                Route['Vitesse max'] = 90
                Route['Capacité']= 1600
                Route['Coefficient']=1.25
            if Route['Epaisseur'] ==3:
                Route['Prop sat']= 0.41
                Route['Sensibilité']=6
                Route['Vitesse max'] = 110
                Route['Capacité']= 3200
                Route['Coefficient']=1.20
    
            if Route['Epaisseur'] ==4:
                Route['Prop sat']= 0.41
                Route['Sensibilité']= 8
                Route['Vitesse max'] = 130
                Route['Capacité']= 5400
                Route['Coefficient']=1.15
    
            Route['Flux']=[0,0,0,0] 
            Route['Etat'] = 1
        return Route
    
    
    def Crea_Liste_Route(self,G):
        """
        Création du dictionnaire des routes
        Longueur_Min : "Longueur min possible d'une route"
        Longueur_Max : "Longueur max possible d'une route"
        Le choix de la longueur d'une route doit être restreint pour de pas avoir de route trop longue ou trop courte.
        Le poids de la route est initialement égal à la longueur de la route.
        """
        Liste_Route = []
        Longueur_Min = 86
        Longueur_Max = 258
        
        for u in range(len(G)):
            Liste_Route.append([])
            for v in range(len(G)):
                Route = self.Crea_Route(G,u,v)
                Liste_Route[u].append(Route)
        
        for u in range(len(G)):
            for v in range(u):
                if Liste_Route[u][v] != {}:
                    Liste_Route[u][v]['Longueur'] = rd.randint(Longueur_Min,Longueur_Max)
                    Liste_Route[v][u]['Longueur'] = Liste_Route[u][v]['Longueur']
                    Liste_Route[v][u]['Vitesse max'] = Liste_Route[u][v]['Vitesse max']
                    Liste_Route[v][u]['Epaisseur'] = Liste_Route[u][v]['Epaisseur']
                    Liste_Route[v][u]['Prop sat'] = Liste_Route[u][v]['Prop sat']
                    Liste_Route[v][u]['Sensibilité'] = Liste_Route[u][v]['Sensibilité']
                    Liste_Route[v][u]['Capacité'] = Liste_Route[u][v]['Capacité']
                    Liste_Route[v][u]['Coefficient']=Liste_Route[u][v]['Coefficient']
                    Liste_Route[u][v]['Poids'] = Liste_Route[u][v]['Longueur']/Liste_Route[u][v]['Vitesse max']               
                    Liste_Route[v][u]['Poids'] = Liste_Route[v][u]['Longueur']/Liste_Route[v][u]['Vitesse max']               
        return Liste_Route
    