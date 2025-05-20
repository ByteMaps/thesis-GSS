# -*- coding: utf-8 -*-

import igraph as ig
import networkx as nx
import matplotlib.pyplot as plt

g = ig.Graph(n=10, edges=[[0,1],[0,5]])
layout = g.layout("kk")
nx_g = nx.Graph()
nx_g.add_edges_from(g.get_edgelist())
pos = nx.spring_layout(nx_g)
nx.draw(nx_g, pos)
plt.show()