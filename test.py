# %%
from ecdfplots import Ecdf_Plotter
from ecdfplots.plottools import ecdf_CI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# %%
raw_data = pd.DataFrame(
    {
        "A": np.random.normal(0, 1, 100),
        "B": np.random.normal(0, 1, 100),
    }
)

imputed_data = raw_data.copy()

raw_data.loc[0:10, "A"] = np.nan
raw_data.loc[10:20, "B"] = np.nan
# %%

# %%
for col in ["A", "B"]:
    n_raw_missing = raw_data[col].isna().sum()
    figx, axx = plt.subplots()
    x_r, y_r, l_r, u_r = ecdf_CI(raw_data[col].values)
    x_i, y_i, l_i, u_i = ecdf_CI(imputed_data[col].values)
    axx.plot(x_r, y_r * 100, linestyle="--", lw=2, label="Raw", c="b")
    axx.plot(x_i, y_i * 100, linestyle="--", lw=2, label="Imputed", c="r")
    axx.plot(x_r, l_r * 100, c="b", alpha=0.2, linestyle="--")
    axx.plot(x_r, u_r * 100, c="b", alpha=0.2, linestyle="--")
    axx.plot(x_i, l_i * 100, c="r", alpha=0.2, linestyle="--")
    axx.plot(x_i, u_i * 100, c="r", alpha=0.2, linestyle="--")
    axx.set_yscale("log")
    axx.set_xscale("log")
    axx.legend()
    axx.set_xlabel(col, size=14)
    axx.set_ylabel("ECDF", size=14)
    axx.set_ylim(bottom=0.15)
    axx.text(
        0.5,
        -0.18,
        s=f"Raw missing: {n_raw_missing}\nTotal samples: {len(imputed_data)}",
        transform=axx.transAxes,
        size=9,
        ha="center",
        va="top",
        bbox=dict(
            boxstyle="round",
            facecolor="none",
            edgecolor="black",
        ),
    )

# %%

plotter = Ecdf_Plotter(raw_data, imputed_data, ["A", "B"])
# %%
plotter.plotter()
# should run
# %%
