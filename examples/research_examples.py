"""
Research-Oriented Examples
Demonstrations for tensor visualizations, harmonic relationships, and multi-dimensional projections
"""
import os
import sys
import math

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from svg_generator import *

def harmonic_circle_projection(canvas: SVGCanvas, center: Point, base_radius: float, 
                               harmonics: List[int], amplitude: float = 20):
    """
    Project harmonic relationships onto a circle.
    Useful for visualizing musical intervals or frequency relationships.
    
    Args:
        harmonics: List of harmonic numbers (e.g., [1, 2, 3, 5, 8, 13] for Fibonacci)
    """
    # Base circle
    canvas.circle(center, base_radius, fill="none", stroke="#333", stroke_width=1)
    
    # Draw harmonics
    for i, h in enumerate(harmonics):
        # Position along circle
        angle = (2 * math.pi * i) / len(harmonics)
        
        # Modulated radius based on harmonic number
        r = base_radius + amplitude * math.log(h + 1)
        
        point = Point(
            center.x + r * math.cos(angle),
            center.y + r * math.sin(angle)
        )
        
        # Color by harmonic ratio
        hue = (360 * math.log(h + 1) / math.log(max(harmonics) + 1))
        canvas.circle(point, 8, fill=f"hsl({hue}, 70%, 60%)", stroke="black", stroke_width=1)
        
        # Draw connecting line
        edge_point = Point(
            center.x + base_radius * math.cos(angle),
            center.y + base_radius * math.sin(angle)
        )
        canvas.line(edge_point, point, stroke=f"hsl({hue}, 70%, 50%)", stroke_width=2)
        
        # Draw connections between related harmonics (octaves, fifths, etc.)
        for j, h2 in enumerate(harmonics[i+1:], i+1):
            # Check for harmonic relationship
            ratio = h2 / h if h != 0 else 0
            
            # Draw connections for simple ratios (octave, fifth, fourth)
            if ratio in [2, 1.5, 1.333, 3/2, 4/3]:
                angle2 = (2 * math.pi * j) / len(harmonics)
                r2 = base_radius + amplitude * math.log(h2 + 1)
                point2 = Point(
                    center.x + r2 * math.cos(angle2),
                    center.y + r2 * math.sin(angle2)
                )
                opacity = 0.3 if ratio == 2 else 0.15
                canvas.add(f'<line x1="{point.x}" y1="{point.y}" x2="{point2.x}" y2="{point2.y}" '
                          f'stroke="#888" stroke-width="1" opacity="{opacity}"/>')

def manifold_projection_2d(canvas: SVGCanvas, center: Point, size: float, 
                          dimensions: List[Tuple[float, float]]):
    """
    Project multi-dimensional tensor data onto 2D using radial layout.
    Each dimension becomes a spoke on a radial plot.
    
    Args:
        dimensions: List of (value, max_value) tuples for each dimension
    """
    n = len(dimensions)
    angle_step = (2 * math.pi) / n
    
    # Draw reference circles
    for r in [0.25, 0.5, 0.75, 1.0]:
        canvas.circle(center, size * r, fill="none", stroke="#ddd", stroke_width=1)
    
    # Draw dimension spokes and plot values
    points = []
    for i, (value, max_val) in enumerate(dimensions):
        angle = i * angle_step - math.pi / 2  # Start at top
        
        # Normalize value
        normalized = (value / max_val) if max_val > 0 else 0
        r = size * normalized
        
        point = Point(
            center.x + r * math.cos(angle),
            center.y + r * math.sin(angle)
        )
        points.append(point)
        
        # Draw spoke
        end = Point(
            center.x + size * math.cos(angle),
            center.y + size * math.sin(angle)
        )
        canvas.line(center, end, stroke="#ccc", stroke_width=1)
        
        # Label (optional)
        label_pos = Point(
            center.x + (size * 1.15) * math.cos(angle),
            center.y + (size * 1.15) * math.sin(angle)
        )
        canvas.circle(label_pos, 3, fill="#666")
    
    # Connect the points to form the projection shape
    canvas.polygon(points, fill="rgba(100, 150, 255, 0.3)", 
                  stroke="#4a90e2", stroke_width=2)
    
    # Mark individual data points
    for point in points:
        canvas.circle(point, 4, fill="#4a90e2", stroke="white", stroke_width=1)

