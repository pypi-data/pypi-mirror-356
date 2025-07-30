"""
Unit tests to check that the command-line argument parser (CXoolArgumentParser)
correctly interprets and stores input when given the minimum required arguments.

This test verifies that three things:
1.- Passing the grid name.
2.- Passing the initial date.
3.- Passing the final date.

Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Arandía, Christian Mario Appendini
C-Xool: ERA5 Atmospheric Boundary Conditions Toolbox for Ocean Modelling with ROMS.
License: GNU GPL v3
"""

import sys

from cxool.cxool_cli import CXoolArgumentParser


def test_parser_minimal_arguments(monkeypatch):
    """Verifies properly parsing."""
    testing_args = ["-a", "grid.nc", "-b", "1983-10-25", "-c", "1983-10-27"]
    monkeypatch.setattr(sys, "argv", ["cxool"] + testing_args)
    parser = CXoolArgumentParser()
    args = parser.args
    assert args.grid_name == "grid.nc"
    assert args.initialdate == "1983-10-25"
    assert args.finaldate == "1983-10-27"
