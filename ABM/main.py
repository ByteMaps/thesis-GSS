from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.parameters import Base, GenT
from src.utils import collect_results
import numpy as np

N = 100
runtime = 50

param_amt = 10
runs = 10_000

if __name__=="__main__":
	print("Setting parameters")
	params = GenT()
	gent_set = np.linspace(0, 3, param_amt)
	index = 0
	print("Initiating loop")
	for gent_param in gent_set:
		i = 0
		params.poisson_avg = gent_param
		while i < (runs/param_amt):
			model = OpinionDynamicsModel(N, Individual, params, runtime, index)
			model.run(savefigs=(i % 100 == 0))											# Run model, save 1/10 figs
			collect_results(model, index, gent_param)

			print(f"Run {model.modeltype}-{index} lambda: {gent_param} successful with {model.total_runs} runs")
			del model
			i += 1
			index += 1
		
	print("\nProcess completed succesfully\n")