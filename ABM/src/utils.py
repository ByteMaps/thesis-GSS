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
	 - 1 peak and a low variance 	-->		0. consensus state
	 - 1 peak and a high variance	-->		1. co-existence state
	 - 2+ peaks						-->		2. polarized state"""

	if amt_peaks == 1:
		if np.var(opinions) < 0.05:
			return 0
		else:
			return 1
	else:
		return 2


def	collect_results(Model, modelrun, poisson_lamb):
	"""Collect statistics for each model round, pass it to CSV saver"""
	OP_mean = round(np.mean(Model.opinions), 5)
	OP_variance = round(np.var(Model.opinions), 5)
	unity = np.sum(Model.link_matrix) / 2

	payload = (modelrun, Model.final_cat, OP_mean, OP_variance, unity, poisson_lamb, Model.total_runs)
	save_as_csv(Model.path, "results.csv", payload)


def	save_as_csv(filepath, filename, data, headers=["Modelrun", "Category", "OPmean", "OPvariance", "Unity", "GenTlambda", "Runs"]):
	"""Save data as a CSV file"""
	makedirs(f"{filepath}", exist_ok=True)
	file_exists = path.isfile(f"{filepath}{filename}")
	
	with open(f"{filepath}{filename}", 'a', newline='') as file:
		writer = csv.writer(file)
		if not file_exists:
			writer.writerow(headers)
		writer.writerow(data)


def	read_counter(file="ABM/counter.txt"):
	"""Get the current cycle num from textfile"""
	if path.exists(file):
		with open(file, 'r') as file:
			return int(file.read())
	else:
		return 0


def	write_counter(index, file="ABM/counter.txt"):
	"""Set the last full cycle num in textfile"""
	if path.exists(file):
		with open(file, 'w') as file:
			file.write(str(index))