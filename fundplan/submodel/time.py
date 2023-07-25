from fundplan.submodel.common import *


VALUATION_YEAR = 2021
VALUATION_MONTH = 12

cal_month = ModelVariable(modelpoint=policy, pol_dep=False)
cal_year = ModelVariable(modelpoint=policy, pol_dep=False)
pol_month = ModelVariable(modelpoint=policy)
pol_year = ModelVariable(modelpoint=policy)


@assign(cal_month)
def cal_month_formula(t):
    if t == 0:
        return VALUATION_MONTH
    else:
        if cal_month(t-1) == 12:
            return 1
        else:
            return cal_month(t-1)+1


@assign(cal_year)
def cal_year_formula(t):
    if t == 0:
        return VALUATION_YEAR
    else:
        if cal_month(t-1) == 12:
            return cal_year(t-1) + 1
        else:
            return cal_year(t-1)


@assign(pol_month)
def pol_month_formula(t):
    if t == 0:
        if elapsed_months() == 0:
            return 0
        reminder = elapsed_months() % 12
        return 12 if reminder == 0 else reminder
    else:
        if pol_month(t-1) == 12:
            return 12
        else:
            return pol_month(t-1) + 1


@assign(pol_year)
def pol_year_formula(t):
    if t == 0:
        return elapsed_months() // 12
    else:
        if pol_month(t-1) == 12:
            return pol_year(t-1) + 1
        else:
            return pol_year(t-1)

