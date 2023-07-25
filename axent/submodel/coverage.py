from cashflower import assign, ModelVariable
from axent.input import coverage

premium_inv_rp_if_b = ModelVariable(modelpoint=coverage)


@assign(premium_inv_rp_if_b)
def premium_inv_rp_if_b_formula(t):
    if t == 0:
        return 0

    if t == 1:
        # return coverage.get("annual_pre") * policies_b TODO
        return coverage.get("annual_pre")

    # return premium_inv_rp_if_b(t-1) * cov_surv_per_prem(t-1) TODO
    return premium_inv_rp_if_b(t-1)
