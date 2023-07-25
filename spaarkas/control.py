from cashflower import variable
from input import main, coverage


@variable()
def is_ax_orv(t):
    if coverage.model_point_data.shape[0] == 0:
        return False
    else:
        cov_code = coverage.get("COV_CD")
        return cov_code == 120 or cov_code == 121


@variable()
def is_ax_schakelspaar(t):
    return main.get("TARCD") == "SCHAKELSPAAR" and not is_ax_orv(t)


@variable()
def is_ax_budgetfonds(t):
    return main.get("TARCD") == "BUDGETFONDS"


@variable()
def is_ax_2040plus(t):
    return main.get("TARCD") == "2040PLUSFONDS"


@variable()
def is_ax_pensioenplus(t):
    return main.get("TARCD") == "PENSIOENPLUS"


@variable()
def is_ax_plusfonds(t):
    return is_ax_2040plus(t) or is_ax_pensioenplus(t)


@variable()
def is_axent(t):
    return is_ax_schakelspaar(t) or is_ax_orv(t) or is_ax_budgetfonds(t) or is_ax_plusfonds(t)
