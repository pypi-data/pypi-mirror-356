#!/usr/bin/env python3
"""
Example to execute C-Xool – V1: Oceanographic exploration

This script prepares the atmospheric forcing over a defined grid for use in ROMS ocean modelling.

Example:
    cxool --grid-name inluum_grid.nc \
          --initialdate 1983-10-25 \
          --finaldate 1983-10-31 \
          --interval 6 \
          --plot-interval 0 \
          --vars-to-interp t2m wind msl tcc avg_snswrf q tp \
          --final-interpolated-file "roms_frc.nc" \
          --data-storage "./raw_era5" \
          --data-subfolder "merged_data"

 Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Aranda, Christian Mario Appendini
     To report bugs, questions, feedback or just greetings, please use:
         cargaezg@iingen.unam.mx
"""


import subprocess


def main():
    command = [
        "cxool",
        "--grid-name",
        "inluum_grid.nc",
        "--initialdate",
        "1983-10-25",
        "--finaldate",
        "1983-10-31",
        "--interval",
        "6",
        "--plot-interval",
        "0",
        "--vars-to-interp",
        "t2m",
        "wind",
        "msl",
        "tcc",
        "avg_snswrf",
        "q",
        "tp",
        "--final-interpolated-file",
        "roms_frc.nc",
        "--data-storage",
        "./raw_era5",
        "--data-subfolder",
        "merged_data",
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running C-Xool: {e}")


if __name__ == "__main__":
    main()
