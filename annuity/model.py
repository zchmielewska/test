import math

from cashflower import assign, ModelVariable, Parameter

from annuity.input import assumption, policy, runplan, coverage
from annuity.utils import get_duration, get_month, freq_to_int


VALUATION_YEAR = 2022
VALUATION_MONTH = 6


cal_month = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(cal_month)
def cal_month_formula(t):
    if t == 0:
        return VALUATION_MONTH
    elif (cal_month(t-1) + 1) % 12 == 1:
        return 1
    else:
        return cal_month(t-1) + 1


cal_year = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(cal_year)
def cal_year_formula(t):
    if t == 0:
        return VALUATION_YEAR
    elif cal_month(t) == 1:
        return cal_year(t-1)+1
    else:
        return cal_year(t-1)


proj_month = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(proj_month)
def proj_month_formula(t):
    if t == 0:
        return 0
    elif t % 12 == 1:
        return 1
    else:
        return proj_month(t-1) + 1


proj_year = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(proj_year)
def proj_year_formula(t):
    if t == 0:
        return 0
    elif t % 12 == 1:
        return proj_year(t-1) + 1
    else:
        return proj_year(t-1)


yearly_forward_rate = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(yearly_forward_rate)
def yearly_forward_rate_formula(t):
    if t == 0:
        return 0
    return assumption["interest_rates"].loc[("Quarterly_SII_with_Group_VA", "SII_T_base", "monthlyforward", str(t) + "M")]["rate"]


forward_rate = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(forward_rate)
def forward_rate_formula(t):
    return (1 + yearly_forward_rate(t)) ** (1 / 12) - 1


v_month_ev = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(v_month_ev)
def v_month_ev_formula(t):
    return 1/(1+forward_rate(t))


inflation_rate = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(inflation_rate)
def inflation_rate_formula(t):
    if t == 0:
        return 0
    yearly_rate = assumption["inflation"].loc[("Daily", "HICP", "spot", str(t) + "M")]["rate"]
    return (1 + yearly_rate) ** (1 / 12) - 1


inflation_rate_expenses = ModelVariable(modelpoint=policy, pol_dep=False)
@assign(inflation_rate_expenses)
def inflation_rate_expenses_formula(t):
    if t == 0:
        return 1
    return inflation_rate_expenses(t-1) * (1+inflation_rate(t-1))


age = ModelVariable(modelpoint=policy)
@assign(age)
def age_formula(t):
    if t == 0:
        age_iss_1 = policy.get("AGE_ISS_1")
        return round(age_iss_1 + elapsed_months(t) / 12)
    elif t % 12 == 0:
        return age(t-1) + 1
    else:
        return age(t-1)


elapsed_months = Parameter(modelpoint=policy)
@assign(elapsed_months)
def elapsed_months_formula():
    iss_yr = policy.get("ISS_YR")
    iss_mth = policy.get("ISS_MTH")
    return (VALUATION_YEAR-iss_yr) * 12 + (VALUATION_MONTH + 1 - iss_mth)


remaining_period = Parameter(modelpoint=policy)
@assign(remaining_period)
def remaining_period_formula():
    return policy.get("BEN_TERM") - elapsed_months(0)


pol_month = ModelVariable(modelpoint=policy)
@assign(pol_month)
def pol_month_formula(t):
    if t == 0:
        return get_month(elapsed_months(t))
    elif pol_month(t-1) == 12:
        return 1
    else:
        return pol_month(t-1) + 1


pol_year = ModelVariable(modelpoint=policy)
@assign(pol_year)
def pol_year_formula(t):
    if t == 0:
        return math.floor((elapsed_months(t) - 1) / 12) + 1
    elif pol_month(t) == 1:
        return pol_year(t-1) + 1
    else:
        return pol_year(t-1)


sex = Parameter(policy)
@assign(sex)
def sex_formula():
    return "Females" if policy.get("SEX_1") == "F" else "Males"


death_rate = ModelVariable(modelpoint=policy)
@assign(death_rate)
def death_rate_formula(t):
    if age(t) >= 120:
        return 1
    if age(t) == age(t-1) and cal_year(t) == cal_year(t-1):
        return death_rate(t-1)
    return assumption["mort_exp_base"].loc[(sex(), age(t), cal_year(t))]["value"]


duration = ModelVariable(modelpoint=policy)
@assign(duration)
def duration_formula(t):
    if pol_year(t) == pol_year(t-1):
        return duration(t-1)
    return get_duration(pol_year(t))


mort_mult = ModelVariable(modelpoint=policy)
@assign(mort_mult)
def mort_mult_formula(t):
    if duration(t) == duration(t-1):
        return mort_mult(t-1)
    return assumption["experience_factors_il_be"].loc[("LYF", duration(t), sex())]["value"]


