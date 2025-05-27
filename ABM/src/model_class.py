import mesa
import numpy as np

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, individual_agent, dist_createlink, dist_removelink):
		super().__init__()
		self.num_agents = N
		self.opinions = np.empty(N)

		# Create agents
		for _ in range(self.num_agents):
			agent = individual_agent(self, dist_createlink, dist_removelink)

	def	run(self):
		"""Run through all agents to test functionality"""
		for agent in self.agents:																						# TODO multiproc
			print(f"Agent {agent.unique_id} with {agent.opinion} has neighbours {agent.find_neighbours(self.agents)}")
		exit()
		