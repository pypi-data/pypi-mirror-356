"""This is the main runner for SAXS Assistant. Broken into multiple try blocks to prevent
overall failure if certain analysis cannot be done.
It runs the SAXS analysis on a DataFrame of that has the name of the files to analyze.
Extracting various features and generating plots that are stored in a dictionary.
This module is designed to be run as a script, and it will process the SAXS data files specified in the input DataFrame.
"""

import numpy as np
import pandas as pd
import warnings
from IPython.display import display, Javascript
import time
from pathlib import Path
import os
from tqdm import tqdm
import logging
from joblib import load, dump
from .rawutils import sasm as SASM

from .rawutils import Profile_Loader
from .rawutils import rawapitry as raw
from .rg_tools import (
    select_final_rg_from_candidates,
    rg_method_1,
    select_best_rg_method,
)
from .utils.helpers import reprocess_sasbdb_q_values
from .features import get_GPA, get_kratky
from .ML import (
    predict_dmax_from_features_only,
    assign_gmm_clusters,
    compute_franke_features,
    load_model,
)


from .PDDF_tools import (
    get_all_pr_results,
    unpack_pr_fits_dict,
    select_best_pr_fit,
)

# import select_best_pr_fit
from .rawutils import sasexceptions as SASEceptions

# Setup logger
logging.basicConfig(level=logging.INFO)

# Helper to store plots
plot_data = {}


def get_unique_output_dir(base_dir="results"):
    """Create a unique output directory by appending an index if the base directory already exists.
    Used in the analyze_and_save function to ensure results are saved in a unique directory, for when multiple instances of script are ran simultaneously.
    This prevents overwriting results from previous runs. Also usful for future steps when updating and combining results.
    :param base_dir: The base directory name to create.
    :return: A Path object pointing to the unique directory.
    """
    base_path = Path(base_dir)
    i = 1
    while base_path.exists():
        base_path = Path(f"{base_dir}_{i}")
        i += 1
    base_path.mkdir(parents=True)
    return base_path


def beep():
    """
    Used for notifications
    """
    display(
        Javascript("""
      (async () => {
          const context = new AudioContext();
          const o = context.createOscillator();
          const g = context.createGain();
          o.type = "sine";
          o.connect(g);
          g.connect(context.destination);
          o.start();
          g.gain.exponentialRampToValueAtTime(0.00001, context.currentTime + 1);
      })();
  """)
    )


def save_plot(sample_id, name, plot_dict):
    plot_data.setdefault(sample_id, {})[name] = plot_dict


# Helper to update a row in murthy_df
def update_murthy_df_row(df, index, updates):
    for key, value in updates.items():
        df.loc[df.index[index], key] = value


# Helper to check if Guinier fit is acceptable
def meets_guinier_criteria(r2, qrgmin, qrgmax):
    return r2 > 0.74 and qrgmin < 0.9 and qrgmax < 1.4


# Helper to calculate residuals
def calculate_residuals(i_fit, i_orig, err_orig):
    residuals = i_orig - i_fit
    normalized = residuals / err_orig
    return residuals, normalized, np.sum(normalized**2) / len(i_fit)


# Helper to get closest match to Guinier Rg


def get_best_pr_match(guinier_rg, rg_min):
    errors = [abs((guinier_rg - rg) / rg) * 100 for rg in rg_min]
    return int(np.argmin(errors)), min(errors)


# Helper to build fin_pr DataFrame
def build_fin_pr_df(
    indices, rg_min, i0_p_list, chi_sq_list, dmax_mins, logas, dmax_err
):
    data = []
    for i in indices:
        data.append(
            [
                i,
                dmax_mins[i],
                round(chi_sq_list[i], 3),
                round(logas[i], 2),
                round(dmax_err[i], 3),
                i0_p_list[i],
                rg_min[i],
            ]
        )
    return pd.DataFrame(
        data,
        columns=["Index", "Dmax", "Chi^2", "Log alpha", "Dmax Error", "Pr i0", "Pr Rg"],
    )


# Start and end time tracker
def track_time():
    start_time = time.time()
    print(
        f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}"
    )
    return start_time


def print_end_time(start_time):
    end_time = time.time()
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"Total Execution Time: {end_time - start_time:.2f} seconds")


