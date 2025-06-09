from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.parameters import Base, GenT
from src.utils import collect_results

N = 100
runtime = 50

runs = 1_000


if __name__=="__main__":
	print("Setting parameters")
	params = Base()
	print("Initiating loop")
	i = 0
	while i < runs:
		model = OpinionDynamicsModel(N, Individual, params, runtime, i)
		category = model.run(savefigs=True)
		# collect_results(model, i, category)
		print(f"Run {model.modeltype}-{i} successful with {model.total_runs}")
		del model
		i += 1
		
	print("\nProcess completed succesfully\n")