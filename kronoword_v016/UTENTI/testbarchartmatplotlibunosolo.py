# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 03:54:51 2013

@author: Administrator
"""
import numpy as np
import matplotlib.pyplot as plt
import datetime

f = open('unosolo.txt', 'r+')
dati_utente = eval (f.read())

if type(dati_utente).__name__=='list':
#if zip(*dati_utente)[0]
    punteggi=dati_utente[0]
    date=dati_utente[1]
    y=punteggi
    x= np.arange(2)  
    
    width = 0.1
    #plt.xticks(1,date)
    p1 = plt.bar(x, y,   width, color='r')
    plt.show()
    

else:
    punteggi=zip(*dati_utente)[0]
    date= zip(*dati_utente)[1]   
    N=len(date)    
    x = np.arange(N)
    y = list(punteggi)
    xticks=list(date)
    width = 0.1
    plt.xticks(x,xticks)
    p1 = plt.bar(x, y,   width, color='r')
    plt.show()


        

