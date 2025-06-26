from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.parameters import GenT
from src.utils import collect_results, read_counter, write_counter
import numpy as np
from sys import exit
import psutil, datetime, time

#================================================ PARAMETERS ==================================================================
#							'''For more parameter options check parameters.py'''

saveto 				= "removedist_runtime_checks"
max_runtime			= 1000

total_runs			= 10
param_amt 			= 10																	# Amount of different parameters to run
sample 				= 100
# poisson_set 		= np.linspace(0, 1, param_amt + 1)
runs 				= 100 * sample

#================================================ PARAMETERS ==================================================================

def	run_model(params, modelrun):
	model = OpinionDynamicsModel(Individual, params, modelrun)
	model.run(savefigs=(i % 20 == 0), showfigs=False)																			# Save figures every 1/5 times
	collect_results(model, modelrun, params.poisson_avg)
	print(f"{model.modeltype} {modelrun} cat: {model.final_cat} ran with lambda: {params.poisson_avg} in {model.total_runs} runs")

def	check_usage(filepath):
	"""Log the CPU usage every run"""
	if not hasattr(psutil, "sensors_battery"):
		pass
	
	cpu_usage = psutil.cpu_percent(interval=1)
	timestamp = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	with open(filepath, 'a') as file:
		file.write(f"{timestamp} ---- {cpu_usage}%\n")


if __name__=="__main__":
	print("Setting parameters")
	params = GenT(runtime=max_runtime, path=saveto)
	params.dist_removelink = 2.0								# ! Consensus test
	
	i = read_counter()

	print(f"Initiating loop at {i}")
	try:
		while i < total_runs:
			poisson_pick = 0 # round(np.random.rand(),3) #round(poisson_set[i // sample], 3) # ! Consensus test
			params.poisson_avg = poisson_pick
			run_model(params, i)
			# check_usage('usage.csv')
			i += 1
	except KeyboardInterrupt:
		write_counter(i)
		print(f"Exiting safely at {i}, model not saved")
		exit(0)

	print(f"\nProgram succesfully terminated\n")
	write_counter(0)
	exit(1)