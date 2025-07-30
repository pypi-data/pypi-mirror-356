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
import os

import cmocean
import cmocean.plots
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import xarray as xr
from cartopy import feature as cfeature
from cartopy.mpl.gridliner import LatitudeFormatter, LongitudeFormatter

from .specifications import ROMSSpecScalar, ROMSSpecVector


class ScalarFormat(matplotlib.ticker.ScalarFormatter):
    """
    Scalar formatter for Matplotlib axes and colourbars with custom string format.

    Args:
        fformat (str): Format string, e.g., "%1.1f".
        offset (bool): Whether to use offset in tick labels.
        mathText (bool): Whether to use math text formatting.
    """

    def __init__(self, fformat="%1.1f", offset=True, mathText=True):
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(
            self, useOffset=offset, useMathText=mathText
        )


def get_cmap_limits(data):
    """
    Calculate the colour map limits based on data range, protected of NaNs.

    Args:
        data (ndarray): Input data array.

    Returns:
        tuple: Lower and upper bounds rounded to nearest integers.
    """
    limits = np.floor(np.nanmin(data)), np.ceil(np.nanmax(data))
    if limits[0] == limits[1]:
        if limits[0] == 0.0:
            limits = (limits[0], limits[0] + 1e-1)
        else:
            limits = (limits[0], limits[0] + abs(limits[0]))
    return limits


def get_ticks(limits, n_ticks):
    """
    Generate N rounded tick values within the given limits.

    Args:
        limits (tuple): Tuple (min, max) defining the range.
        N (int): Number of tick marks.

    Returns:
        ndarray: Array of rounded tick values.
    """
    if np.round(limits[0]) == np.round(limits[1]):
        if np.round(limits[0]) == 0.0:
            return np.round(
                np.linspace(np.round(limits[0]), np.round(limits[0]) + 1e-1, n_ticks), 4
            )
        return np.round(
            np.linspace(
                np.round(limits[0]),
                np.round(limits[0]) + abs(np.round(limits[0])),
                n_ticks,
            ),
            4,
        )
    return np.round(np.linspace(*limits, n_ticks), 2)


def get_data_source(spec, file):
    """
    Retrieve variable data from file according to the variable specification.

    Args:
        spec: ROMSSpecScalar or ROMSSpecVector object defining the variable.
        file (xarray.Dataset): Dataset containing model output.

    Returns:
        xarray.DataArray or tuple: Variable data array(s).

    Raises:
        TypeError: If spec type is unsupported.
    """
    if isinstance(spec, ROMSSpecScalar):
        return file[spec.roms_name]
    if isinstance(spec, ROMSSpecVector):
        return tuple((file[spec.roms_comp_names[0]], file[spec.roms_comp_names[1]]))
    raise TypeError(
        "Unsupported specification type: expected ROMSSpecScalar or ROMSSpecVector."
    )


def plot_variables(
    var_list_to_plot,
    loaded_file_to_plot,
    discrete_colors,
    homogenise_lims,
    interval,
    projected_coords,
    projection,
    var_angle,
    scale_factor,
    arrowdensity,
    output_folder,
    plots_folder,
    plot_format,
):
    """
    Generate plots for a list of scalar or vector variables from a loaded dataset.

    Args:
        var_list_to_plot (list): List of variable specifications.
        loaded_file_to_plot (xarray.Dataset): Dataset with model output.
        discrete_colors (int): Number of discrete colour levels.
        homogenise_lims (bool): Whether to use shared colour limits for all plots.
        interval (int): Time interval for selecting frames to plot.
        projected_coords (tuple): Tuple of projected coordinates (x, y).
        projection (str): Map projection type.
        var_angle (ndarray): Rotation angle of vector fields.
        scale_factor (float): Scale for quiver arrows.
        arrowdensity (int): Arrow spacing for vector fields.
        output_folder (str): Base directory for saving outputs.
        plots_folder (str): Subdirectory for plot outputs.
        plot_format (str): File format for output plots (e.g., "png", "eps", "pdf", "svg").
    """

    if not isinstance(var_list_to_plot, (list, tuple)):
        raise TypeError("Variables have to be specified as list.")

    dates_to_plot = loaded_file_to_plot["time"]

    for spec in var_list_to_plot:

        print(f"Plotting: {spec.roms_name}")

        geo_var = spec.roms_name

        containingfolder = os.path.join(output_folder, plots_folder, geo_var)

        os.makedirs(containingfolder, exist_ok=True)

        vars_to_plot = get_data_source(spec, loaded_file_to_plot)

        plot_single_variable(
            spec,
            vars_to_plot,
            dates_to_plot,
            homogenise_lims,
            interval,
            projected_coords,
            discrete_colors,
            var_angle,
            scale_factor,
            arrowdensity,
            containingfolder,
            projection,
            plot_format,
        )


