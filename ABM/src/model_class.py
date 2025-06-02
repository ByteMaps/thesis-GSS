import mesa
import numpy as np
import utils.visualisation as viz

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

	def	create_plot(self):
		"""Create a plot based on a single model run"""
		edges = viz.form_edges(self.num_agents, self.adj_matrix)
		pos, cmap, G2 = viz.form_network(self.num_agents, edges)

		viz.form_plot(self.num_agents, self.agents.opinion, edges, cmap, G2, pos)