import pandas as pd
from statsmodels.multivariate.manova import MANOVA

data = pd.read_csv("ABM/results/gent_module/results.csv")
# data = pd.select_dtypes(["int64", "float64"])

control_var = "GenTlambda"
dep_vars = [col for col in data.columns if col != control_var]

formula = f"{" + ".join(dep_vars)} ~ {control_var}"
manova = MANOVA.from_formula(formula, data=data)

print(manova.mv_test())