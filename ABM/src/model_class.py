import mesa
import numpy as np
from scipy.stats import wasserstein_distance
from src.visualisation import *

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, params):
		super().__init__()
		self.N 					= N
		self.agents_by_id 		= {}
		self.opinion_dists 		= np.zeros(N)
		self.opinion_dists[-1] 	= 1
		self.sim 				= 0
		self.model				= 0

		self.link_matrix		= np.zeros((N,N), dtype=int)	# TODO check if link_matrix, opinions and values are the same objects as in Agent class
		self.opinions			= np.random.uniform(-1,1,N)
		self.values				= np.random.uniform(-1,1,N)

		self.dist_removelink 	= params.dist_removelink
		self.prob_removelink 	= params.prob_removelink
		self.tries_createlink 	= params.tries_createlink
		self.max_nb 			= params.max_nb
		self.dist_createlink 	= params.dist_createlink
		self.prob_createlink 	= params.prob_createlink
		self.steps_valuechange 	= params.steps_valuechange
		self.rate_valuechange 	= params.rate_valuechange
		self.tries_op_change	= params.tries_op_change
		self.dist_cd			= params.dist_cd
		self.Temp				= params.Temp			

		# Create agents
		for id in range(self.N):
			agent = Agent(self, id, self.opinions[id], self.values[id], self.dist_createlink, self.dist_removelink)
			self.agents_by_id[id] = agent


	def	visualise_network(self, sim, model, opinions, Lmatrix):
		"""Create a plot based on a single model run"""
		edges = form_edges(self.N, Lmatrix)
		pos, cmap, G2 = form_network(self.N, edges)

		form_netw_chart(sim, model, self.N, opinions, cmap, G2, pos)

	def	measure_op_dist(self, step_opinions):
		"""Record the opinion distances and measure using wasserstein_dist"""
		self.opinion_dists[:-1] = self.opinion_dists[1::]		# Shift array for new recs
		self.opinion_dists[-1] = wasserstein_distance(self.opinion_dists, step_opinions)


	def	run(self, runtime, sim, model):												# TODO add order, simulation end checks
		"""Run through all agents to test functionality"""
		i = 0
		opdist = [0 for _ in range(runtime)]
		# step_linkmat = self.link_matrix.copy()
		# self.visualise_network(self.opinions, self.link_matrix)

		while (not all(self.opinion_dists < 0.003) and i < runtime):
			step_opinions = self.opinions.copy()

			self.agents.shuffle_do("remove_neighbours", self._agents)
			self.agents.shuffle_do("find_neighbours")
			self.agents.shuffle_do("change_values", self.rate_valuechange, self.steps_valuechange)
			self.agents.shuffle_do("change_opinion", self.Temp, self.dist_cd, self.tries_op_change)

			# self.measure_op_dist(step_opinions)
			op_std = round(self.opinions.std(), 4)
			opdist[i] = op_std
			op_eq = np.array_equal(step_opinions, self.opinions)
			i += 1
			if i % 5 == 0:
				print(f"Running at {i} with {op_std} equal ops: {op_eq}")

		measure_opdist(opdist, runtime)
		self.visualise_network(sim, model, self.opinions, self.link_matrix)
		form_density_estimate(self.opinions, sim, model)