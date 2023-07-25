from input import fund
from settings import settings
from decrements import *
from market import *
from period import *


# Policy
@variable()
def best_estimate_liabilities(t):
    return pv_benefit_total(t) + pv_exp_comm_total(t) + pv_management_fee_expenses(t) - pv_prem_gross(t) + pv_inv_cost_total(t)


@variable()
def exp_ga_ic_fee():
    return assumption["ga_investment_fee_parameter"].loc["ga_investment_cost_yearly"]["value"]


@variable()
def pv_benefit_total(t):
    # TODO
    # If...
    # If...
    if t > policy_maturity_period() or t >= settings["T_MAX_CALCULATION"]:
        return 0

    total_benefit = claim_maturity(t) + claim_death(t) + claim_surrender(t) + claim_riders(t)
    if t == policy_maturity_period():
        return total_benefit * v_month_ev(t)

    return (total_benefit + pv_benefit_total(t+1)) * v_month_ev(t)


@variable()
def pv_exp_comm_total(t):
    # TODO
    # If
    # If

    if t > policy_maturity_period():
        return 0

    if t == policy_maturity_period():
        return expense_ren(t) * v_month_ev(t)

    if t == settings["T_MAX_CALCULATION"]:
        return expense_ren(t)

    return expense_ren(t) + pv_exp_comm_total(t+1) * v_month_ev(t)


@variable()
def pv_management_fee_expenses(t):
    if t == 0:
        return pv_management_fee_expenses(t+1) * v_month_ev(t)

    if t == policy_maturity_period():
        return management_fee_expenses(t) * v_month_ev(t)

    if t > policy_maturity_period():
        return 0

    return (management_fee_expenses(t) + pv_management_fee_expenses(t+1)) * v_month_ev(t)


@variable()
def management_fee_expenses(t):
    return charge_fund_man_fee_paid_am(t)


@variable()
def expense_ren(t):
    if t == 0:
        return 0

    amount_prem = exp_ren_fix_scl_prem() / 12.0 * 1 * infl_rate_expenses(t)
    amount_pup = exp_ren_fix_scl_pup() / 12.0 * 1 * infl_rate_expenses(t)
    return amount_prem * surv_prem(t - 1) + amount_pup * surv_pup(t - 1)


@variable()
def exp_ren_fix_scl_prem():
    return assumption["ur5_be_bll_maintenance_expenses"].loc[("Cost per policy - MoSes", "SF")]["value"]


@variable()
def exp_ren_fix_scl_pup():
    return assumption["ur5_be_bll_maintenance_expenses"].loc[("Cost per policy - MoSes", "SF")]["value"]


@variable()
def pv_prem_gross(t):
    if t == 0:
        return pv_prem_gross(t + 1) * v_month_ev(t)

    if t == policy_maturity_period():
        return premium_gross_b(t) * v_month_ev(t)

    if t > policy_maturity_period():
        return 0

    return (premium_gross_b(t) + pv_prem_gross(t + 1)) * v_month_ev(t)


@variable()
def premium_gross_b(t):
    return premium_inv_rp(t) + premium_rider_gross(t)


@variable()
def claim_maturity(t):
    if t != policy_maturity_period():
        return 0
    return max(0.0, claim_maturity_bef_max(t))


@variable()
def claim_maturity_bef_max(t):
    # claim_maturity_fund = fund_claim_maturity
    if t != policy_maturity_period():
        return 0

    if is_ax_plusfonds(t):
        return max(fund_claim_maturity(t), premiums_cum_nominal_in_force_tot_e(t))

    return fund_claim_maturity(t)


@variable()
def premiums_cum_nominal_in_force_tot_e(t):
    return premiums_cum_nominal_in_force_pp_e(t) + premiums_cum_nominal_in_force_pu_e(t)


@variable()
def premiums_cum_nominal_in_force_pp_e(t):
    if t > policy_maturity_period():
        return 0

    if t == 0:
        # TODO
        # return sum(premium_cum_nominal_data)
        return 0

    # If
    # TODO

    return (premiums_cum_nominal_in_force_pp_e(t - 1) + premium_inv_rp(t)) * surv_per_prem(t)


@variable()
def premiums_cum_nominal_in_force_pu_e(t):
    if t > policy_maturity_period():
        return 0

    if t == 0:
        # TODO
        # return sum(premium_cum_nominal_data)
        return 0

    return (premiums_cum_nominal_in_force_pu_e(t - 1) + premiums_cum_nominal_in_force_pp_e(t - 1) * paidup_rate()) * \
           surv_per_pup(t)