# multiple try blocks-Prevents overall failure if certain analysis cannot be done
logging.basicConfig(level=logging.ERROR)


# Loading the models once to prevent slow down now bundel_path is actually the bundle in the fn
dmax_bundle = load_model("dmax_predictor_2bundle_05262025.joblib")
gmm_bundle = load_model("gmm_cluster_2bundle_05262025.joblib")

# multiple try blocks-Prevents overall failure if certain analysis cannot be done


def run_analysis(df_wrong, s0=0):
    start_time = track_time()
    df_wrong = df_wrong.reset_index(drop=True)

    for j in tqdm(range(s0, len(df_wrong)), desc="Running SAXS Analysis"):
        sample_id = df_wrong["file name"][j]
        logging.info(f"Analyzing {sample_id} ({j + 1}/{len(df_wrong)})")

        skip_sample = False  # Flagging to skip sample if any error occurs

        try:
            profile = Profile_Loader.load_profiles(
                df_wrong["path"][j] + df_wrong["file name"][j]
            )[0]
            # This resamples data to meet format as GL collection
            # Overall works well, tested with 3,000+ SASBDB files, this doesn't impact and allows faster execution
            # Serves to also use number of points in fit to evaluate fit, as if very low binning, even if have
            # multiple points, the Rg q interval is not good, this way can have a standard on window acceptance
            # if don't want to do this then can just comment out, and add the/10 for files in nm
            if df_wrong["Angular unit"][j] == "1/A":
                reprocessed_arrays = reprocess_sasbdb_q_values(
                    profile._q_raw, profile._i_raw, profile._err_raw
                )
            elif df_wrong["Angular unit"][j] == "1/nm":
                reprocessed_arrays = reprocess_sasbdb_q_values(
                    profile._q_raw / 10, profile._i_raw, profile._err_raw
                )
            profile._q_raw = reprocessed_arrays["q"]
            profile._i_raw = reprocessed_arrays["I"]
            profile._err_raw = reprocessed_arrays["error"]

            q_raw, I_raw, err_raw = profile._q_raw, profile._i_raw, profile._err_raw

            profile.q = profile._q_raw
            profile.i = profile._i_raw
            profile.err = profile._err_raw

            mask = profile.q < 0.255
            q, I, err = profile.q[mask], profile.i[mask], profile.err[mask]
            profile.q = q
            profile.i = I
            profile.err = err

            # Log Profile
            try:
                # used to be plot_2 now profile
                save_plot(
                    sample_id,
                    "profile",
                    {
                        "type": "errorbar",
                        "x": q,
                        "y": I,
                        "yerr": err,
                        "ecolor": "g",
                        "fmt": "o",
                        "yscale": "log",
                        "title": f"Profile of {sample_id}",
                        "xlabel": "q ($\\AA^{-1}$)",
                        "ylabel": "Log(I(q))",
                        "q_truncated": q,
                        "I_truncated": I,
                        "err_truncated": err,
                        "q_untruncated": profile._q_raw,  # these are the untruncated values but sampled
                        "I_untruncated": profile._i_raw,
                        "err_untruncated": profile._err_raw,
                    },
                )
                # plt.close(fig)
            except Exception as e:
                logging.warning(f"Log profile plot failed for {sample_id}: {e}")

        except Exception as e:
            logging.warning(f"Failed to load profile for {sample_id}: {e}")
            df_wrong.loc[df_wrong.index[j], "Fatal Error"] = "Profile Load"
            plot_data.setdefault(sample_id, {})["Flagged"] = True
            print(
                'Did you remember to setup the dataframe with the "path" and "file name" columns?'
            )
            print(
                "If not use the `prepare_dataframe(dataframe_path, data_folder_apth)` function to do so."
            )
            print("for more information type prepare_dataframe??")
            continue

        # GPA Plot
        try:  # plot_1 before now GPA
            gpa_data = get_GPA(I, q, plot=False)
            save_plot(
                sample_id,
                "GPA",
                {
                    "type": "scatter",
                    "x": gpa_data["x"],
                    "y": gpa_data["y"],
                    "title": "GPA: Guinier Region Existence Check",
                    "xlabel": "$q^2$",
                    "ylabel": "qI(q)",
                },
            )
        except Exception as e:
            logging.warning(f"GPA plot failed for {sample_id}: {e}")

        # Kratky
        try:
            kratky_data = get_kratky(q, I, plot=False)
            save_plot(
                sample_id,
                "kratky",
                {
                    "type": "line",
                    "x": kratky_data["x"],
                    "y": kratky_data["y"],
                    "xlabel": "q",
                    "ylabel": "$q^2 I(q)$",
                    "title": "Kratky Plot",
                },
            )

        except Exception as e:
            logging.warning(f"Kratky plot failed for {sample_id}: {e}")

        # AutoRg
        try:
            (
                rg_auto,
                i0_auto,
                rg_err,
                i0_err,
                qmin,
                qmax,
                qrg_min,
                qrg_max,
                idx_min,
                idx_max,
                r_sq,
            ) = raw.auto_guinier(profile)

            update_murthy_df_row(
                df_wrong,
                j,
                {
                    "AutoRg Rg": rg_auto,
                    "AutoRg I0": i0_auto,
                    "AutoRg Rg Err": rg_err,
                    "AutoRg I0 Err": i0_err,
                    "AutoRg qmin": qmin,
                    "AutoRg qmax": qmax,
                    "AutoRg qRg Min": qrg_min,
                    "AutoRg qRg Max": qrg_max,
                    "AutoRg Guinier R²": r_sq,
                    "AutoRg Rg idx min": idx_min,
                    "AutoRg Rg idx max": idx_max,
                },
            )
            plot_data.setdefault(sample_id, {})["Auto Rg"] = {
                "nmin": idx_min,
                "nmax": idx_max,
                "Rg": rg_auto,
                "i0": i0_auto,
                "Rg Err": rg_err,
                "I0 Err": i0_err,
                "qmin": qmin,
                "qmax": qmax,
                "fit qRg Min": qrg_min,
                "fit qRg Max": qrg_max,
                "R2": r_sq,
            }

        except Exception as e:
            logging.warning(f"AutoRg failed for {sample_id}: {e}")
            skip_sample = True  # Flag to skip further analysis for this sample
        if skip_sample:
            df_wrong.loc[df_wrong.index[j], "Fatal Error"] = "Auto Gunier"
            plot_data.setdefault(sample_id, {})["Flagged"] = True
            continue

        # P(r)
        try:
            pr_fits_dict = get_all_pr_results(profile, q, I, err)
            plot_data.setdefault(sample_id, {})["pr_fits"] = pr_fits_dict
            # sample_fits = plot_data["SASDPB9.dat"]["pr_fits"] # This is how can access the Prs for example

            update_murthy_df_row(
                df_wrong,
                j,
                {
                    "Num P(r) Fits": len(pr_fits_dict),
                    "Avg P(r) Rg": np.mean([v["Rg"] for v in pr_fits_dict.values()]),
                },
            )
        except Exception as e:
            logging.warning(f"P(r) fit failed for {sample_id}: {e}")

        # Here now running Method 1 For Rg
        try:
            pr_rg_list = [fit["Rg"] for fit in pr_fits_dict.values()]
            rg_method1_df, rg_method1_all = rg_method_1(q, I, err, pr_rg_list)

            if rg_method1_df is not None:
                plot_data.setdefault(sample_id, {})["Rg Method 1"] = {
                    "candidates_df": rg_method1_df.to_dict(orient="list"),
                    "raw_dicts": rg_method1_all,
                }

                update_murthy_df_row(
                    df_wrong,
                    j,
                    {
                        "Method 1 Rg Count": len(rg_method1_df),
                        "Method 1 Rg Mean": round(rg_method1_df["Rg"].mean(), 2),
                        "Method 1 Best R²": round(rg_method1_df["fit_r2"].max(), 3),
                    },
                )

            # best_fit = rg_method1_df.sort_values(by='fit_r2', ascending=False).iloc[0]
            # update_murthy_df_row(df_wrong, j, {
            #     'Method 1 Rg': best_fit['Rg'],
            #     'Method 1 I0': best_fit['i0'],
            #     'Method 1 qRgmin': best_fit['qRgmin'],
            #     'Method 1 qRgmax': best_fit['qRgmax'],
            #     'Method 1 R²': best_fit['fit_r2'],
            #     'Method 1 Residual Width': best_fit['Res window'],
            #     'Method 1 GPA Peak': best_fit['GPA x peak'],
            #     'Method 1 Peak/Xcross': best_fit['peaks/x-cross']
            # })

        except Exception as e:
            logging.warning(f"Rg Method 1 failed for {sample_id}: {e}")
            skip_sample = True  # Flag to skip further analysis for this sample
        if skip_sample:
            df_wrong.loc[df_wrong.index[j], "Fatal Error"] = "Method 1 Initialization"
            plot_data.setdefault(sample_id, {})["Flagged"] = True
            continue

        # Here doing filtering to get final Rg from method 1
        try:
            final_method1_df = select_final_rg_from_candidates(
                rg_method1_all, q, I, err, sample_id
            )

            if final_method1_df is not None:
                # best_fit = final_method1_df.sort_values(by='fit_r2', ascending=False).iloc[0]
                best_fit = final_method1_df.iloc[0]

                plot_data.setdefault(sample_id, {})["Rg Method 1 Final"] = (
                    final_method1_df.to_dict(orient="list")
                )
                update_murthy_df_row(
                    df_wrong,
                    j,
                    {
                        "Method 1 Final Rg": best_fit["Rg"],
                        "Method 1 Final Rg Err": best_fit["Rg Err"],  # NEW
                        "Method 1 Final I0": best_fit["i0"],  # New
                        "Method 1 Final I0 Err": best_fit["I0 Err"],  # NEW
                        "Method 1 Final R²": best_fit["fit_r2"],
                        "Method 1 qRgmin": best_fit["qRgmin"],
                        "Method 1 qRgmax": best_fit["qRgmax"],
                        "Method 1 GPA Peak": best_fit["GPA x peak"],
                        "Method 1 Res Width": best_fit["Res window"],
                        "Method 1 nmin": best_fit["nmin"],
                        "Method 1 nmax": best_fit["nmax"],
                        "Method 1 Peak/Xcross": best_fit["peaks/x-cross"],
                        "Method 1 GPA x peak": best_fit["GPA x peak"],
                        "Method 1 GPA y peak": best_fit["GPA y peak"],
                    },
                )

            else:
                logging.warning(f"Method 1 could not resolve Rg for {sample_id}")
                skip_sample = True  # Flag to skip further analysis for this sample
                if skip_sample:
                    df_wrong.loc[df_wrong.index[j], "Fatal Error"] = "Method 1 Step 2"
                    plot_data.setdefault(sample_id, {})["Flagged"] = True

                    continue
        except Exception as e:
            logging.warning(f"Rg Method 1 final selection failed for {sample_id}: {e}")
            skip_sample = True  # Flag to skip further analysis for this sample
            if skip_sample:
                df_wrong.loc[df_wrong.index[j], "Fatal Error"] = (
                    "Method 1 Final Selection"
                )
                plot_data.setdefault(sample_id, {})["Flagged"] = True
                continue

        # Here now making selection for Final Rg based on Mean residuals
        try:
            selection = select_best_rg_method(
                q,
                I,
                err,
                rg_auto,
                i0_auto,
                best_fit["Rg"],
                best_fit["i0"],
                rg_auto_err=df_wrong.loc[j, "AutoRg Rg Err"],
                i0_auto_err=df_wrong.loc[j, "AutoRg I0 Err"],
                rg1_err=best_fit["Rg Err"],
                i01_err=best_fit["I0 Err"],
                r2_auto=df_wrong.loc[j, "AutoRg Guinier R²"],
                r2_1=best_fit["fit_r2"],
                sample_id=sample_id,
            )

            if selection:
                update_murthy_df_row(
                    df_wrong,
                    j,
                    {
                        "Final Rg": selection["Final Rg"],
                        "Final qRg min": selection["Final qRg min"],
                        "Final qRg max": selection["Final qRg max"],
                        "Final I0": selection["Final I0"],
                        "Final Rg Err": selection["Final Rg Err"],
                        "Final I0 Err": selection["Final I0 Err"],
                        "Final Rg R²": selection["Final R²"],
                        "Rg Method": selection["Selected Method"],
                        "Final Rg Residual Mean": selection["Residual Stats"][
                            "residual_mean"
                        ][0],
                        "Final Rg Reduced Chi²": selection["Residual Stats"][
                            "Reduced Chi Squared"
                        ][0],
                    },
                )
                if selection["Selected Method"] == "Method 1":
                    df_wrong.loc[df_wrong.index[j], "Final G qRgmin"] = df_wrong.loc[
                        df_wrong.index[j], "Method 1 qRgmin"
                    ]
                    df_wrong.loc[df_wrong.index[j], "Final G qRgmax"] = df_wrong.loc[
                        df_wrong.index[j], "Method 1 qRgmax"
                    ]
                elif selection["Selected Method"] == "AutoRg":
                    df_wrong.loc[df_wrong.index[j], "Final G qRgmin"] = df_wrong.loc[
                        df_wrong.index[j], "AutoRg qRg Min"
                    ]
                    df_wrong.loc[df_wrong.index[j], "Final G qRgmax"] = df_wrong.loc[
                        df_wrong.index[j], "AutoRg qRg Max"
                    ]

                plot_data.setdefault(sample_id, {})["Rg Selection"] = selection
        except Exception as e:
            logging.warning(f"Final Rg selection failed for {sample_id}: {e}")
            skip_sample = True  # Flag to skip further analysis for this sample
            if skip_sample:
                df_wrong.loc[df_wrong.index[j], "Fatal Error"] = "Final Rg Selection"
                plot_data.setdefault(sample_id, {})["Flagged"] = True
                continue

        # Here selecting a Pr from the ones already did

        try:
            pr_fits_dict = plot_data[sample_id]["pr_fits"]
            (
                rg_min,
                pr_rg_err_list,
                i0_p_list,
                pr_i0_err_list,
                chi_sq_list,
                dmax_mins,
                logas,
                dmax_err,
                pr_qmin_list,
                pr_qmax_list,
                pr_list,
                pr_i_orig,
                pr_fit,
                pr_err_orig,
                pr_q_orig,
                pr_qxt,
                nmins,
            ) = unpack_pr_fits_dict(pr_fits_dict)

            fin_pr, best_idx = select_best_pr_fit(
                rg_min,
                pr_rg_err_list,
                i0_p_list,
                pr_i0_err_list,
                chi_sq_list,
                dmax_mins,
                logas,
                dmax_err,
                pr_qmin_list,
                pr_qmax_list,
                df_wrong["Final Rg"][j],
                df_wrong["Final I0"][j],
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
                df_wrong,
                j,
            )

            # Plot 6: Final P(r) used to be called plot_6
            plot_data[sample_id]["pr_plot"] = {
                "type": "scatter",
                "x": pr_list[best_idx][0],
                "y": pr_list[best_idx][1],
                "Rg": rg_min[best_idx],
                "i0": i0_p_list[best_idx],
                "title": f"P(r) Rg: {rg_min[best_idx]}%\n"
                f"Dmax: {round(dmax_mins[best_idx], 0)} +/- {round(fin_pr['Dmax Error'][0], 0)}",
                "xlabel": "r",
                "ylabel": "P(r)",
                "Rgs considered": rg_min,
                "i0s considered": i0_p_list,
                "pr_i_orig": pr_i_orig[best_idx],
                "pr_err_orig": pr_err_orig[best_idx],
                "pr_q_orig": pr_q_orig[best_idx],
                "pr_fit": pr_fit[best_idx],
                "nmins": nmins[best_idx],
                "chis considered": chi_sq_list,
            }
            # Since added the errors
            plot_data[sample_id]["pr_plot"].update(
                {
                    "Rg err": pr_rg_err_list[best_idx],
                    "i0 err": pr_i0_err_list[best_idx],
                    "qmin": pr_qmin_list[best_idx],
                    "qmax": pr_qmax_list[best_idx],
                }
            )

            # Plot 7: Residuals
            residuals = pr_i_orig[best_idx] - pr_fit[best_idx]
            residuals_x = q[nmins[best_idx] :]
            residuals_y = residuals / pr_err_orig[best_idx]
            normalized_residuals = residuals_y
            # plot_7 now called pr_residuals
            plot_data[sample_id]["pr_residuals"] = {
                "type": "scatter",
                "q_extrapolated": pr_qxt[best_idx],
                "i_fit": pr_fit[best_idx],
                "x_line": q[nmins[best_idx] :],
                "y_line": I[nmins[best_idx] :],
                "title": f"Fit/Data $X^2$: {round(chi_sq_list[best_idx], 3)}%\n"
                f"Dmax +/- {round(fin_pr['Dmax Error'][0], 0)}",
                "xlabel": "q",
                "ylabel": "I(q)",
                "residuals_x": residuals_x,
                "residuals_y": residuals_y,
                "Chi_sqr": chi_sq_list[best_idx],
                "normalized residuals": normalized_residuals,
                "gi_bift_i_orig": pr_i_orig[best_idx],
                "err_orig": pr_err_orig[best_idx],
                "nmin": nmins[best_idx],
            }

        except Exception as e:
            logging.warning(
                f"Failed to extract and select final P(r) for {sample_id}: {e}"
            )
            skip_sample = True  # Flag to skip further analysis for this sample
            if skip_sample:
                df_wrong.loc[df_wrong.index[j], "Fatal Error"] = "Final P(r) Selection"
                plot_data.setdefault(sample_id, {})["Flagged"] = True
                continue

        # --- Franke Feature Extraction and Dimensionless Kratky Storage ---
        try:
            final_rg = df_wrong.loc[j, "Final Rg"]
            final_i0 = df_wrong.loc[j, "Final I0"]

            if (
                pd.notna(final_rg)
                and pd.notna(final_i0)
                and final_rg > 0
                and final_i0 > 0
            ):
                # Compute Franke features (no plotting)
                df_wrong = compute_franke_features(
                    q, I, final_rg, final_i0, sample_id, df_wrong, j
                )

                # Now optionally store Dimless Kratky in plot_data
                qRg = q_raw * final_rg
                IqRg2 = ((qRg) ** 2) * I_raw / final_i0

                plot_data.setdefault(sample_id, {})["Dimless Kratky"] = {
                    "type": "line",
                    "x": qRg,
                    "y": IqRg2,
                    "xlabel": "qRg",
                    "ylabel": "$(qRg)^2 I(q)/I(0)$",
                    "title": "Dimensionless Kratky",
                    "qRg": qRg,
                    "qRg^2": IqRg2,
                }

            else:
                logging.warning(
                    f"Skipping Franke features, & Dim Kratky for {sample_id} due to invalid Rg/I0"
                )
                skip_sample = True  # Flag to skip further analysis for this sample
                if skip_sample:
                    df_wrong.loc[df_wrong.index[j], "Fatal Error"] = "Franke Features"
                    continue
            # Here adding the clustering and probabilities
            try:
                gmm_results = assign_gmm_clusters(df_wrong, j, gmm_bundle)
                if gmm_results:
                    plot_data.setdefault(sample_id, {})["GMM Clustering"] = gmm_results
            except Exception as e:
                logging.warning(f"GMM block failed for {sample_id}: {e}")

        except Exception as e:
            logging.warning(f"Franke block failed for {sample_id}: {e}")
        try:
            pred_dmax, dmax_feats = predict_dmax_from_features_only(
                df_wrong, j, dmax_bundle
            )

            df_wrong.loc[df_wrong.index[j], "Predicted Dmax"] = pred_dmax

            if isinstance(dmax_feats, dict) and "error" not in dmax_feats:
                plot_data.setdefault(sample_id, {})["Predicted Dmax"] = {
                    "features_used": dmax_feats,
                    "prediction": pred_dmax,
                }
            else:
                plot_data.setdefault(sample_id, {})["Predicted Dmax"] = {
                    "error": dmax_feats.get("error", "Unknown error")
                }

        except Exception as e:
            logging.warning(f"Final Dmax prediction block failed for {sample_id}: {e}")

    print_end_time(start_time)
    return plot_data, df_wrong


