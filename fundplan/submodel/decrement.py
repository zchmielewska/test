import math

from fundplan.assumption import assumption
from fundplan.submodel.time import *
from fundplan.submodel.utils import *


death_rate_1 = ModelVariable(modelpoint=policy)
death_rate_1_exp = ModelVariable(modelpoint=policy)
death_rate = ModelVariable(modelpoint=policy)
lapse_rate = ModelVariable(modelpoint=policy)
paidup_rate = ModelVariable(modelpoint=policy)
death_rate_dep_exp = ModelVariable(modelpoint=policy)
surv_per = ModelVariable(modelpoint=policy)
surv_per_prem = ModelVariable(modelpoint=policy)
surv_prem = ModelVariable(modelpoint=policy)


@assign(death_rate_1)
def death_rate_1_formula(t):
    integer_age = math.floor(age(t) + policy.get("AGE_ADJ_1"))
    if integer_age > 120:
        return 1
    gender = "Females" if policy.get("SEX_1") == "F" else "Males"
    return assumption["mort_exp_base"].loc[(gender, integer_age, cal_year(t))]["value"]


@assign(death_rate_1_exp)
def death_rate_1_exp_formula(t):
    if age(t) > 120:
        return 1

    prodbm_cd = policy.get("PRODBM_CD")
    prdgrmort = policy.get("PRDGRMORT")
    sex = policy.get("SEX_1")
    code_mod_prodboom = prodbm_cd + "_" + str(prdgrmort) + "_" + sex
    category = assumption["mort_mult_products"].loc[code_mod_prodboom]["mort_mult"]

    duration = get_duration(pol_year(t))
    gender = "Females" if sex == "F" else "Males"
    experience_factor = assumption["experience_factors"].loc[(category, duration, gender)]["value"]
    return experience_factor * death_rate_1(t)


@assign(death_rate)
def death_rate_formula(t):
    rate = death_rate_1_exp(t)
    return 1 - (1-rate)**(1/12)


@assign(lapse_rate)
def lapse_rate_formula(t):
    # TODO
    return 0.005


@assign(paidup_rate)
def paidup_rate_formula(t):
    # TODO
    return 0.002


@assign(death_rate_dep_exp)
def death_rate_dep_exp_formula(t):
    return death_rate(t) * (1 - lapse_rate(t)/2)


@assign(surv_per)
def surv_per_formula(t):
    if t == 0:
        return 1
    else:
        return (1-death_rate(t)) * (1-lapse_rate(t))


@assign(surv_per_prem)
def surv_per_prem_formula(t):
    return surv_per(t) * (1-paidup_rate(t))


@assign(surv_prem)
def surv_prem_formula(t):
    if t == 0:
        return 1
    return surv_prem(t-1) * surv_per_prem(t)
