from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.parameters import GenT
from src.utils import collect_results, read_counter, write_counter
import numpy as np
from sys import exit

#================================================ PARAMETERS ==================================================================
#							'''For more parameter options check parameters.py'''

saveto 				= "final"
max_runtime			= 100

param_amt 			= 10
sample 				= 100
runs 				= param_amt * sample

#================================================ PARAMETERS ==================================================================

def	run_model(poisson_pick, modelrun):
	model = OpinionDynamicsModel(Individual, params, modelrun)
	model.run(savefigs=(i % 5 == 0), showfigs=False)																			# Save figures every 1/x times
	collect_results(model, modelrun, poisson_pick)
	print(f"{model.modeltype} {modelrun} cat: {model.final_cat} ran with lambda: {poisson_pick} in {model.total_runs} runs")


if __name__=="__main__":
	print("Setting parameters")
	params = GenT(runtime=max_runtime, path=saveto)
	poisson_set = np.linspace(0, 5, param_amt + 1)
	
	i = read_counter()

	print(f"Initiating loop at {i}")
	try:
		while i < runs:
			poisson_pick = round(poisson_set[i // sample], 3)
			run_model(poisson_pick, i)
			i += 1
	except KeyboardInterrupt:
		write_counter(i)
		print(f"Exiting safely at {i}, model not saved")
		exit(0)

	print(f"\nProgram succesfully terminated\n")
	write_counter(0)