<div align="right">
This file was written at LIPC, IINGEN, UNAM, <br>
in Sisal, Yucatan, Mexico, <br>
on the 17th of June 2025.
</div>

# C-Xool Example: Toy Model for ROMS Forcing

This folder contains an example of how to use **C-Xool** 
to generate atmospheric forcing for a simplified ROMS setup. 
It serves as a minimal working demonstration of the software.

## Example Description

This toy example shows how to run C-Xool with a real ERA5 variable list over a 
short simulation period using a test grid (`inluum_grid.nc`). 
The goal is to create a ROMS-compatible forcing file (`roms_frc.nc`) 
from ERA5 reanalysis data.
The toy model is not realistic, but it serves the purpose of showing 
that C-Xool successfully generates a working atmospheric forcing file for ROMS.

The example includes:

- An instruction file (`cxool_instructions.txt`)
- A small grid file (`data/inluum_grid.nc`)
- An execution script (`data/run_cxool_example.py`)
- A sample input file for ROMS (`External/inluum.in`)
- A sample CPP header file (`Include/gulfofmexico.h`)
- A README.md file 

<pre><code>
                               ROMS_example
                               ├── cxool_instructions.txt
                               ├── data
                               │   ├── inluum_grid.nc
                               │   └── run_cxool_example.py
                               ├── External
                               │   └── inluum.in
                               ├── Include
                               │      └── gulfofmexico.h
                               ├── README.html
                               └── README.md
</code></pre>

## How to run C-Xool to construct the forcing file

### Option 1: Command-Line Execution


**Go inside the folder `data`**. There, you can run C-Xool directly from the command line with:

```bash
cxool \
  --grid-name data/inluum_grid.nc \
  --initialdate 1983-10-25 \
  --finaldate 1983-10-31 \
  --interval 6 \
  --plot-interval 0 \
  --vars-to-interp t2m wind msl tcc avg_snswrf q tp \
  --final-interpolated-file roms_frc.nc \
  --data-storage ./raw_era5 \
  --data-subfolder merged_data \
  --ref-date "1970-01-01T00:00:00.000000000"
```
This command will:

- Download ERA5 data for the specified interval and variables.
- Interpolate the variables to the ROMS grid.
- Save the output in `roms_frc.nc`.

<br>
<br>
<br>
<br>

### Option 2: Python Script
**Go inside the folder `data`**. You can also execute the entire example with the Python script in the following way:

```bash
python data/run_cxool_example.py
```

This script performs the same actions as the command-line example.
This will produce a file called `roms_frc.nc`, this is the atmospheric forcing file built by C-Xool.

## ROMS Execution

Once the `roms_frc.nc` file is generated, 
You can use it as the atmospheric forcing file in your ROMS simulation. 
The provided ROMS input file `External/inluum.in` and header `Include/gulfofmexico.h` 
illustrate the configuration used for this toy example.
It is the responsibility of the user to set the ROMS required libraries properly and the 
path in each system. Further, the file `External/inluum.in` must be edited so all your paths 
to both the grid and the forcing file are set properly:
<ol start="3">
<li>Set line 1107: `GRDNAME == /set/your/path/here/data/inluum_grid.nc`.</li>
<li>Set line 1197: `FRCNAME == /set/your/path/here/data/roms_frc.nc`.</li>
</ol>


 **IMPORTANT NOTE**

It is the **sole responsibility of the user** to:

- **Download and install a working version of ROMS (2002-2025)**.
- **Configure ROMS according to their system and requirements**.

The authors of C-Xool do **not** distribute or maintain the ROMS source code; ROMS is a well-established, widely recognised ocean modelling system. 
Please refer to [myroms.org](https://www.myroms.org) for official ROMS documentation and downloads.

---

### Authors

- Carlos Argáez García, LIPC, IINGEN, UNAM ([cargaezg@iingen.unam.mx](mailto:cargaezg@iingen.unam.mx))
- Simon Klüpfel, Axelyf, Iceland ([simon.kluepfel@gmail.com](mailto:simon.kluepfel@gmail.com))
- María Eugenia Allende Arandia, LIPC, IINGEN, UNAM ([mallendea@iingen.unam.mx](mailto:mallendea@iingen.unam.mx))
- Christian Mario Appendini Albrechtsen, LIPC, IINGEN, UNAM ([cappendinia@iingen.unam.mx](mailto:cappendinia@iingen.unam.mx))

For questions, bugs, suggestions, or just greetings, contact:  
**cargaezg@iingen.unam.mx**
