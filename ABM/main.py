from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.parameters import Parameters
import numpy as np

N = 100
runs = 15
models = 10

if __name__=="__main__":
	params = Parameters()
	opinions = np.zeros((runs, N, models))

	for i in range(models):
		model = OpinionDynamicsModel(N, Individual, params)
		for j in range(runs):
			print(f"Model: {i}, Run: {j}")
			model.run(params.runtime, j, i)
			opinions[1,:,i] = model.opinions

	np.save('ABM/results/control_OD_model_results', opinions)