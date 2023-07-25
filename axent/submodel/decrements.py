import math

from axent.input import assumption

from axent.submodel.time import *

death_rates_1 = ModelVariable(modelpoint=policy)
# to be added - experience_factors
death_rate_exp = ModelVariable(modelpoint=policy)
death_rate_dep_exp = ModelVariable(modelpoint=policy)
base_lapse_rate = ModelVariable(modelpoint=policy, time_dep=False)
lapse_rate = ModelVariable(modelpoint=policy)
lapse_rate_dep = ModelVariable(modelpoint=policy)
# base_paidup_rate = ModelVariable(modelpoint=policy)


@assign(death_rates_1)
def death_rates_1_formula(t):
    if age(t) > 120:
        return 1
    sex = policy.get("sex_1")
    gender = "Females" if sex == "F" else "Males"
    return assumption["mort_exp_base"].loc[gender, age(t), cal_year(t)]["value"]


@assign(death_rate_exp)
def death_rate_exp_formula(t):
    return 1 - (1-death_rates_1(t))**(1/12)


@assign(death_rate_dep_exp)
def death_rate_dep_exp_formula(t):
    return death_rate_exp(t) * (1 - lapse_rate(t) / 2)


@assign(base_lapse_rate)
def base_lapse_rate_formula():
    tarcd = policy.get("tarcd")
    base_rate = assumption["lapse_pp"].loc[tarcd + "_PP"]["base_rate"]
    return 1 / (1+base_rate)


@assign(lapse_rate)
def lapse_rate_formula(t):
    tarcd = policy.get("tarcd")
    curr_age = age(t) if age(t) <= 81 else 81
    lapse_mult_age = assumption["lapse_mult_age"].loc[(tarcd + "_PP", curr_age)]["value"]
    curr_remyrs = max(math.floor((policy_maturity_period() - t) / 12), 0)
    lapse_mult_remyrs = assumption["lapse_mult_remyrs"].loc[(tarcd + "_PP", curr_remyrs)]["value"]
    return base_lapse_rate(t) * lapse_mult_age * lapse_mult_remyrs


@assign(lapse_rate_dep)
def lapse_rate_dep_formula(t):
    return lapse_rate(t) * (1 - death_rate_exp(t) / 2)


# @assign(base_paidup_rate)
# def base_paidup_rate_formula(t):
#     tarcd = policy.get("tarcd")
#     base_rate = assumption["pup_rates"].loc[tarcd + "_PP"]["base_rate"]
#     return 1 / (1 + base_rate)
