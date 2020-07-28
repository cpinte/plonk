--------
Analysis
--------

.. automodule:: plonk.analysis

~~~~~~~
Profile
~~~~~~~

The :py:class:`Profile` class provides methods for generating radial profiles
from the particle data.

.. autoclass:: plonk.Profile
.. autofunction:: plonk.load_profile

~~~~~~~~~~~~~~~~~~~
Particle quantities
~~~~~~~~~~~~~~~~~~~

.. automodule:: plonk.analysis.particles

~~~~~~~~~~~~~~~
Sink quantities
~~~~~~~~~~~~~~~

.. automodule:: plonk.analysis.sinks

~~~~~~~~~~~~~~~~~
Global quantities
~~~~~~~~~~~~~~~~~

.. automodule:: plonk.analysis.total

~~~~~~~~~~~~~
SPH summation
~~~~~~~~~~~~~

This section contains functions to perform SPH summation and derivatives.

.. autofunction:: plonk.utils.sph.derivative
.. autofunction:: plonk.utils.sph.summation