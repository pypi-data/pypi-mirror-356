"""
This unit test verifies that the interpolation function interpolate_to_grid()
from cxool.interpolation module works correctly by creating a mock input NetCDF dataset,
running the interpolation, and checking that the output file is generated.

It does:
    1.- Generates a dummy grid that fulfils ROMS requirements.
    2.- Generates dummy values for 'msl' and 'wind'.
    3.- Calls function interpolate_to_grid.
    4.- Checks the output file is properly produced.
Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Arandía, Christian Mario Appendini
C-Xool: ERA5 Atmospheric Boundary Conditions Toolbox for Ocean Modelling with ROMS.
License: GNU GPL v3
"""

import warnings

import numpy as np
import xarray as xr
from cxool.interpolation import interpolate_to_grid
from cxool.specifications import ERA5SpecSL, ROMSSpecScalar

warnings.filterwarnings("ignore", message="numpy.ndarray size changed")


class TestingGrid:
    """Generates a ROMS dummy grid correctly."""

    lat_rho = xr.DataArray(
        np.linspace(0, 1, 4).reshape(4, 1).repeat(5, axis=1), dims=("eta_rho", "xi_rho")
    )
    lon_rho = xr.DataArray(
        np.linspace(0, 1, 5).reshape(1, 5).repeat(4, axis=0), dims=("eta_rho", "xi_rho")
    )
    angle = xr.DataArray(np.zeros((4, 5)), dims=("eta_rho", "xi_rho"))


def test_interpolation_function(tmp_path):
    """Generates a set of dummy data to interpolate and verifies the interpolation,
    and the generation of the output file."""
    grid = TestingGrid()
    dummy_ds = xr.Dataset(
        {
            "msl": (["time", "latitude", "longitude"], 1000 + np.random.randn(1, 7, 7)),
            "latitude": (["latitude"], np.linspace(0, 1, 7)),
            "longitude": (["longitude"], np.linspace(0, 1, 7)),
            "time": (["time"], [np.datetime64("2022-01-01")]),
        }
    )
    input_file = tmp_path / "dummy_input.nc"
    dummy_ds.to_netcdf(input_file)

    ts_paths = {"msl": str(input_file)}

    interpolate_to_grid(
        fgrd=grid,
        ncf_filename=str(tmp_path / "out.nc"),
        ref_date="1948-01-01T00:00:00",
        variable_list={
            "msl": ROMSSpecScalar(
                ERA5SpecSL("msl", "msl", "Pa"), "Pair", "MSLP", "Pa", "hPa"
            )
        },
        ts_paths=ts_paths,
        memory_chunks=None,
    )

    with xr.open_dataset(tmp_path / "out.nc") as dummy:
        d_pair = dummy.Pair

    assert (tmp_path / "out.nc").exists()
    assert d_pair[0].shape == grid.lat_rho.shape
    assert d_pair[0].shape == grid.lon_rho.shape
