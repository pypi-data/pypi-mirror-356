"""
Unit tests to check that the CDSHandler class in cxool.cds_handler module
correctly sets the storing paths.

This test verifies that three functions:
1.- Check that the user properly installed their CDS API credentials.
2.- Checks that the '_data' folder is generated for data storing.
3.- Checks that the target folder to store the merged data is
    properly parsed from the CLI and generated.

Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Arandía, Christian Mario Appendini
C-Xool: ERA5 Atmospheric Boundary Conditions Toolbox for Ocean Modelling with ROMS.
License: GNU GPL v3
"""

import os
import sys

import cdsapi
from cxool.cds_handler import CDSHandler
from cxool.cxool_cli import CXoolArgumentParser


def test_cds_credentials():
    """Verifies the credentials are correct."""
    cdsapi.Client()


def test_default_data_storage_path():
    """Verifies generation of folder _data."""
    cdsapi.Client()
    handler = CDSHandler()
    expected_path = os.path.abspath("./_data")
    assert handler.data_storage == expected_path


def test_default_data_merging_path(monkeypatch):
    """Verifies generation of merging folder."""
    cdsapi.Client()
    testing_args = [
        "-a",
        "grid.nc",
        "-b",
        "1983-10-25",
        "-c",
        "1983-10-27",
        "--data-subfolder",
        "merged_path",
    ]
    monkeypatch.setattr(sys, "argv", ["cxool"] + testing_args)
    parser = CXoolArgumentParser()
    args = parser.args
    assert args.data_subfolder == "merged_path"
