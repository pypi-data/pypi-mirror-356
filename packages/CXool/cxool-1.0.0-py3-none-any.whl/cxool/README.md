<div align="right">
This file was written at LIPC, IINGEN, UNAM, <br>
in Sisal, Yucatan, Mexico, <br>
on the 12th of June 2025.
</div>

<h1 align="center" style="margin-bottom: 0.2em;">C-Xool:</h1>
<h1 align="center" style="margin-top: 0em; margin-bottom: 0em;">
  ERA5 Atmospheric Boundary Conditions Toolbox for Ocean Modelling with ROMS</h1>
<h1 align="center" style="margin-top: 0.5em;">Software Documentation</h1>

**This software is called C-Xool and is distributed under the GNU GENERAL PUBLIC LICENSE.**<br>
This file is provided as-is, without any warranty.

---

# Table of Contents

1. [Introduction](#introduction)
2. [Developers](#developers)
3. [Installing C-Xool](#installing-c-xool)
    - [Installation using Mamba and pip (recommended)](#installation-using-mamba-and-pip-recommended)
    - [Required Python libraries](#required-python-libraries)
4. [Architecture](#architecture)
5. [Execution](#execution)
   - [Basic execution](#basic-execution)
   - [Execution of the provided examples](#execution-of-the-provided-examples)
   - [Execution of the provided tests](#execution-of-the-provided-tests)
   - [Required arguments to run C-Xool](#required-arguments-to-run-c-xool)
   - [Optional arguments to run with C-Xool](#optional-arguments-to-run-with-c-xool)
   - [Example of execution](#example-of-execution)
   - [Help and further capabilities](#help-and-further-capabilities)
6. [Support](#support)
7. [Known problems](#known-problems)
8. [Platforms](#platforms)
   - [Note for Linux Users](#note-for-linux-users)
   - [Note for macOS Users](#note-for-macos-users)
   - [Note for Windows Users](#note-for-windows-users)
9. [Ready-to-use examples](#ready-to-use-examples)
10. [ROMS versions tested with an atmospheric forcing built with C-Xool](#roms-versions-tested-with-an-atmospheric-forcing-built-with-c-xool)
11. [Independent notes for the users to consider](#independent-notes-for-the-users-to-consider)
12. [Bibliography](#bibliography)
13. [Supplementary information](#supplementary-information)
---

## Introduction

C-Xool is a Python toolbox designed to prepare atmospheric forcing files for ocean models such as ROMS (Regional Ocean Modelling System). It facilitates downloading, interpolating, plotting, and writing atmospheric data (ERA5) in ROMS-compatible formats.

The toolbox designed and developed at the Coastal Engineering and Processes Laboratory (LIPC, from its Spanish acronym *Laboratorio de Ingeniería y Procesos Costeros*), at the Engineering Institute of the National Autonomous University of Mexico (UNAM, *Universidad Nacional Autónoma de México*), in an office that overlooks the Gulf of Mexico and its beautiful landscape.

C-Xool is open-source and encourages collaboration. If you use C-Xool or improve it, please cite the associated publication [1] and share your improvements.

This README.md file accompanies the code, for more explanations, please refer to [1].

If you have questions, comments, or feedback, contact [**cargaezg@iingen.unam.mx**](mailto\:cargaezg@iingen.unam.mx).

---
<br>
<br>
## Developers

- Carlos Argáez García, LIPC, IINGEN, UNAM ([cargaezg@iingen.unam.mx](mailto\:cargaezg@iingen.unam.mx))
- Simon Klüpfel, Axelyf, Iceland ([simon.kluepfel@gmail.com](mailto\:simon.kluepfel@gmail.com))
- María Eugenia Allende Arandia, LIPC, IINGEN, UNAM ([mallendea@iingen.unam.mx](mailto\:mallendea@iingen.unam.mx))
- Christian Mario Appendini Albrechtsen, LIPC, IINGEN, UNAM ([cappendinia@iingen.unam.mx](mailto\:cappendinia@iingen.unam.mx))

---

## Installing C-Xool

### Installation using Mamba and pip (recommended)

```bash
mamba create -n cxool python
mamba activate cxool
pip install cxool
```
Once installed, you're ready to run C-Xool.

### Required Python libraries

C-Xool relies on the following libraries:

- cartopy
- cdsapi
- cmocean
- copernicusmarine
- dask
- matplotlib
- netcdf4
- numpy
- xarray
- argparse

---

## Architecture

C-Xool is structured into the following modules:

- `cxool_cli.py`: Entry point; handles CLI parsing and orchestration.
- `cds_handler.py`: Handles data retrieval from the Climate Data Store (CDS).
- `interpolation.py`: Performs interpolation of atmospheric variables onto the model grid.
- `plotting.py`: Contains visualisation functions for assessing the final interpolated forcing file.
- `specifications.py`: Defines standard variable names, units, and categories.

---

## Execution

### Basic execution

Once installed, C-Xool is executed from a terminal. <br>
An example of an execution line is the following:

```bash
cxool --grid_name your_grid.nc --initialdate YYYY-MM-DD --finaldate YYYY-MM-DD 
--vars_to_interp var1 var2 var3 --plot_interval int_val 
--final_interpolated_file "ERA5_interpolated_to_grid.nc" 
--output_folder "SoftwareXExample" -o "input"
```

<div style="page-break-after: always; visibility: hidden"> 
<br>
</div>


### Execution of the provided examples

Go into the examples folder. There you have three options:

- GermanNorthernSea: Contains a dummy grid for the Northern Sea between Denmark and Germany. Go to the folder and execute the Python script. This will complete the example run.
- MexicanCaribbean: Contains a dummy grid for the Caribbean Sea off the eastern coast of the Yucatan Peninsula. Go to the folder and execute the Python script. Run the script; it executes the full example.
- ROMS_example: Contains three folders: `data`, `External`, and `Include`. Inside `data`, there is a grid for the northern coast of the Yucatan Peninsula, the Gulf of Mexico, along with a Python script. Go to the folder and execute the Python script. The script runs automatically. Then, set up a ROMS execution using the files included in the folders `External`, and `Include`. This is a toy model in ROMS runs without boundary, climatology, runoff, or tidal forcing files.

### Execution of the provided tests
We have provided a set of unit tests to assess:

- The CDSAPI credentials.
- The execution of the download commands and path settings.
- The execution of the merging different downloaded data batches into one file to be read by interpolation.
- The argument parser reading.
- The interpolation of dummy ERA5 variable `msl` and dummy grid data variables `lat_rho` and `lon_rho`, to a netCDF file.
- The plotting of dummy scalar and vectorial variables.
- The execution of real downloading data, real interpolating onto a provided grid and compared to a reference provided forcing file.

To execute go inside the folder `tests`. Then execute:

```bash
pytest . -v
```


### Required arguments to run C-Xool

- `--grid-name`:  Command expecting a string value as input. Name of the ROMS grid NetCDF file.

- `--initialdate`: Command expecting a numerical value as input. Initial date from which data download and interpolation will begin. Format: `YYYY-MM-DD`. Time is automatically set to **00:00:00** *hrs*.

- `--finaldate`: Command expecting a numerical value as input. Final date for data download and interpolation. Format: `YYYY-MM-DD`. Time is automatically set to **23:00:00** *hrs*.

### Optional arguments to run with C-Xool
- `--ref-date`: Command expecting a string value as input. Reference date for the time variable in the output NetCDF file. Format should follow ISO 8601, e.g., **`1948-01-01T00:00:00.000000000`**. Default value is **`1948-01-01T00:00:00.000000000`**.<br>

- `--interval`: Command expecting a numerical value as input. Time step interval to download data. Time interval in hours for downloading data. Starts from **00:00:00** *hrs* on the initial date.<br>

- `--vars-to-interp`: Command expecting a string value as input. Variables to download and interpolate. Default: `msl`, `wind`, `t2m`, `tcc`. All variables are downloaded using the ERA5 naming convention. There are two types of variables: **scalar variables**, which correspond to most ERA5 variables, and **vector variables**, which specifically refer to wind. The wind has two components, `u` and `v`, and when downloading them with C-Xool, they are referred to as *`wind`*. This means that when using the variable `wind`, C-Xool downloads both wind components, `u` and `v`, at **10 m** above ground. They are treated as a pair from the beginning of execution to the generation of the interpolated forcing file.<br>

- `--plot`: Command expecting strings values as input. Specifies the variables to plot from the final forcing file.<br>

- `--plot-interval`: Command expecting a numerical value as input. Time interval for plotting data in time steps of the netCDF forcing file generated by C-Xool. <br>
Accepts negative values `-t` to plot only the `t`-th slice of the netCDF forcing file.<br> 
It also accepts `0` to plot only the first slice. <br>
A positive value `t`, to plot every `t`-th slice of the interpolated NetCDF, starting from the first slice.<br>

- `--projection`: Command expecting a string value as input. Map projection used to plot the interpolated data. It can be either `stereographic` or `mercator`.<br>

- `--scale-factor`: Command expecting a numerical value as input. Scale factor for `quiver` plots, controlling arrow size. A higher value produces smaller arrows. <br>

- `--arrowdensity`: Command expecting a numerical value as input. Controls arrow density in `quiver` plots. A smaller value produces a denser vector field.<br>

- `--discrete-colors`: Command expecting a numerical value as input. Number of discrete colours used in the plots. <br>

- `--homogenise-limits`: Command expecting a boolean value as input. When enabled, uses consistent colourbar limits across variables, improving visual comparison.<br>

- `--data-storage`: Command expecting a string value as input. Path to the folder where raw ERA5 data will be stored. <br>

- `--data-subfolder`: Command expecting a string value as input. Subdirectory for saving merged raw data.<br>

- `--plots-folder`: Folder for output plots. When `--output-folder` is defined, the folder containing the plots will be created inside it.<br>

- `--output-folder`: Command expecting a string value as input. Folder where the output files will be saved.<br>

- `--memory-chunks`: Command expecting a numerical value as input. Defines the size of the memory chunk (in MB) for processing. Useful for large files.<br>

- `--out-config`: Command expecting a string value as input. Generates a configuration input file that can be reused later.<br>

- `--input-file`: Command expecting a string value as input. Input file containing the configuration instructions to run C-Xool. It can be created manually or using the option: `--out-config name-of-input-file`. <br>

- `--plot-format`: Command expecting a string value as input. Format for saved plots (e.g., `png`, `pdf`, `eps`, `svg`). <br>

- `--version`: C-Xool version.<br>

- `--help`: C-Xool help. Full list of options.



### Example of execution
A basic command line execution example is the following:

```bash
python cxool_cli.py --grid-name model_grid.nc \
  --initialdate 1983-10-25 --finaldate 1983-10-27 \
  --vars-to-interp wind t2m msl tcc \
  --plot msl wind t2m tcc --plot-interval 3 \
  --final-interpolated-file ERA5_interpolated-to-grid.nc \
  --output-folder SoftwareXExample -o input
```

### Help and further capabilities

To see the full list of options, run:

```bash
cxool --help
```

---

## Support

If you encounter issues, please email [**cargaezg@iingen.unam.mx**](mailto\:cargaezg@iingen.unam.mx). We support Spanish, English, Italian, and Yucatec Maya.

---

## Known problems
- You must set up your [ECMWF account](https://www.ecmwf.int/).
- You must set up [CDSAPI](https://cds.climate.copernicus.eu/how-to-api)
- You must install the proper Python environment.
- You must install C-Xool.
- You must install the [aforementioned libraries](#required-python-libraries).
- Grid file, initial date, and final date are mandatory arguments. No default values were provided.

---


## Ready-to-use examples
Inside the installation folder of C-Xool, there is a folder called ```examples``` that contains two subfolders: ```GermanNorthernSea``` and ```MexicanCaribbean```. 
Inside each of these subfolders, a model grid is provided along with a Python script that allows running. <br>


<pre><code>
                                examples/
                                ├── GermanNorthernSea
                                │   ├── example_German_Northern_sea.py
                                │   └── nordseedeu10km_grid.nc
                                ├── MexicanCaribbean
                                │   ├── caribemex10km_grid.nc
                                │   └── example_Mexican_caribbean.py
                                └── ROMS_example
                                    ├── cxool_instructions.txt
                                    ├── data
                                    │   ├── inluum_grid.nc
                                    │   └── run_cxool_example.py
                                    ├── External
                                    │   └── inluum.in
                                    ├── Include
                                    │   └── gulfofmexico.h
                                    ├── README.html
                                    └── README.md    
</code></pre>

---



## Platforms

### Note for Linux Users
C-Xool has been tested on:
<ol start="1">
<li>Fedora Linux 35 Workstation, 64-bit.</li>
<li>Rocky Linux 8.6, 64-bit.</li>
<li>Fedora Linux 41 Workstation, 64-bit.</li>
</ol>

### Note for macOS Users

C-Xool has been tested on macOS. Please report any compatibility issues to the developer.


### Note for Windows Users

C-Xool can be used under Windows via a properly configured Python environment.
It has been tested on:
<ol start="1">
<li>Microsoft Windows 11, Pro, 64 bits.</li>
</ol>
---



## ROMS versions tested with an atmospheric forcing built with C-Xool

We have tested the forcing file compatibility with different ROMS versions. 
The oldest version successfully used was the 2011 release (makefile 1417 2011-05-13 16:51:50Z kate),
which is indeed quite dated. We also verified functionality with the latest ROMS version available on 
GitHub at the time of writing. All worked.

In accordance with the ROMS documentation [2] and recent ROMS-Tools guidelines [3], 
we know the NetCDF structure for atmospheric forcing variables is:

```bash
ATMOS_VAR(time, eta_rho, xi_rho)
```

Given the consistency across ROMS documentation, 
and based on our own testing, we do not anticipate any compatibility issues. 
The expected format for atmospheric forcing variables is well established as:

```bash
ATMOS_VAR(time, eta_rho, xi_rho)
```

and has remained stable across ROMS versions [2,3].


---

## Independent notes for the users to consider
Producing a bathymetric grid for a ROMS model is a hard task that usually requires both good knowledge in coding and ocean-sciences.
This is out of the scope of C-Xool. However, user may want to consider:
<ol start="1">
<li>James, C., *Gridbuilder*, [Austides Consulting](https://austides.com/downloads/), accessed: 10 June 2025.</li>
<li>Ådlandsvik, B., *GridMap – Python toolbox for ROMS grid files based on explicit map projections*, 
		https://github.com/bjornaa/gridmap.</li>
</ol>

---

## Bibliography
[1] *C-Xool, ERA5 Atmospheric Boundary Conditions Toolbox for Ocean Modelling with ROMS*, Argáez, C., Klüpfel, S., Allende Arandía, M. E., Appendini, C. M. Submitted to *SoftwareX*, under review.

[2] ROMS Forcing Package Documentation. Available at: https://www.myroms.org/index.php?page=forcing

[3] ROMS-Tools Documentation – Surface Forcing. Available at: https://roms-tools.readthedocs.io/en/latest/surface_forcing.html


---

## Supplementary information


Modern package managers such as mamba and pip, 
generally ensure a clean installation of the needed dependencies.
However, we provide here the specific versions and distribution channels 
of the key Python libraries we used during our testing and development. 

We do so in the hope that this information serves other users with two purposes:

- Reproducibility: It offers the configurations that were verified to work with C-Xool 
in both Linux and macOS environments. This information can be useful if any user wishes to replicate 
our setup exactly or need to troubleshoot an unexpected behaviour.

- Demonstrated Compatibility: The examples show that C-Xool runs reliably across different platforms, 
Python versions, and package sources (e.g. conda-forge vs pypi). 
This underlines the flexibility and robustness of the tool in varied user environments.

Nevertheless, we recommend installing the latest compatible versions 
in a clean environment.

<div style="page-break-before: always;"></div>

The libraries and settings we used for two different systems, are described as follows:

### Fedora Linux 35 Workstation, 64-bit

In this case, Python version was 3.13.5 and the libraries distributions were as follows:


| Package           | Version    | Channel     |
|-------------------|------------|-------------|
| cartopy           | 0.22.0     | conda-forge |
| cmocean           | 3.1.3      | conda-forge |
| copernicusmarine  | 2.0.1      | conda-forge |
| dask              | 2024.1.0   | conda-forge |
| dask-core         | 2024.1.0   | conda-forge |
| matplotlib        | 3.8.2      | conda-forge |
| matplotlib-base   | 3.8.2      | conda-forge |
| matplotlib-inline | 0.1.7      | conda-forge |
| netcdf4           | 1.6.5      | conda-forge |
| numpy             | 1.26.4     | conda-forge |
| cf_xarray         | 0.10.5     | conda-forge |
| xarray            | 2024.1.1   | conda-forge |





### macOS Big Sur, Version 11.7.10

In this case, Python version was 3.12.2 and the libraries distributions were as follows:

| Package           | Version    | Channel |
|-------------------|------------|---------|
| cartopy           | 0.24.1     | pypi    |
| cmocean           | 4.0.3      | pypi    |
| copernicusmarine  | 2.0.1      | pypi    |
| dask              | 2025.5.1   | pypi    |
| dask-core         | –          | –       |
| matplotlib        | 3.10.3     | pypi    |
| matplotlib-base   | –          | –       |
| matplotlib-inline | –          | –       |
| netcdf4           | 1.7.2      | pypi    |
| numpy             | 2.3.0      | pypi    |
| cf_xarray         | –          | –       |
| xarray            | 2025.6.1   | pypi    |



