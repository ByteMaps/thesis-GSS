from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel
from src.visualisation import form_edges, form_network, form_plot
from src.parameters import Parameters

N = 15

if __name__=="__main__":
	params = Parameters()
	model = OpinionDynamicsModel(N, Individual, params)
	model.run()
	model.create_plot(form_edges, form_network, form_plot)