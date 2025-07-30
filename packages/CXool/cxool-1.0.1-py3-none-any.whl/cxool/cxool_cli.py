# -*- coding: utf-8 -*-
"""
C-Xool: ERA5 Atmospheric Boundary Conditions Toolbox for Ocean Modelling with ROMS.
This is a program to prepare the grid domain with the atmospheric forcing,
to perform ocean simulations using the ROMS model.

 -> This is a free software; you can redistribute it and/or
 -> modify it under the terms of the GNU General Public License
 -> as published by the Free Software Foundation; either version 3
 -> of the License, or (at your option) any later version.
 This program is distributed in the hope that it will be useful,
 -> but WITHOUT ANY WARRANTY; without even the implied warranty of
 -> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 -> GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 -> along with this program.  If not, see <http://www.gnu.org/licenses/>.
 Author and main maintainer: Carlos Argáez
 -> Bibliography attached to the corresponding publication.
 Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Arandía, Christian Mario Appendini
     To report bugs, questions, feedback or just greetings, please use:
         cargaezg@iingen.unam.mx
"""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import xarray as xr
from cartopy import crs as ccrs

from . import __version__
from .cds_handler import CDSHandler, _known_pressure_levels
from .interpolation import interpolate_to_grid
from .plotting import plot_variables
from .specifications import ERA5SpecPL
from .specifications import Rutgers as vardict


