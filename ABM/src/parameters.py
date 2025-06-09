class Base:
	def	__init__(self):
		self.dist_removelink 		= 0.6
		self.prob_removelink 		= 0.1

		self.tries_createlink 		= 10
		self.max_nb 				= 10

		self.dist_createlink 		= 0.2
		self.prob_createlink 		= 0.1

		self.steps_valuechange 		= 10
		self.rate_valuechange 		= 0.05
		self.tries_op_change		= 150
		self.dist_cd				= 1
		self.Temp					= 0.1

		self.savepath				= "ABM/results/tests/"

class GenT(Base):
	def	__init__(self):
		super().__init__()
		self.poisson_avg			= 0.1							# Range 0.1 to 10

		self.savepath				= "ABM/results/gent_module/"

if __name__=="__main__":
	testparam = GenT()
	print(testparam.savepath)