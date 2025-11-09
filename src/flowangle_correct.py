"""
Flowangle Correct Implementation

The control handles form a triangle positioned at a scalar distance
along the perpendicular from each edge of the reference triangle.
"""

import math
from svg_generator import Point, SVGCanvas


def create_flowangle_correct(
    n: int = 3,
    size: float = 300,
    handle_distance: float = 0.5,  # 0.0 to 1.0+ (distance from edge outward)
    center: Point = None
) -> tuple:
    """
    Create flowangle with properly positioned control handles

    Args:
        n: Number of sides (3 for triquetra)
        size: Radius from center to vertices
        handle_distance: How far the handles are from the edge (0.0 = on edge, 1.0 = far out)
        center: Center point

    Returns:
        (vertices, lobes)
    """
    if center is None:
        center = Point(0, 0)

    # Generate vertices
    vertices = []
    angle_step = 2 * math.pi / n
    start_angle = -math.pi / 2

    for i in range(n):
        vertex_angle = start_angle + i * angle_step
        x = center.x + size * math.cos(vertex_angle)
        y = center.y + size * math.sin(vertex_angle)
        vertices.append(Point(x, y))

    # Create lobes
    lobes = []

    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]

        # Midpoint of the edge
        mid_x = (v1.x + v2.x) / 2
        mid_y = (v1.y + v2.y) / 2

        # Vector from center to midpoint (outward direction)
        outward_x = mid_x - center.x
        outward_y = mid_y - center.y

        # Normalize the outward vector
        outward_length = math.sqrt(outward_x**2 + outward_y**2)
        if outward_length > 0:
            outward_x /= outward_length
            outward_y /= outward_length

        # Calculate handle positions
        # Handles are positioned at handle_distance * size from the edge midpoint
        # BUT INWARD (toward center), not outward!
        handle_offset = handle_distance * size

        # Control points should be positioned along the edge, then offset INWARD
        # INWARD means negative offset (toward center)

        # Control point 1: closer to v1
        t1 = 0.33  # 1/3 along the edge
        edge_point1_x = v1.x + (v2.x - v1.x) * t1
        edge_point1_y = v1.y + (v2.y - v1.y) * t1

        control1_x = edge_point1_x - outward_x * handle_offset  # INWARD (negative)
        control1_y = edge_point1_y - outward_y * handle_offset

        # Control point 2: closer to v2
        t2 = 0.67  # 2/3 along the edge
        edge_point2_x = v1.x + (v2.x - v1.x) * t2
        edge_point2_y = v1.y + (v2.y - v1.y) * t2

        control2_x = edge_point2_x - outward_x * handle_offset  # INWARD (negative)
        control2_y = edge_point2_y - outward_y * handle_offset

        lobes.append({
            'start': v1,
            'control1': Point(control1_x, control1_y),
            'control2': Point(control2_x, control2_y),
            'end': v2
        })

    return vertices, lobes


def flowangle_correct_svg(
    n: int = 3,
    size: float = 300,
    handle_distance: float = 0.5,
    center: Point = None,
    stroke: str = '#000000',
    stroke_width: float = 8,
    show_reference: bool = True,
    colors: list = None
) -> str:
    """Generate SVG for correct flowangle"""
    if center is None:
        center = Point(0, 0)

    vertices, lobes = create_flowangle_correct(n, size, handle_distance, center)

    svg_parts = []

    # Reference triangle
    if show_reference:
        polygon_points = ' '.join([f'{v.x:.2f},{v.y:.2f}' for v in vertices])
        svg_parts.append(
            f'<polygon points="{polygon_points}" '
            f'fill="none" stroke="rgba(128, 128, 128, 0.3)" stroke-width="1"/>'
        )

    # Draw lobes
    if colors is None:
        colors = [stroke] * n

    for lobe, color in zip(lobes, colors):
        path = f'M {lobe["start"].x:.2f},{lobe["start"].y:.2f} '
        path += f'C {lobe["control1"].x:.2f},{lobe["control1"].y:.2f} '
        path += f'{lobe["control2"].x:.2f},{lobe["control2"].y:.2f} '
        path += f'{lobe["end"].x:.2f},{lobe["end"].y:.2f}'

        svg_parts.append(
            f'<path d="{path}" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" '
            f'stroke-linecap="round"/>'
        )

    return '\n'.join(svg_parts)


if __name__ == '__main__':
    # Test with different handle distances
    canvas = SVGCanvas(1600, 600)
    canvas.add('<rect width="1600" height="600" fill="#ffffff"/>')

    canvas.add('<text x="800" y="50" font-size="28" font-weight="bold" text-anchor="middle" fill="#333">Flowangle - Handle Distance Parameter</text>')

    distances = [0.3, 0.5, 0.7, 1.0]
    positions = [300, 600, 900, 1200]

    for dist, x in zip(distances, positions):
        canvas.add(f'<text x="{x}" y="90" font-size="14" text-anchor="middle" fill="#666">distance={dist}</text>')

        svg = flowangle_correct_svg(
            n=3,
            size=120,
            handle_distance=dist,
            center=Point(x, 350),
            stroke='#000000',
            stroke_width=6
        )
        canvas.add(svg)

    canvas.save('outputs/flowangle_correct_test.svg')
    print("✓ Saved flowangle_correct_test.svg")
    print("View at: http://localhost:8000/outputs/flowangle_correct_test.svg")