class CXoolArgumentParser:
    """
    Custom argument parser for the C-Xool command-line interface.

    This class defines and processes command-line arguments used to configure and execute
    the C-Xool to  prepare ERA5 atmospheric forcing for ROMS ocean model input.

    Attributes:
        args (argparse.Namespace): Parsed command-line arguments.
    """

    def __init__(self, debug_args=None):
        """
        Initialise the CXoolArgumentParser.

        Args:
            debug_args (list, optional): List of command-line arguments for debugging purposes.
                If None, it will have an error for a missing grid.
        """
        if debug_args is None:
            debug_args = []
        self.debug_args = debug_args

        parser0 = argparse.ArgumentParser(
            prog="C-Xool",
            description="Oceanographic exploration - \
                            prepare the grid domain with the atmospheric forcing, \
                            to perform ocean simulations using the ROMS model.",
            epilog="To report bugs, questions, feedback or just greetings, \
                            please use: cargaezg@iingen.unam.mx. \
                            C-Xool was designed and developed at \
                            the Coastal Engineering and Processes Laboratory \
                            (LIPC, from its Spanish acronym \
                            Laboratorio de Ingeniería y Procesos Costeros),\
                            at the Engineering Institute of the \
                            National Autonomous University of Mexico \
                            (UNAM, Universidad Nacional Autónoma de México).",
            fromfile_prefix_chars="@",
            add_help=False,
        )

        argv0 = sys.argv[1:] + debug_args

        parser0.add_argument("-f", "--config-file")

        cfa, argv1 = parser0.parse_known_args(argv0)
        if cfa.config_file is not None:
            argv = ["@" + cfa.config_file] + argv1
        else:
            argv = argv1

        del parser0

        parser = argparse.ArgumentParser(
            prog="C-Xool",
            description="Oceanographic exploration – \
                    prepares the grid domain with atmospheric forcing \
                    to use in ROMS ocean modelling.",
            epilog="To report bugs, questions, feedback or just greetings, \
                            please use: cargaezg@iingen.unam.mx. \
                            C-Xool was designed and developed at \
                            the Coastal Engineering and Processes Laboratory \
                            (LIPC, from its Spanish acronym \
                            Laboratorio de Ingeniería y Procesos Costeros),\
                            at the Engineering Institute of the \
                            National Autonomous University of Mexico \
                            (UNAM, Universidad Nacional Autónoma de México).",
            fromfile_prefix_chars="@",
        )

        parser.add_argument(
            "-f",
            "--input-file",
            dest="config_file",
            help="Input file containing the configuration instructions to run C-Xool. \
                    It can be created manually or using the <-o config_file> option.",
            metavar="<config_file>",
        )

        ##### THESE LINES ARE FOR GRID PARAMETERS
        parser.add_argument(
            "-a",
            "--grid-name",
            required=True,
            type=str,
            help="Name of the ROMS grid NetCDF file.",
        )

        parser.add_argument(
            "-b",
            "--initialdate",
            required=True,
            type=str,
            help="Initial date from which data download and interpolation will begin.\
                    Format: YYYY-MM-DD. Time is automatically set to 00:00:00.",
        )

        parser.add_argument(
            "-c",
            "--finaldate",
            required=True,
            type=str,
            help="Final date for data download and interpolation. \
                    Format: YYYY-MM-DD. Time is automatically set to 23:00:00.",
        )

        parser.add_argument(
            "-e",
            "--final-interpolated-file",
            default="ERA5_interpolated_to_grid.nc",
            type=str,
            help="Name of the output NetCDF file containing the interpolated onto the ROMS grid, \
                    the atmospheric forcing data. Use quotation marks.",
            metavar="<name_of_your_final_file.nc>",
        )

        parser.add_argument(
            "-rd",
            "--ref-date",
            default="1948-01-01T00:00:00.000000000",
            type=str,
            help="Reference date for the time variable in the output NetCDF file. \
                    Format should be ISO 8601, e.g., '1948-01-01T00:00:00.000000000'.\
                    Default value is 1948-01-01T00:00:00.000000000.",
            metavar="<YYYY-MM-DDTHH:MM:SS.sssssssss>",
        )

        ##### THESE LINES ARE FOR PLOTTING
        parser.add_argument(
            "-g",
            "--plot",
            dest="vars_to_plot",
            nargs="*",
            default=[],
            choices=list(vardict),
            type=str,
            help="Specifies the variables to plot from the final forcing file.",
            metavar="<var1 var2 ...>",
        )  # Use the world wind for variable winds

        parser.add_argument(
            "-gg",
            "--vars-to-interp",
            nargs="+",
            default=["msl", "wind", "t2m", "tcc"],
            type=str,
            help="Variables to download and interpolate. Default: msl, wind, t2m, tcc.",
            metavar="<var1 var2 ...>",
        )  # Use the world wind for variable winds

        parser.add_argument(
            "-g2",
            "--projection",
            default="mercator",
            choices=["stereographic", "mercator"],
            type=str,
            help="Map projection used when plotting the interpolated data.",
        )

        parser.add_argument(
            "-i",
            "--interval",
            default=6,
            type=int,
            help="Time interval in hours for downloading data. \
                    Starts from 00:00 on the initial date.",
            metavar="<Hours>",
        )

        parser.add_argument(
            "-i2",
            "--plot-interval",
            default=10,
            type=int,
            help="Command expecting a numerical value as input.\
                    Time interval for plotting data in time steps of \
                    the netCDF forcing file generated by C-Xool.\
    A negative value -t will plot the t-th slice of the interpolated NetCDF.\
    A value of 0 will plot only the first slice of the interpolated NetCDF.\
    A positive value t, to plot every t-th slice of the interpolated NetCDF,\
    starting from the first slice.",
            metavar="<Hours>",
        )

        parser.add_argument(
            "-j",
            "--scale-factor",
            default=200,
            type=float,
            help="Scale factor for quiver plots, controlling arrow size. \
                    A higher value means smaller arrows.",
            metavar="<Value>",
        )

        parser.add_argument(
            "-k",
            "--arrowdensity",
            default=1,
            type=int,
            help="Controls arrow density in quiver plots. Higher values produce fewer arrows.",
            metavar="<Value>",
        )

        parser.add_argument(
            "-l",
            "--discrete-colors",
            default=10,
            type=int,
            help="Number of discrete colours used in plots. \
                    Higher values highlight atmospheric fronts; \
                    lower values create smoother gradients.",
            metavar="<Value>",
        )

        parser.add_argument(
            "-m",
            "--homogenise-limits",
            action=argparse.BooleanOptionalAction,
            default=True,
            help="When enabled, uses consistent colourbar limits across variables, \
                    improving visual comparison.",
        )

        ##### THESE LINES ARE FOR OUTPUT OPTIONS
        parser.add_argument(
            "-o",
            "--out-config",
            default=None,
            type=str,
            help="Generates a configuration input file to be reused later.",
            metavar="<config_file>",
        )

        parser.add_argument(
            "-n",
            "--output-folder",
            default=".",
            type=str,
            help="Folder where the output files will be saved.",
            metavar="output_directory",
        )

        parser.add_argument(
            "-p",
            "--data-storage",
            default=None,
            type=str,
            help="Path to the directory where raw ERA5 data will be stored.",
            metavar="/path/to/data/storage",
        )

        parser.add_argument(
            "-q",
            "--plots-folder",
            default="plots",
            type=str,
            help="Subdirectory where the plots will be saved.",
            metavar="plot_directory_name",
        )

        parser.add_argument(
            "-r",
            "--data-subfolder",
            default="merged_data",
            type=str,
            help="Subdirectory for saving merged raw data.",
            metavar="merged_directory_name",
        )

        parser.add_argument(
            "--plot-format",
            default="png",
            choices=["png", "pdf", "eps", "svg"],
            type=str,
            help="Format for saved plots.",
        )

        parser.add_argument(
            "-s",
            "--memory-chunks",
            default=None,
            type=int,
            help="Defines the memory chunk size (in MB) for processing. \
                    Useful for large files.",
            metavar="<Value>",
        )

        parser.add_argument(
            "-V", "--version", action="version", version=f"C-Xool version {__version__}"
        )

        self.parser = parser
        self.args = self.parser.parse_args(
            argv,
        )
        self.argv = argv

        if self.args.out_config is not None and cfa.config_file == self.args.out_config:
            raise FileExistsError("Input config file would be overwritten. Aborting.")

        if not set(self.args.vars_to_plot).issubset(set(self.args.vars_to_interp)):
            raise ValueError(
                "Your lists for both interpolating and plotting do not match."
            )
        if self.args.out_config is not None:
            dels = []
            for iv, v in enumerate(argv0):
                if v in ("-o", "--out-config"):
                    dels.extend([iv, iv + 1])
                dels = sorted(set(dels), reverse=True)
                for d in dels:
                    del argv0[d]
            outfile = Path(self.args.output_folder) / self.args.out_config
            os.makedirs(self.args.output_folder, exist_ok=True)
            with open(outfile, "wt", encoding="utf-8") as of:
                of.writelines("\n".join(argv0))


