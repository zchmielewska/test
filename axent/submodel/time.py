import math

from cashflower import assign, ModelVariable, Parameter

from axent.input import policy, runplan


elapsed_months = Parameter(modelpoint=policy)
@assign(elapsed_months)
def elapsed_months_formula():
    iss_yr = policy.get("iss_yr")
    iss_mth = policy.get("iss_mth")
    return (runplan.get("valuation_year") - iss_yr) * 12 + (runplan.get("valuation_month") + 1 - iss_mth)


policy_maturity_period = Parameter(modelpoint=policy)
@assign(policy_maturity_period)
def policy_maturity_period_formula():
    return policy.get("ben_term_k") - elapsed_months()


age = ModelVariable(modelpoint=policy)
@assign(age)
def age_formula(t):
    if t == 0:
        return math.floor(policy.get("age_iss_1") + elapsed_months() / 12)
    if pol_month(t-1) == 12:
        return age(t-1)+1
    return age(t-1)


pol_month = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(pol_month)
def pol_month_formula(t):
    if t == 0:
        mnth = elapsed_months() % 12
        mnth = 12 if mnth == 0 else mnth
        return mnth
    if pol_month(t-1) == 12:
        return 1
    return pol_month(t-1) + 1


pol_year = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(pol_year)
def pol_year_formula(t):
    if t == 0:
        math.floor((elapsed_months() - 1.0) / 12.0) + 1.0
    if pol_month(t) == 1:
        return pol_year(t-1) + 1
    return pol_year(t-1)


cal_month = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(cal_month)
def cal_month_formula(t):
    if t == 0:
        return runplan.get("valuation_month")

    if cal_month(t-1)+1 == 13:
        return 1
    else:
        return cal_month(t-1)+1


cal_year = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(cal_year)
def cal_year_formula(t):
    if t == 0:
        return runplan.get("valuation_year")

    if cal_month(t-1) == 12:
        return cal_year(t-1) + 1

    return cal_year(t-1)
