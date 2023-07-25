import math
from cashflower import variable

from input import main, runplan


@variable(repeat=True)
def projection_year(t):
    if t == 0:
        return 0
    elif t % 12 == 1:
        return projection_year(t - 1) + 1
    else:
        return projection_year(t - 1)


@variable(repeat=True)
def cal_month(t):
    if t == 0:
        return runplan.get("valn_month")
    if cal_month(t-1) == 12:
        return 1
    else:
        return cal_month(t-1) + 1


@variable(repeat=True)
def cal_year(t):
    if t == 0:
        return runplan.get("valn_year")
    if cal_month(t-1) == 12:
        return cal_year(t-1) + 1
    else:
        return cal_year(t-1)


@variable()
def benefit_term(t):
    return main.get("BEN_TERM_K")


@variable()
def elapsed_months():
    """ Number of months elapsed at valuation date. """
    valn_year = runplan.get("valn_year")
    valn_month = runplan.get("valn_month")
    issue_year_data = main.get("ISS_YR")
    issue_month_data = main.get("ISS_MTH")
    return (valn_year - issue_year_data) * 12 + (valn_month + 1 - issue_month_data)


@variable()
def policy_maturity_period():
    """Policy matures when model exceeds omega age or benefit term."""
    ben_term_k = main.get("BEN_TERM_K")

    # Single
    if main.get("NO_INS") == 1:
        period1 = (120 - main.get("AGE_ISS_1")) * 12
    # First-death
    else:
        period1 = (120 - min(main.get("AGE_ISS_1"), main.get("AGE_ISS_2"))) * 12

    if ben_term_k != 9999:
        period2 = ben_term_k - elapsed_months()
        return min(period1, period2)
    else:
        return period1


@variable()
def pol_month(t):
    if t == 0:
        mnth = elapsed_months() % 12
        mnth = 12 if mnth == 0 else mnth
        return mnth
    if pol_month(t-1) == 12:
        return 1
    return pol_month(t-1) + 1


@variable()
def pol_year(t):
    if t == 0:
        return math.floor(elapsed_months() / 12)
    if pol_month(t) == 1:
        return pol_year(t-1) + 1
    return pol_year(t-1)
