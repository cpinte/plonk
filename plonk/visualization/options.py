"""
Plot options.
"""

from collections import namedtuple

FigureOptions = namedtuple(
    'FigureOptions',
    [
        'axis',
        'colorbar',
        'colormap',
        'figure',
        'font_family',
        'font_size',
        'title',
    ],
)

ImageRangeOptions = namedtuple(
    'ImageRangeOptions', ['xrange', 'yrange', 'extent']
)

InterpolationOptions = namedtuple(
    'InterpolationOptions',
    [
        'accelerate',
        'cross_section',
        'density_weighted',
        'distance_to_screen',
        'normalize',
        'number_pixels',
        'opacity',
        'slice_position',
        'z_observer',
    ],
)

RenderOptions = namedtuple(
    'RenderOptions',
    ['render_scale', 'render_min', 'render_max', 'render_fraction_max'],
)

RotationOptions = namedtuple(
    'RotationOptions',
    ['rotation_axis', 'rotation_angle', 'position_angle', 'inclination'],
)

VectorOptions = namedtuple(
    'VectorOptions', ['stream', 'stride', 'vector_color']
)

PlotOptions = namedtuple(
    'PlotOptions',
    [
        'FigureOptions',
        'ImageRangeOptions',
        'InterpolationOptions',
        'RenderOptions',
        'RotationOptions',
        'VectorOptions',
    ],
)

DEFAULT_OPTIONS = PlotOptions(
    FigureOptions(
        axis=None,
        colorbar=True,
        colormap='gist_heat',
        figure=None,
        font_family='sans-serif',
        font_size=12,
        title=None,
    ),
    ImageRangeOptions(xrange=None, yrange=None, extent=None),
    InterpolationOptions(
        accelerate=False,
        cross_section=False,
        density_weighted=False,
        distance_to_screen=0.0,
        normalize=False,
        number_pixels=(512, 512),
        opacity=False,
        slice_position=0.0,
        z_observer=0.0,
    ),
    RenderOptions(
        render_scale='linear',
        render_min=None,
        render_max=None,
        render_fraction_max=None,
    ),
    RotationOptions(
        rotation_axis=None,
        rotation_angle=None,
        position_angle=None,
        inclination=None,
    ),
    VectorOptions(stream=False, stride=25, vector_color='black'),
)