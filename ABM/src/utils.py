import numpy as np
import matplotlib.pyplot as plt
from os import path, makedirs
import csv

def	measure_opdist(opdist):
	"""Visualise the average opinion distance over time in a simple plot"""
	plt.figure()
	plt.xlabel("timestep")
	plt.ylabel("avg opinion distance")
	y = [i for i in range(len(opdist))]
	plt.plot(y, opdist)
	plt.show()

def	assign_categories(amt_peaks, opinions):
	"""Assign categories: If the opinion distribution has 
	 - 1 peak and a low variance 	-->		consensus state, 
	 - 1 peak and a high variance	-->		co-existence state, 
	 - more than 2 peaks			-->		polarized state."""

	if amt_peaks == 1:
		if np.var(opinions) < 0.05:
			return 0
		else:
			return 1
	elif amt_peaks == 2:
		return 2
	else:
		return 3

def	collect_results(Model, modelrun, poisson_lamb):
	"""Collect statistics for each model round, pass it to CSV saver"""
	OP_mean = round(np.mean(Model.opinions), 5)
	OP_variance = round(np.var(Model.opinions), 5)
	unity = np.sum(Model.link_matrix) / 2

	payload = (modelrun, Model.final_cat, OP_mean, OP_variance, unity, poisson_lamb)
	save_as_csv(Model.path, "results.csv", payload)

def	save_as_csv(filepath, filename, data, headers=["modelrun", "category", "OPmean", "OPvariance", "unity", "GenTlambda"]):
	"""Save data as a CSV file"""
	makedirs(f"{filepath}", exist_ok=True)
	file_exists = path.isfile(f"{filepath}{filename}")
	
	with open(f"{filepath}{filename}", 'a', newline='') as file:
		writer = csv.writer(file)
		if not file_exists:
			writer.writerow(headers)
		writer.writerow(data)

def	get_parameters(amt, max, min):
	"""Get the parameter results over a specified interval"""
	return np.linspace(min, max, amt)