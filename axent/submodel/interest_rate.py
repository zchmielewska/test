import math

from cashflower import assign, ModelVariable

from axent.input import assumption, policy

yearly_forward_rate = ModelVariable(modelpoint=policy, pol_dep=False)
forward_rate = ModelVariable(modelpoint=policy, pol_dep=False)
v_month_ev = ModelVariable(modelpoint=policy, pol_dep=False)
cred_rate_mnth_h = ModelVariable(modelpoint=policy, pol_dep=False)


@assign(yearly_forward_rate)
def yearly_forward_rate_formula(t):
    if t == 0:
        return 0
    key = ("Quarterly_SII_with_Group_VA", "SII_T_base", "monthlyforward", str(t)+"M")
    return assumption["interest_rates"].loc[key]["rate"]


@assign(forward_rate)
def forward_rate_formula(t):
    return (1 + yearly_forward_rate(t)) ** (1 / 12) - 1


@assign(v_month_ev)
def v_month_ev_formula(t):
    return 1/(1+forward_rate(t))


@assign(cred_rate_mnth_h)
def cred_rate_mnth_h_formula(t):
    return math.sqrt(1+forward_rate(t)) - 1
