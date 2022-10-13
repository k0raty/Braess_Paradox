# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:50:27 2022

@author: anton
"""

### Fonctions utilisées dans le script d'affichage

# Fonctions avec fonctionnement indépendant du script :
from tkinter import messagebox

def Conversion(n):
    """
    Cette fonction servira à donner la couleurs correspondant au poids dans la représentation de la matrice d'adjacence.
    
    [1:809] ---> [1:99]
    1-51      Gris1-10
    52-106    Gris11-20
    107-166   Gris21-30
    167-232   Gris31-40
    233-305   Gris41-50
    306-386   Gris51-60
    387-476   Gris61-70
    477-576   Gris71-80
    577-687   Gris81-90
    688-809   Gris91-99
    """
    if n < 51:
        n = ((n-1)*10)//51 + 1
    elif n < 106:
        n = ((n-52)*10)//55 + 11
    elif n < 166:
        n = ((n-107)*10)//60 + 21
    elif n < 232:
        n = ((n-167)*10)//66 + 31
    elif n < 305:
        n = ((n-233)*10)//73 + 41
    elif n < 386:
        n = ((n-306)*10)//81 + 51
    elif n < 476:
        n = ((n-387)*10)//90 + 61
    elif n < 576:
        n = ((n-477)*10)//100 + 71
    elif n < 687:
        n = ((n-577)*10)//111 + 81
    elif n < 809:
        n = ((n-688)*9)//122 + 91
    else:
        n = 99
    if n != 0:
        return n-1
    else:
        return n


# Fonctions dont le fonctionnement est lié au script :

def Information():
    """
    Message d'information de l'afficheur.
    """
    Aide = "This interface is used to simulate traffic on a road network, in order to verify the Braess Paradox. \n \n Version 11.0 . The program dates from 16/02/2019 and was remasterised in october 2022 \n \n Made by Guillaume Gautier de La Plaine, Roman Rousseau and Antony Davi."
    
    messagebox.showinfo("Aide Afficheur", Aide)