def analyze_and_save(df_path, start_index=0, end_index=None, output_dir=None):
    """
    Main function to analyze SAXS data from a DataFrame and save results.
    Same as run_analysis but with input and output handling.

    :param df_path: Path to the input Excel file containing the file names, path and angular units.
    :param start_index: Index to start analysis from (default is 0). Useful for analyzing large sets in portions
    :param end_index: If specified, index to stop analysis at (exclusive). Default is None which means all data.
    :param output_dir: Directory to save results. Optional, if not specified, a 'return' folder will be created next to the input file.
    :return: Tuple of plot_data dictionary and updated DataFrame with results.
    """

    def sanitize_path(path_str):
        return Path(str(path_str).strip().strip('"').strip("'"))

    def clean_dataframe_paths(df, column_name):
        df[column_name] = df[column_name].apply(
            lambda x: str(Path(str(x).strip().strip('"').strip("'")))
        )
        return df

    # Clean up and parse input path
    df_path = sanitize_path(df_path)

    # If output_dir is not specified, create a 'return' folder next to the input file
    if output_dir is None:
        output_dir = df_path.parent / "return"
    else:
        output_dir = sanitize_path(output_dir)

    print(f"Using input file: {df_path}")
    print(f"Saving results to: {output_dir}")

    # Load and clean dataframe
    df = pd.read_excel(df_path)
    df = clean_dataframe_paths(df, "path")
    df["path"] = df["path"] + "/"

    # Run analysis
    if end_index is None:
        plot_data, updated_df = run_analysis(df, start_index)
    elif int(end_index) > len(df):
        raise ValueError(
            f"end_index {end_index} is greater than length of df {len(df)}"
        )
    else:
        plot_data, updated_df = run_analysis(df[: int(end_index)], start_index)

    # Save results
    # Only apply auto-folder logic if output_dir wasn't specified
    # This makes sure no overwriting happens if multiple instances of the script are run simultaneously
    if output_dir == "outputs":
        output_dir = get_unique_output_dir("results")
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    dump(plot_data, output_dir / "plot_data.joblib")
    updated_df.to_excel(output_dir / "results.xlsx")
    beep()  # Notify user that analysis is complete
    return plot_data, updated_df


