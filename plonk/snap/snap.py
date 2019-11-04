"""Snap class for snapshot files.

The Snap class contains all information related to a smoothed particle
hydrodynamics simulation snapshot file.
"""

from typing import Callable, Dict, Optional, Tuple, Union

from numpy import ndarray


class Snap:
    """Smoothed particle hydrodynamics Snap object.

    Snapshot files contain the state of the simulation at a point in
    time. Typical minimum data from a smoothed particle hydrodynamics
    simulation include the particle positions and smoothing length, from
    which the density field can be reconstructed, as well as the
    particle type. In addition, the particle velocities are required to
    restart the simulation.

    Other data stored in the snapshot file include equation of state,
    dust, and magnetic field information, as well as numerical
    quantities related to time-stepping.

    Examples
    --------
    To access arrays on the particles.
    >>> snap['position']
    >>> snap['density']

    To access sink arrays.
    >>> snap.sinks['position']
    >>> snap.sinks['spin']
    """

    _array_registry: Dict[str, Callable] = {}

    _array_name_mapper = {
        'xyz': 'position',
        'pos': 'position',
        'vxyz': 'velocity',
        'vel': 'velocity',
        'h': 'smooth',
        'rho': 'density',
        'Bxyz': 'magfield',
        'spinxyz': 'spin',
    }

    _array_split_mapper = {
        'x': ('position', 0),
        'y': ('position', 1),
        'z': ('position', 2),
        'vx': ('velocity', 0),
        'vy': ('velocity', 1),
        'vz': ('velocity', 2),
        'velx': ('velocity', 0),
        'vely': ('velocity', 1),
        'velz': ('velocity', 2),
        'Bx': ('magfield', 0),
        'By': ('magfield', 1),
        'Bz': ('magfield', 2),
        'sx': ('spin', 0),
        'sy': ('spin', 1),
        'sz': ('spin', 2),
    }

    @staticmethod
    def add_array(fn):
        """Add array to Snap."""
        Snap._array_registry[fn.__name__] = fn
        return fn

    def __init__(self):

        self.families = {}
        self.properties = {}
        self.sinks = Sinks()
        self._arrays = {}
        self._file_pointer = {}
        self._num_particles = 0

    def loaded_arrays(self):
        """Return a list of loaded arrays."""
        return tuple(sorted(self._arrays.keys()))

    def available_arrays(self):
        """Return a list of available arrays."""
        return tuple(sorted(self._array_registry.keys()))

    def _get_array(self, name: str, index: Optional[int] = None):
        """Get an array by name."""
        if name in self._arrays:
            if index is None:
                return self._arrays[name]
            return self._arrays[name][:, index]
        elif name in Snap._array_registry:
            self._arrays[name] = Snap._array_registry[name](self)
            return self._arrays[name]
        else:
            raise ValueError('Array not available')

    @property
    def num_particles(self):
        """Return number of particles."""
        if self._num_particles == 0:
            self._num_particles = self['smooth'].size
        return self._num_particles

    def __getitem__(self, name: Union[str, ndarray]) -> ndarray:
        """Return an array, or family, or subset."""
        if isinstance(name, str):
            if name in self.families:
                raise NotImplementedError('')
            elif name in self.available_arrays():
                return self._get_array(name)
            elif name in self._array_name_mapper.keys():
                return self._get_array(self._array_name_mapper[name])
            elif name in self._array_split_mapper.keys():
                return self._get_array(*self._array_split_mapper[name])
            else:
                raise ValueError('Cannot determine item to return')
        elif isinstance(name, ndarray):
            raise NotImplementedError('')

    def __delitem__(self, name):
        """Delete an array from memory."""
        del self._arrays[name]

    def __len__(self):
        """Length as number of particles."""
        return self.num_particles

    def __repr__(self):
        """Dunder repr method."""
        return self.__str__()

    def __str__(self):
        """Dunder str method."""
        return f'<plonk.Snap>'


class Sinks:
    """Sink particles in a Snap."""

    _array_name_mapper = {
        'xyz': 'position',
        'pos': 'position',
        'vxyz': 'velocity',
        'vel': 'velocity',
        'h': 'smooth',
        'spinxyz': 'spin',
    }

    _array_split_mapper = {
        'x': ('position', 0),
        'y': ('position', 1),
        'z': ('position', 2),
        'vx': ('velocity', 0),
        'vy': ('velocity', 1),
        'vz': ('velocity', 2),
        'velx': ('velocity', 0),
        'vely': ('velocity', 1),
        'velz': ('velocity', 2),
        'sx': ('spin', 0),
        'sy': ('spin', 1),
        'sz': ('spin', 2),
        'spinx': ('spin', 0),
        'spiny': ('spin', 1),
        'spinz': ('spin', 2),
    }

    def __init__(self):
        self._data = None

    def add_sinks(self, structured_array: ndarray) -> None:
        """Add sinks via structured array.

        Parameters
        ----------
        structured_array
            A structured ndarray with labels such as 'position',
            'velocity', and so on, representing quantities on the sink
            particles.
        """
        self._data = structured_array

    @property
    def columns(self) -> Tuple[str, ...]:
        """Available sink quantities."""
        return self._data.dtype.names

    def __getitem__(self, name: str) -> ndarray:
        """Return an array."""
        if name in self.columns:
            return self._data[name]
        elif name in self._array_name_mapper:
            return self._data[self._array_name_mapper[name]]
        elif name in self._array_split_mapper:
            array, index = self._array_split_mapper[name]
            return self._data[array][:, index]
        else:
            raise ValueError('Cannot determine quantity to return')

    def __len__(self):
        """Dunder len method."""
        return len(self._data)

    def __repr__(self):
        """Dunder repr method."""
        return self.__str__()

    def __str__(self):
        """Dunder str method."""
        return f'<plonk.snap.Sinks>'