def data_to_plot(fun_geo_var, fun_time_input, fun_interval=None):
    """
    Extract and prepare scalar and vector data for plotting at given time intervals.

    Args:
        fun_geo_var (xarray.DataArray or tuple): Scalar field or a tuple of two xarray.DataArray
        objects representing vector components.
        fun_time_input (xarray.DataArray): Time coordinate associated with the input data.
        fun_interval (int, optional):
            - If None, return all time steps.
            - If > 0, take every `fun_interval`-th frame.
            - If < 0, return only the frame at index `-fun_interval`.

    Returns:
        tuple:
            - time_data (xarray.DataArray): Time steps selected.
            - scalar_data (xarray.DataArray): Scalar field for plotting (either input scalar or
            magnitude of vector).
            - vector_data (tuple or None): Original vector components if input was vector,
            else None.
    """

    if fun_interval is None:
        slc = slice(None)
    elif fun_interval > 0:
        slc = slice(None, None, fun_interval)
    else:
        slc = slice(-fun_interval, -fun_interval + 1)

    time_data = fun_time_input[slc]

    if isinstance(fun_geo_var, tuple):
        vector_data = tuple(arr.isel(time=slc) for arr in fun_geo_var)

        scalar_data = np.sqrt(sum(arr**2 for arr in vector_data))
        scalar_data = scalar_data.transpose("time", "eta_rho", "xi_rho")
    else:
        scalar_data = fun_geo_var.isel(time=slc)

        vector_data = None

    return time_data, scalar_data, vector_data


