import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from os import makedirs
from seaborn import kdeplot
from scipy.signal import find_peaks

# ================ NETWORK GRAPH =======================================

def	form_edges(N, linked_matrix):
	"""Create a list of edges for linked agents"""
	edges=[]
	for i in range(N):
		for j in range(i):
			if linked_matrix[i,j]==1:
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

def form_netw_chart(sim, model, N, opinions, cmap, G2, pos, vmin=-1, vmax=1, savef=False):
	"""Build the plot using matplotlib"""
	plt.figure()
	nx.draw_networkx_edges(G2, pos, alpha=0.4)
	nx.draw_networkx_nodes(G2, pos, node_color=opinions, cmap=cmap, node_size=50, vmin=vmin, vmax=vmax)
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
	sm._A = []
	cbar = plt.colorbar(sm, ax=plt.gca())
	cbar.ax.tick_params(labelsize=15)
	if savef:
		makedirs('ABM/results', exist_ok=True)
		plt.savefig(f"ABM/results/mod_{model}-sim_{sim}.png")
	else:
		plt.show()

# ====================== OP_DIST GRAPH ======================================

def	form_density_estimate(opinions, sim, model, savef=False):					# TODO re-do peak analysis check og-model
	"""Build a kernel density plot based on the opinions data"""
	plt.figure()
	kde_plot = kdeplot(data=opinions)
	plt.xlim(-1,1)
	plt.xlabel('Opinions')
	line = kde_plot.lines[0]
	_, y = line.get_data()
	amt_peaks = len(find_peaks(y, height=max(y)/10, prominence=0.1)[0])  # Consider making parameters configurable

	category = assign_categories(amt_peaks, opinions)
	plt.title(f"Cat {category}")
	if savef:
		try:
			makedirs('ABM/results/kde_plots', exist_ok=True)
			plt.savefig(f"ABM/results/kde_plots/mod_{model}-sim_{sim}-cat_{category}.png")
		except Exception as e:
			print(f"Error saving KDE plot: {e}")
	else:
		plt.show()
	plt.close()  # Close only the current figure
	return category

def	assign_categories(amt_peaks, opinions):
	if amt_peaks == 1:
		if np.var(opinions) < 0.05:
			return 0
		else:
			return 1
	elif amt_peaks == 2:
		return 2
	else:
		return 3
	
# =========== EXTRA ======================

def	measure_opdist(opdist, runtime):
	plt.figure()
	plt.xlabel("timestep")
	plt.ylabel("avg opinion distance")
	y = [i for i in range(runtime)]
	plt.plot(y, opdist)
	plt.show()
	