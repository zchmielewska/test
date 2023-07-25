import pandas as pd

from cashflower import ModelPoint

policy = ModelPoint(data=pd.read_csv("./input/modelpoint/Policy_FundPlan_2021_M12_IF_1pol.csv"))
fund = ModelPoint(data=pd.read_csv("./input/modelpoint/Fund_FundPlan_2021_M12_IF_1pol.csv"))
coverage = ModelPoint(data=pd.read_csv("./input/modelpoint/Coverage_FundPlan_2021_M12_IF_1pol.csv"))
