"""
Algorithmic SVG Generator - Geometric & Fractal-Friendly
"""
import math
from typing import List, Tuple, Callable
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    
    def rotate(self, angle: float, origin=None) -> 'Point':
        """Rotate point around origin by angle (radians)"""
        origin = origin or Point(0, 0)
        p = self - origin
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return Point(
            p.x * cos_a - p.y * sin_a,
            p.x * sin_a + p.y * cos_a
        ) + origin
    
    def distance_to(self, other: 'Point') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class SVGCanvas:
    def __init__(self, width: int = 1000, height: int = 1000):
        self.width = width
        self.height = height
        self.elements = []
        
    def add(self, element: str):
        """Add an SVG element"""
        self.elements.append(element)
        return self
    
    def polygon(self, points: List[Point], fill: str = "none", 
                stroke: str = "black", stroke_width: float = 2, 
                fill_opacity: float = 1.0) -> 'SVGCanvas':
        """Add a polygon"""
        points_str = " ".join(f"{p.x},{p.y}" for p in points)
        self.add(f'<polygon points="{points_str}" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="{stroke_width}" '
                f'fill-opacity="{fill_opacity}"/>')
        return self
    
    def circle(self, center: Point, radius: float, fill: str = "none",
               stroke: str = "black", stroke_width: float = 2) -> 'SVGCanvas':
        """Add a circle"""
        self.add(f'<circle cx="{center.x}" cy="{center.y}" r="{radius}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self
    
    def line(self, p1: Point, p2: Point, stroke: str = "black", 
             stroke_width: float = 2) -> 'SVGCanvas':
        """Add a line"""
        self.add(f'<line x1="{p1.x}" y1="{p1.y}" x2="{p2.x}" y2="{p2.y}" '
                f'stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self
    
    def path(self, d: str, fill: str = "none", stroke: str = "black",
             stroke_width: float = 2) -> 'SVGCanvas':
        """Add a path"""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
                f'stroke-width="{stroke_width}"/>')
        return self
    
    def group(self, elements: List[str], transform: str = None) -> 'SVGCanvas':
        """Add a group of elements with optional transform"""
        transform_attr = f' transform="{transform}"' if transform else ''
        self.add(f'<g{transform_attr}>')
        for elem in elements:
            self.add(elem)
        self.add('</g>')
        return self
    
    def render(self) -> str:
        """Render the complete SVG"""
        header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">'
        footer = '</svg>'
        return header + '\n  ' + '\n  '.join(self.elements) + '\n' + footer
    
    def save(self, filename: str):
        """Save SVG to file"""
        with open(filename, 'w') as f:
            f.write(self.render())
        print(f"Saved to {filename}")

# ============ GEOMETRIC PRIMITIVES ============

def regular_polygon(center: Point, radius: float, sides: int, 
                    rotation: float = 0) -> List[Point]:
    """Generate points for a regular polygon"""
    points = []
    angle_step = (2 * math.pi) / sides
    for i in range(sides):
        angle = rotation + i * angle_step
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        points.append(Point(x, y))
    return points

def equilateral_triangle(center: Point, size: float) -> List[Point]:
    """Generate equilateral triangle pointing up"""
    return regular_polygon(center, size, 3, rotation=-math.pi/2)

def sierpinski_triangle(canvas: SVGCanvas, p1: Point, p2: Point, p3: Point, 
                       depth: int, color_fn: Callable = None):
    """Generate Sierpinski triangle fractal"""
    if depth == 0:
        color = color_fn(depth) if color_fn else f"hsl({depth * 30}, 70%, 50%)"
        canvas.polygon([p1, p2, p3], fill=color, stroke="none")
        return
    
    # Calculate midpoints
    m1 = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)
    m2 = Point((p2.x + p3.x)/2, (p2.y + p3.y)/2)
    m3 = Point((p3.x + p1.x)/2, (p3.y + p1.y)/2)
    
    # Recurse on three smaller triangles
    sierpinski_triangle(canvas, p1, m1, m3, depth - 1, color_fn)
    sierpinski_triangle(canvas, m1, p2, m2, depth - 1, color_fn)
    sierpinski_triangle(canvas, m3, m2, p3, depth - 1, color_fn)

def koch_snowflake(start: Point, end: Point, depth: int) -> List[Point]:
    """Generate Koch snowflake edge"""
    if depth == 0:
        return [start, end]
    
    # Divide line into three segments
    delta = end - start
    p1 = start + delta * (1/3)
    p2 = start + delta * (2/3)
    
    # Create the peak
    angle = math.pi / 3  # 60 degrees
    peak = Point(
        p1.x + (p2.x - p1.x) * math.cos(angle) - (p2.y - p1.y) * math.sin(angle),
        p1.y + (p2.x - p1.x) * math.sin(angle) + (p2.y - p1.y) * math.cos(angle)
    )
    
    # Recurse on four segments
    points = []
    points.extend(koch_snowflake(start, p1, depth - 1)[:-1])
    points.extend(koch_snowflake(p1, peak, depth - 1)[:-1])
    points.extend(koch_snowflake(peak, p2, depth - 1)[:-1])
    points.extend(koch_snowflake(p2, end, depth - 1))
    
    return points

# ============ TRANSFORMS ============

def scale_points(points: List[Point], factor: float, origin: Point = None) -> List[Point]:
    """Scale points around origin"""
    origin = origin or Point(0, 0)
    return [origin + (p - origin) * factor for p in points]

def rotate_points(points: List[Point], angle: float, origin: Point = None) -> List[Point]:
    """Rotate points around origin"""
    origin = origin or Point(0, 0)
    return [p.rotate(angle, origin) for p in points]

def translate_points(points: List[Point], dx: float, dy: float) -> List[Point]:
    """Translate points"""
    return [Point(p.x + dx, p.y + dy) for p in points]

# ============ EXAMPLE USAGE ============

if __name__ == "__main__":
    # Example: Create a Sierpinski triangle
    import os

    canvas = SVGCanvas(800, 800)

    p1 = Point(400, 100)
    p2 = Point(100, 700)
    p3 = Point(700, 700)

    sierpinski_triangle(canvas, p1, p2, p3, depth=6)

    # Save to outputs directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    canvas.save(os.path.join(output_dir, 'sierpinski.svg'))
