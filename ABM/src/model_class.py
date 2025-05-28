import mesa
import numpy as np

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, dist_createlink, dist_removelink):
		super().__init__()
		self.num_agents = N
		self.adj_matrix = np.zeros((N,N), dtype=float)											# Keep track of links between agents, optimised type

		# Create agents
		for id in range(self.num_agents):
			agent = Agent(self, id, dist_createlink=dist_createlink, dist_removelink=dist_removelink)

	def	run(self):
		"""Run through all agents to test functionality"""
		# print(self.adj_matrix)
		self.agents.shuffle_do("print_adjacency")
		print(self.adj_matrix)