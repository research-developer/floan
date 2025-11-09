"""
Flowangle Research - Parameterizing and normalizing the flowangle shape

A flowangle is a triquetra-like shape with:
- A base polygon (triangle for 3n-flowangle)
- Curved paths connecting vertices with bezier curves
- Two key parameters:
  - flow: radius of bezier control handles from anchor points
  - angle: angle of handles relative to canvas center
"""

import math
from svg_generator import Point, SVGCanvas

# Hand-graphed 3n-flowangle data
HAND_GRAPHED = {
    'polygon': [
        Point(973.68, 45.95),    # Top
        Point(473.68, 911.98),   # Bottom-left
        Point(1473.68, 911.98),  # Bottom-right
    ],
    'path': 'M1473.68,911.98C1045.94,1339.72,493.98,45.95,973.68,45.95s-94.06,1271.96-500,866.03c-405.94-405.94,1427.75-427.75,1000,0Z'
}


def analyze_triangle():
    """Analyze the base triangle to find center and key measurements"""
    points = HAND_GRAPHED['polygon']

    # Calculate centroid (center)
    cx = sum(p.x for p in points) / len(points)
    cy = sum(p.y for p in points) / len(points)
    center = Point(cx, cy)

    # Calculate distances from center to each vertex
    distances = [math.sqrt((p.x - cx)**2 + (p.y - cy)**2) for p in points]

    # Calculate angles from center to each vertex
    angles = [math.atan2(p.y - cy, p.x - cx) for p in points]

    print("=== Base Triangle Analysis ===")
    print(f"Center: ({cx:.2f}, {cy:.2f})")
    print(f"\nVertices:")
    for i, (p, d, a) in enumerate(zip(points, distances, angles)):
        print(f"  V{i}: ({p.x:.2f}, {p.y:.2f}) - dist={d:.2f}, angle={math.degrees(a):.2f}°")

    # Calculate side lengths
    side_lengths = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        length = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
        side_lengths.append(length)

    print(f"\nSide lengths:")
    for i, length in enumerate(side_lengths):
        print(f"  Side {i}: {length:.2f}")

    return center, points, distances, angles


def parse_path_data():
    """Parse the SVG path data to extract bezier control points"""
    path = HAND_GRAPHED['path']

    # Manual parsing of the hand-graphed path
    # M1473.68,911.98 - Move to bottom-right vertex
    # C1045.94,1339.72,493.98,45.95,973.68,45.95 - Cubic bezier to top vertex
    # s-94.06,1271.96,-500,866.03 - Smooth cubic (relative)
    # c-405.94,-405.94,1427.75,-427.75,1000,0 - Cubic bezier (relative)
    # Z - Close path

    print("\n=== Path Decomposition ===")
    print("Segment 1: Bottom-right → Top")
    print("  Start: (1473.68, 911.98)")
    print("  Control 1: (1045.94, 1339.72)")
    print("  Control 2: (493.98, 45.95)")
    print("  End: (973.68, 45.95)")

    # For 's' command, first control point is reflection of previous second control
    # Previous second control: (493.98, 45.95)
    # End of previous: (973.68, 45.95)
    # Reflected control: (973.68 + (973.68 - 493.98), 45.95 + (45.95 - 45.95))
    #                   = (1453.38, 45.95)

    print("\nSegment 2: Top → Bottom-left (smooth cubic)")
    print("  Start: (973.68, 45.95)")
    print("  Control 1 (reflected): (1453.38, 45.95)")
    print("  Control 2 (relative): (973.68 - 94.06, 45.95 + 1271.96) = (879.62, 1317.91)")
    print("  End (relative): (973.68 - 500, 45.95 + 866.03) = (473.68, 911.98)")

    # For 'c' command (relative cubic)
    print("\nSegment 3: Bottom-left → Bottom-right (relative cubic)")
    print("  Start: (473.68, 911.98)")
    print("  Control 1 (relative): (473.68 - 405.94, 911.98 - 405.94) = (67.74, 506.04)")
    print("  Control 2 (relative): (473.68 + 1427.75, 911.98 - 427.75) = (1901.43, 484.23)")
    print("  End (relative): (473.68 + 1000, 911.98 + 0) = (1473.68, 911.98)")

    # Return structured data
    segments = [
        {
            'start': Point(1473.68, 911.98),
            'control1': Point(1045.94, 1339.72),
            'control2': Point(493.98, 45.95),
            'end': Point(973.68, 45.95),
        },
        {
            'start': Point(973.68, 45.95),
            'control1': Point(1453.38, 45.95),
            'control2': Point(879.62, 1317.91),
            'end': Point(473.68, 911.98),
        },
        {
            'start': Point(473.68, 911.98),
            'control1': Point(67.74, 506.04),
            'control2': Point(1901.43, 484.23),
            'end': Point(1473.68, 911.98),
        }
    ]

    return segments


