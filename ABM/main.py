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

if __name__=="__main__":
	print("Setting parameters")
	params = GenT()
	gent_set = np.linspace(0, 5, param_amt)
	
	i = read_counter()
	# gent_index = 0
	print(f"Initiating loop at {i}")
	try:
		while i < runs:
			poisson_pick = gent_set[i // sample]

			model = OpinionDynamicsModel(N, Individual, params, runtime, i)
			model.run(savefigs=(i % 100 == 0), showfigs=False)														# Save 1/10 figures
			collect_results(model, i, poisson_pick)

			print(f"{model.modeltype} {i} ran with lambda: {poisson_pick} in {model.total_runs} runs")
			i += 1
			write_counter(i)
	except KeyboardInterrupt:
		print(f"Exiting safely at {i-1}")
		exit(0)

	print("\nProcess completed succesfully\n")

	# while gent_index in range(len(gent_set)):
	# 	params.poisson_avg = gent_set[i % (runs/param_amt)]
	# 	while i < (runs/param_amt):
	# 		model = OpinionDynamicsModel(N, Individual, params, runtime, index)
	# 		model.run(savefigs=False)#(i % 100 == 0))											# Run model, save 1/10 figs
	# 		# collect_results(model, index, gent_set[gent_index])

	# 		print(f"Run {model.modeltype}-{index} lambda: {gent_set[gent_index]} successful with {model.total_runs} runs")
	# 		del model
	# 		i += 1
	# 		index += 1
		