death_rate_1_exp = ModelVariable(modelpoint=policy)
@assign(death_rate_1_exp)
def death_rate_1_exp_formula(t):
    if age(t) >= 120:
        return 1
    return death_rate(t) * mort_mult(t)


death_rate_exp = ModelVariable(modelpoint=policy)
@assign(death_rate_exp)
def death_rate_exp_formula(t):
    return 1 - (1-death_rate_1_exp(t))**(1/12)


surv_per = ModelVariable(modelpoint=policy)
@assign(surv_per)
def surv_per_formula(t):
    return 1 - death_rate_exp(t)


surv = ModelVariable(modelpoint=policy)
@assign(surv)
def surv_formula(t):
    return surv_pup(t)


policies_b = ModelVariable(modelpoint=policy)
@assign(policies_b)
def policies_b_formula(t):
    return surv(t-1)


surv_pup = ModelVariable(modelpoint=policy)
@assign(surv_pup)
def surv_pup_formula(t):
    if t == 0:
        return 1
    else:
        return surv_pup(t-1) * surv_per(t)


annuity_pmt_annual = ModelVariable(modelpoint=coverage)
@assign(annuity_pmt_annual)
def annuity_pmt_annual_formula(t):
    if t == 0:
        return coverage.get("ANN_BEF")

    index_perc = 1
    index_amount = 0

    if pol_month(t) == 0 and t > 1:
        index_perc = 1 + coverage.get("ANN_INC_PC")/100
        index_amount = coverage.get("ANN_INC_AM")

    return annuity_pmt_annual(t-1) * index_perc + index_amount


annuity_pmt_if = ModelVariable(modelpoint=coverage)
@assign(annuity_pmt_if)
def annuity_pmt_if_formula(t):
    return annuity_pmt_annual(t) * surv_pup(t)


freq = Parameter(modelpoint=policy)
@assign(freq)
def freq_formula():
    prem_freq = policy.get("PREM_FREQ")
    return freq_to_int(prem_freq)


annuity_pmt = ModelVariable(modelpoint=coverage)
@assign(annuity_pmt)
def annuity_pmt_formula(t):
    if pol_month(t) % (12 / freq()) == 0:
        return annuity_pmt_if(t) / freq()
    return 0


claim_annuity = ModelVariable(modelpoint=policy)
@assign(claim_annuity)
def claim_annuity_formula(t):
    result = 0
    for c in range(coverage.size):
        result += annuity_pmt(t, c)
    return result


pv_benefit_total = ModelVariable(modelpoint=policy)
@assign(pv_benefit_total)
def pv_benefit_total_formula(t):
    if t > remaining_period():
        return 0
    return (claim_annuity(t) + pv_benefit_total(t+1)) * v_month_ev(t)


exp_ren_fix = ModelVariable(modelpoint=policy, pol_dep=False, time_dep=False)
@assign(exp_ren_fix)
def exp_ren_fix_formula():
    return assumption["ur5_be_bll_maintenance_expenses"].loc[("Cost per policy - MoSes", "SF")]["value"]


expense_ren = ModelVariable(modelpoint=policy)
@assign(expense_ren)
def expense_ren_formula(t):
    return exp_ren_fix(t) / 12 * policies_b(t) * surv_per(t) * inflation_rate_expenses(t)


pv_exp_comm_total = ModelVariable(modelpoint=policy)
@assign(pv_exp_comm_total)
def pv_exp_comm_total_formula(t):
    if t > remaining_period():
        return 0
    return (expense_ren(t) + pv_exp_comm_total(t+1)) * v_month_ev(t)


exp_ga_ic_fee = ModelVariable(modelpoint=policy, pol_dep=False, time_dep=False)
@assign(exp_ga_ic_fee)
def exp_ga_ic_fee_formula():
    return assumption["ga_investment_fee_parameter"].loc["ga_investment_cost_yearly"]["value"]


expense_fee = ModelVariable(modelpoint=policy)
@assign(expense_fee)
def expense_fee_formula(t):
    return exp_ga_ic_fee(t) / (10**4 * 12) * (pv_benefit_total(t) + pv_exp_comm_total(t))


pv_inv_cost_total = ModelVariable(modelpoint=policy)
@assign(pv_inv_cost_total)
def pv_inv_cost_total_formula(t):
    if t > remaining_period():
        return 0
    return (expense_fee(t) + pv_inv_cost_total(t+1)) * v_month_ev(t)


best_estimate_liabs = ModelVariable(modelpoint=policy)
@assign(best_estimate_liabs)
def best_estimate_liabs_formula(t):
    return pv_benefit_total(t) + pv_exp_comm_total(t) + pv_inv_cost_total(t)
