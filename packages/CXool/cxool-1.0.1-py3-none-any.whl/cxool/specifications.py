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
from dataclasses import dataclass


@dataclass
class ERA5SpecSL:
    """
    Specification for a single-level ERA5 variable.
    Class for keeping track of the variable specs and scalings.

    Attributes:
        name (str): Short variable name as used in ERA5.
        long_name (str): Descriptive name for the variable.
        unit (str): Physical units of the variable.
    """

    name: str
    long_name: str
    unit: str


@dataclass
class ERA5SpecPL(ERA5SpecSL):
    """
    Specification for a pressure-level ERA5 variable.

    Inherits:
        ERA5SpecSL

    Additional Attributes:
        pressure_level (int): Pressure level in hPa associated with the variable.
    """

    pressure_level: int


@dataclass
class ROMSSpecScalar:
    """
    Specification for a scalar variable in ROMS using a single ERA5 source.

    Attributes:
        era5spec (list): List containing one ERA5SpecSL object.
        roms_name (str): Variable name used in ROMS NetCDF output.
        roms_long_name (str): Descriptive long name for ROMS output.
        roms_unit (str): Units in the ROMS file.
        plot_unit (str): Units to be used for plotting.
        scale (float): Scaling factor to apply to data. Default is 1.0.
        shift (float): Offset to apply to data. Default is 0.0.
        plottype (str): Optional entry, how the variable should be plotted following the CMOCEAN
        convention.
    """

    era5spec: list
    #
    roms_name: str
    roms_long_name: str
    roms_unit: str
    plot_unit: str
    # transform
    scale: float = 1.0
    shift: float = 0.0
    plottype: str = None

    def __post_init__(self):
        assert isinstance(self.era5spec, ERA5SpecSL)
        self.era5spec = [self.era5spec]


@dataclass
class ROMSSpecVector:
    """
    Specification for a vector variable in ROMS using two ERA5 components.

    This class is used to define how a vector quantity (e.g., wind or current)
    is constructed from two ERA5 variables (typically u and v components), and
    how it should appear in ROMS forcing and output files.

    Attributes:
        era5spec (list): A list of two ERA5SpecSL instances representing the u and v components.
        roms_name (str): Combined name for the vector variable in ROMS.
        roms_long_name (str): Descriptive long name for the vector variable.
        roms_unit (str): Unit of the variable in ROMS NetCDF files.
        roms_comp_names (list): Names for the individual u and v components in ROMS.
        roms_comp_long_names (list): Descriptive names for the u and v components.
        plot_unit (str): Unit used when plotting the variable.
        scale (float, optional): Multiplicative factor applied to both components. Default is 1.0.
        shift (float, optional): Additive offset applied to both components. Default is 0.0.
        plottype (str, optional): Optional entry, how the variable should be plotted following
        the CMOCEAN convention."
    """

    era5spec: list
    #
    roms_name: str
    roms_long_name: str
    roms_unit: str
    # transform
    roms_comp_names: list
    roms_comp_long_names: list
    plot_unit: str
    scale: float = 1.0
    shift: float = 0.0
    plottype: str = None

    @property
    def name(self):
        """
        Prevents access to a single name property for vector specifications.

        Raises:
            NotImplementedError: Always raised to indicate that vector variables
            do not have a unified 'name' property.
        """
        raise NotImplementedError(
            "Vector variables do not support a single 'name' attribute."
        )

    def __post_init__(self):
        """
        Validates the ERA5 specification list after dataclass initialisation.

        Ensures:
            - The `era5spec` list contains exactly two components (e.g., u and v).

        Raises:
            AssertionError: If `era5spec` does not contain exactly two elements.
        """
        assert len(self.era5spec) == 2


Rutgers = {
    "msl": ROMSSpecScalar(
        ERA5SpecSL("msl", "mean_sea_level_pressure", "Pa"),
        "Pair",
        "Mean sea level pressure",
        "hPa",
        "hPa",
        scale=1.0e-2,
        plottype="diff",
    ),
    "t2m": ROMSSpecScalar(
        ERA5SpecSL("t2m", "2m_temperature", "K"),
        "Tair",
        "2 metre temperature",
        "C",
        "°C",
        shift=-273.15,
        plottype="thermal",
    ),
    "tcc": ROMSSpecScalar(
        ERA5SpecSL("tcc", "total_cloud_cover", "(0-1)"),
        "cloud",
        "Total cloud cover",
        "(0-1)",
        "(0-1)",
        plottype="balance",
    ),
    "avg_snswrf": ROMSSpecScalar(
        ERA5SpecSL(
            "avg_snswrf", "mean_surface_net_short_wave_radiation_flux", "W m$^{-2}$"
        ),
        "swrad",
        "Mean surface net short-wave radiation flux",
        "W m-2",
        "W m$^{-2}$",
        plottype="solar",
    ),
    "avg_sdlwrf": ROMSSpecScalar(
        ERA5SpecSL(
            "avg_sdlwrf", "mean_surface_downward_long_wave_radiation_flux", "W m$^{-2}$"
        ),
        "lwrad_down",
        "Mean surface downward long-wave radiation flux",
        "W m-2",
        "W m$^{-2}$",
        plottype="solar",
    ),
    "avg_snlwrf": ROMSSpecScalar(
        ERA5SpecSL(
            "avg_snlwrf", "mean_surface_net_long_wave_radiation_flux", "W m$^{-2}$"
        ),
        "lwrad",
        "Mean surface net long-wave radiation flux",
        "W m-2",
        "W m$^{-2}$",
        plottype="solar",
    ),
    "avg_slhtf": ROMSSpecScalar(
        ERA5SpecSL("avg_slhtf", "mean_surface_latent_heat_flux", "W m$^{-2}$"),
        "latent",
        "Mean surface latent heat flux",
        "W m-2",
        "W m$^{-2}$",
        plottype="solar",
    ),
    "avg_ishf": ROMSSpecScalar(
        ERA5SpecSL("avg_ishf", "mean_surface_sensible_heat_flux", "W m$^{-2}$"),
        "sensible",
        "Mean surface sensible heat flux",
        "W m-2",
        "W m$^{-2}$",
        plottype="solar",
    ),
    "tp": ROMSSpecScalar(
        ERA5SpecSL("tp", "total_precipitation", "m"),
        "rain",
        "Total precipitation",
        "kg m-2 s-1",
        "kg m$^{-2}$ s$^{-1}$",
        scale=10.0 / 36.0,
        plottype="rain",
    ),
    "e": ROMSSpecScalar(
        ERA5SpecSL("e", "evaporation", "m of water equivalent"),
        "evap",
        "Evaporation",
        "kg m-3",
        "kg m$^{-3}$",
        scale=10.0 / 36.0,
        plottype="rain",
    ),
    "cc": ROMSSpecScalar(
        ERA5SpecPL("cc", "fraction_of_cloud_cover", "0-1", pressure_level=300),
        "fcloud",
        "cloud fraction",
        "0-1",
        "0-1",
        plottype="balance",
    ),
    "q": ROMSSpecScalar(
        ERA5SpecPL("q", "specific_humidity", "kg kg$^{-1}$", pressure_level=1000),
        "Qair",
        "surface specific humidity",
        "kg kg-1",
        "kg kg$^{-1}$",
        scale=10.0 / 36.0,
        plottype="rain",
    ),
    "wind": ROMSSpecVector(
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
    ),
}
