"""
Unit tests to verify that the plot_variables() function in your cxool.plotting module
successfully generates plot image files when provided with minimal, synthetic data.

It does:
    1. Generates a dummy dataset with scalar and vector fields ('Pair', 'Uwind', 'Vwind').
    2. Defines ROMS variable specifications using ERA5 metadata.
    3. Calls plot_variables().
    4. Verifies that PNG output files are written to the expected output folders.

Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Arandía, Christian Mario Appendini
C-Xool: ERA5 Atmospheric Boundary Conditions Toolbox for Ocean Modelling with ROMS.
License: GNU GPL v3
"""

import numpy as np
import xarray as xr
from cartopy import crs as ccrs
from cxool.plotting import plot_variables
from cxool.specifications import ERA5SpecSL, ROMSSpecScalar, ROMSSpecVector


def test_plot_variables(tmp_path):
    """Generates a dummy data set to plot and verifies that the plotting function works,
    and that the files are generated."""
    time = [np.datetime64("1993-10-25T00")]
    scalar = np.random.rand(1, 4, 6)

    ds = xr.Dataset(
        {
            "Pair": (["time", "eta_rho", "xi_rho"], scalar),
            "Uwind": (["time", "eta_rho", "xi_rho"], scalar),
            "Vwind": (["time", "eta_rho", "xi_rho"], scalar),
            "time": ("time", time),
            "lat": (["eta_rho", "xi_rho"], np.linspace(0, 1, 24).reshape(4, 6)),
            "lon": (["eta_rho", "xi_rho"], np.linspace(0, 1, 24).reshape(4, 6)),
        }
    )

    projected = np.dstack(
        np.meshgrid(np.linspace(0, 10, 4), np.linspace(0, 10, 6))
    ).reshape(4, 6, 2)
    angle = xr.DataArray(np.zeros((4, 6)), dims=["eta_rho", "xi_rho"])

    specpair = ROMSSpecScalar(
        ERA5SpecSL("msl", "mean_sea_level_pressure", "Pa"),
        "Pair",
        "Mean sea level pressure",
        "hPa",
        "hPa",
        scale=1.0e-2,
        plottype="diff",
    )
    specwind = ROMSSpecVector(
        [
            ERA5SpecSL("u10", "10m_u_component_of_wind", "ms$^{-1}$"),
            ERA5SpecSL("v10", "10m_v_component_of_wind", "ms$^{-1}$"),
        ],
        roms_name="Wind",
        roms_long_name="10 metre wind",
        roms_unit="ms-1",
        plot_unit="ms$^{-1}$",
        roms_comp_names=["Uwind", "Vwind"],
        roms_comp_long_names=["10 metre U wind component", "10 metre V wind component"],
        plottype="speed",
    )

    plot_variables(
        var_list_to_plot=[specpair, specwind],
        loaded_file_to_plot=ds,
        discrete_colors=5,
        homogenise_lims=True,
        interval=1,
        projected_coords=projected,
        projection=ccrs.PlateCarree(),
        var_angle=angle,
        scale_factor=100,
        arrowdensity=1,
        output_folder=tmp_path,
        plots_folder="plots",
        plot_format="png",
    )

    pairfolder = tmp_path / "plots" / "Pair"
    pairfiles = list(pairfolder.glob("*.png"))
    windfolder = tmp_path / "plots" / "Wind"
    windfiles = list(windfolder.glob("*.png"))
    assert len(pairfiles) > 0, "No plot files were generated"
    assert len(windfiles) > 0, "No plot generated for Uwind (wind vectors)"