import pandas as pd
from pathlib import Path
from datetime import datetime


def prepare_dataframe(dataframe_path=None, folder_path=None, angular_unit=None):
    """
    Prepares and saves a dataframe for SAXS analysis with required columns:
    - 'file name'
    - 'path'
    - 'Angular unit'

    Parameters:
    ----------
    dataframe_path : str or Path, optional
        Path to an existing Excel file with 'file name' and 'path' columns.
    folder_path : str or Path, optional
        If dataframe_path is not provided, use this to create a new dataframe.
    angular_unit : str
        Unit of the angular axis. Can be '1/A', 'A', '1/nm', or 'nm'.

    Returns:
    -------
    pd.DataFrame
        Formatted dataframe ready for analysis.
    """
    print("folder_path before parsing:", folder_path)

    if angular_unit is None:
        raise ValueError(
            "You must provide the 'angular_unit' argument (e.g., '1/A', 'nm')."
        )

    # Normalize angular unit
    angular_unit = angular_unit.strip().lower()
    if angular_unit in ["a", "1/a"]:
        angular_unit = "1/A"
    elif angular_unit in ["nm", "1/nm"]:
        angular_unit = "1/nm"
    else:
        raise ValueError("angular_unit must be '1/A' or '1/nm'")

    save_path = None

    if dataframe_path:
        dataframe_path = Path(str(dataframe_path).strip().strip('"').strip("'"))
        df = pd.read_excel(dataframe_path)

        if "path" not in df.columns or "file name" not in df.columns:
            raise ValueError("Dataframe must contain 'file name' and 'path' columns.")

        # Clean up paths
        df["path"] = df["path"].apply(
            lambda x: str(Path(str(x).strip().strip('"').strip("'")))
        )
        df["path"] = df["path"].apply(lambda x: x if x.endswith("/") else x + "/")

        save_path = dataframe_path.with_stem(dataframe_path.stem + "_input")

    elif folder_path:
        folder_path = Path(str(folder_path).strip().strip('"').strip("'"))
        if not folder_path.is_dir():
            raise ValueError(f"{folder_path} is not a valid directory.")

        all_files = sorted([f.name for f in folder_path.glob("*") if f.is_file()])
        df = pd.DataFrame(
            {
                "file name": all_files,
                "path": [str(folder_path.resolve().as_posix()) + "/"] * len(all_files),
            }
        )

        # Save to parent of folder with timestamp
        today = datetime.now().strftime("%b_%d_%y")  # e.g., Jun_19_25
        save_path = folder_path.parent / f"input_df_{today}.xlsx"

    else:
        raise ValueError("You must provide either 'dataframe_path' or 'folder_path'.")

    # Add angular unit
    df["Angular unit"] = angular_unit

    # Save
    df.to_excel(save_path, index=False)
    print(f"Saved cleaned dataframe to: {save_path}")

    return df
