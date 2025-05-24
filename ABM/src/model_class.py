import mesa
from mesa import Model
from agent_class import Individual

class OpinionDynamicsModel(Model):
	"""A model with some number of agents."""
	def __init__(self, N):				# TODO : Add parameters for the model
		super().__init__()
		self.num_agents = N
		