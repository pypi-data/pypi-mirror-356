"""
This test shows how to run the C-Xool toolbox with a realistic grid file,
a short date interval, and selected ERA5 variables ('msl' and 'wind') for testing.
It then compares the output with a given and trusted reference NetCDF file to ensure
numerical agreement within a reasonable tolerance.

It does:
    1.- Call function main.
    2.- Perform a full run.
    3.- Compares the results with a referenced.

 Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Aranda, Christian Mario Appendini
     To report bugs, questions, feedback or just greetings, please use:
         cargaezg@iingen.unam.mx
"""

import sys

import numpy as np
import xarray as xr
from cxool.cxool_cli import main

sys.argv = [
    "cxool",
    "--grid-name",
    "nordseedeu10km_grid.nc",
    "--interval=6",
    "--initialdate",
    "1993-12-31",
    "--finaldate",
    "1994-01-01",
    "--vars-to-interp",
    "msl",
    "wind",
    "--final-interpolated-file",
    "forcing_Deu_NorthernSea.nc",
]


def test_differences():
    """Fully runs C-Xool to compare with a trusted reference."""
    main()
    with xr.open_dataset("reference_Deu_NS.nc") as refe:
        with xr.open_dataset("forcing_Deu_NorthernSea.nc") as forcing:
            diff = refe["Pair"] - forcing["Pair"]
            assert np.abs(diff.values).sum() <= 1e-5
            diff = refe["Pair"] - forcing["Pair"]
            assert np.abs(diff.values).sum() <= 1e-5
            diff = refe["Pair"] - forcing["Pair"]
            assert np.abs(diff.values).sum() <= 1e-5
