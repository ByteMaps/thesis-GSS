import mesa
import numpy as np
from scipy.stats import wasserstein_distance
from src.visualisation import *

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, params, runtime):
		super().__init__()
		self.N 					= N								# Amount of agents
		self.sim 				= 0
		self.model				= 0
		self.runtime			= runtime
		self.modeltype			= type(params).__name__ 

		self.link_matrix		= np.zeros((N,N), dtype=int)	# TODO check if link_matrix, opinions and values are the same objects as in Agent class
		self.opinions			= np.random.uniform(-1,1,N)		# np array with generated opinions
		self.values				= np.random.uniform(-1,1,N)		# np array with generated values
		self.stubbornness		= np.random.rand(N)
		self.persuasiveness		= np.random.rand(N)

		# Imported parameters
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

		# GenT parameters
		self.birth_death_prob    = params.birth_death_prob
		self.turnover_tries      = params.turnover_tries

		# Create agents
		self.agents_by_id 		= {}							# Dict of agent objects accessible by unique_id
		for id in range(self.N):
			agent = Agent(self, id, self.opinions[id], self.values[id], self.stubbornness[id], self.persuasiveness[id])
			self.agents_by_id[id] = agent

		self.opinion_dists 		= np.zeros((N, self.runtime))
		self.opinion_matrix		= np.zeros((N, self.runtime))
		self.opinion_matrix[0]	= self.opinions

	def	visualise_network(self, sim, model, opinions, Lmatrix):
		"""Create a network plot based on a single model run"""
		edges = form_edges(self.N, Lmatrix)
		pos, cmap, G2 = form_network(self.N, edges)

		form_netw_chart(sim, model, self.N, opinions, cmap, G2, pos)

	def	measure_op_dist(self, step_opinions, step):
		"""Record the opinion distances and measure using wasserstein_dist, save in opinion_dists"""
		self.opinion_dists[:-1] = self.opinion_dists[1::]		# Shift array for new recs
		self.opinion_dists[step] = wasserstein_distance(self.opinion_dists, step_opinions)

	def	gen_turnover(self):
		"""Pick out a random agent and reset its params"""			# * Hendrickx & Martin, 2017
		random_id = np.random.randint(0,self.N)
		agent = self.agents_by_id[random_id]
		agent.opinion			= np.random.uniform(-1,1,1)
		agent.values			= np.random.uniform(-1,1,1)
		agent.stubbornness		= np.random.rand(1)
		agent.persuasiveness	= np.random.rand(1)
		agent.link_row = 0

	def turnover_check(self):
		"""Attempt turnover_tries times to implement GenT"""
		for _ in range(self.turnover_tries):
			if np.random.rand() < self.migration_prob:
				self.gen_turnover()

	def	run(self, sim=0, model=0, test=False):
		"""Run through all agents to test functionality"""
		i = 0
		opdist = [0 for _ in range(self.runtime)]														# TODO see if still needed
		self.visualise_network(self.sim, self.model, self.opinions, self.link_matrix)

		while (not all(self.opinion_dists < 0.003) and i < self.runtime):
			step_opinions = self.opinions.copy()

			self.agents.shuffle_do("remove_neighbours", self._agents)
			self.agents.shuffle_do("find_neighbours")
			self.agents.shuffle_do("change_values", self.rate_valuechange, self.steps_valuechange)
			self.agents.shuffle_do("change_opinion", self.Temp, self.dist_cd, self.tries_op_change)

			# Generational turnover checks
			if self.modeltype == "GenT":
				self.turnover_check()

			self.opinion_dists = 0		# TODO get the opinion distance from this step compared to the previous one

			i += 1
			if i % 5 == 0:
				print(f"Running at {i}")

		form_density_estimate(self.opinions, sim, model)
		self.visualise_network(sim, model, self.opinions, self.link_matrix)