@variable()
def claim_death(t):
    result = 0
    # TODO
    for c in range(coverage.model_point_data.shape[0]):
        result += death_claims_si(t)
    if is_axent(t):
        return result
    if t + elapsed_months() < benefit_term(t) / 2:
        return max(result, release_death_pp(t) * sum_ins_factor())
    return result


@variable()
def claim_surrender(t):
    if t >= policy_maturity_period():
        return 0
    return max(0.0, claim_surrender_bef_max(t))


@variable()
def claim_surrender_bef_max(t):
    # TODO
    if t >= policy_maturity_period():
        return 0

    ax_plusfonds_sv_fund_mult_pc = 0.95
    prepaid_risk_premium = 0

    fund_surr_claim_pp = fund_claim_surrender_pp(t)
    # fund_surr_claim_pu = fund_claim_surrender_pu(t)
    fund_surr_claim_pu = 0

    if is_ax_plusfonds(t):
        fund_surr_claim_pp *= ax_plusfonds_sv_fund_mult_pc
        # fund_surr_claim_pu *= ax_plusfonds_sv_fund_mult_pc

        fund_surr_claim_pp = max(fund_surr_claim_pp, premiums_cum_nominal_in_force_pp_e(t) * lapse_rate_dep(t))
        # fund_surr_claim_pu = max(fund_surr_claim_pu, premiums_cum_nominal_in_force_pu_e(t) * lapse_rate_dep(t))

    if is_axent(t) and not is_ax_plusfonds(t):
        # prepaid_risk_premium = reserve_tar(t) * lapse_rate_dep(t)
        prepaid_risk_premium = 0 * lapse_rate_dep(t)

    return fund_surr_claim_pp + fund_surr_claim_pu + prepaid_risk_premium


@variable()
def claim_riders(t):
    key = (main.get("PRODBM_CD"), pol_year(t))
    waiverpremium_rate = assumption["waiverpremium"].loc[key]["value"]
    return premium_rider_gross(t) * waiverpremium_rate


@variable()
def premium_rider_gross(t):
    # TODO
    # If...
    # If...
    return premium_care_if_b(t) / rider_prem_freq()


@variable()
def premium_care_if_b(t):
    if t == 0:
        return 0
    # TODO
    # If...
    # If...
    # If...
    return premium_care_if_b(t-1) * surv_per_prem(t-1)


@variable()
def rider_prem_freq():
    rider_prem_freq_code = main.get("RID_PRM_FR")
    if rider_prem_freq_code == "M":
        return 12
    elif rider_prem_freq_code == "Q":
        return 4
    elif rider_prem_freq_code == "H":
        return 2
    elif rider_prem_freq_code == "Y" or rider_prem_freq_code == "S":
        return 1
    elif rider_prem_freq_code == "O":
        return 0
    else:
        raise ValueError(f"Incorrect value for in 'rid_prm_fr' column {rider_prem_freq_code}.")


@variable()
def alloc_units():
    # return alloc_units_before_purchase(t) - charge_bid_spread(t)
    # TODO
    return 0


@variable()
def alloc_units_before_purchase(t):
    # return premium_inv_rp(t) - net_prem_b(t) - expense_loadings(t) + (discount_employee_b(t) + discount_volume_b(t)) / prem_freq - init_exp;
    # TODO
    return 0


@variable()
def charge_exp_ren_dal_perc():
    key = (main.get("TARCD"), main.get("ISS_YR"))
    return assumption["product_features_dal_perc"].loc[key]["value"]


@variable()
def sum_ins_factor():
    key = main.get("TARCD") + "_" + coverage.get("PREMPAY_CD")
    return assumption["product_features"].loc[key]["perc_fund"]


# Coverage
@variable()
def sum_ins_prem_res_if_e_koersplan(t):
    """Premiums accumulated with db interest data up to valuation date."""
    if t == 0:
        return coverage.get("PRMTBIP")
    else:
        return 0


@variable()
def sum_assured_if(t):
    """Coverage"""
    # axent has a different formula
    if t == 0:
        return 0
    return sum_ins_prem_res_if_e_koersplan(t - 1)


@variable()
def death_claims_si(t):
    return death_rate_dep_exp_cov(t) * sum_assured_if(t)


