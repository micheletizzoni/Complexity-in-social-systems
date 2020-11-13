# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 17:32:39 2013

@author: Michele
"""

import networkx as nx
from collections import defaultdict
import random

edgelist=defaultdict(list)#dizionario contiene link ad ogni timestep

finput=open('./Dataset_sexual_network.csv','r')
for line in finput.readlines():
    
    if line[0]!='#':#non è un commento
        s=line.strip().split(';')
        
        day=int(s[2])
        edge=(int(s[0]), int(s[1]))
                
        edgelist[day].append(edge)
        
finput.close()

G_agg=nx.Graph()#questo è il grafo aggregato
G_agg.disease_status={}

daystart=800
dayend=1800
for d in edgelist:
    if d>=800 and d<=1800:
        links=edgelist[d]
        G_agg.add_edges_from(links)#aggiungo i link al grafo

print "La rete aggregata ha ", len(G_agg.nodes())," nodi"
print "La rete aggregata ha ", len(G_agg.edges())," links"


#SI model sul grafo aggregato
#scelgo il seed dell'epidemia come un nodo a caso
seed_links=edgelist[daystart]
random.shuffle(seed_links)
seed=seed_links[0][0]

print "Il degree del seed è ", G_agg.degree(seed)

infected_nodes=[]
infected_nodes.append(seed)

for n in G_agg.nodes():
    if n in infected_nodes:
        G_agg.disease_status[n]=1
        #infected
    else:
        G_agg.disease_status[n]=0
        #susceptible

fout=open('./SI_sex_network_epidemic_curve.dat','w')
for t in xrange(0,1000):
    
    #ciclo sui nodi infetti per la trasmissione
    for i in infected_nodes:
        for j in G_agg.neighbors(i):
            if G_agg.disease_status[j]==0:
                G_agg.disease_status[j]=1#probabilità di infezione=1!
                
    #ciclo per aggiornare l'elenco dei nodi infetti
    infected_nodes=[]
    for n in G_agg.nodes():
        if G_agg.disease_status[n]==1:
            infected_nodes.append(n)
 
    #stampo il numero di nodi infetti a ogni time-step
    fout.write(str(t)+' '+str(len(infected_nodes))+'\n')
fout.close()

print "La size finale dell'epidemia è ", float(len(infected_nodes))/len(G_agg.nodes())

