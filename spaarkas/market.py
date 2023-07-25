from cashflower import variable
from input import assumption


@variable()
def forward_rate(t):
    if t == 0:
        return 0

    key = ("Quarterly_SII_with_Group_VA", "SIIinIFRS17_T_base", "forward", f"{t}M")
    yearly_rate = assumption["interest_rates"].loc[key]["rate"]
    monthly_rate = (1 + yearly_rate) ** (1 / 12) - 1
    return monthly_rate


@variable()
def v_month_ev(t):
    return 1 / (1+forward_rate(t))


@variable()
def inflation_rate(t):
    if t == 0:
        return 0

    key = ("Quarterly_SII_with_Group_VA", "SII_T_HICP", "forward", f"{t}M")
    yearly_rate = assumption["interest_rates"].loc[key]["rate"]
    monthly_rate = (1 + yearly_rate) ** (1 / 12) - 1
    return monthly_rate


@variable()
def infl_rate_expenses(t):
    if t == 0:
        return 1

    return infl_rate_expenses(t-1) * (1 + inflation_rate(t-1))
