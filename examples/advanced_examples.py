"""
Advanced Examples - Algorithmic SVG Patterns
Demonstrating composition, recursion, and geometric transformations
"""
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from svg_generator import *

def mandala_recursive(canvas: SVGCanvas, center: Point, radius: float, 
                      depth: int, branches: int = 6):
    """Create a recursive mandala pattern"""
    if depth == 0 or radius < 2:
        canvas.circle(center, radius, fill=f"hsl({depth * 40}, 70%, 60%)", 
                     stroke="none")
        return
    
    # Draw center circle
    canvas.circle(center, radius, fill="none", stroke=f"hsl({depth * 40}, 70%, 50%)", 
                 stroke_width=1)
    
    # Create branches
    angle_step = (2 * math.pi) / branches
    for i in range(branches):
        angle = i * angle_step
        branch_center = Point(
            center.x + radius * math.cos(angle),
            center.y + radius * math.sin(angle)
        )
        mandala_recursive(canvas, branch_center, radius * 0.4, depth - 1, branches)

def golden_spiral(canvas: SVGCanvas, start: Point, size: float, iterations: int):
    """Create a golden ratio spiral with squares"""
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    current_pos = start
    current_size = size
    angle = 0
    
    for i in range(iterations):
        # Draw square
        hue = (i * 30) % 360
        canvas.polygon([
            current_pos,
            Point(current_pos.x + current_size, current_pos.y),
            Point(current_pos.x + current_size, current_pos.y + current_size),
            Point(current_pos.x, current_pos.y + current_size)
        ], fill=f"hsl({hue}, 60%, 70%)", stroke="black", stroke_width=2)
        
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

def lsystem_tree(canvas: SVGCanvas, start: Point, length: float, angle: float, 
                 depth: int, branch_angle: float = math.pi/6):
    """Generate an L-system tree fractal"""
    if depth == 0:
        return
    
    # Calculate end point
    end = Point(
        start.x + length * math.cos(angle),
        start.y + length * math.sin(angle)
    )
    
    # Draw branch
    width = depth * 0.5
    color_intensity = 30 + depth * 10
    canvas.line(start, end, stroke=f"rgb({color_intensity}, {100 + color_intensity}, {color_intensity})", 
               stroke_width=width)
    
    # Recurse with smaller branches
    new_length = length * 0.7
    lsystem_tree(canvas, end, new_length, angle - branch_angle, depth - 1, branch_angle)
    lsystem_tree(canvas, end, new_length, angle + branch_angle, depth - 1, branch_angle)

def sacred_geometry_flower(canvas: SVGCanvas, center: Point, radius: float, petals: int = 6):
    """Create a flower of life / sacred geometry pattern"""
    # Center circle
    canvas.circle(center, radius, fill="none", stroke="#4a90e2", stroke_width=2)
    
    # Surrounding circles
    angle_step = (2 * math.pi) / petals
    for i in range(petals):
        angle = i * angle_step
        petal_center = Point(
            center.x + radius * math.cos(angle),
            center.y + radius * math.sin(angle)
        )
        canvas.circle(petal_center, radius, fill="none", stroke="#4a90e2", stroke_width=2)
    
    # Inner intersections (creates the sacred geometry effect)
    for i in range(petals):
        angle1 = i * angle_step
        angle2 = ((i + 1) % petals) * angle_step
        
        p1 = Point(center.x + radius * math.cos(angle1), center.y + radius * math.sin(angle1))
        p2 = Point(center.x + radius * math.cos(angle2), center.y + radius * math.sin(angle2))
        
        # Draw connecting arc or line
        canvas.line(p1, p2, stroke="#e24a90", stroke_width=1)

def penrose_tiling_seed(canvas: SVGCanvas, center: Point, size: float, iterations: int):
    """Create a simplified Penrose tiling pattern"""
    phi = (1 + math.sqrt(5)) / 2
    
    def draw_kite(p1: Point, p2: Point, depth: int):
        if depth == 0:
            # Calculate other two points of kite
            mid = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)
            perp_angle = math.atan2(p2.y - p1.y, p2.x - p1.x) + math.pi/2
            height = p1.distance_to(p2) * 0.618
            
            p3 = Point(mid.x + height * math.cos(perp_angle), 
                      mid.y + height * math.sin(perp_angle))
            p4 = Point(mid.x - height * 0.382 * math.cos(perp_angle),
                      mid.y - height * 0.382 * math.sin(perp_angle))
            
            hue = (depth * 60) % 360
            canvas.polygon([p1, p3, p2, p4], fill=f"hsl({hue}, 60%, 70%)", 
                          stroke="black", stroke_width=1)
            return
        
        # Subdivide (simplified)
        mid = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)
        draw_kite(p1, mid, depth - 1)
        draw_kite(mid, p2, depth - 1)
    
    # Create initial star pattern
    num_points = 10
    for i in range(num_points):
        angle1 = (2 * math.pi * i) / num_points
        angle2 = (2 * math.pi * (i + 1)) / num_points
        
        p1 = Point(center.x + size * math.cos(angle1), center.y + size * math.sin(angle1))
        p2 = Point(center.x + size * math.cos(angle2), center.y + size * math.sin(angle2))
        
        draw_kite(p1, p2, iterations)

# ============ GENERATE EXAMPLES ============

if __name__ == "__main__":
    # Set up output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    # Example 1: Mandala
    canvas1 = SVGCanvas(600, 600)
    mandala_recursive(canvas1, Point(300, 300), 120, depth=4, branches=8)
    canvas1.save(os.path.join(output_dir, 'mandala.svg'))

    # Example 2: Golden Spiral
    canvas2 = SVGCanvas(600, 600)
    golden_spiral(canvas2, Point(250, 250), 150, iterations=12)
    canvas2.save(os.path.join(output_dir, 'golden_spiral.svg'))

    # Example 3: L-System Tree
    canvas3 = SVGCanvas(600, 600)
    lsystem_tree(canvas3, Point(300, 550), 120, -math.pi/2, depth=10)
    canvas3.save(os.path.join(output_dir, 'lsystem_tree.svg'))

    # Example 4: Sacred Geometry
    canvas4 = SVGCanvas(600, 600)
    sacred_geometry_flower(canvas4, Point(300, 300), 80, petals=6)
    # Add nested layers
    sacred_geometry_flower(canvas4, Point(300, 300), 50, petals=6)
    sacred_geometry_flower(canvas4, Point(300, 300), 30, petals=6)
    canvas4.save(os.path.join(output_dir, 'sacred_geometry.svg'))

    # Example 5: Penrose-inspired tiling
    canvas5 = SVGCanvas(600, 600)
    penrose_tiling_seed(canvas5, Point(300, 300), 200, iterations=3)
    canvas5.save(os.path.join(output_dir, 'penrose.svg'))

    print("✓ Generated all examples!")
