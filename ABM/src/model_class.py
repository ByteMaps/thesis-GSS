import mesa
import numpy as np
from scipy.stats import wasserstein_distance
from src.visualisation import *
from src.utils import *

class OpinionDynamicsModel(mesa.Model):

	def __init__(self, Agent, params, model=0):
		super().__init__()
		self.N 					= params.N							# Amount of agents
		self.modelrun			= model								# Model id
		self.runtime			= params.runtime
		self.modeltype			= type(params).__name__ 
		self.link_matrix		= np.zeros((self.N,self.N), dtype=int)
		self.path				= params.savepath

		self.opinions			= np.random.uniform(-1,1,self.N)		# np array with generated opinions
		self.values				= np.random.uniform(-1,1,self.N)		# np array with generated values
		self.stubbornness		= np.random.rand(self.N)
		self.persuasiveness		= np.random.rand(self.N)

		# Base parameters
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
		self.poisson_range	    = np.random.poisson(params.poisson_avg, size=self.runtime)

		# Create agents
		self.agents_by_id 		= {}									# Dict of agent objects accessible by unique_id
		for id in range(self.N):
			agent = Agent(self, id, self.opinions[id], self.values[id], self.stubbornness[id], self.persuasiveness[id])
			self.agents_by_id[id] = agent

		# Monitor matrices
		self.opinion_dists 		= np.zeros(10)							# array of wasserstein op dist
		self.opinion_dists[-1]	= 1										# Circumvent main while loop first
		self.opinion_hist		= np.zeros(self.N)						# 1D matrix of last opinions

		self.total_runs			= 0
		self.final_cat			= "N"


	def turnover_check(self, i):
		"""Attempt turnover_tries times to implement GenT"""

		for _ in range(self.poisson_range[i]):
			random_id = np.random.randint(0,self.N)
			self.agents_by_id[random_id].gen_turnover(self.agents_by_id)


	def	agents_shuffle(self):
		"""Randomise model events for AgentSet"""

		self.agents.shuffle_do("remove_neighbours", self._agents)
		self.agents.shuffle_do("find_neighbours")
		self.agents.shuffle_do("change_values", self.rate_valuechange, self.steps_valuechange)
		self.agents.shuffle_do("change_opinion", self.Temp, self.dist_cd, self.tries_op_change)
		for id, agent in self.agents_by_id.items():													# ? ugly, but looks like it works?
			self.opinions[id] = agent.opinion														# Update opinions matrix


	def	run(self, savefigs=False, showfigs=False):
		"""Run through all agents to test functionality"""
		i = 0
		if not(showfigs):
			matplotlib.use('Agg')																								# Prevent image generation

		while (not(all(self.opinion_dists < 0.003)) and i < self.runtime):
			
			self.agents_shuffle()

			self.turnover_check(i)																								# Generational turnover check

			if self.runtime > 100 and i % 10 == 0:																				# Check progress for longer runtimes
				print(f"Step {i} - avg dist: {round(np.mean(self.opinion_dists), 3)}, Opinion std: {round(np.std(self.opinions),3)}")

			i += 1
			self.total_runs += 1
			self.opinion_dists[:-1] = self.opinion_dists[1::]
			self.opinion_dists[-1] = round(wasserstein_distance(self.opinion_hist, self.opinions),5)							# Calc distance
			self.opinion_hist = self.opinions.copy()

		self.final_cat = form_density_estimate(self.modeltype, self.opinions, self.modelrun, self.path, savefigs, showfigs)
		visualise_network(self.modeltype, self.modelrun, self.N, self.opinions, \
					 		self.link_matrix, self.final_cat, self.path, savefigs, showfigs)