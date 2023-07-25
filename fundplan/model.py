from fundplan.modelpoint import coverage, fund
from fundplan.submodel.decrement import *
from fundplan.submodel.time import *


age_adj_1_riskprem = ModelVariable(modelpoint=coverage, time_dep=False)
death_rate_1_riskprem = ModelVariable(modelpoint=coverage)
death_rate_riskprem = ModelVariable(modelpoint=coverage)
prem_freq = ModelVariable(modelpoint=coverage, time_dep=False)
premium_inv_rp_if_b = ModelVariable(modelpoint=coverage)
premium_inv_rp = ModelVariable(modelpoint=coverage)
sum_ins_prem_res_if_b = ModelVariable(modelpoint=coverage)
death_claims_si = ModelVariable(modelpoint=coverage)

fund_e = ModelVariable(modelpoint=fund)
claims_death_units = ModelVariable(modelpoint=fund)

claim_death = ModelVariable(modelpoint=policy)


@assign(age_adj_1_riskprem)
def age_adj_1_riskprem_formula():
    sex = policy.get("SEX_1").lower()
    col_name = "age_adj_" + sex
    res_bas_cd = coverage.get("RES_BAS_CD")
    return assumption["mort_riskprem"].loc[("FP", str(res_bas_cd))][col_name]


@assign(death_rate_1_riskprem)
def death_rate_1_riskprem_formula(t):
    age_adjusted = max(age(t) + age_adj_1_riskprem(t), 0) + policy.get("AGE_ADJ_1")
    if age_adjusted > 120:
        return 1

    sex = policy.get("SEX_1").lower()
    col_name = "mort_table_res_" + sex
    res_bas_cd = coverage.get("RES_BAS_CD")
    mort_table_res = assumption["mort_riskprem"].loc[("FP", str(res_bas_cd))][col_name].lower()
    return assumption["mort_table_res"].loc[math.floor(age_adjusted)][mort_table_res]


@assign(death_rate_riskprem)
def death_rate_riskprem_formula(t):
    rate = max(0, min(1, death_rate_1_riskprem(t)))
    return 1 - (1-rate)**(1/12)


@assign(prem_freq)
def prem_freq_formula():
    ind = coverage.get("PREM_FREQ")
    if ind == "M":
        return 12
    elif ind == "Q":
        return 4
    elif ind == "H":
        return 2
    else:
        return 1


@assign(premium_inv_rp_if_b)
def premium_inv_rp_if_b_formula(t):
    if t == 0:
        return 0
    elif t == 1:
        return coverage.get("ANNUAL_PRE")
    else:
        return premium_inv_rp_if_b(t-1) * surv_per_prem(t-1)


@assign(premium_inv_rp)
def premium_inv_rp_formula(t):
    if pol_month(t) % 12 / prem_freq() == 0:
        return premium_inv_rp_if_b(t) / prem_freq
    else:
        return 0


@assign(sum_ins_prem_res_if_b)
def sum_ins_prem_res_if_b_formula(t):
    if t == 0:
        return coverage.get("PREM_PAID")
    else:
        return sum_ins_prem_res_if_b(t-1) * surv_per_prem(t-1) + premium_inv_rp(t)


@assign(death_claims_si)
def death_claims_si_formula(t):
    return death_rate_dep_exp(t) * sum_ins_prem_res_if_b(t)


@assign(fund_e)
def fund_e_formula(t):
    if t == 0:
        fund_code = fund.get("FONDSCD")
        price = assumption["inv_ret_fund"].loc[fund_code]["price"]
        units = fund.get("UNITAANT")
        return price * units
    # TODO
    else:
        return fund_e(t-1)


@assign(claim_death)
def claim_death_formula(t):
    sum_death_claims = 0
    for i in range(coverage.size):
        sum_death_claims += death_claims_si(t, i)
    # TODO
    return 0


@assign(claims_death_units)
def claims_death_units_formula(t):
    if t == 0:
        return 0
    else:
        return max(0, fund_e(t-1)) * death_rate_dep_exp(t) / (1-death_rate_dep_exp(t))
