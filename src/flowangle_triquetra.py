"""
Flowangle Triquetra - Three separate intersecting curved paths

This creates the classic triquetra appearance where three independent
curved lobes pass through the center and intersect each other.
"""

import math
from svg_generator import Point, SVGCanvas
from flowangle import create_flowangle


def create_triquetra_lobes(
    n: int = 3,
    size: float = 300,
    flow: float = 1.5,
    angle: float = 60,
    center: Point = None
) -> list:
    """
    Create n separate lobe paths that intersect through the center

    Each lobe is a curve that goes from one vertex, through/past the center,
    to another vertex (not adjacent).

    Args:
        n: Number of lobes (3 for classic triquetra)
        size: Radius from center to vertices
        flow: Control handle distance multiplier
        angle: Handle angle offset in degrees
        center: Center point

    Returns:
        List of path strings, one for each lobe
    """
    if center is None:
        center = Point(0, 0)

    # Get vertices from base flowangle
    vertices, segments = create_flowangle(n, size, flow, angle, center)

    lobes = []

    # For a 3n-flowangle, we want 3 lobes:
    # Lobe 0: vertex 0 → center → vertex 1 (skipping vertex in between)
    # Lobe 1: vertex 1 → center → vertex 2
    # Lobe 2: vertex 2 → center → vertex 0

    for i in range(n):
        # Start vertex
        start_vertex = vertices[i]
        # End vertex (next one around)
        end_vertex = vertices[(i + 1) % n]

        # Calculate flow distance
        flow_distance = size * flow

        # Convert angle parameter to radians
        angle_rad = math.radians(angle)

        # Angle from center to start vertex
        start_angle_to_center = math.atan2(start_vertex.y - center.y, start_vertex.x - center.x)
        # Angle from center to end vertex
        end_angle_to_center = math.atan2(end_vertex.y - center.y, end_vertex.x - center.x)

        # Control point 1: extends from start vertex towards center
        # Use the same control point from the flowangle segment
        control1_angle = start_angle_to_center + angle_rad
        control1 = Point(
            start_vertex.x + flow_distance * math.cos(control1_angle),
            start_vertex.y + flow_distance * math.sin(control1_angle)
        )

        # Control point 2: extends from end vertex towards center
        control2_angle = end_angle_to_center - angle_rad
        control2 = Point(
            end_vertex.x + flow_distance * math.cos(control2_angle),
            end_vertex.y + flow_distance * math.sin(control2_angle)
        )

        # Create the lobe path as a cubic bezier
        path = f'M {start_vertex.x:.2f},{start_vertex.y:.2f} '
        path += f'C {control1.x:.2f},{control1.y:.2f} '
        path += f'{control2.x:.2f},{control2.y:.2f} '
        path += f'{end_vertex.x:.2f},{end_vertex.y:.2f}'

        lobes.append(path)

    return lobes, vertices


def flowangle_triquetra_svg(
    n: int = 3,
    size: float = 300,
    flow: float = 1.5,
    angle: float = 60,
    center: Point = None,
    stroke: str = '#000000',
    stroke_width: float = 8,
    show_reference_polygon: bool = True
) -> str:
    """
    Generate SVG for triquetra-style flowangle with separate intersecting lobes

    Args:
        n: Number of lobes
        size: Radius from center to vertices
        flow: Control handle distance multiplier
        angle: Handle angle offset in degrees
        center: Center point
        stroke: Stroke color for the lobes
        stroke_width: Width of each lobe
        show_reference_polygon: If True, show faded background polygon

    Returns:
        SVG elements as string
    """
    if center is None:
        center = Point(0, 0)

    svg_parts = []

    lobes, vertices = create_triquetra_lobes(n, size, flow, angle, center)

    # Draw reference polygon (faded)
    if show_reference_polygon:
        polygon_points = ' '.join([f'{v.x:.2f},{v.y:.2f}' for v in vertices])
        svg_parts.append(
            f'<polygon points="{polygon_points}" '
            f'fill="none" '
            f'stroke="rgba(128, 128, 128, 0.3)" '
            f'stroke-width="1"/>'
        )

    # Draw each lobe
    for lobe_path in lobes:
        svg_parts.append(
            f'<path d="{lobe_path}" '
            f'fill="none" '
            f'stroke="{stroke}" '
            f'stroke-width="{stroke_width}" '
            f'stroke-linecap="round" '
            f'stroke-linejoin="round"/>'
        )

    return '\n'.join(svg_parts)


