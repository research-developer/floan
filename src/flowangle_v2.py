"""
Flowangle V2 - Corrected implementation with outward-bulging lobes

The triangle vertices are anchor points where the curves START and END.
The curves bulge OUTWARD from the triangle, creating rounded lobes.
"""

import math
from svg_generator import Point, SVGCanvas


def create_flowangle_v2(
    n: int = 3,
    size: float = 300,
    flow: float = 1.5,
    angle: float = 60,
    center: Point = None
) -> tuple:
    """
    Create flowangle with outward-bulging lobes

    Args:
        n: Number of sides (3 for triquetra)
        size: Radius from center to vertices
        flow: How far the curve bulges outward (multiplier of size)
        angle: Angle of control handles relative to the edge tangent
        center: Center point

    Returns:
        (vertices, lobes) where lobes is a list of bezier path data
    """
    if center is None:
        center = Point(0, 0)

    # Generate vertices of regular polygon
    vertices = []
    angle_step = 2 * math.pi / n
    start_angle = -math.pi / 2  # Start at top

    for i in range(n):
        vertex_angle = start_angle + i * angle_step
        x = center.x + size * math.cos(vertex_angle)
        y = center.y + size * math.sin(vertex_angle)
        vertices.append(Point(x, y))

    # Create lobes - each lobe connects two adjacent vertices
    # and bulges OUTWARD from the triangle
    lobes = []

    angle_rad = math.radians(angle)

    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]

        # Calculate the angle of the edge from v1 to v2
        edge_angle = math.atan2(v2.y - v1.y, v2.x - v1.x)

        # The control points should be perpendicular to the edge, pointing OUTWARD
        # "Outward" means away from the center

        # Midpoint of the edge
        mid_x = (v1.x + v2.x) / 2
        mid_y = (v1.y + v2.y) / 2

        # Angle from center to midpoint (this is the "outward" direction)
        outward_angle = math.atan2(mid_y - center.y, mid_x - center.x)

        # Calculate how far out the bulge should go
        bulge_distance = size * flow

        # Control point 1: offset from v1, influenced by both edge direction and outward direction
        # We want it to go outward and follow the curve
        control1_angle = edge_angle + math.pi / 2 + angle_rad
        control1 = Point(
            v1.x + bulge_distance * math.cos(outward_angle) * 0.5,
            v1.y + bulge_distance * math.sin(outward_angle) * 0.5
        )

        # Control point 2: offset from v2, mirror of control1
        control2_angle = edge_angle + math.pi / 2 - angle_rad
        control2 = Point(
            v2.x + bulge_distance * math.cos(outward_angle) * 0.5,
            v2.y + bulge_distance * math.sin(outward_angle) * 0.5
        )

        # Actually, let me recalculate this properly
        # The bulge point should be at the midpoint of the edge, pushed outward
        bulge_x = mid_x + bulge_distance * math.cos(outward_angle)
        bulge_y = mid_y + bulge_distance * math.sin(outward_angle)

        # Control points are positioned to create smooth curve through the bulge point
        # They should be along the line from vertex to bulge, at 1/3 and 2/3 distance
        control1 = Point(
            v1.x + (bulge_x - v1.x) * 0.5,
            v1.y + (bulge_y - v1.y) * 0.5
        )

        control2 = Point(
            v2.x + (bulge_x - v2.x) * 0.5,
            v2.y + (bulge_y - v2.y) * 0.5
        )

        lobes.append({
            'start': v1,
            'control1': control1,
            'control2': control2,
            'end': v2
        })

    return vertices, lobes


def flowangle_v2_svg(
    n: int = 3,
    size: float = 300,
    flow: float = 1.5,
    angle: float = 60,
    center: Point = None,
    stroke: str = '#000000',
    stroke_width: float = 8,
    show_reference: bool = True
) -> str:
    """Generate SVG for flowangle v2"""
    if center is None:
        center = Point(0, 0)

    vertices, lobes = create_flowangle_v2(n, size, flow, angle, center)

    svg_parts = []

    # Reference triangle
    if show_reference:
        polygon_points = ' '.join([f'{v.x:.2f},{v.y:.2f}' for v in vertices])
        svg_parts.append(
            f'<polygon points="{polygon_points}" '
            f'fill="none" stroke="rgba(128, 128, 128, 0.3)" stroke-width="1"/>'
        )

    # Draw lobes
    for lobe in lobes:
        path = f'M {lobe["start"].x:.2f},{lobe["start"].y:.2f} '
        path += f'C {lobe["control1"].x:.2f},{lobe["control1"].y:.2f} '
        path += f'{lobe["control2"].x:.2f},{lobe["control2"].y:.2f} '
        path += f'{lobe["end"].x:.2f},{lobe["end"].y:.2f}'

        svg_parts.append(
            f'<path d="{path}" fill="none" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" '
            f'stroke-linecap="round"/>'
        )

    return '\n'.join(svg_parts)


if __name__ == '__main__':
    canvas = SVGCanvas(1200, 1200)
    canvas.add('<rect width="1200" height="1200" fill="#ffffff"/>')

    canvas.add('<text x="600" y="80" font-size="36" font-weight="bold" text-anchor="middle" fill="#333">Flowangle V2 Test</text>')
    canvas.add('<text x="600" y="115" font-size="18" text-anchor="middle" fill="#666">Outward-bulging lobes</text>')

    svg = flowangle_v2_svg(
        n=3,
        size=400,
        flow=1.5,
        angle=60,
        center=Point(600, 650),
        stroke='#000000',
        stroke_width=10,
        show_reference=True
    )
    canvas.add(svg)

    canvas.save('outputs/flowangle_v2_test.svg')
    print("✓ Saved flowangle_v2_test.svg")
    print("View at: http://localhost:8000/outputs/flowangle_v2_test.svg")
