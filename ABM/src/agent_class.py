import mesa
import numpy as np
from math import exp

class Individual(mesa.Agent):
	"""An agent within the opinion dynamics model."""
	__slots__ = ["link_row", "opinion", "values", "stubbornness", "persuasiveness"] 		# Prevent creating dynamic attributes & save RAM

	def __init__(self, model, unique_id, opinion, values, stubbornness, persuasiveness):
		super().__init__(model)

		self.unique_id 			= unique_id

		self.opinion 			= opinion
		self.values 			= values
		self.stubbornness 		= stubbornness
		self.persuasiveness 	= persuasiveness

		self.link_row 			= model.link_matrix[self.unique_id]

	def	remove_neighbours(self, agentset):														# TODO review agentset use
		"""Remove from link_matrix row on distances"""
		removelink_random = np.random.uniform(0,1,self.model.N)
		for agent in agentset:
			agent_id = agent.unique_id
			if agent_id != self.unique_id:
				if (abs(agent.opinion - self.opinion) >= self.model.dist_removelink) and \
					(removelink_random[agent_id] <= self.model.prob_removelink):
					self.link_row[agent.unique_id] = 0
					agent.link_row[self.unique_id] = 0

	def	find_neighbours(self):
		"""Add to link_matrix row on distances"""
		for i in range(self.model.tries_createlink):
			if sum(self.link_row) < self.model.max_nb:
				agent = self.model.agents_by_id[np.random.randint(0,self.model.N)]
				agent_id = agent.unique_id
				if agent_id != self.unique_id:
					if (abs(agent.opinion - self.opinion) <= self.model.dist_createlink):
						self.link_row[agent.unique_id] = 1
						agent.link_row[self.unique_id] = 1


	def	change_values(self, rate_valuechange, steps_valuechange):
		"""Change the values of the agent based on"""
		for _ in range(steps_valuechange):
			neighbour_values = self.link_row * self.model.values
			denom = sum(abs(neighbour_values) > 0)
			if denom == 0:
				opt_val = 0
			else:
				opt_val = sum(neighbour_values) / denom
			dist = opt_val - self.values
			self.values = self.values + rate_valuechange * dist

	def	change_opinion(self, T, distcd, tries_opinionchange=10):
		"""Change the opinion of the agent based on others"""
		stub_random = np.random.uniform(0,1,tries_opinionchange)
		for i in range(tries_opinionchange):
			if stub_random[i] < 1-self.stubbornness:
				new_op = np.random.rand(1)*2-1
				neighbour_ops = self.model.opinions * self.link_row					# ! improved to self.model.ops, check if correct
				val_dist = abs(self.values - self.model.values)
				val_signs = (self.link_row * (val_dist > distcd)).astype(int)*2		# ! review .astype error, maybe [] works still

				E_old = sum(abs(val_signs - abs(self.opinion * self.link_row - neighbour_ops)) * self.persuasiveness)
				E_new = sum(abs(val_signs - abs(new_op - neighbour_ops)) * self.persuasiveness)
				dH = E_new - E_old
				if dH < 0:
					self.opinion = new_op
				elif stub_random[i] < exp(-dH/T):
					self.opinion = new_op

	def	gen_turnover(self, all_agents):
		"""Reset self parameters & re-establish in space"""
		self.opinion				= np.random.uniform(-1,1,1)
		self.values					= np.random.uniform(-1,1,1)
		self.stubbornness			= np.random.rand(1)
		self.persuasiveness			= np.random.rand(1)
		self.link_row 				= np.zeros(self.model.N, dtype=int)

		for _, agent in all_agents.items():
			agent.link_row[self.unique_id] = 0


	# def	_update_neighbour_opinions(self):
	# 	"""Updates the self neighbour array values"""
	# 	self.neighbour_ops = self.link_row * self.opinion

	# def	_update_neighbour_op_distances(self):
	# 	"""Updates the self neighbour distance array"""
	# 	self.neighbour_dist = abs(self.opinion - self.neighbour_ops)