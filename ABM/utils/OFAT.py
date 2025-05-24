"""This module contains the One Factor At a Time (OFAT) class for experimentation on the Generational Opinion Dynamics (GOD) model."""
import numpy as np
import pandas as pd
from src.model_class import OpinionDynamicsModel
from src.agent_class import Individual

class OFAT:
	"""One Factor At a Time (OFAT) class for experimentation on the Generational Opinion Dynamics (GOD) model."""

	def __init__(self, N, num_steps, num_trials):
		self.N = N
		self.num_steps = num_steps
		self.num_trials = num_trials
		self.results = pd.DataFrame(columns=["trial", "step", "opinion", "value", "stubbornness", "persuasiveness"])
		self.trial_results = pd.DataFrame(columns=["trial", "step", "opinion", "value", "stubbornness", "persuasiveness"])

	def run_experiment(self, param_name, param_values):
		"""Run the OFAT experiment for a given parameter."""
		for param_value in param_values:
			print(f"Running experiment with {param_name} = {param_value}")
			self.run_single_experiment(param_name, param_value)
			self.trial_results.to_csv(f"results/{param_name}_{param_value}.csv", index=False)
			self.trial_results = pd.DataFrame(columns=["trial", "step", "opinion", "value", "stubbornness", "persuasiveness"])
			print(f"Results saved to results/{param_name}_{param_value}.csv")
			print(f"Experiment with {param_name} = {param_value} completed.")
			print("--------------------------------------------------")

	def run_single_experiment(self, param_name, param_value):
		"""Run a single experiment with a specific parameter value."""
		for trial in range(self.num_trials):
			print(f"Running trial {trial + 1} for {param_name} = {param_value}")
			model = OpinionDynamicsModel(self.N)
			self.set_parameter(model, param_name, param_value)
			for step in range(self.num_steps):
				model.step()
				self.collect_data(model, trial, step)