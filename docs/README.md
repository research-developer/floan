# 🔷 Algorithmic SVG Generator

A Python-based framework for creating geometrically precise, fractal-friendly, and algorithmically-generated SVG graphics.

## 🎯 Philosophy

- **Functional composition**: Build complex shapes from simple primitives
- **Mathematical precision**: Use actual geometric calculations, not approximations
- **Fractal-friendly**: Designed for recursive and self-similar structures
- **Immediate feedback**: Generate and visualize instantly

## 📁 Structure

```
/home/claude/
├── svg_generator.py      # Core framework and primitives
├── advanced_examples.py  # Demo patterns (mandala, spiral, trees, etc.)
└── your_experiment.py    # Your custom experiments

/mnt/user-data/outputs/
├── viewer.html          # Visual browser for all SVGs
└── *.svg               # Generated outputs
```

## 🚀 Quick Start

### 1. Basic Usage

```python
from svg_generator import *

# Create canvas
canvas = SVGCanvas(800, 800)

# Draw a triangle
points = equilateral_triangle(Point(400, 400), 200)
canvas.polygon(points, fill="lightblue", stroke="navy")

# Save
canvas.save("/mnt/user-data/outputs/my_shape.svg")
```

### 2. Fractal Example

```python
from svg_generator import *

canvas = SVGCanvas(800, 800)

# Sierpinski triangle
p1 = Point(400, 100)
p2 = Point(100, 700)
p3 = Point(700, 700)

sierpinski_triangle(canvas, p1, p2, p3, depth=6)
canvas.save("/mnt/user-data/outputs/fractal.svg")
```

### 3. View Results

Open: `/mnt/user-data/outputs/viewer.html`

The viewer auto-refreshes to show all SVGs in the outputs folder.

## 🧩 Core Components

### Point Class
```python
p = Point(100, 200)
p2 = p.rotate(math.pi/4, origin=Point(0, 0))
distance = p.distance_to(p2)
```

### SVGCanvas Methods
- `polygon(points, fill, stroke, stroke_width)`
- `circle(center, radius, ...)`
- `line(p1, p2, ...)`
- `path(d, ...)`
- `group(elements, transform)`

### Geometric Primitives
- `regular_polygon(center, radius, sides, rotation)` - n-sided regular polygon
- `equilateral_triangle(center, size)` - Equilateral triangle
- `sierpinski_triangle(canvas, p1, p2, p3, depth)` - Sierpinski fractal
- `koch_snowflake(start, end, depth)` - Koch curve

### Transformations
- `scale_points(points, factor, origin)`
- `rotate_points(points, angle, origin)`
- `translate_points(points, dx, dy)`

## 🎨 Built-in Examples

Run `python advanced_examples.py` to generate:
- **Mandala**: Recursive circular pattern with branches
- **Golden Spiral**: Fibonacci-based squares
- **L-System Tree**: Branching fractal tree
- **Sacred Geometry**: Flower of life pattern
- **Penrose Tiling**: Aperiodic tiling inspired by Penrose

## 💡 Patterns You Can Explore

### Recursive Structures
```python
def fractal_tree(canvas, start, length, angle, depth):
    if depth == 0: return
    end = Point(start.x + length * cos(angle), 
                start.y + length * sin(angle))
    canvas.line(start, end)
    fractal_tree(canvas, end, length*0.7, angle-π/6, depth-1)
    fractal_tree(canvas, end, length*0.7, angle+π/6, depth-1)
```

### Parametric Curves
```python
def parametric_shape(t):
    r = 100 + 50 * sin(5*t)
    return Point(400 + r*cos(t), 400 + r*sin(t))

points = [parametric_shape(t) for t in linspace(0, 2*π, 360)]
canvas.polygon(points, fill="none", stroke="purple")
```

### Tessellations
```python
for row in range(10):
    for col in range(10):
        center = Point(col*60 + 30, row*60 + 30)
        hexagon = regular_polygon(center, 25, 6)
        canvas.polygon(hexagon, fill=f"hsl({(row+col)*30}, 70%, 60%)")
```

## 🔧 Extending the Framework

### Add Custom Primitives

Edit `svg_generator.py` and add your function:

```python
def star(center: Point, outer_radius: float, inner_radius: float, 
         points: int = 5) -> List[Point]:
    """Generate a star shape"""
    pts = []
    angle_step = math.pi / points
    for i in range(points * 2):
        angle = i * angle_step - math.pi/2
        r = outer_radius if i % 2 == 0 else inner_radius
        pts.append(Point(
            center.x + r * math.cos(angle),
            center.y + r * math.sin(angle)
        ))
    return pts
```

### Add Color Functions

```python
def color_by_depth(depth: int, max_depth: int) -> str:
    hue = (depth / max_depth) * 360
    return f"hsl({hue}, 70%, 60%)"

def color_by_position(p: Point, canvas_size: int) -> str:
    hue = (p.x / canvas_size) * 360
    return f"hsl({hue}, 70%, 60%)"
```

## 🎯 Workflow Tips

1. **Rapid iteration**: Keep viewer.html open, run scripts, refresh browser
2. **Start simple**: Test basic shapes before adding recursion
3. **Use depth limits**: Prevent infinite recursion during testing
4. **Parameterize everything**: Make constants into function parameters
5. **Compose primitives**: Combine simple shapes to create complexity

## 🧮 Mathematical Constants

```python
import math

math.pi        # π
math.e         # Euler's number
math.tau       # 2π
phi = (1 + math.sqrt(5)) / 2  # Golden ratio (1.618...)
```

## 📐 Useful Angles

```python
math.pi / 6    # 30°
math.pi / 4    # 45°
math.pi / 3    # 60°
math.pi / 2    # 90°
math.pi        # 180°
math.tau       # 360°
```

## 🐛 Debugging

```python
# Print points for inspection
print(f"Point: ({p.x:.2f}, {p.y:.2f})")

# Visualize construction lines
canvas.circle(center, 3, fill="red")  # Mark center
canvas.line(p1, p2, stroke="red", stroke_width=0.5)  # Guide

# Use distinct colors for depth levels
color = f"hsl({depth * 40}, 70%, 60%)"
```

## 🚀 Next Steps

1. Explore `advanced_examples.py` for inspiration
2. Create your own experiment file
3. Extend `svg_generator.py` with custom primitives
4. Share your algorithmic creations!

## 🔬 For Your Research

This framework is designed to support:
- **Tensor visualizations**: 48-manifold projections
- **Biological patterns**: Protein structure visualizations
- **Musical geometry**: Harmonic relationships as shapes
- **Semantic structures**: Alphabet kernel visualizations
- **Fractal analysis**: Multi-scale recursive patterns

The functional, composable design makes it easy to translate mathematical concepts into precise visual representations.
