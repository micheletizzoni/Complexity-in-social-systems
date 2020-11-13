# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 17:32:39 2013

@author: Michele
"""

import networkx as nx
from datetime import datetime,timedelta

G=nx.DiGraph()

start='2002/01/01'
FMT = '%Y/%m/%d'
startdate = datetime.strptime(start,FMT)

finput=open('./Dataset_sexual_network.csv','r')
for line in finput.readlines():
    
    if line[0]!='#':#non è un commento
        s=line.strip().split(';')

        day=startdate+timedelta(days=int(s[2]))
        
        G.add_edge(int(s[1]),int(s[0]), start=day.strftime('%d/%m/%Y'), end=day.strftime('%d/%m/%Y'))
finput.close()

print G.edges(data='True')

nx.write_gexf(G,'./prova.gexf',version='1.2draft')       