def plot_single_variable(
    spec,
    var_to_plot_01,
    dates_to_plot,
    homogenise_limits,
    interval,
    projected_coord,
    discrete_colors,
    var_angle,
    scale_factor,
    arrowdensity,
    containingfolder,
    projection,
    plot_format,
):
    """
    Generate and save a sequence of plots for a single variable across time.

    Args:
        spec (dict): Variable specification, defining plotting attributes (e.g., name, label,
        type).
        var_to_plot_01 (xarray.DataArray or tuple): Data array for scalar or tuple of (u, v)
        components for vector data.
        dates_to_plot (xarray.DataArray): Time coordinates corresponding to data slices
        to be plotted.
        homogenise_limits (bool): Whether to apply common colour limits across all time steps.
        interval (int): Time step interval for plotting.
        projected_coord (tuple): Tuple of projected coordinates (x, y) matching the variable data.
        discrete_colors (int): Number of discrete colour levels in the colormap.
        var_angle (xarray.DataArray): Angle for rotating vector data if necessary.
        scale_factor (float): Scale for quiver arrows (used in vector plots).
        arrowdensity (int): Controls spacing of arrows in vector plots.
        containingfolder (str): Path to folder containing the NetCDF file or input data.
        projection (str): Projection type used in the plot (e.g., 'mercator').
        plot_format (str): File format for saved plots (e.g., 'png', 'pdf').

    Returns:
        Plots that are saved to disk.
    """

    time_data, scalar_data, vector_data = data_to_plot(
        var_to_plot_01, dates_to_plot, interval
    )

    if homogenise_limits:
        scalar_limits = get_cmap_limits(scalar_data)
    else:
        scalar_limits = None

    if not discrete_colors:
        levelsgeovar = 256
    elif isinstance(discrete_colors, int) and discrete_colors > 1:
        levelsgeovar = discrete_colors + 1
    else:
        raise TypeError(
            f"discrete values must be a positive integer larger than one or one of \
                    (0, False, None), got {discrete_colors}"
        )

    if not discrete_colors:
        n_ticks = 10
    else:
        n_ticks = levelsgeovar

    if vector_data is not None:
        cosrot = np.cos(var_angle)
        sinrot = np.sin(var_angle)
        uv = xr.concat(
            [
                cosrot * vector_data[0] - sinrot * vector_data[1],
                sinrot * vector_data[0] + cosrot * vector_data[1],
            ],
            dim="uv",
        )
        uv = uv.transpose("uv", "time", "eta_rho", "xi_rho")

    if scalar_limits is not None:
        level_boundaries_geo_var0 = np.linspace(*scalar_limits, levelsgeovar)
        tick_values0 = get_ticks(scalar_limits, n_ticks)
    for t, _date in enumerate(np.array(time_data)):
        geo_var = spec.roms_name

        file_name = (
            str(geo_var)
            + "_date_"
            + str(_date)[0:19]
            .replace("-", "_")
            .replace("T", "_at_hr_")
            .replace(":", "_")
            + "."
            + plot_format
        )

        if os.path.exists(containingfolder + "/" + file_name):
            print(str(file_name) + " already exits")
            continue

        fi = plt.figure(figsize=(24, 18), dpi=100)
        ax = plt.axes(projection=projection)
        ax.add_feature(cfeature.LAND.with_scale("50m"), linewidth=0.5)
        ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=5, edgecolor="k")

        cmap = getattr(cmocean.cm, spec.plottype)

        if scalar_limits is not None:
            level_boundaries_geo_var = level_boundaries_geo_var0
            tick_values = tick_values0
        else:
            limits = get_cmap_limits(scalar_data[t])

            level_boundaries_geo_var = np.linspace(*limits, levelsgeovar)
            tick_values = get_ticks(limits, n_ticks)

        s = ax.contourf(
            projected_coord[:, :, 0],
            projected_coord[:, :, 1],
            scalar_data.isel(time=t),
            level_boundaries_geo_var,
            cmap=cmap,
        )

        cb = plt.colorbar(
            s,
            ticks=tick_values,
            boundaries=level_boundaries_geo_var,
            values=(level_boundaries_geo_var[:-1] + level_boundaries_geo_var[1:]) / 2,
            aspect=20,
            ax=plt.gca(),
            alpha=0.75,
        )

        cb.ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.2f"))

        lname = spec.roms_long_name
        sname = spec.roms_name

        ax.set_title(
            lname
            + " ("
            + spec.plot_unit
            + ")\n"
            + str(_date)[0:19].replace("-", " ").replace("T", " at ")
            + " hr\n",
            fontsize=45,
        )
        cb.set_label(sname + " (" + spec.plot_unit + ")", size=36)

        if vector_data is not None:

            ax.quiver(
                projected_coord[::arrowdensity, ::arrowdensity, 0],
                projected_coord[::arrowdensity, ::arrowdensity, 1],
                uv[0, t, ::arrowdensity, ::arrowdensity],
                uv[1, t, ::arrowdensity, ::arrowdensity],
                color="k",
                scale=scale_factor,
                linewidths=1,
                width=0.0005,
                edgecolor="0",
                headwidth=7,
                headaxislength=7,
                headlength=15,
            )

        cb.ax.tick_params(labelsize=36, length=0)
        cb.set_alpha(0.2)
        cb.outline.set_visible(False)
        grids = ax.gridlines(
            draw_labels=True, linewidth=1.0, color="gray", alpha=0.5, linestyle="--"
        )

        grids.top_labels = False
        grids.bottom_labels = True
        grids.left_labels = True
        grids.right_labels = False
        grids.ylines = True
        grids.xlines = True

        grids.xformatter = LongitudeFormatter()
        grids.yformatter = LatitudeFormatter()
        grids.xlabel_style = {"size": 36, "color": "gray"}
        grids.ylabel_style = {"size": 36, "color": "gray"}

        outputpath = os.path.join(containingfolder, file_name)
        print("Writing file: " + str(outputpath))
        fi.savefig(outputpath, bbox_inches="tight")

        plt.clf()
        plt.close()
        ax.clear()
