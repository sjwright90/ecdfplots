# %%
from .helperfnc import ecdf_CI
from pandas import DataFrame, read_csv
from numpy import array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path


class Ecdf_Plotter:
    def __init__(
        self,
        raw_data,
        imputed_data,
        metals,
        destination="./",
        filename="ECDF_plots.pdf",
    ):
        if isinstance(raw_data, DataFrame):
            self.raw_data = raw_data
        else:
            try:
                raw_data = Path(raw_data)
                if raw_data.exists() & (raw_data.suffix == ".csv"):
                    self.raw_data = read_csv(raw_data)
            except:
                raise TypeError("raw_data must be a DataFrame or a path to a .csv file")
        if isinstance(imputed_data, DataFrame):
            self.imputed_data = imputed_data
        else:
            try:
                imputed_data = Path(imputed_data)
                if imputed_data.exists() & (imputed_data.suffix == ".csv"):
                    self.imputed_data = read_csv(imputed_data)
            except:
                raise TypeError(
                    "imputed_data must be a DataFrame or a path to a .csv file"
                )

        self.destination = Path(destination)

        self.filename = Path(filename)
        if self.filename.suffix != ".pdf":
            self.filename = self.filename.with_suffix(".pdf")

        if array(metals).ndim == 0:
            raise TypeError("metals must be list-like")
        else:
            self.metals = metals

    def reset_data(self, raw_data=None, imputed_data=None):
        if raw_data is not None:
            if isinstance(raw_data, DataFrame):
                self.raw_data = raw_data
            else:
                try:
                    raw_data = Path(raw_data)
                    if raw_data.exists() & (raw_data.suffix == ".csv"):
                        self.raw_data = read_csv(raw_data)
                except:
                    raise TypeError(
                        "raw_data must be a DataFrame or a path to a .csv file"
                    )
        if imputed_data is not None:
            if isinstance(imputed_data, DataFrame):
                self.imputed_data = imputed_data
            else:
                try:
                    imputed_data = Path(imputed_data)
                    if imputed_data.exists() & (imputed_data.suffix == ".csv"):
                        self.imputed_data = read_csv(imputed_data)
                except:
                    raise TypeError(
                        "imputed_data must be a DataFrame or a path to a .csv file"
                    )

    def reset_metals(self, metals):
        metals = array(metals)
        if metals.ndim == 0:
            raise TypeError("metals must be list-like")
        else:
            self.metals = metals

    def reset_filename(self, filename):
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")
        else:
            if not filename.endswith(".pdf"):
                filename += ".pdf"
            self.filename = filename

    def plotter(self):
        with PdfPages(self.destination / self.filename) as pdf:  # type: ignore
            for col in self.imputed_data.loc[:, self.metals].columns:
                figx, axx = plt.subplots()
                x_r, y_r, l_r, u_r = ecdf_CI(self.raw_data[col].values)
                x_i, y_i, l_i, u_i = ecdf_CI(self.imputed_data[col].values)
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
                pdf.savefig(figx)
                plt.close()
