import mesa
import numpy as np
from scipy.stats import wasserstein_distance
from src.visualisation import *

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, params):
		super().__init__()
		self.N 					= N								# Amount of agents
		self.agents_by_id 		= {}							# Dict of agent objects accessible by unique_id
		self.opinion_dists 		= np.zeros(N)					# TODO check functionality
		self.opinion_dists[-1] 	= 1
		self.sim 				= 0
		self.model				= 0

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
		self.birth_death_prob	= params.birth_death_prob
		self.turnover_tries		= params.turnover_tries	

		# Create agents
		for id in range(self.N):
			agent = Agent(self, id, self.opinions[id], self.values[id], self.stubbornness[id], self.persuasiveness[id])
			self.agents_by_id[id] = agent

	def	visualise_network(self, sim, model, opinions, Lmatrix):
		"""Create a network plot based on a single model run"""
		edges = form_edges(self.N, Lmatrix)
		pos, cmap, G2 = form_network(self.N, edges)

		form_netw_chart(sim, model, self.N, opinions, cmap, G2, pos)

	def	measure_op_dist(self, step_opinions):
		"""Record the opinion distances and measure using wasserstein_dist, save in opinion_dists"""
		self.opinion_dists[:-1] = self.opinion_dists[1::]		# Shift array for new recs
		self.opinion_dists[-1] = wasserstein_distance(self.opinion_dists, step_opinions)

	def	gen_turnover(self):
		"""Pick out a random agent and reset its params"""
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

	def	run(self, runtime, sim, model, test=False, GenT=False):
		"""Run through all agents to test functionality"""
		i = 0
		opdist = [0 for _ in range(runtime)]
		self.visualise_network(self.sim, self.model, self.opinions, self.link_matrix)

		while (not all(self.opinion_dists < 0.003) and i < runtime):
			step_opinions = self.opinions.copy()

			self.agents.shuffle_do("remove_neighbours", self._agents)
			self.agents.shuffle_do("find_neighbours")
			self.agents.shuffle_do("change_values", self.rate_valuechange, self.steps_valuechange)
			self.agents.shuffle_do("change_opinion", self.Temp, self.dist_cd, self.tries_op_change)

			# Generational turnover checks
			self.turnover_check()

			# self.measure_op_dist(step_opinions)
			op_std = round(self.opinions.std(), 4)
			opdist[i] = op_std
			op_eq = np.array_equal(step_opinions, self.opinions)
			i += 1
			if i % 5 == 0:
				print(f"Running at {i} with {op_std} equal ops: {op_eq}")

		form_density_estimate(self.opinions, sim, model)
		measure_opdist(opdist, runtime)
		self.visualise_network(sim, model, self.opinions, self.link_matrix)