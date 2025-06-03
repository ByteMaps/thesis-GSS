from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.visualisation import form_edges, form_network, form_plot
from time import time

# ================ PARAMETERS ===================================

N = 15

dist_removelink 	= 0.6
prob_removelink 	= 0.15
tries_createlink 	= 10
max_nb 				= 10
dist_createlink 	= 0.4
prob_createlink 	= 0.1
tries_valuechange 	= 10
rate_valuechange 	= 0.05
tries_op_change		= 150
dist_cd				= 1
Temp				= 0.1

# ================ PARAMETERS ===================================

if __name__=="__main__":
	model = OpinionDynamicsModel(N, Individual, dist_createlink, dist_removelink)
	model.run()
	model.create_plot(form_edges, form_network, form_plot)