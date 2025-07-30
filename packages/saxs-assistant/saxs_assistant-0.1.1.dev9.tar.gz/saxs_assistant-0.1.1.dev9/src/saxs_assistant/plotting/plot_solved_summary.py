import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from ..features import min_max_function
from ..rg_tools import get_residuals_guinier_plot
from joblib import load


def plot_solved_summary(
    plot_data_path, output_folder="./summary_plots", pdf_name="solved_summary.pdf"
):
    # Load data internally
    if isinstance(plot_data_path, str):
        plot_data = load(plot_data_path)
    else:
        raise ValueError("plot_data_path should be a string path to a .joblib file")

    os.makedirs(output_folder, exist_ok=True)
    pdf_path = os.path.join(output_folder, pdf_name)

    with PdfPages(pdf_path) as pdf:
        for sample_id, plot_item in plot_data.items():
            if "Flagged" in plot_item:
                continue  # Skip flagged entries

            file_name = plot_item["profile"]["title"].split(" ")[-1]
            sample_short = file_name.split(".")[0]

            # --- Setup master figure for one sample (4 stacked rows) ---
            fig = plt.figure(figsize=(8.5, 12))
            outer_gs = gridspec.GridSpec(
                4, 1, hspace=0.4, height_ratios=[1, 1, 1.1, 1.1]
            )

            # --- Row 1: Profile, GPA, Dimless Kratky ---
            gs1 = gridspec.GridSpecFromSubplotSpec(
                1, 3, subplot_spec=outer_gs[0], wspace=0.4
            )
            axs = [fig.add_subplot(gs1[0, i]) for i in range(3)]

            axs[0].errorbar(
                plot_item["profile"]["x"],
                plot_item["profile"]["y"],
                plot_item["profile"]["yerr"],
                ecolor="g",
                fmt="bo",
                markersize=2,
                elinewidth=0.5,
            )
            axs[0].set_yscale("log")
            axs[0].set_title(file_name, fontsize=7.5)
            axs[0].set_xlabel(r"$q$ $(\mathrm{\AA}^{-1})$", fontsize=7)
            axs[0].set_ylabel(r"$log(I(q))$", fontsize=7)
            axs[0].tick_params(axis="both", which="major", labelsize=7)

            axs[1].plot(
                plot_item["GPA"]["x"], plot_item["GPA"]["y"], "ob", markersize=2
            )
            axs[1].set_title("GPA", fontsize=7.5)
            axs[1].set_xlabel(r"$q$ $(\mathrm{\AA}^{-2})$", fontsize=7)
            axs[1].xaxis.get_offset_text().set_fontsize(6.5)
            axs[1].set_ylabel(f"${plot_item['GPA']['ylabel']}$", fontsize=7)
            axs[1].tick_params(axis="both", which="major", labelsize=7)

            axs[2].plot(
                plot_item["Dimless Kratky"]["x"],
                plot_item["Dimless Kratky"]["y"],
                "ob",
                markersize=2,
            )
            axs[2].set_title("Dimensionless Kratky", fontsize=7.5)
            axs[2].set_xlabel(r"$qR_g$", fontsize=7)
            axs[2].set_ylabel(r"$(qR_g)^2 I(q)/I(0)$", fontsize=7)
            axs[2].axvline(x=3**0.5, color="red", linestyle="--", linewidth=1)
            axs[2].axhline(
                y=1.1, color="red", linestyle="--", label="Globular Crosshairs"
            )
            axs[2].legend(fontsize=6.5, loc="best")
            axs[2].set_xlim([0, 6])
            axs[2].set_ylim([0, 2])
            axs[2].tick_params(axis="both", which="major", labelsize=7)

            # --- Row 2: GPA fits (Auto and Method 1) and GMM Clustering ---
            gs2 = gridspec.GridSpecFromSubplotSpec(
                1, 3, subplot_spec=outer_gs[1], width_ratios=[2.8, 2.8, 0.9], wspace=0.4
            )
            selected = plot_item["Rg Selection"]["Selected Method"]
            for idx, label, rg_key in zip(
                [0, 1],
                ["Auto $R_g$", "PDDF-Informed"],
                ["Auto Rg", "Rg Method 1 Final"],
            ):
                ax = fig.add_subplot(gs2[0, idx])
                rg = plot_item[rg_key]["Rg"] if idx == 0 else plot_item[rg_key]["Rg"][0]
                i0 = plot_item[rg_key]["i0"] if idx == 0 else plot_item[rg_key]["i0"][0]
                nmin = (
                    plot_item[rg_key]["nmin"]
                    if idx == 0
                    else plot_item[rg_key]["nmin"][0]
                )
                nmax = (
                    plot_item[rg_key]["nmax"]
                    if idx == 0
                    else plot_item[rg_key]["nmax"][0]
                )
                x_maxs, y_maxs, plot_params = get_dim_GPA2(
                    plot_item["profile"]["y"],
                    plot_item["profile"]["x"],
                    rg,
                    i0,
                    nmin,
                    nmax,
                )
                gpa_ = plot_params["data"]
                ax.plot(gpa_["x"], gpa_["y"], "bo", markersize=3, label="Data")
                ax.plot(
                    gpa_["included_x"],
                    gpa_["included_y"],
                    "o",
                    color="orange",
                    markersize=3,
                    label="Included Data",
                )
                ax.plot(
                    gpa_["guinier_x"], gpa_["guinier_y"], "g--", label="Calculated I(q)"
                )
                for x_val, y_data, y_model in zip(
                    gpa_["x"], gpa_["y"], gpa_["guinier_y"]
                ):
                    ax.plot(
                        [x_val, x_val],
                        [y_data, y_model],
                        color="red",
                        linewidth=1,
                        alpha=0.7,
                    )
                ax.axvline(x=1.5, linestyle="--", color="purple")
                ax.axhline(
                    y=np.log(0.7428),
                    linestyle="--",
                    color="purple",
                    label="Ideal Peak Location",
                )
                ax.set_xlabel(r"$(q R_g)^2$", fontsize=7)
                ax.set_ylabel("ln[$q$$R_g$$I(q)$/$I(0)$]", fontsize=7)
                ax.set_xlim([0, 4])
                ax.set_ylim([-2, 0])
                ax.set_title(label, fontsize=7.5)
                ax.legend(fontsize=6.5)
                ax.tick_params(labelsize=7)
                if idx == 1 and selected == "Method 1":
                    for spine in ax.spines.values():
                        spine.set_edgecolor("green")
                        spine.set_linewidth(2)
                elif idx == 0 and selected == "AutoRg":
                    for spine in ax.spines.values():
                        spine.set_edgecolor("green")
                        spine.set_linewidth(2)

            ax3 = fig.add_subplot(gs2[0, 2])
            prob_found = plot_item["GMM Clustering"]["Probabilities"]
            assigned_cluster = plot_item["GMM Clustering"]["Cluster"]
            probs = [prob_found[f"Cluster {i}"] for i in range(5)]
            labels = ["0 (Fd)", "1 (Pd)", "2 (Ds)", "3 (Gb)", "4 (Fx)"]
            colors = ["red", "skyblue", "green", "orange", "purple"]
            ax3.barh(range(len(probs)), probs, color=colors)
            ax3.set_xlim(0, 1)
            ax3.set_yticks([])
            ax3.set_xticks([0, 0.5, 1.0])
            ax3.set_title("Cluster\nProbs", fontsize=7.5)
            ax3.tick_params(axis="x", labelsize=7)
            for i, (label, prob) in enumerate(zip(labels, probs)):
                fontweight = "bold" if i == assigned_cluster else "normal"
                ax3.text(
                    -0.02,
                    i,
                    label,
                    va="center",
                    ha="right",
                    fontsize=6,
                    fontweight=fontweight,
                    transform=ax3.get_yaxis_transform(),
                )
                ax3.text(
                    prob + 0.02,
                    i,
                    f"{prob * 100:.1f}%",
                    va="center",
                    ha="left",
                    fontsize=7,
                )
            for spine in ["top", "right"]:
                ax3.spines[spine].set_visible(False)

            # --- Row 3: Auto & PDDF-Informed Guinier Residuals ---
            gs3 = gridspec.GridSpecFromSubplotSpec(
                2,
                2,
                subplot_spec=outer_gs[2],
                height_ratios=[2.5, 1],
                wspace=0.25,
                hspace=0.1,
            )

            # ---------- Left Column: Auto Guinier ----------
            results_auto = get_residuals_guinier_plot(
                plot_item["profile"]["y"],
                plot_item["profile"]["x"],
                plot_item["profile"]["yerr"],
                plot_item["Auto Rg"]["nmin"],
                plot_item["Auto Rg"]["nmax"],
            )
            ax_top = fig.add_subplot(gs3[0, 0])
            ax_bot = fig.add_subplot(gs3[1, 0], sharex=ax_top)

            ax_top.plot(
                results_auto["x_all"],
                results_auto["y_all"],
                "o",
                color="gray",
                alpha=0.8,
                markersize=2,
            )
            ax_top.plot(
                results_auto["x_fit"],
                results_auto["y_fit"],
                "o",
                color="blue",
                markersize=2,
            )
            ax_top.plot(
                results_auto["x_fit"],
                results_auto["y_model"],
                "-",
                color="red",
                linewidth=1,
                label=r"$R^2$ " + str(round(plot_item["Auto Rg"]["R2"], 3)),
            )
            ax_top.set_title(
                "Auto Guinier: $R_g$: "
                + str(round(plot_item["Auto Rg"]["Rg"], 2))
                + r"$\pm$"
                + str(round(plot_item["Auto Rg"]["Rg Err"], 2)),
                fontsize=7,
            )

            ax_top.set_ylabel(r"$\ln[I(q)]$", fontsize=7)
            ax_top.tick_params(axis="both", which="major", labelsize=7)
            ax_top.axvline(
                x=results_auto["x_fit"][0], linestyle="--", color="red", linewidth=1
            )
            ax_top.axvline(
                x=results_auto["x_fit"][-1], linestyle="--", color="red", linewidth=1
            )
            ax_top.set_ylim(
                [results_auto["y_model"].min() - 0.5, results_auto["y_all"].max() + 0.5]
            )
            ax_top.set_xlim(
                [0, results_auto["x_fit"][-1] + (results_auto["x_fit"].ptp() * 0.10)]
            )
            ax_top.tick_params(labelbottom=False)  # hides x-tick labels on top
            ax_top.legend(fontsize=6.5, loc="upper right")

            ax_bot.plot(
                results_auto["x_fit"], results_auto["residuals"], "b-", linewidth=1
            )
            ax_bot.axhline(y=0, linestyle="--", color="red", linewidth=1)
            ax_bot.set_xlabel(r"$q^2$ $(\mathrm{\AA}^{-2})$", fontsize=7)
            ax_bot.xaxis.set_major_formatter(FormatStrFormatter("%.4f"))
            ax_bot.set_ylabel(r"$\Delta \ln[I(q)] / \sigma(q)$", fontsize=7)
            ax_bot.tick_params(axis="both", which="major", labelsize=7)

            # ---------- Right Column: Method 1 ----------
            results_m1 = get_residuals_guinier_plot(
                plot_item["profile"]["y"],
                plot_item["profile"]["x"],
                plot_item["profile"]["yerr"],
                plot_item["Rg Method 1 Final"]["nmin"][0],
                plot_item["Rg Method 1 Final"]["nmax"][0],
            )
            ax_top = fig.add_subplot(gs3[0, 1])
            ax_bot = fig.add_subplot(gs3[1, 1], sharex=ax_top)

            # ax_top, ax_bot = axes[0, 1], axes[1, 1]

            ax_top.plot(
                results_m1["x_all"],
                results_m1["y_all"],
                "o",
                color="gray",
                alpha=0.8,
                markersize=2,
            )
            ax_top.plot(
                results_m1["x_fit"],
                results_m1["y_fit"],
                "o",
                color="blue",
                markersize=2,
            )
            ax_top.plot(
                results_m1["x_fit"],
                results_m1["y_model"],
                "-",
                color="red",
                linewidth=1,
                label=r"$R^2$ "
                + str(round(plot_item["Rg Method 1 Final"]["fit_r2"][0], 3)),
            )
            ax_top.set_title(
                "PDDF-Informed: $R_g$: "
                + str(round(plot_item["Rg Method 1 Final"]["Rg"][0], 2))
                + r"$\pm$"
                + str(round(plot_item["Rg Method 1 Final"]["Rg Err"][0], 2)),
                fontsize=7,
            )

            ax_top.set_ylabel(r"$\ln[I(q)]$", fontsize=7)
            ax_top.tick_params(axis="both", which="major", labelsize=7)
            ax_top.axvline(
                x=results_m1["x_fit"][0], linestyle="--", color="red", linewidth=1
            )
            ax_top.axvline(
                x=results_m1["x_fit"][-1], linestyle="--", color="red", linewidth=1
            )
            ax_top.set_ylim(
                [results_m1["y_model"].min() - 0.5, results_m1["y_all"].max() + 0.5]
            )
            ax_top.set_xlim(
                [0, results_m1["x_fit"][-1] + (results_m1["x_fit"].ptp() * 0.10)]
            )
            ax_top.tick_params(labelbottom=False)  # hides x-tick labels on top
            ax_top.legend(fontsize=6.5, loc="upper right")

            ax_bot.plot(results_m1["x_fit"], results_m1["residuals"], "b-", linewidth=1)
            ax_bot.axhline(y=0, linestyle="--", color="red", linewidth=1)
            ax_bot.set_xlabel(r"$q^2$ $(\mathrm{\AA}^{-2})$", fontsize=7)
            ax_bot.xaxis.set_major_formatter(FormatStrFormatter("%.4f"))
            ax_bot.set_ylabel(r"$\Delta \ln[I(q)] / \sigma(q)$", fontsize=7)
            ax_bot.tick_params(axis="both", which="major", labelsize=7)

            # Row 4 PDDF

            # ======= Left panel: PDDF Fit + Residuals =======
            gs4 = gridspec.GridSpecFromSubplotSpec(
                1, 2, subplot_spec=outer_gs[3], width_ratios=[3.2, 2.8], wspace=0.3
            )
            gs4_left = gridspec.GridSpecFromSubplotSpec(
                2, 1, subplot_spec=gs4[0], height_ratios=[2, 1], hspace=0.05
            )

            # Top: Fit
            # ax_fit = fig.add_subplot(gs4_left[0])
            # [your plotting code for fit...]

            # ======= Right panel: PDDF Plot =======
            # ax_pddf = fig.add_subplot(gs4[1])
            # [your PDDF curve plotting code...]

            # Top: Fit
            ax_fit = fig.add_subplot(gs4_left[0])
            ax_fit.plot(
                plot_item["pr_plot"]["pr_q_orig"],
                plot_item["pr_plot"]["pr_i_orig"],
                "o",
                color="blue",
                alpha=0.8,
                markersize=2,
                label="Data",
                linewidth=1,
            )
            ax_fit.plot(
                plot_item["pr_residuals"]["q_extrapolated"][1:],
                plot_item["pr_residuals"]["i_fit"],
                color="red",
                linewidth=1,
                label="Fitted Region",
            )
            ax_fit.set_yscale("log")
            ax_fit.set_title("Data/Fit", fontsize=7.5)

            ax_fit.set_ylabel(r"$I(q)$", fontsize=7)
            ax_fit.tick_params(axis="both", which="major", labelsize=7)
            ax_fit.legend(fontsize=7)

            # Bottom: Residuals
            ax_res = fig.add_subplot(gs4_left[1], sharex=ax_fit)
            ax_res.plot(
                plot_item["pr_residuals"]["residuals_x"],
                plot_item["pr_residuals"]["residuals_y"],
                "b-",
                linewidth=1,
            )
            ax_res.axhline(y=0, linestyle="--", color="red", linewidth=1)

            ax_res.set_xlabel(r"$q$ $(\mathrm{\AA})$", fontsize=7)
            ax_res.set_ylabel(r"$\Delta [I(q)]/\sigma(q)$", fontsize=7)
            ax_res.tick_params(axis="both", which="major", labelsize=7)

            # ======= Right panel: PDDF Plot =======
            predicted_dmax = plot_item["Predicted Dmax"]["prediction"]
            BIFT_dmax = plot_item["pr_plot"]["x"][-1]
            diff_dmax = (abs(predicted_dmax - BIFT_dmax) / BIFT_dmax) * 100

            ax_pddf = fig.add_subplot(gs4[1])
            ax_pddf.plot(
                plot_item["pr_plot"]["x"],
                plot_item["pr_plot"]["y"],
                "bo-",
                markersize=2,
                linewidth=1.5,
                label=f"BIFT $D_{{max}}$ = {BIFT_dmax:.1f} Å",
            )

            ax_pddf.set_xlabel(r"$r$ $(\mathrm{\AA})$", fontsize=7)
            ax_pddf.set_ylabel(r"$P(r)$", fontsize=7)
            xmax = max(predicted_dmax, BIFT_dmax)
            ax_pddf.set_xlim(0, xmax * 1.05)
            ax_pddf.set_ylim(bottom=0)
            ax_pddf.tick_params(axis="both", which="major", labelsize=7.5)
            ax_pddf.set_title(
                "PDDF $R_g$:"
                + str(round(plot_item["pr_plot"]["Rg"], 2))
                + "+/-"
                + str(round(plot_item["pr_plot"]["Rg err"], 2)),
                fontsize=7.5,
            )

            # Optional: vertical Dmax line
            if diff_dmax < 20:
                ax_pddf.axvline(
                    predicted_dmax,
                    color="green",
                    linestyle="--",
                    linewidth=1.5,
                    alpha=0.7,
                    label=f"Predicted $D_{{max}}$ = {predicted_dmax:.1f} Å",
                )
            elif diff_dmax >= 20:
                ax_pddf.axvline(
                    predicted_dmax,
                    color="red",
                    linestyle="--",
                    linewidth=1.5,
                    alpha=0.7,
                    label=f"Predicted $D_{{max}}$ = {predicted_dmax:.1f} Å",
                )

            ax_pddf.legend(fontsize=7)

            # fig.savefig(f'SI1_row4_Pr_residuals_{id}.png', dpi=300, bbox_inches='tight')
            # plt.show()

            pdf.savefig(fig)
            plt.close(fig)

    print(f"Saved PDF summary to {pdf_path}")
    return pdf_path


