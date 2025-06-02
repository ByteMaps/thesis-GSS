import mesa
import numpy as np

class Individual(mesa.Agent):
	"""An agent within the opinion dynamics model."""
	__slots__ = ["opinion", "values", "dist_createlink", "dist_removelink", "linked_agents"] 		# Prevent creating dynamic attributes & save RAM

	def __init__(self, model, unique_id, opinion, dist_createlink, dist_removelink):
		super().__init__(model)

		self.unique_id = unique_id
		self.adjacency_row = model.adj_matrix[self.unique_id]
		self.link_row = model.link_matrix[self.unique_id]

		self.opinion = opinion
		self.dist_createlink = dist_createlink
		self.dist_removelink = dist_removelink

	def	find_neighbours(self, agentset):
		"""Update adj_matrix and link_matrix row on distances"""
		for agent in agentset:
			agent_id = agent.unique_id
			agent_opinion = agent.opinion
			if agent_id != self.unique_id:
				dist = abs(agent_opinion - self.opinion)
				self.adjacency_row[agent_id] = dist
				self.link_row[agent_id] = np.where(dist <= self.dist_createlink, 1, 0)  # Update link_row for this agent
	

	def	print_adjacency(self):
		"""Print the row's own adjacency row from the adj_matrix (Model)"""
		self.adjacency_row[self.unique_id] = 1
		print(f"Agent {self.unique_id} has row {self.adjacency_row}\n")