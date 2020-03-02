"""Global (total) quantities.

Calculate various global (total) quantities on the particles.
"""

from typing import Tuple, Union

import numpy as np
from numpy import ndarray

from . import particles
from ..snap.snap import Snap, SubSnap

SnapLike = Union[Snap, SubSnap]


def center_of_mass(snap: SnapLike, ignore_accreted: bool = True) -> ndarray:
    """Calculate the center of mass.

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


def mass(snap: SnapLike, ignore_accreted: bool = True) -> float:
    """Calculate the total mass.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    float
        The total mass.
    """
    if ignore_accreted:
        h: ndarray = snap['smooth']
        mass: ndarray = snap['mass'][h > 0]
    else:
        mass = snap['mass']

    return mass.sum()


def accreted_mass(snap: SnapLike) -> float:
    """Calculate the accreted mass.

    Parameters
    ----------
    snap
        The Snap object.

    Returns
    -------
    float
        The accreted mass.
    """
    h: ndarray = snap['smooth']
    mass: ndarray = snap['mass'][~(h > 0)]

    return mass.sum()


def momentum(snap: SnapLike, ignore_accreted: bool = True) -> ndarray:
    """Calculate the total momentum.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    ndarray
        The total linear momentum like (px, py, pz).
    """
    return particles.momentum(snap=snap, ignore_accreted=ignore_accreted).sum(axis=0)


def angular_momentum(
    snap: SnapLike,
    origin: Union[ndarray, Tuple[float, float, float]] = (0.0, 0.0, 0.0),
    ignore_accreted: bool = True,
) -> ndarray:
    """Calculate the total angular momentum.

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
        The total angular momentum like (lx, ly, lz).
    """
    return particles.angular_momentum(
        snap=snap, origin=origin, ignore_accreted=ignore_accreted
    ).sum(axis=0)


def specific_angular_momentum(
    snap: SnapLike,
    origin: Union[ndarray, Tuple[float, float, float]] = (0.0, 0.0, 0.0),
    ignore_accreted: bool = True,
) -> ndarray:
    """Calculate the total specific angular momentum.

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
        The total specific angular momentum on the particles like
        (hx, hy, hz).
    """
    return particles.specific_angular_momentum(
        snap=snap, origin=origin, ignore_accreted=ignore_accreted
    ).sum(axis=0)


def kinetic_energy(snap: SnapLike, ignore_accreted: bool = True) -> float:
    """Calculate the total kinetic energy.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    float
        The total kinetic energy.
    """
    return particles.kinetic_energy(snap=snap, ignore_accreted=ignore_accreted).sum(
        axis=0
    )


def specific_kinetic_energy(snap: SnapLike, ignore_accreted: bool = True) -> float:
    """Calculate the total specific kinetic energy.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    float
        The total specific kinetic energy.
    """
    return particles.specific_kinetic_energy(
        snap=snap, ignore_accreted=ignore_accreted
    ).sum(axis=0)


def inclination(snap: SnapLike, ignore_accreted: bool = True) -> float:
    """Calculate the inclination with respect to the xy-plane.

    The inclination is calculated by taking the angle between the
    angular momentum vector and the z-axis, with the angular momentum
    calculated with respect to the center of mass.

    Parameters
    ----------
    snap
        The Snap object.
    ignore_accreted : optional
        Ignore accreted particles. Default is True.

    Returns
    -------
    float
        The mean inclination.
    """
    angmom = angular_momentum(snap=snap, ignore_accreted=ignore_accreted)
    return np.arccos(angmom[2] / np.linalg.norm(angmom))