def get_dim_GPA2(I, q, rg, i0, nmin, nmax, plot=False):
    """Another Dimensionless GPA function that uses the same logic as get_dim_GPA but with different outputs, in
    the format of dictionary for plotting.
    Args:
        I (array): Intensity data.
        q (array): q values.
        rg (float): Radius of gyration.
        i0 (float): Intensity at zero angle.
        nmin (int): Minimum index for the range of interest.
        nmax (int): Maximum index for the range of interest.
        Returns:
        x_maxs (float): Maximum x value.
        y_maxs (float): Maximum y value.
        plot_params (dict): Dictionary containing plot parameters.
    """
    y = np.log((q * rg * I) / i0)
    x = (q * rg) ** 2
    index_max_y = np.argmax(y)
    index_max_plot = np.argmin(abs(x - 4))
    x_mins, x_maxs, y_mins, y_maxs = min_max_function(
        y[:index_max_plot], x[:index_max_plot]
    )

    # Prepare plot data for saving
    plot_params = {
        "type": "Dimensionless GPA",
        "data": {
            "x": x,
            "y": y,
            "included_x": x[nmin : nmax + 1],
            "included_y": y[nmin : nmax + 1],
            "guinier_x": x,
            "guinier_y": np.log((q * rg * (i0 * np.exp(-((rg**2 * q**2) / 3)))) / i0),
        },
        "lines": [
            {
                "x": [1.5, 1.5],
                "y": [-2, 0],
                "style": "--",
                "label": "Ideal Vertical Line",
            },
            {
                "x": [0, 4],
                "y": [np.log(0.7428), np.log(0.7428)],
                "style": "--",
                "label": "Ideal Horizontal Line",
            },
        ],
        "labels": {
            "title": "Dim GPA Rg: Peak",
            "xlabel": "$(Rgq)^2$",
            "ylabel": "ln[qRgI(q)/I(0)]",
        },
        "limits": {"xlim": [0, 4], "ylim": [-2, 0]},
    }

    if plot == True:
        fig, ax = plt.subplots()
        # Plot data
        ax.plot(plot_params["data"]["x"], plot_params["data"]["y"], "o", label="Data")
        ax.plot(
            plot_params["data"]["included_x"],
            plot_params["data"]["included_y"],
            "o",
            label="Included",
        )
        ax.plot(
            plot_params["data"]["guinier_x"],
            plot_params["data"]["guinier_y"],
            "--",
            label="Guinier Approximation",
        )
        # Plot lines
        for line in plot_params["lines"]:
            ax.plot(line["x"], line["y"], line["style"], label=line["label"])
        # Set labels and limits
        ax.set_title(plot_params["labels"]["title"])
        ax.set_xlabel(plot_params["labels"]["xlabel"])
        ax.set_ylabel(plot_params["labels"]["ylabel"])
        ax.set_xlim(plot_params["limits"]["xlim"])
        ax.set_ylim(plot_params["limits"]["ylim"])
        ax.legend()
        plt.show()

    return x_maxs, y_maxs, plot_params
