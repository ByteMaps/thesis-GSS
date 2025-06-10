from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.parameters import Base, GenT
from src.utils import collect_results, read_counter, write_counter
import numpy as np
from sys import exit

N = 100
runtime = 50

param_amt = 10
sample = 1_000
runs = param_amt * sample

def	run_model(param, i):
	model = OpinionDynamicsModel(N, Individual, params, runtime, i)
	model.run(savefigs=(i % 100 == 0), showfigs=False)
	collect_results(model, i, poisson_pick)
	print(f"{model.modeltype} {i} cat: {model.final_cat} ran with lambda: {poisson_pick} in {model.total_runs} runs")
	del model

if __name__=="__main__":
	print("Setting parameters")
	params = GenT()
	gent_set = np.linspace(0, 5, param_amt)
	
	i = read_counter()
	print(f"Initiating loop at {i}")
	try:
		while i < runs:
			poisson_pick = round(gent_set[i // sample], 3)
			run_model(poisson_pick, i)
			i += 1
	except KeyboardInterrupt:
		write_counter(i)
		print(f"Exiting safely at {i-1}")
		exit(0)

	print(f"\nProgram succesfully terminated\n")
		