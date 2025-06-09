import matplotlib.pyplot
import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from random import randint
from os import makedirs
from seaborn import kdeplot
from scipy.signal import find_peaks

from src.utils import *

matplotlib.use('Agg')

# ================ NETWORK GRAPH =======================================

def	form_edges(N, link_matrix):
	"""Create a list of edges for linked agents"""
	edges=[]
	for i in range(N):
		for j in range(i):
			if link_matrix[i,j]==1:
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

def form_netw_chart(modeltype, model, N, category, opinions, cmap, G2, pos, path, savef):
	"""Build the plot using matplotlib"""
	plt.figure()
	nx.draw_networkx_edges(G2, pos, alpha=0.4)
	nx.draw_networkx_nodes(G2, pos, node_color=opinions, cmap=cmap, node_size=50, vmin=-1, vmax=1)
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=-1, vmax=1))
	sm._A = []
	cbar = plt.colorbar(sm, ax=plt.gca())
	cbar.ax.tick_params(labelsize=15)
	if savef:
		makedirs(f"{path}networkx", exist_ok=True)
		plt.savefig(f"{path}networkx/{modeltype}_{model}-cat_{category}.png")
	else:
		plt.show()
	plt.close('all')

def	visualise_network(modeltype, model, N, opinions, link_matrix, category, path, savef=False):
	"""Create a network plot based on a single model run"""
	edges = form_edges(N, link_matrix)
	pos, cmap, G2 = form_network(N, edges)

	form_netw_chart(modeltype, model, N, category, opinions, cmap, G2, pos, path, savef)

# ====================== OP_DIST GRAPH ======================================

def	form_density_estimate(modeltype, opinions, model, path, savef=False):
	"""Build a kernel density plot based on the opinions data"""
	plt.figure()
	kde_plot = kdeplot(data=opinions)
	plt.xlim(-1,1)
	plt.xlabel('Opinions')
	line = kde_plot.lines[0]
	_, y = line.get_data()
	amt_peaks = len(find_peaks(y, height=max(y)/10, prominence=0.1)[0])

	category = assign_categories(amt_peaks, opinions)
	plt.title(f"Cat {category}")
	if savef:
		makedirs(f"{path}kde_plots", exist_ok=True)
		plt.savefig(f"{path}kde_plots/{modeltype}_{model}-cat_{category}.png")
	# else:
	# 	plt.show()
	plt.close('all')
	return category