def padl(x):
    """
    Pad the input value(s) to the nearest lower quarter (0.25) and subtract 0.5.

    This is used to adjust geospatial boundaries for plotting or interpolation
    by extending the range slightly beyond the minimum.

    Args:
        x (float or array-like): Input number(s) to be padded.

    Returns:
        float or array-like: Adjusted value(s).
    """

    return np.floor(x * 4.0) / 4.0 - 0.5


def padr(x):
    """
    Pad the input value(s) to the nearest upper quarter (0.25) and add 0.5.

    This is used to adjust geospatial boundaries for plotting or interpolation
    by extending the range slightly beyond the maximum.

    Args:
        x (float or array-like): Input number(s) to be padded.

    Returns:
        float or array-like: Adjusted value(s).
    """

    return np.ceil(x * 4.0) / 4.0 + 0.5


class CXool:
    """
    Initialise the C-Xool main class to prepare ERA5 atmospheric forcing for ROMS.
    """

    def __init__(
        self,
        grid,
        ini_date,
        fin_date,
        interval,
        ref_date,
        variable_list,
        data_storage,
        output_folder,
        plots_folder,
        data_subfolder,
        plot_format,
        memory_chunks,
        out_config,
    ):
        """
        Initialise the C-Xool main class to prepare ERA5 atmospheric forcing for ROMS.

        Args:
            grid (str): Path to the ROMS grid NetCDF file.
            ini_date (str): Initial date in 'YYYY-MM-DD' format for data retrieval.
            fin_date (str): Final date in 'YYYY-MM-DD' format for data retrieval.
            interval (int): Temporal resolution in hours (e.g. 6 for 6-hourly data).
            ref_date (str): Reference date used to compute the days number in the NetCDF file.
            variable_list (str, list): Specifies ERA5 variables to retrieve and interpolate.
            data_storage (str): Path where raw ERA5 data will be saved.
            output_folder (str): Path where the final interpolated file will be saved.
            plots_folder (str): Path to save optional diagnostic plots.
            data_subfolder (str): Subfolder structure within `data_storage` for organisation.
            plot_format (str): File format for plots (e.g. "png", "eps, "pdf", "svg").
            memory_chunks (int): Chunk sizes for xarray/dask processing.
            out_config (str): Path to the output configuration or log file.
        """

        self.data_storage = data_storage
        self.output_folder = output_folder
        self.plots_folder = plots_folder
        self.data_subfolder = data_subfolder
        self.plot_format = plot_format
        self.out_config = out_config
        self.interval = interval
        self.ref_date = ref_date
        self.grid = grid.copy()
        lat = self.grid.lat_rho.values
        lon = self.grid.lon_rho.values
        self.ini_date = ini_date
        self.fin_date = fin_date

        self.variable_list = variable_list

        self.lim_lat = (lat.min(), lat.max())
        self.lim_lon = (lon.min(), lon.max())

        self.lim_lat_pad = (padl(self.lim_lat[0]), padr(self.lim_lat[1]))
        self.lim_lon_pad = (padl(self.lim_lon[0]), padr(self.lim_lon[1]))

        self.lim_nwse = (lat.max(), lon.min(), lat.min(), lon.max())
        padfuns = (padr, padl, padl, padr)
        self.lim_nwse_pad = tuple(
            (pf(x).item() for pf, x in zip(padfuns, self.lim_nwse))
        )

        self._ts_paths = None
        self.memory_chunks = memory_chunks

    def prepare_timeseries(self, force_splice=False):
        """
        Prepare ERA5 timeseries data for each variable in the list.

        This method checks whether interpolated data already exists. If not, or if
        forced by the user, it downloads and processes the necessary ERA5 data.

        Args:
            force_splice (bool, optional): If True, regenerate interpolated timeseries.
        """

        if not force_splice and self._ts_paths is not None:
            return
        self._ts_paths = {}

        cdsh = CDSHandler(self.data_storage)

        vlist = sum((v.era5spec for v in self.variable_list.values()), start=[])

        for variable in vlist:
            varlab = variable.name
            print(f"Processing raw data for variable: {varlab}")
            fname = (
                f"{self.output_folder}/{self.data_subfolder}/{varlab}_"
                + str(self.ini_date)
                + "_"
                + str(self.fin_date)
                + ".nc"
            )

            self._ts_paths[varlab] = fname

            if isinstance(variable, ERA5SpecPL):
                pressure_level = variable.pressure_level
            else:
                pressure_level = None

            tsds = cdsh.get_timeseries(
                variable.long_name,
                self.ini_date,
                self.fin_date,
                self.lim_nwse_pad,
                self.interval,
                pressure_level,
            )
            os.makedirs(os.path.dirname(fname), exist_ok=True)

            if tsds[varlab].isnull().sum().compute().item() > 0:
                raise ValueError(
                    "Nans have been found in ERA5 data. Execution stopped."
                )

            tsds.to_netcdf(fname)  # Export netcdf file and save it.
            tsds.close()

    def interpolate(self, filename):
        """
        Interpolate ERA5 timeseries data onto the ROMS grid.

        This method performs horizontal interpolation of all specified ERA5 variables
        onto the model grid and stores the result in a NetCDF file.

        Args:
            filename (str): Path to the output NetCDF file where interpolated data will be saved.
        """

        interpolate_to_grid(
            self.grid,
            filename,
            self.ref_date,
            self.variable_list,
            self._ts_paths,
            self.memory_chunks,
        )

    def plotit(
        self,
        file_to_plot,
        gridfile,
        varlist,
        projection="mercator",
        interval=10,
        scale_factor=500,
        arrowdensity=15,
        discrete_colors=10,
        homogenise_limits=False,
        output_folder=".",
        plots_folder=None,
        plot_format="png",
    ):
        """
        Generate plots of the interpolated ERA5 variables on the ROMS grid.

        This method produces time-series plots for each variable using the specified projection.
        It supports scalar and vector fields (e.g. wind), with options for colour discretisation,
        arrow scaling, and temporal interval.

        Args:
            file_to_plot (str): Path to the NetCDF file containing interpolated variables.
            gridfile (str): Path to the ROMS grid file.
            varlist (list): List of variable names to plot.
            projection (str, optional): Map projection to use ("mercator" by default).
            interval (int, optional): Time step interval to skip between plots.
            scale_factor (int, optional): Scaling factor for vector arrows.
            arrowdensity (int, optional): Density of arrows for vector fields.
            discrete_colors (int, optional): Number of discrete colour levels for scalar fields.
            homogenise_limits (bool, optional): Whether to apply uniform colourbar across plots.
            output_folder (str, optional): Base directory for output files.
            plots_folder (str, optional): Subfolder for storing generated plots.
            plot_format (str, optional): Format of the saved plot images (e.g., "png", "pdf").
        """

        loaded_file_to_plot = xr.open_dataset(file_to_plot)

        with xr.open_dataset(gridfile) as new:
            angle = new.angle
            cen_lat = float(((new.lat_rho.max() + new.lat_rho.min()) / 2))
            cen_lon = float(((new.lon_rho.max() + new.lon_rho.min()) / 2))

        wgs84 = ccrs.CRS("WGS84", globe=None)

        if projection == "stereographic":
            projection = ccrs.Stereographic(
                central_latitude=cen_lat,
                central_longitude=cen_lon,
                false_easting=0.0,
                false_northing=0.0,
                true_scale_latitude=None,
                globe=None,
            )

        elif projection == "mercator":
            projection = ccrs.Mercator(
                central_longitude=cen_lon,
                false_easting=0.0,
                false_northing=0.0,
                latitude_true_scale=None,
                globe=None,
            )
        else:
            raise TypeError(f'unknown projection: "{projection}"')

        x = loaded_file_to_plot["lon"]
        y = loaded_file_to_plot["lat"]
        xx = projection.transform_points(
            wgs84, np.array(x).flatten(), np.array(y).flatten()
        )

        projected_grid = xx.reshape(x.shape + (3,))

        plot_variables(
            varlist,
            loaded_file_to_plot,
            discrete_colors,
            homogenise_limits,
            interval,
            projected_grid,
            projection,
            angle,
            scale_factor,
            arrowdensity,
            output_folder,
            plots_folder,
            plot_format,
        )


