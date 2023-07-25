import pandas as pd

from cashflower import Runplan, ModelPoint


runplan = Runplan(data=pd.DataFrame({
    "version": [1],
    "valuation_year": [2022],
    "valuation_month": [6]
}))


policy = ModelPoint(data=pd.read_csv("./input/modelpoint/Policy_annuity_2022_M06_IF.csv"))
coverage = ModelPoint(data=pd.read_csv("./input/modelpoint/Coverage_annuity_2022_M06_IF.csv"))


assumption = dict()
assumption["mort_exp_base"] = pd.read_csv(
    "./input/assumptions/mort_exp_base.csv",
    index_col=("gender", "age", "year")
)


assumption["experience_factors_il_be"] = pd.read_csv(
    "./input/assumptions/experience_factors_il_be.csv",
    index_col=("category", "duration", "gender")
)


assumption["interest_rates"] = pd.read_csv(
    "./input/assumptions/interest_rates_sii_aegon.csv",
    index_col=("runkey", "scenarioname", "type", "maturityidentifier")
)


assumption["inflation"] = pd.read_csv(
    "./input/assumptions/interest_rates_market.csv",
    index_col=("runkey", "scenarioname", "type", "maturityidentifier")
)


assumption["ur5_be_bll_maintenance_expenses"] = pd.read_csv(
    "./input/assumptions/ur5_be_bll_maintenance_expenses.csv",
    index_col=("name", "comment")
)


assumption["ga_investment_fee_parameter"] = pd.read_csv(
    "./input/assumptions/ga_investment_fee_parameter.csv",
    index_col=("name", )
)

