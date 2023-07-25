from axent.input import fund
from axent.submodel.decrements import *
from axent.submodel.interest_rate import *


fund_e = ModelVariable(modelpoint=fund)
fund_e_between = ModelVariable(modelpoint=fund)
charge_fund_man_fee = ModelVariable(modelpoint=fund)
charge_exp_ren_dal_perc = Parameter(modelpoint=fund)
charge_exp_ren_dal = ModelVariable(modelpoint=fund)
management_fee = Parameter(modelpoint=fund)
charge_fund_man_fee_am = ModelVariable(modelpoint=fund)
fund_e_bef = ModelVariable(modelpoint=fund)
release_death = ModelVariable(modelpoint=fund)
fund_m_bef = ModelVariable(modelpoint=fund)
fund_b = ModelVariable(modelpoint=fund)


@assign(fund_e)
def fund_e_formula(t):
    if t == 0:
        fund_units_curr = fund.get("unitsavprt")
        fund_code = int(fund.get("fondscd"))
        price = assumption["inv_ret_fund"].loc[fund_code]["PRICE"]
        return fund_units_curr * price
    # return max(0.0, fund_e_between(t) - paid_up_claims_units(t));
    pass

@assign(fund_e_between)
def fund_e_between_formula(t):
    # return max(0.0, fund_e_bef(t) - charge_fund_man_fee(t));
    pass


@assign(charge_fund_man_fee)
def charge_fund_man_fee_formula(t):
    # return charge_exp_ren_dal(t) + charge_fund_man_fee_am(t)
    pass


@assign(charge_exp_ren_dal_perc)
def charge_exp_ren_dal_perc_formula():
    prodbm_cd = policy.get("prodbm_cd")
    iss_yr = policy.get("iss_yr")
    return assumption["product_features_dal_perc"].loc[prodbm_cd, iss_yr]["value"]


@assign(charge_exp_ren_dal)
def charge_exp_ren_dal_formula(t):
    # return fund_bef * charge_exp_ren_dal_perc
    pass


@assign(charge_fund_man_fee_am)
def charge_fund_man_fee_am_formula(t):
    # return fund_e_bef(t) * management_fee() / 12
    pass


@assign(management_fee)
def management_fee_formula():
    fund_code = fund.get("fondscd")
    return assumption["sa_management_fee_and_rebate_bll"].loc[fund_code]["managementfee_including3bpservicefee"]


@assign(fund_e_bef)
def fund_e_bef_formula(t):
    # return max(0.0, (fund_m_bef(t) - release_death(t) - release_surrender(t)) * (1 + cred_rate_mnth_h(t)))
    pass


@assign(release_death)
def release_death_formula(t):
    # return fund_m_bef(t) * death_rate_dep_exp(t);
    pass


@assign(fund_m_bef)
def fund_m_bef_formula(t):
    return fund_b(t) * (1 + cred_rate_mnth_h(t))


@assign(fund_b)
def fund_b_formula(t):
    # return max(0, fund_e(t-1) + alloc_units(t))
    return 0 # TODO