@variable()
def death_rate_dep_exp_cov(t):
    return death_rate(t) * (1.0 - lapse_rate() / 2.0)


@variable()
def postid():
    return coverage.get("POSTID")


@variable()
def premium_inv_rp(t):
    if (pol_month(t) % 12 / prem_freq()) + math.floor(prem_freq() / 12) == 1:
        return premium_inv_rp_if_b(t) / prem_freq()
    return 0.0


@variable()
def premium_inv_rp_if_b(t):
    if t == 0:
        return 0
    elif t == 1:
        return coverage.get("ANNUAL_PRE")
    else:
        return premium_inv_rp_if_b(t - 1) * cov_surv_per_prem(t - 1)


@variable()
def cov_surv_per_prem(t):
    return cov_surv_per(t) * (1.0 - paidup_rate())


@variable()
def cov_surv_per(t):
    if t == 0:
        return 1
    else:
        return (1 - death_rate(t)) * (1 - lapse_rate())


@variable()
def death_rate(t):
    if main.get("NO_INS") == 1:
        rate = death_rate_1_exp(t)
    else:
        rate = 1 - (1 - death_rate_1_exp(t)) * (1 - death_rate_2_exp(t))

    rate = min(0, max(rate, 1))

    # Convert to monthly
    return 1 - (1 - rate) ** (1 / 12)


@variable()
def prem_freq():
    prem_freq_indicator = coverage.get("PREM_FREQ")
    if prem_freq_indicator == "M":
        return 12

    if prem_freq_indicator == "Q":
        return 4

    if prem_freq_indicator == "H":
        return 2

    if prem_freq_indicator == "Y" or prem_freq_indicator == "S":
        return 1

    if prem_freq_indicator == "O":
        return 0

# Fund
@variable()
def fund_price():
    fund_code = fund.get("FONDSCD")
    return assumption["inv_ret_fund"].loc[fund_code]["price"]


@variable()
def fund_e_pp(t):
    if t == 0:
        fund_units_curr = fund.get("UNITSAVPRT")
        return fund_units_curr * fund_price()
    else:
        return max(0, fund_e_between_pp(t) - paid_up_claims_e_pp(t))


@variable()
def fund_e_between_pp(t):
    return max(0, fund_e_bef_pp(t) - charge_fund_man_fee(t))


@variable()
def paid_up_claims_e_pp(t):
    return fund_e_between_pp(t) * paidup_rate_dep(t)


@variable()
def fund_e_bef_pp(t):
    return max(0, (fund_m_bef_pp(t) - release_death_pp(t) - release_surrender_pp(t)) * (1 + cred_rate_mnth_h(t)))


@variable()
def fund_m_bef_pp(t):
    return fund_b_pp(t) * (1 + cred_rate_mnth_h(t))


@variable()
def fund_b_pp(t):
    if t == 0:
        return fund_e_pp(t)
    else:
        return max(0.0, fund_e_pp(t - 1) + fund_alloc_units_pp())


@variable()
def fund_alloc_units_pp():
    return alloc_units() * fund.get("BELEGPRC") / 100


@variable()
def cred_rate_mnth_h(t):
    if t == 0:
        return 0
    else:
        key = ("Quarterly_SII_with_Group_VA", "SIIinIFRS17_T_base", "forward", f"{t}M")
        yearly_rate = assumption["interest_rates"].loc[key]["rate"]
        monthly_rate = (1 + yearly_rate) ** (1 / 12) - 1
        return math.sqrt(1 + monthly_rate) - 1


@variable()
def release_death_pp(t):
    return fund_m_bef_pp(t) * death_rate_dep_exp(t)


@variable()
def release_surrender_pp(t):
    return fund_m_bef_pp(t) * lapse_rate_dep(t)


@variable()
def charge_fund_man_fee(t):
    return charge_exp_ren_dal(t) + charge_fund_man_fee_am(t)


@variable()
def charge_fund_man_fee_am(t):
    fundmgt_am = assumption["other_fund_costs"].loc[("KP", fund.get("FONDSCD"))]["column1"]
    return fund_e_bef_pp(t) * fundmgt_am / 12


@variable()
def charge_fund_man_fee_paid_am(t):
    fundmgt_am = assumption["other_fund_costs"].loc[("KP", fund.get("FONDSCD"))]["column4"]
    return fund_e_bef_pp(t) * fundmgt_am / 12


