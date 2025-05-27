import mesa
import numpy as np

class OpinionDynamicsModel(mesa.Model):
	"""A model with some number of agents."""
	def __init__(self, N, Agent, dist_createlink, dist_removelink):
		super().__init__()
		self.num_agents = N

		# Create agents
		for i in range(self.num_agents):
			agent = Agent(self, i, dist_createlink=dist_createlink, dist_removelink=dist_removelink)

	def	run(self):
		"""Run through all agents to test functionality"""
		
		agents_opinions = [agent.linked_agents for agent in self.agents]
		print(agents_opinions)