dbgargs = []


def main():
    """
    Main entry point for the C-Xool command-line interface.

    Parses command-line arguments using CXoolArgumentParser and initiates the processing
    pipeline. If an error occurs during parsing, it prints the error and exits with status 1.
    """
    # pylint: disable=broad-exception-caught
    # We want to keep here a broad exception because this will deal with the input parameters.
    try:
        cxa = CXoolArgumentParser(dbgargs)
    except Exception as e:
        print("Error: ", str(e))
        sys.exit(1)
    instructions = cxa.args

    ps = {
        a.split("/")[0]: (int(a.split("/")[1]) if "/" in a else None)
        for a in instructions.vars_to_interp
    }

    for v in ps.keys():
        if v not in vardict:
            raise KeyError(f"Wrong variable name: The {v} is not a valid variable.")

    for p in ps.values():
        if p is not None and p not in _known_pressure_levels:
            raise ValueError(
                f"Wrong level pressure value: the level {p} is not a valid value."
            )

    vd = {a: vardict[a] for a in ps}
    for v, p in ps.items():
        if p is not None:
            vd[v].era5spec[0].pressure_level = p

    grid = xr.open_dataset(instructions.grid_name)

    if any(w not in grid.dims for w in ["eta_rho", "xi_rho"]):
        raise ValueError(
            "The provided grid does not contain required variables 'xi_rho' and 'eta_rho' \
                    as standard grid for ROMS."
        )

    cx = CXool(
        grid,
        instructions.initialdate,
        instructions.finaldate,
        instructions.interval,
        instructions.ref_date,
        vd,
        instructions.data_storage,
        instructions.output_folder,
        instructions.plots_folder,
        instructions.data_subfolder,
        instructions.plot_format,
        instructions.memory_chunks,
        instructions.out_config,
    )

    cx.prepare_timeseries()
    ncf_filename = os.path.join(cx.output_folder, instructions.final_interpolated_file)

    cx.interpolate(ncf_filename)

    if len(instructions.vars_to_plot):

        varlist = [vd[v] for v in instructions.vars_to_plot]
        cx.plotit(
            ncf_filename,
            instructions.grid_name,
            varlist,
            instructions.projection,
            instructions.plot_interval,
            instructions.scale_factor,
            instructions.arrowdensity,
            instructions.discrete_colors,
            instructions.homogenise_limits,
            instructions.output_folder,
            instructions.plots_folder,
            instructions.plot_format,
        )

    print("Task accomplished, bye.")


if __name__ == "__main__":
    pass