def recursive_tensor_subdivision(canvas: SVGCanvas, p1: Point, p2: Point, p3: Point,
                                depth: int, factor: int = 3):
    """
    Recursive subdivision inspired by tensor decomposition.
    Each triangle subdivides into smaller triangles based on a factorization.
    
    Args:
        factor: Subdivision factor (e.g., 3 for dividing into 9 parts)
    """
    if depth == 0:
        # Base case: draw the triangle
        hue = depth * 40
        canvas.polygon([p1, p2, p3], 
                      fill=f"hsl({hue}, 70%, {60 + depth * 5}%)", 
                      stroke="black", stroke_width=0.5)
        return
    
    # Calculate subdivision points along each edge
    def interpolate_points(start: Point, end: Point, n: int) -> List[Point]:
        return [Point(
            start.x + (end.x - start.x) * i / n,
            start.y + (end.y - start.y) * i / n
        ) for i in range(n + 1)]
    
    # Get points along each edge
    edge1 = interpolate_points(p1, p2, factor)
    edge2 = interpolate_points(p2, p3, factor)
    edge3 = interpolate_points(p3, p1, factor)
    
    # Create grid of triangles
    # Simplified: just subdivide into corner and center triangles
    mid12 = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)
    mid23 = Point((p2.x + p3.x)/2, (p2.y + p3.y)/2)
    mid31 = Point((p3.x + p1.x)/2, (p3.y + p1.y)/2)
    
    # Recurse on smaller triangles
    recursive_tensor_subdivision(canvas, p1, mid12, mid31, depth - 1, factor)
    recursive_tensor_subdivision(canvas, mid12, p2, mid23, depth - 1, factor)
    recursive_tensor_subdivision(canvas, mid31, mid23, p3, depth - 1, factor)
    recursive_tensor_subdivision(canvas, mid12, mid23, mid31, depth - 1, factor)

