from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.parameters import Parameters, GenT
import numpy as np

N = 10
runtime = 3
runs = 15
models = 10

if __name__=="__main__":
	print("Setting parameters")
	params = GenT()
	# opinions = np.zeros((runs, N, models))

	print("Initiating model")
	model = OpinionDynamicsModel(N, Individual, params, runtime)
	print("Running model")
	print(model.modeltype)
	model.run()

	# for i in range(models):
	# 	model = OpinionDynamicsModel(N, Individual, params)
	# 	for j in range(runs):
	# 		print(f"Model: {i}, Run: {j}")
	# 		model.run(params.runtime, j, i)
	# 		opinions[j,:,i] = model.opinions			# TODO check if j instead of 1

	# np.save('ABM/results/control_OD_model_results', opinions)