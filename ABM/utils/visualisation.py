import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# TODO integrate code with model runs

def	form_adjacency_matrix(agent_links, N):
	"""Form the adjacency matrix for the agents in the model using the linked neighbour arrays"""

	adjacency_matrix = np.eye(N)

	for i in range(N):
		for j in range(N):
			if j in agent_links[i]:
				adjacency_matrix[i, j] = 1
			else:
				adjacency_matrix[i, j] = 0

	return adjacency_matrix

def	form_edges(N, G, adj_matrix):
	edges=[]
	# Create a list of edges from the adjacency matrix
	for i in range(N):
		for j in range(i):
			if G[i,j]==1:
				edges.append((i,j))

	return edges

def	form_plot(edges):											# TODO sort out this code, comments & subtasks
	cmap = plt.cm.viridis # plt.cm.hot #
	G2 = nx.Graph()
	G2.add_nodes_from(np.arange(0,N))
	G2.add_edges_from(edges)
	pos = nx.spring_layout(G2,seed=10)

	plt.figure()
	edgesdraw = nx.draw_networkx_edges(G2, pos, alpha=0.4)
	nodesdraw = nx.draw_networkx_nodes(G2, pos, node_color=opinions, cmap=cmap, node_size=50, vmin=vmin, vmax=vmax)
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin = vmin, vmax=vmax))
	sm._A = []
	cbar = plt.colorbar(sm, ax=plt.gca())
	cbar.ax.tick_params(labelsize=15)