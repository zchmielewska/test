import pandas as pd

from cashflower import Runplan, ModelPointSet


runplan = Runplan(data=pd.DataFrame({
    "version": [1, 2],
    "portfolio": ["spaarkas", "axent"],
    "valn_year": 2023,
    "valn_month": 3
}))


main = ModelPointSet(data=pd.read_csv("input/202303/model_point/KISS_Koersplan_2023_M03_Policy_IF.CSV"))
coverage = ModelPointSet(data=pd.read_csv("input/202303/model_point/KISS_Koersplan_2023_M03_Coverage_IF.CSV"))
fund = ModelPointSet(data=pd.read_csv("input/202303/model_point/KISS_Koersplan_2023_M03_Fund_IF.CSV"))

assumption = dict()
assumption["ga_investment_fee_parameter"] = pd.read_csv("input/202303/assumptions/ga_investment_fee_parameter.csv", index_col=["name"])
assumption["interest_rates"] = pd.read_csv("input/202303/assumptions/interest_rates_sii_aegon.csv", index_col=["runkey", "scenarioname", "type", "maturityidentifier"])
assumption["inv_ret_fund"] = pd.read_csv("input/202303/assumptions/inv_ret_fund.csv", index_col="fund_number")
assumption["mort_exp_base"] = pd.read_csv("input/202303/assumptions/mort_exp_base.csv", index_col=["gender", "age", "year"])
assumption["mort_riskprem"] = pd.read_csv("input/202303/assumptions/mort_riskprem.csv", index_col=["model", "tarcd_rg"])
assumption["lapse_pp"] = pd.read_csv("input/202303/assumptions/lapse_pp.csv", index_col=["prodboomcd"])
assumption["other_fund_costs"] = pd.read_csv("input/202303/assumptions/other_fund_costs.csv", index_col=["model", "fund_number"])
assumption["pup_rates"] = pd.read_csv("input/202303/assumptions/pup_rates.csv", index_col=["prodboomcd"])
assumption["product_features"] = pd.read_csv("input/202303/assumptions/product_features.csv", index_col=["tarcd"])
assumption["product_features_dal_perc"] = pd.read_csv("input/202303/assumptions/product_features_dal_perc.csv", index_col=["tarcd", "year"])
assumption["ur5_be_bll_maintenance_expenses"] = pd.read_csv(
    "input/202303/assumptions/ur5_be_bll_maintenance_expenses.csv", index_col=["name", "comment"])
assumption["waiverpremium"] = pd.read_csv("input/202303/assumptions/waiverpremium.csv", index_col=["prodboomcd", "policy_year"])
