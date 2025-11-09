"""
Flowangle Generator - Algorithmic generation of triquetra-like shapes

A flowangle is defined by:
- n: number of sides (3 for triquetra-like)
- flow: normalized control handle distance (0.0-2.0, default ~1.0)
- angle: handle rotation in degrees relative to center-vertex line (-180 to 180)
"""

import math
from svg_generator import Point, SVGCanvas
from typing import List, Tuple


def create_flowangle(
    n: int = 3,
    size: float = 300,
    flow: float = 1.0,
    angle: float = 105.0,
    center: Point = None
) -> Tuple[List[Point], List[dict]]:
    """
    Create a flowangle shape

    Args:
        n: Number of sides (vertices)
        size: Radius from center to vertices
        flow: Control handle distance as multiplier of size (0.0-2.0)
        angle: Angle offset of handles in degrees relative to center-vertex line
        center: Center point (default: origin)

    Returns:
        (vertices, bezier_segments)
    """
    if center is None:
        center = Point(0, 0)

    # Generate vertices of regular polygon
    vertices = []
    angle_step = 2 * math.pi / n

    # Start at top (270° / -90°)
    start_angle = -math.pi / 2

    for i in range(n):
        vertex_angle = start_angle + i * angle_step
        x = center.x + size * math.cos(vertex_angle)
        y = center.y + size * math.sin(vertex_angle)
        vertices.append(Point(x, y))

    # Calculate flow distance (control handle length)
    flow_distance = size * flow

    # Convert angle parameter to radians
    angle_rad = math.radians(angle)

    # Create bezier segments connecting vertices
    segments = []

    for i in range(n):
        start_vertex = vertices[i]
        end_vertex = vertices[(i + 1) % n]

        # Angle from center to start vertex
        start_angle_to_center = math.atan2(start_vertex.y - center.y, start_vertex.x - center.x)

        # Angle from center to end vertex
        end_angle_to_center = math.atan2(end_vertex.y - center.y, end_vertex.x - center.x)

        # Control point 1: extends from start vertex
        # The control angle is offset from the center-to-vertex line
        control1_angle = start_angle_to_center + angle_rad
        control1 = Point(
            start_vertex.x + flow_distance * math.cos(control1_angle),
            start_vertex.y + flow_distance * math.sin(control1_angle)
        )

        # Control point 2: extends from end vertex
        # The control angle is offset in the opposite direction
        control2_angle = end_angle_to_center - angle_rad
        control2 = Point(
            end_vertex.x + flow_distance * math.cos(control2_angle),
            end_vertex.y + flow_distance * math.sin(control2_angle)
        )

        segments.append({
            'start': start_vertex,
            'control1': control1,
            'control2': control2,
            'end': end_vertex
        })

    return vertices, segments


def flowangle_to_svg(
    n: int = 3,
    size: float = 300,
    flow: float = 1.0,
    angle: float = 105.0,
    center: Point = None,
    fill: str = 'none',
    stroke: str = '#0066CC',
    stroke_width: float = 2,
    show_construction: bool = False
) -> str:
    """
    Generate SVG path string for a flowangle

    Args:
        n: Number of sides
        size: Radius from center to vertices
        flow: Control handle distance multiplier
        angle: Handle angle offset in degrees
        center: Center point
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width
        show_construction: If True, show construction lines and control points

    Returns:
        SVG path string
    """
    if center is None:
        center = Point(0, 0)

    vertices, segments = create_flowangle(n, size, flow, angle, center)

    # Build SVG path
    svg_parts = []

    # Start path at first vertex
    first_seg = segments[0]
    path = f'M {first_seg["start"].x:.2f},{first_seg["start"].y:.2f} '

    # Add cubic bezier curves for each segment
    for seg in segments:
        path += f'C {seg["control1"].x:.2f},{seg["control1"].y:.2f} '
        path += f'{seg["control2"].x:.2f},{seg["control2"].y:.2f} '
        path += f'{seg["end"].x:.2f},{seg["end"].y:.2f} '

    # Close path
    path += 'Z'

    # Main path
    svg_parts.append(f'<path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')

    # Construction geometry (optional)
    if show_construction:
        # Draw vertices
        for v in vertices:
            svg_parts.append(f'<circle cx="{v.x:.2f}" cy="{v.y:.2f}" r="3" fill="red"/>')

        # Draw center
        svg_parts.append(f'<circle cx="{center.x:.2f}" cy="{center.y:.2f}" r="4" fill="darkred"/>')

        # Draw control points and lines
        for seg in segments:
            # Control points
            svg_parts.append(f'<circle cx="{seg["control1"].x:.2f}" cy="{seg["control1"].y:.2f}" r="3" fill="blue" opacity="0.6"/>')
            svg_parts.append(f'<circle cx="{seg["control2"].x:.2f}" cy="{seg["control2"].y:.2f}" r="3" fill="blue" opacity="0.6"/>')

            # Control lines
            svg_parts.append(f'<line x1="{seg["start"].x:.2f}" y1="{seg["start"].y:.2f}" x2="{seg["control1"].x:.2f}" y2="{seg["control1"].y:.2f}" stroke="blue" stroke-width="1" opacity="0.3"/>')
            svg_parts.append(f'<line x1="{seg["end"].x:.2f}" y1="{seg["end"].y:.2f}" x2="{seg["control2"].x:.2f}" y2="{seg["control2"].y:.2f}" stroke="blue" stroke-width="1" opacity="0.3"/>')

    return '\n'.join(svg_parts)


