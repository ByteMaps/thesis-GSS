import mesa
import numpy as np

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, dist_createlink, dist_removelink):
		super().__init__()
		self.num_agents = N
		self.adj_matrix = np.zeros((N,N), dtype=float)					# Distances between agents ([0,2])
		self.link_matrix = np.zeros((N,N), dtype=int)					# Links between agents (1,0)						

		# Create agents
		for id in range(self.num_agents):
			agent = Agent(self, id, dist_createlink=dist_createlink, dist_removelink=dist_removelink)

	def	run(self):
		"""Run through all agents to test functionality"""
		# print(self.adj_matrix)
		self.agents.shuffle_do("find_neighbours", self.agents)
		print(self.adj_matrix)
		print(self.link_matrix)