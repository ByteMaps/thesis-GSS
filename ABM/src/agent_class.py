import mesa
import numpy as np

class Individual(mesa.Agent):
	"""An agent within the opinion dynamics model."""
	__slots__ = ["opinion", "values", "dist_createlink", "dist_removelink", "linked_agents"] 		# Prevent creating dynamic attributes & save RAM

	def __init__(self, model, unique_id, opinion, dist_createlink, dist_removelink):
		super().__init__(model)

		self.unique_id = unique_id
		self.link_row = model.link_matrix[self.unique_id]

		self.opinion = opinion
		self.dist_createlink = dist_createlink
		self.dist_removelink = dist_removelink

	def	find_neighbours(self, agentset):
		"""Add to link_matrix row on distances"""
		for agent in agentset:
			agent_id = agent.unique_id
			if agent_id != self.unique_id:
				if (abs(agent.opinion - self.opinion) <= self.dist_createlink):
					self.link_row[agent.unique_id] = 1
					agent.link_row[self.unique_id] = 1

	def	remove_neighbours(self, agentset):
		"""Remove from link_matrix row on distances"""
		removelink_random = np.random.uniform(0,1,self.model.num_agents)
		for agent in agentset:
			agent_id = agent.unique_id
			if agent_id != self.unique_id:
				if (abs(agent.opinion - self.opinion) >= self.dist_removelink) and \
					(removelink_random[agent_id] <= self.model.prob_removelink):
					self.link_row[agent.unique_id] = 0
					agent.link_row[self.unique_id] = 0

	def	change_opinion(self):
		"""N"""
		pass