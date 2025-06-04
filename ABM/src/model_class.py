import mesa
import numpy as np

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, params):
		super().__init__()
		self.N = N
		self.agents_by_id = {}

		self.link_matrix = np.zeros((N,N), dtype=int)					# Links between agents (1,0)
		self.opinions = np.random.rand(N)*2-1							# ? Why the * 2 - 1
		self.values = np.random.rand(N)*2-1

		self.dist_removelink 	= params.dist_removelink
		self.prob_removelink 	= params.prob_removelink
		self.tries_createlink 	= params.tries_createlink
		self.max_nb 			= params.max_nb
		self.dist_createlink 	= params.dist_createlink
		self.prob_createlink 	= params.prob_createlink
		self.tries_valuechange 	= params.tries_valuechange
		self.rate_valuechange 	= params.rate_valuechange
		self.tries_op_change	= params.tries_op_change
		self.dist_cd			= params.dist_cd
		self.Temp				= params.Temp			

		# Create agents
		for id in range(self.N):
			agent = Agent(self, id, self.opinions[id], self.values[id], self.dist_createlink, self.dist_removelink)
			self.agents_by_id[id] = agent

	def	run(self):
		"""Run through all agents to test functionality"""
		self.agents.shuffle_do("find_neighbours", self._agents)
		self.agents.shuffle_do("remove_neighbours", self._agents)
		print(self.link_matrix)

	def	create_plot(self, form_edges, form_network, form_plot):
		"""Create a plot based on a single model run"""
		edges = form_edges(self.N, self.link_matrix)
		pos, cmap, G2 = form_network(self.N, edges)

		form_plot(self.N, self.opinions, cmap, G2, pos)