@variable()
def charge_exp_ren_dal(t):
    if main.get("ISS_YR") < man_fee_am_issue_date_koersplan() and cal_month(t) == 12:
        return fund_e_bef_pp(t) * charge_exp_ren_dal_perc()
    if main.get("ISS_YR") >= man_fee_am_issue_date_koersplan() and pol_month(t) == 12:
        return fund_e_bef_pp(t) * charge_exp_ren_dal_perc()
    return 0


@variable()
def man_fee_am_issue_date_koersplan():
    key = main.get("TARCD") + "_" + coverage.get("PREMPAY_CD")
    return assumption["product_features"].loc[key]["man_fee_am_iss_dat"]


@variable()
def fund_claim_maturity(t):
    if t != policy_maturity_period():
        return 0
    return max(0, release_maturity(t)) + loss_guarantee(t) - charge_offer_spread_claim_maturity(t)


@variable()
def release_maturity(t):
    if t != policy_maturity_period():
        return 0
    return max(0, fund_e_between_pp(t))


@variable()
def fund_val_guaranteed_if(t):
    if t == 0:
        return 0
    return fund.get("GARKAP") * surv_prem(t - 1)


@variable()
def loss_guarantee(t):
    total_units_at_mat = fund_e_between_pp(t)
    return max(0, fund_val_guaranteed_if(t) - total_units_at_mat)


@variable()
def charge_offer_spread_claim_maturity(t):
    verkoop_kst_am = assumption["other_fund_costs"].loc[("KP", fund.get("FONDSCD"))]["column1"]
    return max(0, fund_e_between_pp(t)) * verkoop_kst_am


@variable()
def fund_claim_surrender_pp(t):
    # fund->claim_surrender
    # TODO
    # If...
    # If...
    return release_surrender_pp(t) - charge_offer_spread_claim_surrender_pp(t)


@variable()
def charge_offer_spread_claim_surrender_pp(t):
    # TODO
    # If...
    # If...
    charge_offer_spread_perc = assumption["other_fund_costs"].loc[("KP", fund.get("FONDSCD"))]["column1"]
    return release_surrender_pp(t) * charge_offer_spread_perc


@variable()
def interest_tar_mth():
    interest_tar = float(assumption["mort_riskprem"].loc[("KP", str(coverage.get("RES_BAS_CD")))]["interest"])
    return (1.0 + interest_tar)**(1.0 / 12.0) - 1.0


@variable()
def v_month_curr_basis_tar():
    return 1/(1+interest_tar_mth())


@variable()
def v_half_month_curr_basis_tar():
    return math.sqrt(v_month_curr_basis_tar())


@variable()
def claims_si_pv(t):
    if t == settings["T_MAX_CALCULATION"]:
        return death_claims_si(t) * v_half_month_curr_basis_tar()
    return claims_si_pv(t + 1) * v_month_curr_basis_tar() + death_claims_si(t) * v_half_month_curr_basis_tar()


@variable()
def vsa(t):
    """Value of sum assured"""
    return claims_si_pv(t)


@variable()
def net_premium_if_b(t):
    if t == 0:
        return coverage.get("NET_RISPRE")
    return net_premium_if_b(t - 1) * surv_per_prem(t - 1)


@variable()
def premium_pv(t):
    if t == settings["T_MAX_CALCULATION"]:
        return premium_inv_rp(t)
    return premium_pv(t + 1) * v_month_curr_basis_tar() + premium_inv_rp(t)


@variable()
def annuity_factor(t):
    if t == 0:
        return 0

    if premium_inv_rp_if_b(t) == 0:
        return 0

    return premium_pv(t) / premium_inv_rp_if_b(t)


@variable()
def vnp(t):
    return net_premium_if_b(t) * annuity_factor(t)


@variable()
def reserve_basic(t):
    """Same as reserve_basic_tar since only 1 coverage"""
    return vsa(t) - vnp(t)


@variable()
def expense_fee(t):
    # return exp_ga_ic_fee() / (1e4 * 12.0) * reserve_basic_tar(t)
    return exp_ga_ic_fee() / (1e4 * 12.0) * reserve_basic(t)


@variable()
def pv_inv_cost_total(t):
    if t == settings["T_MAX_CALCULATION"]:
        return expense_fee(t)
    return (expense_fee(t) + pv_inv_cost_total(t + 1)) * v_month_ev(t)
