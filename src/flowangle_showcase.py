"""
Flowangle Showcase - Generate beautiful examples of flowangles
"""

from flowangle import create_flowangle, flowangle_to_svg
from svg_generator import Point, SVGCanvas


def create_showcase():
    """Create a showcase of beautiful flowangle configurations"""

    canvas = SVGCanvas(1600, 1200)
    canvas.add('<rect width="1600" height="1200" fill="#1a1a1a"/>')

    # Winner: 60° @ 1.5 flow
    canvas.add('<text x="800" y="60" font-size="32" font-weight="bold" text-anchor="middle" fill="#ffffff">3n-Flowangle Showcase</text>')
    canvas.add('<text x="800" y="95" font-size="16" text-anchor="middle" fill="#888888">Exploring the triquetra-like flowangle space</text>')

    # Layout: 3 columns x 2 rows
    configs = [
        {'name': 'Winner: 60° × 1.5', 'angle': 60, 'flow': 1.5, 'color': '#00ffcc'},
        {'name': 'Classic Triquetra', 'angle': 105, 'flow': 1.05, 'color': '#ff6b6b'},
        {'name': 'Sharp Points', 'angle': 135, 'flow': 1.5, 'color': '#4ecdc4'},
        {'name': 'Soft Curves', 'angle': 75, 'flow': 0.75, 'color': '#ffd93d'},
        {'name': 'Bold Flow', 'angle': 90, 'flow': 1.25, 'color': '#a78bfa'},
        {'name': 'Geometric', 'angle': 120, 'flow': 1.0, 'color': '#fb923c'},
    ]

    positions = [
        (400, 400), (800, 400), (1200, 400),
        (400, 850), (800, 850), (1200, 850),
    ]

    for config, pos in zip(configs, positions):
        center = Point(pos[0], pos[1])

        # Draw flowangle
        svg = flowangle_to_svg(
            n=3,
            size=180,
            flow=config['flow'],
            angle=config['angle'],
            center=center,
            fill=f'{config["color"]}22',
            stroke=config['color'],
            stroke_width=3
        )
        canvas.add(svg)

        # Draw label
        canvas.add(f'<text x="{pos[0]}" y="{pos[1] + 250}" font-size="14" font-weight="bold" text-anchor="middle" fill="#ffffff">{config["name"]}</text>')
        canvas.add(f'<text x="{pos[0]}" y="{pos[1] + 270}" font-size="12" text-anchor="middle" fill="#888888">angle={config["angle"]}° flow={config["flow"]}</text>')

    canvas.save('outputs/flowangle_showcase.svg')
    print("✓ Saved flowangle_showcase.svg")


def create_winner_highres():
    """Create high-resolution render of the winning configuration"""

    canvas = SVGCanvas(1200, 1200)

    # Gradient background
    canvas.add('''
    <defs>
        <radialGradient id="bg">
            <stop offset="0%" style="stop-color:#2a2a3a;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#1a1a2a;stop-opacity:1" />
        </radialGradient>
    </defs>
    ''')
    canvas.add('<rect width="1200" height="1200" fill="url(#bg)"/>')

    # Title
    canvas.add('<text x="600" y="80" font-size="36" font-weight="bold" text-anchor="middle" fill="#ffffff">Winner Flowangle</text>')
    canvas.add('<text x="600" y="115" font-size="18" text-anchor="middle" fill="#00ffcc">60° angle × 1.5 flow</text>')

    # Main flowangle - large
    center = Point(600, 600)
    svg = flowangle_to_svg(
        n=3,
        size=450,
        flow=1.5,
        angle=60,
        center=center,
        fill='rgba(0, 255, 204, 0.05)',
        stroke='#00ffcc',
        stroke_width=6
    )
    canvas.add(svg)

    # Add subtle glow effect
    canvas.add(f'''
    <circle cx="{center.x}" cy="{center.y}" r="500" fill="none" stroke="#00ffcc" stroke-width="1" opacity="0.1"/>
    <circle cx="{center.x}" cy="{center.y}" r="520" fill="none" stroke="#00ffcc" stroke-width="1" opacity="0.05"/>
    ''')

    # Stats
    canvas.add('<text x="600" y="1100" font-size="14" text-anchor="middle" fill="#888888">Perfectly balanced triquetra-like form</text>')
    canvas.add('<text x="600" y="1120" font-size="14" text-anchor="middle" fill="#888888">Smooth curves with elegant proportions</text>')

    canvas.save('outputs/flowangle_winner.svg')
    print("✓ Saved flowangle_winner.svg")


def create_n_variations():
    """Create variations with different numbers of sides"""

    canvas = SVGCanvas(1600, 600)
    canvas.add('<rect width="1600" height="600" fill="#f8f8f8"/>')

    canvas.add('<text x="800" y="50" font-size="28" font-weight="bold" text-anchor="middle" fill="#333">n-Flowangle Variations</text>')
    canvas.add('<text x="800" y="75" font-size="14" text-anchor="middle" fill="#666">Same parameters (60° × 1.5), different n values</text>')

    n_values = [3, 4, 5, 6, 8]
    x_positions = [200, 450, 700, 950, 1200]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']

    for n, x, color in zip(n_values, x_positions, colors):
        center = Point(x, 350)

        svg = flowangle_to_svg(
            n=n,
            size=120,
            flow=1.5,
            angle=60,
            center=center,
            fill=f'{color}22',
            stroke=color,
            stroke_width=3
        )
        canvas.add(svg)

        canvas.add(f'<text x="{x}" y="520" font-size="18" font-weight="bold" text-anchor="middle" fill="#333">{n}n-Flowangle</text>')

    canvas.save('outputs/flowangle_n_variations.svg')
    print("✓ Saved flowangle_n_variations.svg")


if __name__ == '__main__':
    print("Generating flowangle showcase images...\n")
    create_showcase()
    create_winner_highres()
    create_n_variations()
    print("\n✓ All showcase images generated!")
    print("\nView them at:")
    print("  http://localhost:8000/outputs/flowangle_showcase.svg")
    print("  http://localhost:8000/outputs/flowangle_winner.svg")
    print("  http://localhost:8000/outputs/flowangle_n_variations.svg")
