from src.agent_class import Individual
from src.model_class import OpinionDynamicsModel

# ================ PARAMETERS ===================================
N = 10

dist_removelink = 0.6
dist_createlink = 0.4

# ================ PARAMETERS ===================================

if __name__=="__main__":
	model = OpinionDynamicsModel(N, Individual, dist_createlink, dist_removelink)
	model.run()