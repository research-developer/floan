"""
svGen - Algorithmic SVG Generator

A Python framework for creating geometrically precise, fractal-friendly,
and algorithmically-generated SVG graphics.
"""

from .svg_generator import (
    Point,
    SVGCanvas,
    regular_polygon,
    equilateral_triangle,
    sierpinski_triangle,
    koch_snowflake,
    scale_points,
    rotate_points,
    translate_points,
)

__version__ = "0.1.0"
__all__ = [
    "Point",
    "SVGCanvas",
    "regular_polygon",
    "equilateral_triangle",
    "sierpinski_triangle",
    "koch_snowflake",
    "scale_points",
    "rotate_points",
    "translate_points",
]
