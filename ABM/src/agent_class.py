import mesa
import numpy as np

class Individual(mesa.Agent):
	"""An agent within the opinion dynamics model."""
	__slots__ = ["opinion", "values", "dist_createlink", "dist_removelink", "linked_agents"] 		# Prevent creating dynamic attributes & save RAM

	def __init__(self, model, unique_id, dist_createlink, dist_removelink):
		super().__init__(model)

		self.unique_id = unique_id
		self.adjacency_row = model.adj_matrix[self.unique_id]

		self.opinion = round(self.random.uniform(-1,1),3)
		self.dist_createlink = dist_createlink
		self.dist_removelink = dist_removelink

	def	find_neighbours(self, agentset):
		"""Find all candidates to form links with and connect to them"""
		candidates = np.copy(self.linked_agents)
		candidates = [neighbour.unique_id for neighbour in agentset if abs(neighbour.opinion - self.opinion) <= self.dist_createlink and neighbour.unique_id != self.unique_id]

		return candidates
	
	def	form_links(self, candidates):
		"""Run candidates through prob_createlink and tries_createlink to see if a connection can happen"""
		
		for candidate in candidates:										# Add candidate to linked agents # TODO add prob_create and tries_create to it
			self.linked_agents[candidate.unique_id] = candidate

	def	print_adjacency(self):
		self.adjacency_row[self.adjacency_row != self.unique_id] = 1										# TODO index row properly (i,j) for uniqueID
		print(f"Agent {self.unique_id} has row {self.adjacency_row}\n")