def create_triquetra_examples():
    """Create examples of triquetra-style flowangles"""

    # Example 1: Basic triquetra
    canvas = SVGCanvas(1000, 1000)
    canvas.add('<rect width="1000" height="1000" fill="#ffffff"/>')

    canvas.add('<text x="500" y="60" font-size="32" font-weight="bold" text-anchor="middle" fill="#333">Triquetra Flowangle</text>')
    canvas.add('<text x="500" y="90" font-size="16" text-anchor="middle" fill="#666">Three separate intersecting lobes</text>')

    svg = flowangle_triquetra_svg(
        n=3,
        size=350,
        flow=1.5,
        angle=60,
        center=Point(500, 550),
        stroke='#000000',
        stroke_width=8,
        show_reference_polygon=True
    )
    canvas.add(svg)

    canvas.save('outputs/flowangle_triquetra.svg')
    print("✓ Saved flowangle_triquetra.svg")


    # Example 2: Different stroke widths
    canvas2 = SVGCanvas(1600, 600)
    canvas2.add('<rect width="1600" height="600" fill="#f8f8f8"/>')

    canvas2.add('<text x="800" y="50" font-size="24" font-weight="bold" text-anchor="middle" fill="#333">Triquetra Stroke Widths</text>')

    widths = [4, 6, 8, 10]
    positions = [300, 600, 900, 1200]

    for width, x in zip(widths, positions):
        canvas2.add(f'<text x="{x}" y="90" font-size="14" text-anchor="middle" fill="#666">width={width}</text>')

        svg = flowangle_triquetra_svg(
            n=3,
            size=130,
            flow=1.5,
            angle=60,
            center=Point(x, 350),
            stroke='#000000',
            stroke_width=width,
            show_reference_polygon=True
        )
        canvas2.add(svg)

    canvas2.save('outputs/flowangle_triquetra_widths.svg')
    print("✓ Saved flowangle_triquetra_widths.svg")


    # Example 3: Parameter exploration
    canvas3 = SVGCanvas(1600, 1200)
    canvas3.add('<rect width="1600" height="1200" fill="#ffffff"/>')

    canvas3.add('<text x="800" y="50" font-size="24" font-weight="bold" text-anchor="middle" fill="#333">Triquetra Parameter Exploration</text>')

    flow_values = [0.75, 1.0, 1.25, 1.5]
    angle_values = [45, 60, 75]

    y_start = 150
    x_start = 250

    # Headers
    canvas3.add('<text x="100" y="250" font-size="14" font-weight="bold" text-anchor="middle" fill="#666">Flow →</text>')

    for i, flow in enumerate(flow_values):
        x = x_start + i * 350
        canvas3.add(f'<text x="{x}" y="120" font-size="14" text-anchor="middle" fill="#666">{flow}</text>')

    canvas3.add('<text x="100" y="400" font-size="14" font-weight="bold" text-anchor="middle" fill="#666" transform="rotate(-90, 100, 400)">Angle →</text>')

    for j, angle in enumerate(angle_values):
        y = y_start + 100 + j * 350
        canvas3.add(f'<text x="150" y="{y}" font-size="14" text-anchor="middle" fill="#666">{angle}°</text>')

    for i, flow in enumerate(flow_values):
        for j, angle in enumerate(angle_values):
            x = x_start + i * 350
            y = y_start + 100 + j * 350

            svg = flowangle_triquetra_svg(
                n=3,
                size=120,
                flow=flow,
                angle=angle,
                center=Point(x, y),
                stroke='#000000',
                stroke_width=6,
                show_reference_polygon=True
            )
            canvas3.add(svg)

    canvas3.save('outputs/flowangle_triquetra_params.svg')
    print("✓ Saved flowangle_triquetra_params.svg")


    # Example 4: Colored lobes
    canvas4 = SVGCanvas(1000, 1000)
    canvas4.add('<rect width="1000" height="1000" fill="#f8f8f8"/>')

    canvas4.add('<text x="500" y="60" font-size="32" font-weight="bold" text-anchor="middle" fill="#333">Colored Triquetra</text>')
    canvas4.add('<text x="500" y="90" font-size="16" text-anchor="middle" fill="#666">Each lobe with different color</text>')

    lobes, vertices = create_triquetra_lobes(
        n=3,
        size=350,
        flow=1.5,
        angle=60,
        center=Point(500, 550)
    )

    # Draw reference polygon
    polygon_points = ' '.join([f'{v.x:.2f},{v.y:.2f}' for v in vertices])
    canvas4.add(f'<polygon points="{polygon_points}" fill="none" stroke="rgba(128, 128, 128, 0.3)" stroke-width="1"/>')

    # Draw each lobe with different color
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    for lobe_path, color in zip(lobes, colors):
        canvas4.add(
            f'<path d="{lobe_path}" '
            f'fill="none" '
            f'stroke="{color}" '
            f'stroke-width="8" '
            f'stroke-linecap="round"/>'
        )

    canvas4.save('outputs/flowangle_triquetra_colored.svg')
    print("✓ Saved flowangle_triquetra_colored.svg")


    # Example 5: Large hero image
    canvas5 = SVGCanvas(1200, 1200)
    canvas5.add('<rect width="1200" height="1200" fill="#ffffff"/>')

    canvas5.add('<text x="600" y="80" font-size="36" font-weight="bold" text-anchor="middle" fill="#333">Triquetra 3n-Flowangle</text>')
    canvas5.add('<text x="600" y="115" font-size="18" text-anchor="middle" fill="#666">60° × 1.5 • Three Intersecting Lobes</text>')

    svg = flowangle_triquetra_svg(
        n=3,
        size=450,
        flow=1.5,
        angle=60,
        center=Point(600, 650),
        stroke='#000000',
        stroke_width=10,
        show_reference_polygon=True
    )
    canvas5.add(svg)

    canvas5.save('outputs/flowangle_triquetra_hero.svg')
    print("✓ Saved flowangle_triquetra_hero.svg")


if __name__ == '__main__':
    print("Generating triquetra flowangle examples...\n")
    create_triquetra_examples()
    print("\n✓ All triquetra examples generated!")
    print("\nView them at:")
    print("  http://localhost:8000/outputs/flowangle_triquetra.svg")
    print("  http://localhost:8000/outputs/flowangle_triquetra_widths.svg")
    print("  http://localhost:8000/outputs/flowangle_triquetra_params.svg")
    print("  http://localhost:8000/outputs/flowangle_triquetra_colored.svg")
    print("  http://localhost:8000/outputs/flowangle_triquetra_hero.svg")
