# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:39:58 2022

@author: anton
"""
import random as rd

class city():
    
    def __init__(self,G):
        Liste_Ville  = self.Crea_Liste_Ville(G)
        
    def Crea_Liste_Ville(self,G):
        
        #Crée la liste des influences de chaque ville.
        #Plus la ville est influente, plus le nombre de départs et d'arrivées est important.
        
        Liste_Ville = []
        for i in range(len(G)):
            a=rd.randint(1,100)/100
            while a==1:
                a=rd.randint(1,100)/100
            Liste_Ville.append(a)
        return(Liste_Ville)
