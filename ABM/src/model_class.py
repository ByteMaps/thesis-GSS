import mesa
import numpy as np

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, dist_createlink, dist_removelink):
		super().__init__()
		self.num_agents = N
		self.link_matrix = np.zeros((N,N), dtype=int)					# Links between agents (1,0)
		self.opinions = np.random.rand(N)*2-1
		self.values = np.random.rand(N)*2-1

		self.prob_removelink = 0.15					

		# Create agents
		for id in range(self.num_agents):
			agent = Agent(self, id, self.opinions[id], self.values[id], dist_createlink, dist_removelink)

	def	run(self):
		"""Run through all agents to test functionality"""
		self.agents.shuffle_do("find_neighbours", self._agents)
		self.agents.shuffle_do("remove_neighbours", self._agents)
		print(self.link_matrix)

	def	create_plot(self, form_edges, form_network, form_plot):
		"""Create a plot based on a single model run"""
		edges = form_edges(self.num_agents, self.link_matrix)
		pos, cmap, G2 = form_network(self.num_agents, edges)

		form_plot(self.num_agents, self.opinions, cmap, G2, pos)