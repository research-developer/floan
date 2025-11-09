"""
Flowangle Final - Using the actual hand-graphed bezier curves as reference

Each lobe goes from vertex[i] to vertex[i+1] and bulges OUTWARD.
The control points are positioned to create the smooth curved lobes.
"""

import math
from svg_generator import Point, SVGCanvas


def create_flowangle_final(
    n: int = 3,
    size: float = 300,
    flow: float = 1.05,
    angle: float = 105,
    center: Point = None
) -> tuple:
    """
    Create flowangle using the EXACT same math as the hand-graphed version

    The hand-graphed data shows us that the control points create curves
    that bulge outward from the triangle edges.
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
    flow_distance = size * flow
    angle_rad = math.radians(angle)

    for i in range(n):
        start_vertex = vertices[i]
        end_vertex = vertices[(i + 1) % n]

        # Angles from center to vertices
        start_angle_to_center = math.atan2(start_vertex.y - center.y, start_vertex.x - center.x)
        end_angle_to_center = math.atan2(end_vertex.y - center.y, end_vertex.x - center.x)

        # Control points:
        # control1 extends from start_vertex at angle (start_angle_to_center + angle_rad)
        # control2 extends from end_vertex at angle (end_angle_to_center - angle_rad)

        control1 = Point(
            start_vertex.x + flow_distance * math.cos(start_angle_to_center + angle_rad),
            start_vertex.y + flow_distance * math.sin(start_angle_to_center + angle_rad)
        )

        control2 = Point(
            end_vertex.x + flow_distance * math.cos(end_angle_to_center - angle_rad),
            end_vertex.y + flow_distance * math.sin(end_angle_to_center - angle_rad)
        )

        lobes.append({
            'start': start_vertex,
            'control1': control1,
            'control2': control2,
            'end': end_vertex
        })

    return vertices, lobes


def flowangle_final_svg(
    n: int = 3,
    size: float = 300,
    flow: float = 1.05,
    angle: float = 105,
    center: Point = None,
    stroke: str = '#000000',
    stroke_width: float = 8,
    show_reference: bool = True,
    colors: list = None
) -> str:
    """Generate SVG for final flowangle"""
    if center is None:
        center = Point(0, 0)

    vertices, lobes = create_flowangle_final(n, size, flow, angle, center)

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
    # Test with different parameters
    canvas = SVGCanvas(1600, 800)
    canvas.add('<rect width="1600" height="800" fill="#ffffff"/>')

    canvas.add('<text x="800" y="50" font-size="28" font-weight="bold" text-anchor="middle" fill="#333">Flowangle Final - Parameter Test</text>')

    # Test 1: Classic (105° × 1.05)
    canvas.add('<text x="400" y="90" font-size="14" text-anchor="middle" fill="#666">Classic: 105° × 1.05</text>')
    svg1 = flowangle_final_svg(
        n=3,
        size=150,
        flow=1.05,
        angle=105,
        center=Point(400, 450),
        stroke='#000000',
        stroke_width=6
    )
    canvas.add(svg1)

    # Test 2: Winner (60° × 1.5)
    canvas.add('<text x="800" y="90" font-size="14" text-anchor="middle" fill="#666">Winner: 60° × 1.5</text>')
    svg2 = flowangle_final_svg(
        n=3,
        size=150,
        flow=1.5,
        angle=60,
        center=Point(800, 450),
        stroke='#ff6b6b',
        stroke_width=6
    )
    canvas.add(svg2)

    # Test 3: Colored (60° × 1.5)
    canvas.add('<text x="1200" y="90" font-size="14" text-anchor="middle" fill="#666">Colored: 60° × 1.5</text>')
    svg3 = flowangle_final_svg(
        n=3,
        size=150,
        flow=1.5,
        angle=60,
        center=Point(1200, 450),
        stroke_width=6,
        colors=['#ff6b6b', '#4ecdc4', '#45b7d1']
    )
    canvas.add(svg3)

    canvas.save('outputs/flowangle_final_test.svg')
    print("✓ Saved flowangle_final_test.svg")
    print("View at: http://localhost:8000/outputs/flowangle_final_test.svg")
