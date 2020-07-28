# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Types of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]

## [0.5.1] - 2020-07-11

### Added

- Analysis functions for sink particles.
- Function to animate particle plots.
- Different colours per particle type in particle plots.
- Tqdm progress bar for animation.

### Changed

- Use Matplotlib consistent argument names in particle_plot.

### Fixed

- Fix bug in standard deviation shading in Profile.

## [0.5.0] - 2020-04-20

### Added

- Neighbour finding via kd-tree.
- Compute SPH derivatives using kd-tree.
- IPython tab completion for Snap arrays and Profile profiles.
- Profile can have ndim==1 which gives a linear profile, useful for box calculations.
- Option to turn off caching of particle arrays, so that they are always read from file.
- Write derived arrays to HDF5 file, and read arrays from that file onto a Snap.
- Added logging of warning and other information messages.

### Changed

- Generalize sub-types: dust_type → sub_type: this allows for Phantom boundary particle sub-types.

### Removed

- Remove `Visualization` class in favour of just returning matplotlib's Axes and Figure objects.

## [0.4.1] - 2020-03-24

### Added

- Add scatter plots, i.e. particle plots with variable color and size markers.
- Add `extra_quantities` method to easily calculate extra quantities on the snapshot.
- Allow for setting array units, whether the array is rotatable, and whether it is a dust on derived arrays.
- Profiles are automatically generated from any 1d Snap quantity.
- Access individual dust quantities on profiles via '_001', etc.
- Read Phantom equation of state information to get pressure, sound speed, temperature.
- Add extra Snap quantities, e.g. Stokes number.
- Add extra profiles, e.g. Toomre Q.
- Allow accessing components of Snap quantities via '_x', etc.
- Calculate standard deviation on profiles.

### Changed

- Use verbose names for all snapshot quantities, e.g. 'dust_fraction' not 'dustfrac' and 'velocity_divergence' not 'divv'.

### Removed

- Remove `Evolution` object in favour of pandas DataFrame.

## [0.4.0] - 2020-03-15

### Added

- Add physical units on the `Snap` object.
- Physical units are compatible with all visualization and analysis modules.

## [0.3.1] - 2020-03-06

### Added

- Add many analysis functions.
- Animations of visualizations.

### Changed

- Make it easier to add profiles to Profile
- Make `plonk.visualize.plot` easier to use.

### Fixed

- Fix bug in `Snap.rotate` not rotating sink particles.

## [0.3.0] - 2019-12-07

### Changed

- Interpolation functions are now written in Python and JIT-compiled with Numba.

## [0.2.1] - 2019-11-27

### Added

- Add the JOSS paper describing the code.

## [0.2.0] - 2019-11-06

### Changed

- Use KDEpy for interpolation.

## [0.1.0] - 2019-06-28

- Initial release.