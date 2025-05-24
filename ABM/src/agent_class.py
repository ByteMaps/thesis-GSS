import mesa
from mesa import Agent

class Individual(mesa.Agent):
	"""An agent within the opinion dynamics model."""
	__slots__ = ["opinion", "values", "stubbornness", "persuasiveness"] 				# Prevent creating dynamic attributes & save RAM

	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)

		self.opinion = self.random.random(-1,1)
		self.values = self.random.random(-1,1)
		self.stubbornness = self.random.random(0,1)
		self.persuasiveness = self.random.random(0,1)

	def change_value(self, new_value):
		"""Change the agent's value to a new value."""
		pass

	def change_opinion(self, new_opinion):
		"""Change the agent's opinion to a new opinion."""
		pass