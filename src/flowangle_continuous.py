"""
Continuous Flowangle - A single smooth path tracing through all vertices

Creates one continuous flowing path that connects all vertices in a smooth,
traceable curve (like drawing without lifting your pen).
"""

import math
from svg_generator import Point, SVGCanvas
from flowangle import create_flowangle


def create_continuous_flowangle_path(
    n: int = 3,
    size: float = 300,
    flow: float = 1.5,
    angle: float = 60,
    center: Point = None
) -> str:
    """
    Create a continuous path that flows through all n vertices

    Instead of n separate bezier segments, this creates one smooth
    continuous path that you could trace with your finger.

    Args:
        n: Number of vertices (3 for triquetra-like)
        size: Radius from center to vertices
        flow: Control handle distance multiplier
        angle: Handle angle offset in degrees
        center: Center point

    Returns:
        SVG path string (single continuous path)
    """
    if center is None:
        center = Point(0, 0)

    vertices, segments = create_flowangle(n, size, flow, angle, center)

    # Build one continuous path through all segments
    path = f'M {segments[0]["start"].x:.2f},{segments[0]["start"].y:.2f} '

    for seg in segments:
        # Add cubic bezier curve to next vertex
        path += f'C {seg["control1"].x:.2f},{seg["control1"].y:.2f} '
        path += f'{seg["control2"].x:.2f},{seg["control2"].y:.2f} '
        path += f'{seg["end"].x:.2f},{seg["end"].y:.2f} '

    # Close the path to make it continuous
    path += 'Z'

    return path


def flowangle_continuous_svg(
    n: int = 3,
    size: float = 300,
    flow: float = 1.5,
    angle: float = 60,
    center: Point = None,
    stroke: str = '#00ffcc',
    stroke_width: float = 3,
    fill: str = 'none',
    show_reference_polygon: bool = True
) -> str:
    """
    Generate SVG for a continuous flowangle with optional reference polygon

    Args:
        n: Number of vertices
        size: Radius from center to vertices
        flow: Control handle distance multiplier
        angle: Handle angle offset in degrees
        center: Center point
        stroke: Stroke color for the flowangle path
        stroke_width: Width of the stroke
        fill: Fill color (default 'none' for just the path)
        show_reference_polygon: If True, show faded background polygon

    Returns:
        SVG elements as string
    """
    if center is None:
        center = Point(0, 0)

    svg_parts = []

    # Get the vertices for reference polygon
    vertices, segments = create_flowangle(n, size, flow, angle, center)

    # Draw reference polygon (faded)
    if show_reference_polygon:
        polygon_points = ' '.join([f'{v.x:.2f},{v.y:.2f}' for v in vertices])
        svg_parts.append(
            f'<polygon points="{polygon_points}" '
            f'fill="rgba(255, 255, 255, 0.05)" '
            f'stroke="rgba(255, 255, 255, 0.2)" '
            f'stroke-width="1"/>'
        )

    # Draw the continuous flowangle path
    path = create_continuous_flowangle_path(n, size, flow, angle, center)
    svg_parts.append(
        f'<path d="{path}" '
        f'fill="{fill}" '
        f'stroke="{stroke}" '
        f'stroke-width="{stroke_width}" '
        f'stroke-linejoin="round" '
        f'stroke-linecap="round"/>'
    )

    return '\n'.join(svg_parts)


