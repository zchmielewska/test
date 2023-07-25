from control import *
from input import assumption
from period import *


@variable()
def death_rate_1_exp(t):
    age = int(round(main.get("AGE_ISS_1") + (t - 1 + elapsed_months()) / 12, 2))
    if age > 120:
        return 0

    sex = main.get("SEX_1")
    gender = "Males" if sex == "M" else "Females"
    return assumption["mort_exp_base"].loc[(gender, age, cal_year(t))]["value"]


@variable()
def death_rate_2_exp(t):
    if main.get("NO_INS") == 1:
        return 0

    age = int(round(main.get("AGE_ISS_2") + (t - 1 + elapsed_months()) / 12, 2))
    if age > 120:
        return 0

    sex = main.get("SEX_2")
    gender = "Males" if sex == "M" else "Females"
    return assumption["mort_exp_base"].loc[(gender, age, cal_year(t))]["value"]


@variable()
def death_rate_exp(t):
    no_ins = main.get("NO_INS")
    if no_ins == 2:
        rate = 1 - (1 - death_rate_1_exp(t)) * (1 - death_rate_2_exp(t))
    else:
        rate = death_rate_1_exp(t)

    rate = max(0, min(1, rate))
    monthly_rate = 1 - pow(1 - rate, 1 / 12)
    return monthly_rate

@variable()
def lapse_rate():
    prodbm_cd = main.get("PRODBM_CD") + "_PP"
    base_rate = assumption["lapse_pp"].loc[prodbm_cd]["base_rate"]
    return 1 / (1 + base_rate)


@variable()
def lapse_rate_pup():
    prodbm_cd = main.get("PRODBM_CD") + "_PUP"
    base_rate = assumption["lapse_pp"].loc[prodbm_cd]["base_rate"]
    return 1 / (1 + base_rate)


@variable()
def paidup_rate():
    prodbm_cd = main.get("PRODBM_CD")
    base_rate = assumption["pup_rates"].loc[prodbm_cd]["base_rate"]
    partly_rate = assumption["pup_rates"].loc[prodbm_cd]["partly_rate"]
    rate = 1 / (1 + base_rate)
    rate = rate * partly_rate
    return rate


@variable()
def death_rate_dep_exp(t):
    return death_rate_exp(t) * (1 - lapse_rate() / 2)


@variable()
def death_rate_dep_exp_pup(t):
    return death_rate_exp(t) * (1 - lapse_rate_pup() / 2)


@variable()
def lapse_rate_dep(t):
    return lapse_rate() * (1 - death_rate_exp(t) / 2)


@variable()
def paidup_rate_dep(t):
    if not is_axent(t):
        return paidup_rate() * (1 - death_rate_dep_exp_pup(t) - lapse_rate_dep(t))

    return paidup_rate() * (1 - death_rate_dep_exp(t) - lapse_rate_dep(t))


@variable()
def surv_per(t):
    return 1 - death_rate_exp(t) * (1 - lapse_rate())


@variable()
def surv_per_prem(t):
    return surv_per(t) * paidup_rate()


@variable()
def surv_per_pup(t):
    return (1 - death_rate_exp(t)) * (1 - lapse_rate_pup())


@variable()
def surv_prem(t):
    if t == 0:
        return 0
    return surv_prem(t - 1) * surv_per_prem(t)


@variable()
def surv_per_tar(t):
    if t == 0:
        return 1
    else:
        # return 1.0 - death_rate_riskprem(t)
        # TODO
        return 0

def surv_pup(t):
    # TODO
    # If
    # If
    # If
    if t == 0:
        return 0

    paid_up = paidup_rate()
    return (surv_pup(t - 1) + surv_prem(t - 1) * paid_up) * surv_per_pup(t)