def create_parameter_grid(
    output_path: str = 'outputs/flowangle_parameter_grid.svg',
    n: int = 3
):
    """
    Create a visual grid showing flowangle variations across flow and angle parameters

    This is a REPL-style visualization for parameter exploration
    """
    # Parameter ranges to test
    flow_values = [0.5, 0.75, 1.0, 1.25, 1.5]
    angle_values = [60, 75, 90, 105, 120, 135]

    # Grid layout
    cell_size = 250
    padding = 50
    shape_size = 80  # Radius of each flowangle

    grid_width = len(flow_values) * cell_size + padding * 2
    grid_height = len(angle_values) * cell_size + padding * 2

    canvas = SVGCanvas(grid_width, grid_height)

    # Background
    canvas.add(f'<rect width="{grid_width}" height="{grid_height}" fill="#f8f8f8"/>')

    # Title
    canvas.add(f'<text x="{grid_width/2}" y="30" font-size="20" font-weight="bold" text-anchor="middle" fill="#333">{n}n-Flowangle Parameter Grid</text>')

    # Column headers (flow values)
    canvas.add(f'<text x="25" y="70" font-size="12" font-weight="bold" fill="#666">Flow →</text>')
    for i, flow in enumerate(flow_values):
        x = padding + i * cell_size + cell_size / 2
        canvas.add(f'<text x="{x}" y="70" font-size="14" text-anchor="middle" fill="#333">{flow:.2f}</text>')

    # Row headers (angle values)
    canvas.add(f'<text x="25" y="100" font-size="12" font-weight="bold" fill="#666" transform="rotate(-90, 25, 100)">Angle →</text>')
    for j, angle in enumerate(angle_values):
        y = padding + 50 + j * cell_size + cell_size / 2
        canvas.add(f'<text x="40" y="{y}" font-size="14" text-anchor="middle" fill="#333">{angle}°</text>')

    # Generate grid of flowangles
    for i, flow in enumerate(flow_values):
        for j, angle in enumerate(angle_values):
            # Cell position
            cx = padding + i * cell_size + cell_size / 2
            cy = padding + 50 + j * cell_size + cell_size / 2

            center = Point(cx, cy)

            # Draw light cell border
            cell_x = padding + i * cell_size
            cell_y = padding + 50 + j * cell_size
            canvas.add(f'<rect x="{cell_x}" y="{cell_y}" width="{cell_size}" height="{cell_size}" fill="none" stroke="#ddd" stroke-width="1"/>')

            # Generate flowangle
            svg = flowangle_to_svg(
                n=n,
                size=shape_size,
                flow=flow,
                angle=angle,
                center=center,
                fill='rgba(102, 153, 255, 0.1)',
                stroke='#0066CC',
                stroke_width=2
            )

            canvas.add(svg)

    canvas.save(output_path)
    return output_path


if __name__ == '__main__':
    import sys

    # Test 1: Generate single flowangle with construction
    print("Generating test flowangle with construction lines...")
    canvas = SVGCanvas(800, 800)
    canvas.add(f'<rect width="800" height="800" fill="#f8f8f8"/>')

    svg = flowangle_to_svg(
        n=3,
        size=300,
        flow=1.05,
        angle=105,
        center=Point(400, 400),
        fill='rgba(255, 100, 100, 0.1)',
        stroke='#CC0066',
        stroke_width=3,
        show_construction=True
    )
    canvas.add(svg)
    canvas.save('outputs/flowangle_test.svg')
    print("✓ Saved to outputs/flowangle_test.svg")

    # Test 2: Generate parameter exploration grid
    print("\nGenerating parameter grid for exploration...")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    path = create_parameter_grid(n=n)
    print(f"✓ Saved to {path}")
    print(f"\nGrid shows {n}n-flowangles across:")
    print("  Flow: 0.5 to 1.5 (left to right)")
    print("  Angle: 60° to 135° (top to bottom)")
