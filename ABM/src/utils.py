import numpy as np
import matplotlib.pyplot as plt
from os import makedirs, path
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

def	collect_results(model, modelrun, category):
	"""Collect statistics for each model round, pass it to CSV saver"""
	OP_mean = round(np.mean(model.opinions), 5)
	OP_variance = round(np.var(model.opinions), 5)
	unity = np.sum(model.link_matrix) / 2

	payload = (modelrun, category, OP_mean, OP_variance, unity)
	save_as_csv("ABM/results/results.csv", payload)

def	save_as_csv(filename, data, headers=["modelrun", "category", "OPmean", "OPvariance", "unity"]):
	"""Save data as a CSV file"""
	file_exists = path.isfile(filename)
	
	with open(filename, 'a', newline='') as file:
		writer = csv.writer(file)
		if not file_exists:
			writer.writerow(headers)
		writer.writerow(data)