def calculate_flow_angle_parameters(center, segments):
    """
    Calculate 'flow' and 'angle' parameters for each control point

    flow: distance from anchor point to control point (normalized by segment length)
    angle: angle of control handle relative to center-to-anchor direction
    """
    print("\n=== Flow & Angle Parameters ===")

    for i, seg in enumerate(segments):
        print(f"\nSegment {i}:")

        # Analyze control point 1
        anchor = seg['start']
        control = seg['control1']

        # Flow: distance from anchor to control
        flow_dist = math.sqrt((control.x - anchor.x)**2 + (control.y - anchor.y)**2)

        # Angle of control relative to anchor
        control_angle = math.atan2(control.y - anchor.y, control.x - anchor.x)

        # Angle from center to anchor (for reference)
        center_to_anchor_angle = math.atan2(anchor.y - center.y, anchor.x - center.x)

        # Relative angle (control handle angle relative to center-anchor line)
        relative_angle = control_angle - center_to_anchor_angle

        print(f"  Control 1:")
        print(f"    Anchor: ({anchor.x:.2f}, {anchor.y:.2f})")
        print(f"    Control: ({control.x:.2f}, {control.y:.2f})")
        print(f"    Flow distance: {flow_dist:.2f}")
        print(f"    Control angle: {math.degrees(control_angle):.2f}°")
        print(f"    Center→Anchor angle: {math.degrees(center_to_anchor_angle):.2f}°")
        print(f"    Relative angle: {math.degrees(relative_angle):.2f}°")

        # Analyze control point 2
        control2 = seg['control2']
        end = seg['end']

        flow_dist2 = math.sqrt((control2.x - end.x)**2 + (control2.y - end.y)**2)
        control_angle2 = math.atan2(control2.y - end.y, control2.x - end.x)
        center_to_end_angle = math.atan2(end.y - center.y, end.x - center.x)
        relative_angle2 = control_angle2 - center_to_end_angle

        print(f"  Control 2:")
        print(f"    Anchor: ({end.x:.2f}, {end.y:.2f})")
        print(f"    Control: ({control2.x:.2f}, {control2.y:.2f})")
        print(f"    Flow distance: {flow_dist2:.2f}")
        print(f"    Control angle: {math.degrees(control_angle2):.2f}°")
        print(f"    Center→Anchor angle: {math.degrees(center_to_end_angle):.2f}°")
        print(f"    Relative angle: {math.degrees(relative_angle2):.2f}°")


def visualize_decomposition(center, segments):
    """Create a visualization showing the decomposition"""
    canvas = SVGCanvas(2000, 1400)

    # Draw center point
    canvas.add(f'<circle cx="{center.x}" cy="{center.y}" r="5" fill="red"/>')

    # Draw base triangle
    triangle_points = HAND_GRAPHED['polygon']
    points_str = ' '.join([f"{p.x},{p.y}" for p in triangle_points])
    canvas.add(f'<polygon points="{points_str}" fill="none" stroke="#888888" stroke-width="2"/>')

    # Draw each segment with different colors
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

    for i, seg in enumerate(segments):
        # Draw bezier curve
        path = f"M {seg['start'].x},{seg['start'].y} "
        path += f"C {seg['control1'].x},{seg['control1'].y} "
        path += f"{seg['control2'].x},{seg['control2'].y} "
        path += f"{seg['end'].x},{seg['end'].y}"

        canvas.add(f'<path d="{path}" fill="none" stroke="{colors[i]}" stroke-width="3"/>')

        # Draw control points
        canvas.add(f'<circle cx="{seg["control1"].x}" cy="{seg["control1"].y}" r="8" fill="{colors[i]}" opacity="0.7"/>')
        canvas.add(f'<circle cx="{seg["control2"].x}" cy="{seg["control2"].y}" r="8" fill="{colors[i]}" opacity="0.7"/>')

        # Draw control lines (from anchor to control)
        canvas.add(f'<line x1="{seg["start"].x}" y1="{seg["start"].y}" x2="{seg["control1"].x}" y2="{seg["control1"].y}" stroke="{colors[i]}" stroke-width="1" opacity="0.5"/>')
        canvas.add(f'<line x1="{seg["end"].x}" y1="{seg["end"].y}" x2="{seg["control2"].x}" y2="{seg["control2"].y}" stroke="{colors[i]}" stroke-width="1" opacity="0.5"/>')

        # Draw lines from center to vertices
        canvas.add(f'<line x1="{center.x}" y1="{center.y}" x2="{seg["start"].x}" y2="{seg["start"].y}" stroke="#CCCCCC" stroke-width="1" opacity="0.3"/>')

    return canvas


if __name__ == '__main__':
    print("Flowangle Decomposition and Analysis\n")

    # Step 1: Analyze base triangle
    center, vertices, distances, angles = analyze_triangle()

    # Step 2: Parse and decompose path
    segments = parse_path_data()

    # Step 3: Calculate flow and angle parameters
    calculate_flow_angle_parameters(center, segments)

    # Step 4: Create visualization
    canvas = visualize_decomposition(center, segments)
    canvas.save('outputs/flowangle_decomposition.svg')
    print("\n✓ Visualization saved to outputs/flowangle_decomposition.svg")
