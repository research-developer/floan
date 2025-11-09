"""
Flowangle Examples - Demonstrating the flowangle primitive

This module shows practical usage of the flowangle shape in various contexts.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flowangle import flowangle_to_svg
from svg_generator import Point, SVGCanvas


def example_logo():
    """Example: Using flowangle as a logo"""
    canvas = SVGCanvas(600, 600)

    # Background
    canvas.add('<rect width="600" height="600" fill="#ffffff"/>')

    # Main flowangle logo
    svg = flowangle_to_svg(
        n=3,
        size=220,
        flow=1.5,
        angle=60,
        center=Point(300, 300),
        fill='#0066ff',
        stroke='#0044cc',
        stroke_width=4
    )
    canvas.add(svg)

    # Inner accent
    svg_inner = flowangle_to_svg(
        n=3,
        size=140,
        flow=1.5,
        angle=60,
        center=Point(300, 300),
        fill='#ffffff',
        stroke='#0066ff',
        stroke_width=2
    )
    canvas.add(svg_inner)

    canvas.save('outputs/flowangle_logo.svg')
    print("✓ Saved flowangle_logo.svg")


def example_mandala():
    """Example: Flowangle-based mandala"""
    canvas = SVGCanvas(800, 800)

    # Background
    canvas.add('<rect width="800" height="800" fill="#1a1a2a"/>')

    center = Point(400, 400)
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#a78bfa']

    # Create layers of flowangles with rotation
    for i, (size, flow, color) in enumerate([
        (300, 1.5, colors[0]),
        (250, 1.4, colors[1]),
        (200, 1.3, colors[2]),
        (150, 1.2, colors[3]),
        (100, 1.1, colors[4]),
        (50, 1.0, colors[5]),
    ]):
        # Rotate each layer slightly
        rotation_offset = i * 10

        svg = flowangle_to_svg(
            n=3,
            size=size,
            flow=flow,
            angle=60 + rotation_offset,
            center=center,
            fill='none',
            stroke=color,
            stroke_width=2
        )
        canvas.add(svg)

    canvas.save('outputs/flowangle_mandala.svg')
    print("✓ Saved flowangle_mandala.svg")


def example_pattern():
    """Example: Tiled flowangle pattern"""
    canvas = SVGCanvas(1000, 800)

    # Background
    canvas.add('<rect width="1000" height="800" fill="#f0f0f0"/>')

    # Grid of flowangles
    spacing = 200
    size = 70

    for y in range(0, 800, spacing):
        for x in range(0, 1000, spacing):
            # Offset every other row
            offset_x = spacing // 2 if (y // spacing) % 2 == 1 else 0

            svg = flowangle_to_svg(
                n=3,
                size=size,
                flow=1.5,
                angle=60,
                center=Point(x + offset_x + spacing // 2, y + spacing // 2),
                fill='rgba(102, 153, 255, 0.1)',
                stroke='#6699ff',
                stroke_width=2
            )
            canvas.add(svg)

    canvas.save('outputs/flowangle_pattern.svg')
    print("✓ Saved flowangle_pattern.svg")


def example_morphing():
    """Example: Morphing flowangle sequence"""
    canvas = SVGCanvas(1600, 400)

    # Background
    canvas.add('<rect width="1600" height="400" fill="#2a2a3a"/>')

    # Morph through angle values
    angles = [45, 60, 75, 90, 105, 120, 135, 150]
    x_positions = [i * 200 + 100 for i in range(len(angles))]

    for angle, x in zip(angles, x_positions):
        svg = flowangle_to_svg(
            n=3,
            size=80,
            flow=1.5,
            angle=angle,
            center=Point(x, 200),
            fill='rgba(0, 255, 204, 0.1)',
            stroke='#00ffcc',
            stroke_width=2
        )
        canvas.add(svg)

        # Label
        canvas.add(f'<text x="{x}" y="330" font-size="12" text-anchor="middle" fill="#00ffcc">{angle}°</text>')

    canvas.save('outputs/flowangle_morphing.svg')
    print("✓ Saved flowangle_morphing.svg")


def example_multi_n():
    """Example: Combined n-flowangles"""
    canvas = SVGCanvas(800, 800)

    # Dark background
    canvas.add('<rect width="800" height="800" fill="#1a1a2a"/>')

    center = Point(400, 400)

    # Overlapping flowangles with different n values
    configs = [
        (8, 280, '#ffeaa7'),
        (6, 240, '#a78bfa'),
        (5, 200, '#4ecdc4'),
        (4, 160, '#45b7d1'),
        (3, 120, '#ff6b6b'),
    ]

    for n, size, color in configs:
        svg = flowangle_to_svg(
            n=n,
            size=size,
            flow=1.5,
            angle=60,
            center=center,
            fill='none',
            stroke=color,
            stroke_width=2,
        )
        canvas.add(svg)

    # Center accent
    canvas.add(f'<circle cx="{center.x}" cy="{center.y}" r="8" fill="#ffffff"/>')

    canvas.save('outputs/flowangle_multi_n.svg')
    print("✓ Saved flowangle_multi_n.svg")


def example_comparison():
    """Example: Side-by-side parameter comparison"""
    canvas = SVGCanvas(1200, 400)

    # Background
    canvas.add('<rect width="1200" height="400" fill="#ffffff"/>')

    # Title
    canvas.add('<text x="600" y="40" font-size="20" font-weight="bold" text-anchor="middle" fill="#333">Flowangle Parameter Comparison</text>')

    configs = [
        {'name': 'Low Flow', 'flow': 0.5, 'angle': 90},
        {'name': 'Medium Flow', 'flow': 1.0, 'angle': 90},
        {'name': 'High Flow', 'flow': 1.5, 'angle': 90},
        {'name': 'Low Angle', 'flow': 1.5, 'angle': 60},
        {'name': 'Medium Angle', 'flow': 1.5, 'angle': 90},
        {'name': 'High Angle', 'flow': 1.5, 'angle': 120},
    ]

    positions = [
        (200, 200), (400, 200), (600, 200),
        (800, 200), (1000, 200), (1200, 200),
    ]

    # Adjust positions to be within canvas
    positions = [
        (200, 200), (400, 200), (600, 200),
        (200, 350), (400, 350), (600, 350),
    ]

    # Resize canvas for 2 rows
    canvas = SVGCanvas(800, 550)
    canvas.add('<rect width="800" height="550" fill="#ffffff"/>')
    canvas.add('<text x="400" y="40" font-size="20" font-weight="bold" text-anchor="middle" fill="#333">Flowangle Parameter Comparison</text>')

    for config, pos in zip(configs, positions):
        svg = flowangle_to_svg(
            n=3,
            size=60,
            flow=config['flow'],
            angle=config['angle'],
            center=Point(pos[0], pos[1]),
            fill='rgba(102, 153, 255, 0.1)',
            stroke='#6699ff',
            stroke_width=2
        )
        canvas.add(svg)

        # Label
        canvas.add(f'<text x="{pos[0]}" y="{pos[1] + 90}" font-size="12" font-weight="bold" text-anchor="middle" fill="#333">{config["name"]}</text>')
        canvas.add(f'<text x="{pos[0]}" y="{pos[1] + 105}" font-size="10" text-anchor="middle" fill="#666">flow={config["flow"]} angle={config["angle"]}°</text>')

    canvas.save('outputs/flowangle_comparison.svg')
    print("✓ Saved flowangle_comparison.svg")


if __name__ == '__main__':
    print("Generating flowangle examples...\n")

    example_logo()
    example_mandala()
    example_pattern()
    example_morphing()
    example_multi_n()
    example_comparison()

    print("\n✓ All examples generated!")
    print("\nView them at:")
    print("  http://localhost:8000/outputs/flowangle_logo.svg")
    print("  http://localhost:8000/outputs/flowangle_mandala.svg")
    print("  http://localhost:8000/outputs/flowangle_pattern.svg")
    print("  http://localhost:8000/outputs/flowangle_morphing.svg")
    print("  http://localhost:8000/outputs/flowangle_multi_n.svg")
    print("  http://localhost:8000/outputs/flowangle_comparison.svg")
