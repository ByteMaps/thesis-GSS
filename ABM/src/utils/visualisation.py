import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import randint

# TODO integrate code with model runs

def	form_edges(N, adj_matrix):
	"""Create a list of edges for linked agents"""
	edges=[]
	for i in range(N):
		for j in range(i):
			if adj_matrix[i,j]==1:
				edges.append((i,j))

	return edges

def	form_network(N, edges):
	"""Set up the networkx graph for plotting, use theme viridis"""
	cmap = plt.cm.viridis
	G2 = nx.Graph()
	G2.add_nodes_from(np.arange(0,N))
	G2.add_edges_from(edges)
	pos = nx.spring_layout(G2,seed=10)
	return pos, cmap, G2

def	form_plot(N, opinions, edges, cmap, G2, pos, vmin=-1, vmax=1, savef=False):
	"""Build the plot using matplotlib"""
	plt.figure()
	edgesdraw = nx.draw_networkx_edges(G2, pos, alpha=0.4)
	nodesdraw = nx.draw_networkx_nodes(G2, pos, node_color=opinions, cmap=cmap, node_size=50, vmin=vmin, vmax=vmax)
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin = vmin, vmax=vmax))
	sm._A = []
	cbar = plt.colorbar(sm, ax=plt.gca())
	cbar.ax.tick_params(labelsize=15)
	if savef:
		plt.savefig("figures/%i.png", i=randint(0,100))