def semantic_alphabet_kernel(canvas: SVGCanvas, center: Point, radius: float,
                            letters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """
    Visualize alphabetic structure with semantic operations.
    Places letters on a circle and draws connections based on position relationships.
    
    Inspired by alphabet kernel theory - each letter is a node with structural relationships.
    """
    n = len(letters)
    angle_step = (2 * math.pi) / n
    
    # Draw main circle
    canvas.circle(center, radius, fill="none", stroke="#333", stroke_width=2)
    
    letter_positions = {}
    
    for i, letter in enumerate(letters):
        angle = i * angle_step - math.pi / 2  # Start at top (A at 12 o'clock)
        
        pos = Point(
            center.x + radius * math.cos(angle),
            center.y + radius * math.sin(angle)
        )
        letter_positions[letter] = (pos, i)
        
        # Draw letter position
        hue = (i / n) * 360
        canvas.circle(pos, 12, fill=f"hsl({hue}, 70%, 60%)", stroke="black", stroke_width=1)
    
    # Draw semantic relationships
    # Example: vowels form inner pentagon
    vowels = "AEIOU"
    vowel_points = [letter_positions[v][0] for v in vowels if v in letter_positions]
    if len(vowel_points) >= 3:
        canvas.polygon(vowel_points, fill="rgba(255, 100, 100, 0.2)", 
                      stroke="#e24a90", stroke_width=2)
    
    # Draw connections for letter pairs with specific relationships
    # Example: pairs that differ by a fixed interval
    for i, l1 in enumerate(letters):
        # Connect to letter 13 positions away (opposite on circle - complementary)
        opposite_idx = (i + n // 2) % n
        l2 = letters[opposite_idx]
        
        p1 = letter_positions[l1][0]
        p2 = letter_positions[l2][0]
        
        canvas.add(f'<line x1="{p1.x}" y1="{p1.y}" x2="{p2.x}" y2="{p2.y}" '
                  f'stroke="#ccc" stroke-width="0.5" opacity="0.3"/>')

def fibonacci_spiral_manifold(canvas: SVGCanvas, start: Point, size: float, iterations: int):
    """
    Fibonacci spiral with manifold projection overlay.
    Demonstrates self-similar scaling and golden ratio relationships.
    """
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    current_pos = start
    current_size = size
    angle = 0
    
    points = [current_pos]
    
    for i in range(iterations):
        # Color based on iteration
        hue = (i * 30) % 360
        
        # Draw square
        square_points = [
            current_pos,
            Point(current_pos.x + current_size, current_pos.y),
            Point(current_pos.x + current_size, current_pos.y + current_size),
            Point(current_pos.x, current_pos.y + current_size)
        ]
        canvas.polygon(square_points, fill=f"hsl({hue}, 60%, 70%)", 
                      stroke="black", stroke_width=1.5)
        
        # Draw quarter-circle arc in the square
        arc_center = square_points[2]  # Bottom-right corner
        canvas.circle(arc_center, current_size, fill="none", 
                     stroke=f"hsl({hue}, 80%, 40%)", stroke_width=2)
        
        # Track center points for manifold projection
        center = Point(current_pos.x + current_size/2, current_pos.y + current_size/2)
        points.append(center)
        
        # Move to next position (spiral outward)
        if i % 4 == 0:
            current_pos = Point(current_pos.x, current_pos.y - current_size)
        elif i % 4 == 1:
            current_pos = Point(current_pos.x + current_size, current_pos.y)
        elif i % 4 == 2:
            current_pos = Point(current_pos.x, current_pos.y + current_size)
        else:
            current_pos = Point(current_pos.x - current_size, current_pos.y)
        
        current_size = current_size / phi
    
    # Draw manifold overlay connecting centers
    for i in range(len(points) - 1):
        canvas.line(points[i], points[i+1], stroke="rgba(255, 0, 0, 0.5)", stroke_width=2)

# ============ GENERATE EXAMPLES ============

if __name__ == "__main__":
    # Set up output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    # Example 1: Harmonic Circle
    canvas1 = SVGCanvas(800, 800)
    # Musical intervals: fundamental, octave, fifth, fourth, major third, minor third
    harmonics = [1, 2, 3, 4, 5, 6, 8, 9, 12, 16]
    harmonic_circle_projection(canvas1, Point(400, 400), 150, harmonics, amplitude=30)
    canvas1.save(os.path.join(output_dir, 'harmonic_circle.svg'))
    
    # Example 2: Manifold Projection
    canvas2 = SVGCanvas(800, 800)
    # Example tensor data: 8 dimensions with random-ish values
    dimensions = [(0.8, 1.0), (0.6, 1.0), (0.9, 1.0), (0.4, 1.0),
                  (0.7, 1.0), (0.5, 1.0), (0.85, 1.0), (0.3, 1.0)]
    manifold_projection_2d(canvas2, Point(400, 400), 300, dimensions)
    canvas2.save(os.path.join(output_dir, 'manifold_projection.svg'))
    
    # Example 3: Tensor Subdivision
    canvas3 = SVGCanvas(800, 800)
    p1 = Point(400, 100)
    p2 = Point(100, 700)
    p3 = Point(700, 700)
    recursive_tensor_subdivision(canvas3, p1, p2, p3, depth=4, factor=3)
    canvas3.save(os.path.join(output_dir, 'tensor_subdivision.svg'))
    
    # Example 4: Alphabet Kernel
    canvas4 = SVGCanvas(800, 800)
    semantic_alphabet_kernel(canvas4, Point(400, 400), 250)
    canvas4.save(os.path.join(output_dir, 'alphabet_kernel.svg'))
    
    # Example 5: Fibonacci Spiral Manifold
    canvas5 = SVGCanvas(800, 800)
    fibonacci_spiral_manifold(canvas5, Point(300, 300), 180, iterations=10)
    canvas5.save(os.path.join(output_dir, 'fibonacci_manifold.svg'))
    
    print("✓ Generated all research-oriented examples!")
