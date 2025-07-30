"""
Example: Minimal C-Xool run
This script shows how to run C-Xool from the command line using real options,
with a specified grid, time interval, and list of ERA5 variables.
 Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Aranda, Christian Mario Appendini
     To report bugs, questions, feedback or just greetings, please use:
         cargaezg@iingen.unam.mx
"""

import sys

from cxool.cxool_cli import main

sys.argv = [
    "cxool",
    "--grid-name",
    "nordseedeu10km_grid.nc",
    "--interval=6",
    "--initialdate",
    "1993-10-25",
    "--finaldate",
    "1993-10-30",
    "--vars-to-interp",
    "msl",
    "t2m",
    "tcc",
    "avg_snswrf",
    "avg_sdlwrf",
    "avg_snlwrf",
    "avg_slhtf",
    "avg_ishf",
    "wind",
    "--final-interpolated-file",
    "forcing_Deu_NorthernSea.nc",
    "--plot",
    "msl",
    "t2m",
    "tcc",
    "avg_snswrf",
    "avg_sdlwrf",
    "avg_snlwrf",
    "avg_slhtf",
    "avg_ishf",
    "wind",
    "--plot-interval",
    "3",
    "--plot-format",
    "png",
    "--projection",
    "stereographic",
    "--output-folder",
    "outputfolder",
]

main()
