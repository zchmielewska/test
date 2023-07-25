import pandas as pd

from cashflower import Runplan, ModelPoint


runplan = Runplan(data=pd.DataFrame({
    "version": [1],
    "valuation_year": [2021],
    "valuation_month": [12]
}))


policy = ModelPoint(data=pd.read_csv("./input/202112/modelpoint/Axent_2021_M12_Policy_IF_10.csv")[1:2])
fund = ModelPoint(data=pd.read_csv("./input/202112/modelpoint/Axent_2021_M12_Fund_IF.csv"))
coverage = ModelPoint(data=pd.read_csv("./input/202112/modelpoint/Axent_2021_M12_Coverage_IF.csv"))
charge = ModelPoint(data=pd.read_csv("./input/202112/modelpoint/Axent_2021_M12_Charge_IF.csv"))


assumption = dict()
assumption["experience_factors_il_be"] = pd.read_csv(
    "./input/202112/assumption/experience_factors_il_be.csv",
    index_col=("category", "duration", "gender"))

assumption["inv_ret_fund"] = pd.read_csv(
    "./input/202112/assumption/inv_ret_fund.csv",
    index_col="FUND_NUMBER")

assumption["interest_rates"] = pd.read_csv(
    "./input/202112/assumption/interest_rates.csv",
    index_col=("runkey", "scenarioname", "type", "maturityidentifier"))

assumption["lapse_mult_age"] = pd.read_csv(
    "./input/202112/assumption/lapse_mult_age.csv",
    index_col=("prodboomcd", "age"))

assumption["lapse_mult_remyrs"] = pd.read_csv(
    "./input/202112/assumption/lapse_mult_remyrs.csv",
    index_col=("prodboomcd", "remaining_years"))

assumption["lapse_pp"] = pd.read_csv(
    "./input/202112/assumption/lapse_pp.csv",
    index_col="prodboomcd")

assumption["mort_exp_base"] = pd.read_csv(
    "./input/202112/assumption/mort_exp_base.csv",
    index_col=("gender", "age", "year"))

assumption["other_fund_costs"] = pd.read_csv(
    "./input/202112/assumption/other_fund_costs.csv")

assumption["product_features"] = pd.read_csv(
    "./input/202112/assumption/product_features.csv",
    index_col="tarcd")

assumption["product_features_dal_deffer"] = pd.read_csv(
    "./input/202112/assumption/product_features_dal_deffer.csv",
    index_col=("tarcd", "year"))

assumption["product_features_dal_perc"] = pd.read_csv(
    "./input/202112/assumption/product_features_dal_perc.csv",
    index_col=("tarcd", "year"))

assumption["pup_mult_polyr"] = pd.read_csv(
    "./input/202112/assumption/pup_mult_polyr.csv",
    index_col="prodboomcd")

assumption["pup_mult_prem"] = pd.read_csv(
    "./input/202112/assumption/pup_mult_prem.csv",
    index_col="prodboomcd")

# assumption["pup_rates"] = pd.read_csv(
#     "./input/assumption/pup_rates.csv",
#     index_col="prodboomcd")

assumption["sa_management_fee_and_rebate_bll"] = pd.read_csv(
    "./input/202112/assumption/sa_management_fee_and_rebate_bll.csv",
    index_col="number")
