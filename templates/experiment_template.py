"""
Experiment Template - Quick Start for Algorithmic SVG Generation

Copy this file and modify for your explorations.
"""
import os
import sys
import math

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from svg_generator import *

# ============ YOUR CUSTOM FUNCTIONS ============

def my_custom_shape(canvas: SVGCanvas, center: Point, size: float, **params):
    """
    Template for creating custom algorithmic shapes.
    
    Args:
        canvas: SVGCanvas to draw on
        center: Center point of the shape
        size: Base size parameter
        **params: Additional parameters (depth, color, etc.)
    """
    # Your algorithm here
    pass

def recursive_pattern(canvas: SVGCanvas, center: Point, size: float, depth: int):
    """
    Template for recursive/fractal patterns.
    
    Args:
        canvas: SVGCanvas to draw on
        center: Center point
        size: Current size (gets smaller with recursion)
        depth: Recursion depth (0 = base case)
    """
    if depth == 0:
        # Base case: draw something simple
        canvas.circle(center, size, fill=f"hsl({depth * 30}, 70%, 60%)")
        return
    
    # Recursive case: draw and recurse
    canvas.circle(center, size, fill="none", stroke="black")
    
    # Example: 4 smaller copies around the center
    for i in range(4):
        angle = i * math.pi / 2
        offset = size * 0.7
        new_center = Point(
            center.x + offset * math.cos(angle),
            center.y + offset * math.sin(angle)
        )
        recursive_pattern(canvas, new_center, size * 0.4, depth - 1)

def parametric_function(t: float, **params) -> Point:
    """
    Template for parametric curve generation.
    
    Args:
        t: Parameter value (typically 0 to 2π)
        **params: Additional parameters (amplitude, frequency, etc.)
    
    Returns:
        Point on the curve
    """
    # Example: circle
    r = params.get('radius', 100)
    center = params.get('center', Point(500, 500))
    
    x = center.x + r * math.cos(t)
    y = center.y + r * math.sin(t)
    
    return Point(x, y)

def generate_parametric_shape(canvas: SVGCanvas, param_fn, 
                              t_start: float = 0, 
                              t_end: float = 2*math.pi, 
                              steps: int = 360,
                              **kwargs):
    """
    Generate shape from parametric function.
    
    Args:
        canvas: SVGCanvas to draw on
        param_fn: Function that takes t and returns Point
        t_start: Start parameter value
        t_end: End parameter value
        steps: Number of points to generate
        **kwargs: Additional parameters for styling
    """
    points = []
    dt = (t_end - t_start) / steps
    
    for i in range(steps):
        t = t_start + i * dt
        points.append(param_fn(t))
    
    fill = kwargs.get('fill', 'none')
    stroke = kwargs.get('stroke', 'black')
    stroke_width = kwargs.get('stroke_width', 2)
    
    canvas.polygon(points, fill=fill, stroke=stroke, stroke_width=stroke_width)

# ============ EXPERIMENT CODE ============

def main():
    """
    Main experiment function.
    Modify this to create your designs.
    """
    
    # Create canvas
    canvas = SVGCanvas(1000, 1000)
    
    # Example 1: Simple shape
    center = Point(500, 500)
    triangle = equilateral_triangle(center, 200)
    canvas.polygon(triangle, fill="lightblue", stroke="navy", stroke_width=3)
    
    # Example 2: Recursive pattern
    # recursive_pattern(canvas, Point(300, 300), 100, depth=3)
    
    # Example 3: Parametric curve
    # generate_parametric_shape(canvas, parametric_function, steps=360,
    #                          radius=150, center=Point(700, 300),
    #                          stroke="purple", stroke_width=2)
    
    # Save output
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    canvas.save(os.path.join(output_dir, 'experiment.svg'))
    print("✓ Experiment saved!")

if __name__ == "__main__":
    main()
