# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 17:32:39 2013

@author: Michele
"""

import networkx as nx
from collections import defaultdict
import random

edgelist=defaultdict(list)

finput=open('./Dataset_sexual_network.csv','r')
for line in finput.readlines():
    
    if line[0]!='#':#non è un commento
        s=line.strip().split(';')
        
        day=int(s[2])
        edge=(int(s[0]), int(s[1]))
                
        edgelist[day].append(edge)
        
finput.close()

G_dyn=nx.Graph()#questo è il grafo dinamico
G_dyn.disease_status={}

daystart=800
dayend=1800
#SI model sul grafo dinamico
#scelgo il seed dell'epidemia come un nodo a caso
seed_links=edgelist[daystart]
random.shuffle(seed_links)
seed=seed_links[0][0]

infected_nodes=[]
infected_nodes.append(seed)

G_dyn.add_edges_from(seed_links)#aggiungo soltanto i link attivi il primo giorno

for n in G_dyn.nodes():
    if n in infected_nodes:
        G_dyn.disease_status[n]=1
        #infected
    else:
        G_dyn.disease_status[n]=0
        #susceptible


fout=open('./SI_sex_network_epidemic_curve_dynamic.dat','w')
for t in xrange(daystart,dayend+1):

    links=edgelist[t]#questi sono i link attivi al giorno t
    
    if t==daystart:
        print "La rete dinamica ha ", len(G_dyn.nodes())," nodi al giorno ", daystart
        print "La rete dinamica ha ", len(G_dyn.edges())," links al giorno ", daystart
        print "Il degree del seed è ", G_dyn.degree(seed)
    else:
        G_dyn.add_edges_from(links)
        for e in links:
            if e[0] not in G_dyn.disease_status:
                G_dyn.disease_status[e[0]]=0
            if e[1] not in G_dyn.disease_status:
                G_dyn.disease_status[e[1]]=0

    
    #ciclo sui nodi infetti per la trasmissione
    for i in infected_nodes:
        for j in G_dyn.neighbors(i):
            if G_dyn.disease_status[j]==0:
                G_dyn.disease_status[j]=1
                
    #ciclo per aggiornare l'elenco dei nodi infetti
    infected_nodes=[]
    for n in G_dyn.nodes():
        if G_dyn.disease_status[n]==1:
            infected_nodes.append(n)
 
    #stampo il numero di nodi infetti a ogni time-step
    fout.write(str(t-800)+' '+str(len(infected_nodes))+'\n')
    
    G_dyn.remove_edges_from(links)
    
fout.close()

print "La size finale dell'epidemia è ", float(len(infected_nodes))/len(G_dyn.nodes())

