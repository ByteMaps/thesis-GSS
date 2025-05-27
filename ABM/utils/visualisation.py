import numpy as np

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