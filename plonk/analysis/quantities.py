"""Analysis quantities.

Calculate various quantities on the particles.
"""

from typing import Tuple, Union

import numpy as np
from numpy import ndarray

from ..snap.snap import Snap, SubSnap

SnapLike = Union[Snap, SubSnap]


def center_of_mass(snap: SnapLike, ignore_accreted: bool = True) -> ndarray:
    """Calculate the center of mass on a snapshot.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The center of mass as a vector (cx, cy, cz).
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        mass: ndarray = snap['mass'][h > 0]
        pos: ndarray = snap['position'][h > 0]
    else:
        mass = snap['mass']
        pos = snap['position']

    return (mass[:, np.newaxis] * pos).sum(axis=0)


def momentum(snap: SnapLike, ignore_accreted: bool = True) -> ndarray:
    """Calculate the momentum.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The linear momentum on the particles.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        mass: ndarray = snap['mass'][h > 0]
        vel: ndarray = snap['velocity'][h > 0]
    else:
        mass = snap['mass']
        vel = snap['velocity']

    return mass[:, np.newaxis] * vel


def angular_momentum(
    snap: SnapLike,
    origin: Union[ndarray, Tuple[float, float, float]] = (0.0, 0.0, 0.0),
    ignore_accreted: bool = True,
) -> ndarray:
    """Calculate the angular momentum.

    Parameters
    ----------
    snap
        The Snap object.
    origin : optional
        The origin around which to compute the angular momentum as a
        ndarray or tuple (x, y, z). Default is (0, 0, 0).
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The angular momentum on the particles.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        mass: ndarray = snap['mass'][h > 0]
        pos: ndarray = snap['position'][h > 0]
        vel: ndarray = snap['velocity'][h > 0]
    else:
        mass = snap['mass']
        pos = snap['position']
        vel = snap['velocity']

    origin = np.array(origin)
    pos = pos - origin

    return mass[:, np.newaxis] * np.cross(pos, vel)


def specific_angular_momentum(
    snap: SnapLike,
    origin: Union[ndarray, Tuple[float, float, float]] = (0.0, 0.0, 0.0),
    ignore_accreted: bool = True,
) -> ndarray:
    """Calculate the specific angular momentum.

    Parameters
    ----------
    snap
        The Snap object.
    origin : optional
        The origin around which to compute the angular momentum as a
        ndarray or tuple (x, y, z). Default is (0, 0, 0).
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The angular momentum on the particles.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        pos: ndarray = snap['position'][h > 0]
        vel: ndarray = snap['velocity'][h > 0]
    else:
        pos = snap['position']
        vel = snap['velocity']

    origin = np.array(origin)
    pos = pos - origin

    return np.cross(pos, vel)


def kinetic_energy(snap: SnapLike, ignore_accreted: bool = True) -> ndarray:
    """Calculate the kinetic energy.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The kinetic energy on the particles.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        mass: ndarray = snap['mass'][h > 0]
        vel: ndarray = snap['velocity'][h > 0]
    else:
        mass = snap['mass']
        vel = snap['velocity']

    return 1 / 2 * mass * np.linalg.norm(vel, axis=1) ** 2


def specific_kinetic_energy(snap: SnapLike, ignore_accreted: bool = True) -> ndarray:
    """Calculate the specific kinetic energy.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The specific kinetic energy on the particles.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        vel: ndarray = snap['velocity'][h > 0]
    else:
        vel = snap['velocity']

    return 1 / 2 * np.linalg.norm(vel, axis=1) ** 2


def semi_major_axis(
    snap: SnapLike,
    gravitational_parameter: float,
    origin: Union[ndarray, Tuple[float, float, float]] = (0.0, 0.0, 0.0),
    ignore_accreted: bool = True,
) -> ndarray:
    """Calculate the semi-major axis.

    The semi-major axis of particles around a mass specified by
    gravitational parameter with an optional to specify the position of
    the mass.

    Parameters
    ----------
    snap
        The Snap object.
    gravitational_parameter
        The gravitational parameter (G*M).
    origin : optional
        The origin around which to compute the angular momentum as a
        ndarray or tuple (x, y, z). Default is (0, 0, 0).
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The semi-major axis on the particles.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        pos: ndarray = snap['position'][h > 0]
        vel: ndarray = snap['velocity'][h > 0]
    else:
        pos = snap['position']
        vel = snap['velocity']

    origin = np.array(origin)
    pos = pos - origin

    mu = gravitational_parameter

    radius = np.linalg.norm(pos, axis=1)

    specific_angular_momentum = np.cross(pos, vel)
    specific_angular_momentum_magnitude = np.linalg.norm(
        specific_angular_momentum, axis=1
    )

    specific_kinetic_energy = 1 / 2 * np.linalg.norm(vel, axis=1) ** 2
    specific_potential_energy = -mu / radius
    specific_energy = specific_kinetic_energy + specific_potential_energy

    eccentricity = np.sqrt(
        1 + 2 * specific_energy * (specific_angular_momentum_magnitude / mu) ** 2
    )

    return specific_angular_momentum_magnitude ** 2 / (mu * (1 - eccentricity ** 2))


def eccentricity(
    snap: SnapLike,
    gravitational_parameter: float,
    origin: Union[ndarray, Tuple[float, float, float]] = (0.0, 0.0, 0.0),
    ignore_accreted: bool = True,
) -> ndarray:
    """Calculate the eccentricity.

    The eccentricity of particles around a mass specified by
    gravitational parameter with an optional to specify the position of
    the mass.

    Parameters
    ----------
    snap
        The Snap object.
    gravitational_parameter
        The gravitational parameter (G*M).
    origin : optional
        The origin around which to compute the angular momentum as a
        ndarray or tuple (x, y, z). Default is (0, 0, 0).
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The eccentricity on the particles.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        pos: ndarray = snap['position'][h > 0]
        vel: ndarray = snap['velocity'][h > 0]
    else:
        pos = snap['position']
        vel = snap['velocity']

    origin = np.array(origin)
    pos = pos - origin

    mu = gravitational_parameter

    radius = np.linalg.norm(pos, axis=1)

    specific_angular_momentum = np.cross(pos, vel)
    specific_angular_momentum_magnitude = np.linalg.norm(
        specific_angular_momentum, axis=1
    )

    specific_kinetic_energy = 1 / 2 * np.linalg.norm(vel, axis=1) ** 2
    specific_potential_energy = -mu / radius
    specific_energy = specific_kinetic_energy + specific_potential_energy

    return np.sqrt(
        1 + 2 * specific_energy * (specific_angular_momentum_magnitude / mu) ** 2
    )


def Roche_sphere(m1: float, m2: float, separation: float):
    """Calculate an estimate of the Roche sphere.

    Uses the formula from Eggleton (1983) ApJ 268, 368-369.

    Parameters
    ----------
    m1
        The mass of the body around which to calculate the Roche sphere.
    m2
        The mass of the second body.

    """
    q = m1 / m2
    return (
        separation
        * 0.49
        * q ** (2 / 3)
        / (0.6 * q ** (2 / 3) + np.log(1.0 + q ** (1 / 3)))
    )
