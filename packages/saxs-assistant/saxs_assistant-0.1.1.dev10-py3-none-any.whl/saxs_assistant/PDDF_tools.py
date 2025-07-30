"""
This module provides tools for working with PDDF (Pair Distribution Function) data and selection.
This includes functions to characterize the data like the Elongation ratio from Putnam 2016
"""

import pandas as pd
from scipy.integrate import trapezoid
import numpy as np
import warnings
import logging
from .rawutils import rawapitry as raw

# ******************************************************************************
# This file is part of SAXS Assistant.
#
#    All code from SAXS Assisstant can be used freely for non-commercial purposes.
#    If you use this code in your work, please cite the following publications:
# Add The GPA citation
# Add Franke citation
# Add Raw citation
# SAXS Assistant citation
#    SAXS Assistant is based on the code from RAW, which is a SAXS data analysis software.
#
#
#    SAXS Assistant utilizes parts of the code from RAW
#    SAXS Assistant is shared for helping the community with SAXS data analysis.
#    but it is not a replacement for RAW, and does not include all the features of RAW.
#    SAXS Assisant does not offer warranty-- use at your own risk and evaluate the results carefully.


#    RAW is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RAW is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RAW.  If not, see <http://www.gnu.org/licenses/>.
#
# ******************************************************************************
def get_ER(p, r):
    """
    Calculate the Elongation Ratio (ER) from a PDDF.
    If available, some returned values from BIFT cause issues with the
    calculation of the ER, so if this is the case, this isn't calculated.
    Parameters
      ----------
      p : numpy.ndarray
        The PDDF values, P(r)
      r : numpy.ndarray
        The distance values, r
    """
    pr_peak = pd.Series(p, name="P(r)").idxmax()
    P_r = pd.DataFrame({"r": r, "P(r)": p})

    r_spacing = []
    last_r = 0
    current_r = 0
    for j in range(len(P_r["r"])):
        current_r = P_r["r"][j]
        r_spacing.append(current_r - last_r)

        last_r = current_r
    r_spacing = pd.Series(r_spacing, name="delta r")
    P_r = pd.concat([P_r, r_spacing], axis=1)

    zero_R = trapezoid(
        P_r["P(r)"][: pr_peak + 1],
        x=P_r["r"][: pr_peak + 1],
        dx=P_r["delta r"][1],
        axis=-1,
    )
    R_dmax = trapezoid(
        P_r["P(r)"][pr_peak:], x=P_r["r"][pr_peak:], dx=P_r["delta r"][1], axis=-1
    )
    ER = R_dmax / zero_R
    return ER


def unpack_pr_fits_dict(pr_fits_dict):
    """
    Unpacks a pr_fits_dict into the separate lists needed for ranking.
    Returns:
        rg_min, i0_p_list, chi_sq_list, dmax_mins, logas, dmax_err, pr_list,
        pr_i_orig, pr_fit, pr_err_orig, pr_q_orig, pr_qxt, nmins
    """
    rg_min, i0_p_list, chi_sq_list, dmax_mins = [], [], [], []
    logas, dmax_err = [], []
    pr_rg_err, pr_i0_err, pr_qmin, pr_qmax = [], [], [], []
    pr_list, pr_i_orig, pr_fit, pr_err_orig, pr_q_orig, pr_qxt, nmins = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )

    for nmin, fit in pr_fits_dict.items():
        try:
            rg_min.append(fit["Rg"])
            pr_rg_err.append(fit.get("Rg Err", np.nan))  # New
            i0_p_list.append(fit["I0"])
            pr_i0_err.append(fit.get("I0 Err", np.nan))  # New
            chi_sq_list.append(fit["Chi^2"])
            dmax_mins.append(fit["Dmax"])
            logas.append(fit.get("Log Alpha", 0))
            dmax_err.append(fit.get("Dmax Error", 0))
            pr_qmin.append(fit.get("qmin", np.nan))  # New
            pr_qmax.append(fit.get("qmax", np.nan))  # New
            pr_list.append(fit["p(r)"])
            pr_i_orig.append(fit["i_orig"])
            pr_fit.append(fit["i_fit"])
            pr_err_orig.append(fit["err_orig"])
            pr_q_orig.append(fit["q_orig"])
            pr_qxt.append(fit.get("q_extrap", fit["q_orig"]))
            nmins.append(nmin)
        except KeyError as e:
            logging.warning(f"Missing key in pr_fits_dict[{nmin}]: {e}")
            continue

    return (
        rg_min,
        pr_rg_err,
        i0_p_list,
        pr_i0_err,
        chi_sq_list,
        dmax_mins,
        logas,
        dmax_err,
        pr_qmin,
        pr_qmax,
        pr_list,
        pr_i_orig,
        pr_fit,
        pr_err_orig,
        pr_q_orig,
        pr_qxt,
        nmins,
    )


