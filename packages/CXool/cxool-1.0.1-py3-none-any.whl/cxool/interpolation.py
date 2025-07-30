#!/usr/bin/env python3
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

import numpy as np
import xarray as xr

from .specifications import ROMSSpecScalar, ROMSSpecVector


def interpolate_to_grid(
    fgrd, ncf_filename, ref_date, variable_list, ts_paths, memory_chunks
):
    """
    Interpolate ERA5 variables onto the target ROMS grid and save to NetCDF.

    Args:
        fgrd (dict): Dictionary containing ROMS grid coordinates and masks.
        ncf_filename (str): Output path for the resulting NetCDF forcing file.
        ref_date (str): Reference date used to compute the days number in the NetCDF file.
        variable_list (dict): Dictionary mapping variable names to their ERA5 specifications.
        ts_paths (dict): Dictionary mapping variable names to their corresponding ERA5 NetCDF files.
        memory_chunks (int): Chunk sizes to use when loading datasets with xarray.

    Returns:
        None: The function writes output directly to the specified NetCDF file.
    """

    tsvs = [s.name for v in variable_list.values() for s in v.era5spec]

    # make this an exception here...
    assert all(v in ts_paths for v in tsvs)

    with xr.open_mfdataset(
        [ts_paths[v] for v in tsvs],
        chunks=({"time": memory_chunks} if memory_chunks is not None else None),
    ) as ds:

        # interpolate
        gds = ds.interp(
            latitude=fgrd.lat_rho,
            longitude=fgrd.lon_rho,
            kwargs={"fill_value": -9999.0},
        )

        # Quality CONTROL:
        cont = 0
        for v in tsvs:
            cont += np.isnan(gds[v].values).any()
        if cont > 0:
            raise ValueError(
                "Nans have been found after the interpolation. Execution stopped."
            )

    # gather information
    dats = []
    staffelberg = {
        "latitude": "lat",
        "longitude": "lon",
    }

    for v in variable_list.values():
        if isinstance(v, ROMSSpecScalar):
            ename = v.era5spec[0].name
            dats.append(
                (ename, v.roms_name, v.roms_long_name, v.roms_unit, v.scale, v.shift)
            )
            staffelberg[ename] = v.roms_name
        else:
            for i in range(2):
                ename = v.era5spec[i].name
                dats.append(
                    (
                        ename,
                        v.roms_comp_names[i],
                        v.roms_comp_long_names[i],
                        v.roms_unit,
                        v.scale,
                        v.shift,
                    )
                )
                staffelberg[ename] = v.roms_comp_names[i]

    # rotate vectors

    cosrot = np.cos(fgrd.angle, dtype="float32")
    sinrot = np.sin(fgrd.angle, dtype="float32")

    for v in variable_list.values():
        if isinstance(v, ROMSSpecVector):
            u, v = [x.name for x in v.era5spec]

            ru = cosrot * gds[u] + sinrot * gds[v]
            rv = -sinrot * gds[u] + cosrot * gds[v]

            gds[u] = ru.transpose("time", "eta_rho", "xi_rho")
            gds[v] = rv.transpose("time", "eta_rho", "xi_rho")

    # scale and set attributes
    for d in dats:
        name, _, clname, cunit, scale, shift = d
        gds[name] *= scale
        gds[name] += shift
        gds[name].attrs.update(
            {
                "long_name": clname,
                "units": cunit,
                "time": "time",
                "standard_name": name,
                "coordinates": "time lon lat",
            }
        )
    gds.attrs = {
        "history": "Created by C-Xool, V1",
        "institution": "Unidad Académica Sisal, Universidad Nacional Autónoma de México (UNAM)",
        "source": "ERA5 weather files",
        "conventions": "CF-1.0",
    }
    # rename
    gds = gds.rename(staffelberg)
    # cleanup
    keep_var = list(staffelberg.values()) + ["time", "lat", "lon"]
    dump_var = [v for v in list(gds.variables) if v not in keep_var]
    gds = gds.drop_vars(dump_var)

    # save the final file
    print("Start writing the forcing file...")

    for name in gds.data_vars:
        if gds[name].dtype.kind in ["f", "i"]:
            gds[name] = gds[name].where(np.isfinite(gds[name]), 1.0e35)
            gds[name].attrs["_FillValue"] = 1.0e35

    dateref = np.datetime64(ref_date)
    ref_date_cleaned = (
        ref_date.split("T")[0] + " " + ref_date.split("T")[1].split(".")[0]
    )
    gds["time"] = (
        (gds["time"].values - dateref).astype("timedelta64[ns]").astype("int64")
        / (24 * 3600 * 1e9)
    ).astype("float64")
    gds["time"].attrs.update(
        {
            "long_name": "time",
            "units": f"days since {ref_date_cleaned}",
            "field": "time, scalar, series",
            "calendar": "gregorian",
        }
    )

    gds.to_netcdf(ncf_filename)
    print("The forcing file '" + ncf_filename + "' has been created.")


#    return


if __name__ == "__main__":
    pass
