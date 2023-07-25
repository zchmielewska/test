from cashflower import assign, ModelVariable

from fundplan.modelpoint import policy


VALUATION_YEAR = 2021
VALUATION_MONTH = 12


age = ModelVariable(modelpoint=policy)
elapsed_months = ModelVariable(modelpoint=policy, time_dep=False)


@assign(age)
def age_formula(t):
    age_issue = policy.get("AGE_ISS_1")
    return round(age_issue + (t - 1 + elapsed_months()) / 12, 2)


@assign(elapsed_months)
def elapsed_months_formula():
    issue_year = policy.get("ISS_YR")
    issue_month = policy.get("ISS_MTH")
    return (VALUATION_YEAR - issue_year) * 12 + (VALUATION_MONTH + 1 - issue_month)