def get_all_pr_results(profile, q, I, err):
    """
    Runs raw.bift at different nmin values and stores the full results for later evaluation.
    #Here maybe dont need to send q, I, err
    """
    pr_fits = {}
    for nmin in range(0, 26, 5):
        # print(f"Running P(r) at nmin = {nmin}"+ "q = "+str(q[nmin]))
        try:
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            (
                gi_bift,
                gi_bift_dmax,
                gi_bift_rg,
                gi_bift_i0,
                gi_bift_dmax_err,
                gi_bift_rg_err,
                gi_bift_i0_err,
                gi_bift_chi_sq,
                gi_bift_log_alpha,
                gi_bift_log_alpha_err,
                gi_bift_evidence,
                gi_bift_evidence_err,
            ) = raw.bift(profile, idx_min=nmin, pr_pts=100, use_guinier_start=False)

            try:
                er = get_ER(gi_bift.p, gi_bift.r)
            except:
                er = None

            pr_fits[nmin] = {
                "Rg": gi_bift_rg,
                "Rg Err": gi_bift_rg_err,
                "I0 Err": gi_bift_i0_err,
                "I0": gi_bift_i0,
                "Dmax": gi_bift_dmax,
                "Chi^2": gi_bift_chi_sq,
                "Log Alpha": gi_bift_log_alpha,
                "Dmax Error": gi_bift_dmax_err,
                "ER": er,
                "q_orig": gi_bift.q_orig,
                "q_extrap": gi_bift.q_extrap,
                "qmin": np.min(gi_bift.q_orig),
                "qmax": np.max(gi_bift.q_orig),
                "i_fit": gi_bift.i_fit,
                "i_orig": gi_bift.i_orig,
                "err_orig": gi_bift.err_orig,
                "p(r)": (gi_bift.r, gi_bift.p),
            }
        except AttributeError:
            logging.warning(
                f"P(r) AttributeError at nmin = {nmin} for {df_wrong['file name'][j]}"
            )  # Gotta fix this
        except Exception as e:
            logging.warning(
                f"P(r) failed at nmin = {nmin} for {df_wrong['file name'][j]}: {e}"
            )
    return pr_fits


def select_best_pr_fit(
    pr_rg_list,
    pr_rg_err_list,
    pr_i0_list,
    pr_i0_err_list,
    chi_sq_list,
    dmax_list,
    log_alpha_list,
    dmax_err_list,
    pr_qmin_list,
    pr_qmax_list,  # ✅ NEW
    final_guinier_rg,
    final_guinier_i0,
    pr_list,
    pr_i_orig,
    pr_fit,
    pr_err_orig,
    pr_q_orig,
    pr_qxt,
    nmins,
    q,
    I,
    err,
    sample_id,
    murthy_df,
    j,
):
    """
    V2. Selects the best P(r) curve whose Rg is within 15% of the final Guinier Rg.
    Updates murthy_df and plot_data with selected P(r). Prioritizes the Rg similarity, followed by Chi distance to 1,
    then the Dmax error, and then the Log Alpha, the candidate Pr at the top of dataframe is returned.
    """
    import numpy as np

    def abs_percent_error(a, b):
        return abs(a - b) / b * 100

    try:
        # Identify indices of candidate P(r) fits within 15% of Guinier Rg
        rg_diffs = [abs_percent_error(final_guinier_rg, rg) for rg in pr_rg_list]
        candidate_inds = np.argwhere(np.array(rg_diffs) < 15).flatten()

        if len(candidate_inds) == 0:
            murthy_df.loc[murthy_df.index[j], "Flag"] = "No PR match to Rg"
            logging.warning(f"No valid P(r) match for {sample_id}")
            return None

        # Build candidate dataframe
        rows = []
        for i in candidate_inds:
            rows.append(
                [
                    i,
                    dmax_list[i],
                    round(chi_sq_list[i], 3),
                    round(log_alpha_list[i], 2),
                    round(dmax_err_list[i], 3),
                    pr_i0_list[i],
                    final_guinier_i0,
                    pr_rg_list[i],
                    final_guinier_rg,
                    abs(
                        1 - round(chi_sq_list[i], 3),
                    ),
                    abs(pr_rg_list[i] - final_guinier_rg),
                ]
            )
        fin_pr = pd.DataFrame(
            rows,
            columns=[
                "Index",
                "Dmax",
                "Chi^2",
                "Log alpha",
                "Dmax Error",
                "Pr i0",
                "G i0",
                "Pr Rg",
                "G Rg",
                "chi dist",
                "Rg Abs dif",
            ],
        )

        # Sort to select best
        # fin_pr = fin_pr.sort_values(by=['chi dist', 'Dmax Error', 'Log alpha'], ascending=[True, True, False]).reset_index(drop=True)
        fin_pr = fin_pr.sort_values(
            by=["Rg Abs dif", "chi dist", "Dmax Error", "Log alpha"],
            ascending=[True, True, True, False],
        ).reset_index(drop=True)

        # display(fin_pr)
        best_idx = int(fin_pr["Index"][0])

        # Update dataframe
        murthy_df.loc[murthy_df.index[j], "Dmax"] = round(dmax_list[best_idx], 4)
        murthy_df.loc[murthy_df.index[j], "Chi^2"] = round(chi_sq_list[best_idx], 4)
        murthy_df.loc[murthy_df.index[j], "Dmax Error RAW"] = round(
            fin_pr["Dmax Error"][0], 4
        )
        murthy_df.loc[murthy_df.index[j], "Pr Rg"] = round(pr_rg_list[best_idx], 4)
        murthy_df.loc[murthy_df.index[j], "Pr i0"] = pr_i0_list[best_idx]
        murthy_df.loc[murthy_df.index[j], "Pr Log Alpha"] = log_alpha_list[best_idx]
        murthy_df.loc[murthy_df.index[j], "Pr nmin"] = round(nmins[best_idx], 4)
        murthy_df.loc[murthy_df.index[j], "Pr Rg Err"] = round(
            pr_rg_err_list[best_idx], 4
        )
        murthy_df.loc[murthy_df.index[j], "Pr i0 Err"] = round(
            pr_i0_err_list[best_idx], 4
        )
        murthy_df.loc[murthy_df.index[j], "Pr qmin"] = round(pr_qmin_list[best_idx], 4)
        murthy_df.loc[murthy_df.index[j], "Pr qmax"] = round(pr_qmax_list[best_idx], 4)
        return fin_pr, best_idx

    except Exception as e:
        logging.warning(f"Error selecting final P(r) for {sample_id}: {e}")
        murthy_df.loc[murthy_df.index[j], "Flag"] = "PR selection error"
        return None
