"""Units."""

import copy

import pint

units = pint.UnitRegistry()
Quantity = units.Quantity

# Add units
units.define('solar_mass = 1.9891e30 kg')
units.define('solar_radius = 6.959500e8 m')
units.define('earth_mass = 5.979e24 kg')
units.define('earth_radius = 6.371315e6 m')
units.define('jupiter_mass = 1.89813e27 kg')

# Array names with corresponding units as a string
array_units_str = {
    'accretion_radius': 'length',
    'alpha_viscosity_numerical': 'dimensionless',
    'density': 'density',
    'differential_velocity': 'velocity',
    'dust_fraction': 'dimensionless',
    'dust_to_gas_ratio': 'dimensionless',
    'gravitational_potential': 'energy',
    'internal_energy': 'specific_energy',
    'last_injection_time': 'time',
    'magnetic_field': 'magnetic_field',
    'mass': 'mass',
    'mass_accreted': 'mass',
    'position': 'length',
    'pressure': 'pressure',
    'smoothing_length': 'length',
    'softening_radius': 'length',
    'sound_speed': 'velocity',
    'spin': 'angular_momentum',
    'stopping_time': 'time',
    'sub_type': 'dimensionless',
    'timestep': 'time',
    'type': 'dimensionless',
    'velocity': 'velocity',
    'velocity_divergence': 'frequency',
}

# Some default units
units_default = {
    'accretion_radius': 'm',
    'angular_momentum': 'kg * m ** 2 / s',
    'azimuthal_angle': 'rad',
    'density': 'kg / m ** 3',
    'differential_velocity': 'm / s',
    'gravitational_potential': 'J',
    'internal_energy': 'J / kg',
    'keplerian_frequency': 'Hz',
    'kinetic_energy': 'J',
    'last_injection_time': 's',
    'magnetic_field': 'T',
    'mass': 'kg',
    'mass_accreted': 'kg',
    'momentum': 'kg * m / s',
    'polar_angle': 'rad',
    'position': 'm',
    'pressure': 'Pa',
    'projection': 'm',
    'radius_cylindrical': 'm',
    'radius_spherical': 'm',
    'semi_major_axis': 'm',
    'smoothing_length': 'm',
    'softening_radius': 'm',
    'sound_speed': 'm / s',
    'specific_angular_momentum': 'm ** 2 / s',
    'spin': 'kg * m ** 2 / s',
    'stopping_time': 's',
    'temperature': 'K',
    'timestep': 's',
    'velocity': 'm / s',
    'velocity_divergence': 'Hz',
    'velocity_radial_cylindrical': 'm / s',
    'velocity_radial_spherical': 'm / s',
}


def units_dict():
    """Return a dictionary of arrays with unit strings.

    Like the following:

        `{'density': 'kg / m ** 3', ... 'position': 'm', ... }`

    This is useful for setting units for plots.
    """
    return copy.copy(units_default)


def generate_units_array_dictionary(units_dictionary):
    """Generate units array dictionary.

    Parameters
    ----------
    units_dictionary
        TODO: See generate_units_dictionary.

    Returns
    -------
    units
        A dictionary of units as Pint quantities.
    """
    _units = dict()
    for arr, unit in array_units_str.items():
        _units[arr] = units_dictionary[unit]
    return _units


def generate_units_dictionary(length, mass, time, temperature, magnetic_field):
    """Generate units dictionary.

    Parameters
    ----------
    length
        Length unit as a Pint quantity.
    mass
        Mass unit as a Pint quantity.
    time
        Time unit as a Pint quantity.
    temperature
        Temperature unit as a Pint quantity.
    magnetic_field
        Magnetic field unit as a Pint quantity.

    Returns
    -------
    units
        A dictionary of units as Pint quantities.
    """
    _units = dict()

    _units['dimensionless'] = length / length
    _units['length'] = length
    _units['time'] = time
    _units['mass'] = mass
    _units['magnetic_field'] = magnetic_field.to('tesla')
    _units['frequency'] = (1 / time).to('hertz')
    _units['velocity'] = length / time
    _units['momentum'] = mass * length / time
    _units['angular_momentum'] = mass * length ** 2 / time
    _units['specific_angular_momentum'] = length ** 2 / time
    _units['density'] = mass / length ** 3
    _units['acceleration'] = length / time ** 2
    _units['force'] = (mass * length / time ** 2).to('newton')
    _units['energy'] = (mass * length ** 2 / time ** 2).to('joule')
    _units['specific_energy'] = (length ** 2 / time ** 2).to('joule/kg')
    _units['pressure'] = (mass / time ** 2 / length).to('pascal')
    _units['temperature'] = 1.0 * temperature
    _units['entropy'] = (mass * length ** 2 / time ** 2).to('joule') / temperature

    return _units
