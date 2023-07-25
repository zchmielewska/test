import pandas as pd


assumption = dict()
assumption["coverage_features"] = pd.read_csv(
    "./input/assumption/coverage_features.csv",
    index_col=("model", "covg_cd")
)

assumption["mort_riskprem"] = pd.read_csv(
    "./input/assumption/mort_riskprem.csv",
    index_col=("model", "tarcd_rg")
)

assumption["mort_table_res"] = pd.read_csv(
    "./input/assumption/mort_table_res.csv",
    index_col="age"
)

assumption["mort_exp_base"] = pd.read_csv(
    "./input/assumption/mort_exp_base.csv",
    index_col=("gender", "age", "year")
)

assumption["mort_mult_products"] = pd.read_csv(
    "./input/assumption/mort_mult_products.csv",
    index_col="prodboomcd"
)

assumption["experience_factors"] = pd.read_csv(
    "./input/assumption/experience_factors_il_be.csv",
    index_col=("category", "duration", "gender")
)

assumption["inv_ret_fund"] = pd.read_csv(
    "./input/assumption/inv_ret_fund.csv",
    index_col="fund_number"
)
