class Base:
	def	__init__(self, runtime=100, N=100, path="base"):
		self.savepath				= f"ABM/results/{path}/"
		self.runtime				= runtime
		self.N						= N

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


class GenT(Base):
	def	__init__(self, runtime=100, N=100, path="gent_module"):
		super().__init__()
		self.poisson_avg			= 0.1

		self.runtime				= runtime
		self.N						= N
		self.savepath				= f"ABM/results/{path}/"

if __name__=="__main__":
	testparam = GenT()
	print(testparam.savepath)