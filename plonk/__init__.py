"""
Plonk
=====

**Plonk** is a Python package for analyzing and visualizing smoothed
particle hydrodynamics simulation data.

Features
--------

  - Read in Phantom HDF dump files.
  - Access particle and sink arrays as Numpy structured arrays.
  - Access simulation parameters and units.
  - Compute extra quantities on particles.
  - Visualize data using interpolation provided by Splash.

See https://plonk.readthedocs.io/ for documentation. The source code is
available at https://github.com/dmentipl/plonk.
"""

from . import analysis
from .core.dump import Dump
from .core.evolution import Evolution
from .core.simulation import Simulation
from . import visualization

__all__ = ['Dump', 'Evolution', 'Simulation', 'analysis', 'visualization']