def create_continuous_examples():
    """Create examples of continuous flowangles"""

    # Example 1: Basic 3n-flowangle with reference polygon
    canvas = SVGCanvas(1000, 1000)
    canvas.add('<rect width="1000" height="1000" fill="#1a1a2a"/>')

    canvas.add('<text x="500" y="60" font-size="32" font-weight="bold" text-anchor="middle" fill="#ffffff">Continuous 3n-Flowangle</text>')
    canvas.add('<text x="500" y="90" font-size="16" text-anchor="middle" fill="#888888">Single smooth traceable path through all vertices</text>')

    svg = flowangle_continuous_svg(
        n=3,
        size=350,
        flow=1.5,
        angle=60,
        center=Point(500, 550),
        stroke='#00ffcc',
        stroke_width=4,
        show_reference_polygon=True
    )
    canvas.add(svg)

    canvas.save('outputs/flowangle_continuous.svg')
    print("✓ Saved flowangle_continuous.svg")


    # Example 2: Different stroke widths
    canvas2 = SVGCanvas(1600, 600)
    canvas2.add('<rect width="1600" height="600" fill="#2a2a3a"/>')

    canvas2.add('<text x="800" y="50" font-size="24" font-weight="bold" text-anchor="middle" fill="#ffffff">Continuous Flowangle - Stroke Width Variations</text>')

    widths = [2, 4, 6, 8]
    positions = [300, 600, 900, 1200]
    colors = ['#ff6b6b', '#4ecdc4', '#ffd93d', '#a78bfa']

    for width, x, color in zip(widths, positions, colors):
        canvas2.add(f'<text x="{x}" y="90" font-size="14" text-anchor="middle" fill="#888888">width={width}</text>')

        svg = flowangle_continuous_svg(
            n=3,
            size=130,
            flow=1.5,
            angle=60,
            center=Point(x, 350),
            stroke=color,
            stroke_width=width,
            show_reference_polygon=True
        )
        canvas2.add(svg)

    canvas2.save('outputs/flowangle_continuous_widths.svg')
    print("✓ Saved flowangle_continuous_widths.svg")


    # Example 3: Filled vs outline
    canvas3 = SVGCanvas(1400, 700)
    canvas3.add('<rect width="1400" height="700" fill="#f8f8f8"/>')

    canvas3.add('<text x="700" y="50" font-size="24" font-weight="bold" text-anchor="middle" fill="#333">Continuous Flowangle - Fill vs Outline</text>')

    # Left: Outline only
    canvas3.add('<text x="350" y="90" font-size="16" text-anchor="middle" fill="#666">Outline Only</text>')
    svg_outline = flowangle_continuous_svg(
        n=3,
        size=230,
        flow=1.5,
        angle=60,
        center=Point(350, 400),
        stroke='#0066ff',
        stroke_width=4,
        fill='none',
        show_reference_polygon=True
    )
    canvas3.add(svg_outline)

    # Right: Filled
    canvas3.add('<text x="1050" y="90" font-size="16" text-anchor="middle" fill="#666">Filled</text>')
    svg_filled = flowangle_continuous_svg(
        n=3,
        size=230,
        flow=1.5,
        angle=60,
        center=Point(1050, 400),
        stroke='#0066ff',
        stroke_width=3,
        fill='rgba(102, 153, 255, 0.3)',
        show_reference_polygon=True
    )
    canvas3.add(svg_filled)

    canvas3.save('outputs/flowangle_continuous_fill.svg')
    print("✓ Saved flowangle_continuous_fill.svg")


    # Example 4: Parameter variations (flow and angle)
    canvas4 = SVGCanvas(1600, 1200)
    canvas4.add('<rect width="1600" height="1200" fill="#1a1a2a"/>')

    canvas4.add('<text x="800" y="50" font-size="24" font-weight="bold" text-anchor="middle" fill="#ffffff">Continuous Flowangle Parameter Exploration</text>')

    # Grid of variations
    flow_values = [0.75, 1.0, 1.25, 1.5]
    angle_values = [60, 75, 90]

    y_start = 150
    x_start = 250

    canvas4.add('<text x="100" y="200" font-size="14" font-weight="bold" text-anchor="middle" fill="#888888">Flow →</text>')

    for i, flow in enumerate(flow_values):
        x = x_start + i * 350
        canvas4.add(f'<text x="{x}" y="120" font-size="14" text-anchor="middle" fill="#888888">{flow}</text>')

    canvas4.add('<text x="100" y="400" font-size="14" font-weight="bold" text-anchor="middle" fill="#888888" transform="rotate(-90, 100, 400)">Angle →</text>')

    for j, angle in enumerate(angle_values):
        y = y_start + 100 + j * 350
        canvas4.add(f'<text x="150" y="{y}" font-size="14" text-anchor="middle" fill="#888888">{angle}°</text>')

    colors = ['#ff6b6b', '#4ecdc4', '#ffd93d']

    for i, flow in enumerate(flow_values):
        for j, angle in enumerate(angle_values):
            x = x_start + i * 350
            y = y_start + 100 + j * 350

            svg = flowangle_continuous_svg(
                n=3,
                size=120,
                flow=flow,
                angle=angle,
                center=Point(x, y),
                stroke=colors[j],
                stroke_width=3,
                show_reference_polygon=True
            )
            canvas4.add(svg)

    canvas4.save('outputs/flowangle_continuous_params.svg')
    print("✓ Saved flowangle_continuous_params.svg")


    # Example 5: Large high-quality render
    canvas5 = SVGCanvas(1200, 1200)

    # Gradient background
    canvas5.add('''
    <defs>
        <radialGradient id="bg2">
            <stop offset="0%" style="stop-color:#2a2a3a;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#1a1a2a;stop-opacity:1" />
        </radialGradient>
    </defs>
    ''')
    canvas5.add('<rect width="1200" height="1200" fill="url(#bg2)"/>')

    canvas5.add('<text x="600" y="80" font-size="36" font-weight="bold" text-anchor="middle" fill="#ffffff">3n-Flowangle</text>')
    canvas5.add('<text x="600" y="115" font-size="18" text-anchor="middle" fill="#00ffcc">Continuous Path • 60° × 1.5</text>')

    # Large flowangle
    svg = flowangle_continuous_svg(
        n=3,
        size=450,
        flow=1.5,
        angle=60,
        center=Point(600, 650),
        stroke='#00ffcc',
        stroke_width=5,
        fill='rgba(0, 255, 204, 0.05)',
        show_reference_polygon=True
    )
    canvas5.add(svg)

    # Subtle glow
    canvas5.add(f'<circle cx="600" cy="650" r="500" fill="none" stroke="#00ffcc" stroke-width="1" opacity="0.1"/>')

    canvas5.save('outputs/flowangle_continuous_hero.svg')
    print("✓ Saved flowangle_continuous_hero.svg")


if __name__ == '__main__':
    print("Generating continuous flowangle examples...\n")
    create_continuous_examples()
    print("\n✓ All continuous examples generated!")
    print("\nView them at:")
    print("  http://localhost:8000/outputs/flowangle_continuous.svg")
    print("  http://localhost:8000/outputs/flowangle_continuous_widths.svg")
    print("  http://localhost:8000/outputs/flowangle_continuous_fill.svg")
    print("  http://localhost:8000/outputs/flowangle_continuous_params.svg")
    print("  http://localhost:8000/outputs/flowangle_continuous_hero.svg")
