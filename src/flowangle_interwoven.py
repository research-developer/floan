"""
Interwoven Flowangle - Shows the three separate intersecting paths

This creates the classic triquetra appearance where you can see
the individual paths weaving over and under each other.
"""

from flowangle import create_flowangle
from svg_generator import Point, SVGCanvas


def flowangle_interwoven_svg(
    n: int = 3,
    size: float = 300,
    flow: float = 1.5,
    angle: float = 60,
    center: Point = None,
    colors: list = None,
    stroke_width: float = 20,
    gap_width: float = 5,
    show_all: bool = True
) -> str:
    """
    Generate interwoven flowangle paths that cross over/under each other

    Args:
        n: Number of sides (3 for triquetra)
        size: Radius from center to vertices
        flow: Control handle distance multiplier
        angle: Handle angle offset in degrees
        center: Center point
        colors: List of colors for each path (defaults to RGB for n=3)
        stroke_width: Width of each path
        gap_width: Width of gap for under-crossing effect
        show_all: If True, show all paths; if False, show only outline

    Returns:
        SVG elements as string
    """
    if center is None:
        center = Point(0, 0)

    if colors is None:
        if n == 3:
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
        else:
            # Generate colors for n paths
            colors = [f'hsl({i * 360 / n}, 70%, 60%)' for i in range(n)]

    vertices, segments = create_flowangle(n, size, flow, angle, center)

    svg_parts = []

    # Draw each segment as a separate path
    for i, (seg, color) in enumerate(zip(segments, colors)):
        # Create path for this segment
        path = f'M {seg["start"].x:.2f},{seg["start"].y:.2f} '
        path += f'C {seg["control1"].x:.2f},{seg["control1"].y:.2f} '
        path += f'{seg["control2"].x:.2f},{seg["control2"].y:.2f} '
        path += f'{seg["end"].x:.2f},{seg["end"].y:.2f}'

        # Draw the path with white outline for "gap" effect
        svg_parts.append(f'<path d="{path}" fill="none" stroke="white" stroke-width="{stroke_width + gap_width * 2}" stroke-linecap="round"/>')

        # Draw the colored path on top
        svg_parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>')

    return '\n'.join(svg_parts)


def create_interwoven_examples():
    """Create examples showing interwoven flowangles"""

    # Example 1: Classic 3n-flowangle with interwoven paths
    canvas = SVGCanvas(1000, 1000)
    canvas.add('<rect width="1000" height="1000" fill="#2a2a3a"/>')

    canvas.add('<text x="500" y="60" font-size="32" font-weight="bold" text-anchor="middle" fill="#ffffff">Interwoven 3n-Flowangle</text>')
    canvas.add('<text x="500" y="90" font-size="16" text-anchor="middle" fill="#888888">Separate paths crossing over/under each other</text>')

    svg = flowangle_interwoven_svg(
        n=3,
        size=350,
        flow=1.5,
        angle=60,
        center=Point(500, 550),
        stroke_width=25,
        gap_width=6
    )
    canvas.add(svg)

    canvas.save('outputs/flowangle_interwoven.svg')
    print("✓ Saved flowangle_interwoven.svg")


    # Example 2: Comparison - outline vs interwoven
    canvas2 = SVGCanvas(1400, 700)
    canvas2.add('<rect width="1400" height="700" fill="#1a1a2a"/>')

    canvas2.add('<text x="700" y="50" font-size="28" font-weight="bold" text-anchor="middle" fill="#ffffff">Flowangle: Outline vs Interwoven</text>')

    # Left: Outline (silhouette)
    canvas2.add('<text x="350" y="100" font-size="18" text-anchor="middle" fill="#888888">Outline/Silhouette</text>')

    from flowangle import flowangle_to_svg
    outline_svg = flowangle_to_svg(
        n=3,
        size=250,
        flow=1.5,
        angle=60,
        center=Point(350, 400),
        fill='rgba(255, 107, 107, 0.2)',
        stroke='#ff6b6b',
        stroke_width=4
    )
    canvas2.add(outline_svg)

    # Right: Interwoven paths
    canvas2.add('<text x="1050" y="100" font-size="18" text-anchor="middle" fill="#888888">Interwoven Paths</text>')

    interwoven_svg = flowangle_interwoven_svg(
        n=3,
        size=250,
        flow=1.5,
        angle=60,
        center=Point(1050, 400),
        stroke_width=22,
        gap_width=5
    )
    canvas2.add(interwoven_svg)

    canvas2.save('outputs/flowangle_comparison_styles.svg')
    print("✓ Saved flowangle_comparison_styles.svg")


    # Example 3: Different stroke widths
    canvas3 = SVGCanvas(1600, 600)
    canvas3.add('<rect width="1600" height="600" fill="#f8f8f8"/>')

    canvas3.add('<text x="800" y="50" font-size="24" font-weight="bold" text-anchor="middle" fill="#333">Stroke Width Variations</text>')

    widths = [(10, 3), (15, 4), (20, 5), (25, 6)]
    positions = [300, 600, 900, 1200]

    for (stroke, gap), x in zip(widths, positions):
        canvas3.add(f'<text x="{x}" y="90" font-size="14" text-anchor="middle" fill="#666">width={stroke} gap={gap}</text>')

        svg = flowangle_interwoven_svg(
            n=3,
            size=130,
            flow=1.5,
            angle=60,
            center=Point(x, 350),
            stroke_width=stroke,
            gap_width=gap,
            colors=['#ff6b6b', '#4ecdc4', '#ffd93d']
        )
        canvas3.add(svg)

    canvas3.save('outputs/flowangle_stroke_widths.svg')
    print("✓ Saved flowangle_stroke_widths.svg")


    # Example 4: n-variations with interwoven style
    canvas4 = SVGCanvas(1600, 600)
    canvas4.add('<rect width="1600" height="600" fill="#2a2a3a"/>')

    canvas4.add('<text x="800" y="50" font-size="24" font-weight="bold" text-anchor="middle" fill="#ffffff">Interwoven n-Flowangles</text>')

    n_values = [3, 4, 5, 6, 8]
    x_positions = [250, 500, 750, 1000, 1250]

    for n, x in zip(n_values, x_positions):
        canvas4.add(f'<text x="{x}" y="90" font-size="14" text-anchor="middle" fill="#888888">{n}n-Flowangle</text>')

        # Generate n colors
        colors = [f'hsl({i * 360 / n}, 70%, 60%)' for i in range(n)]

        svg = flowangle_interwoven_svg(
            n=n,
            size=110,
            flow=1.5,
            angle=60,
            center=Point(x, 350),
            stroke_width=18,
            gap_width=4,
            colors=colors
        )
        canvas4.add(svg)

    canvas4.save('outputs/flowangle_interwoven_n_variations.svg')
    print("✓ Saved flowangle_interwoven_n_variations.svg")


if __name__ == '__main__':
    print("Generating interwoven flowangle examples...\n")
    create_interwoven_examples()
    print("\n✓ All interwoven examples generated!")
    print("\nView them at:")
    print("  http://localhost:8000/outputs/flowangle_interwoven.svg")
    print("  http://localhost:8000/outputs/flowangle_comparison_styles.svg")
    print("  http://localhost:8000/outputs/flowangle_stroke_widths.svg")
    print("  http://localhost:8000/outputs/flowangle_interwoven_n_variations.svg")
