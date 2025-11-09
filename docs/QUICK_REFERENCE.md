# 🔷 Quick Reference Cheat Sheet

## Instant Start
```python
from svg_generator import *
canvas = SVGCanvas(800, 800)
# ... your code ...
canvas.save("/mnt/user-data/outputs/output.svg")
```

## Essential Shapes

### Triangle
```python
points = equilateral_triangle(Point(400, 400), 200)
canvas.polygon(points, fill="lightblue", stroke="navy")
```

### Regular Polygon
```python
# Pentagon, Hexagon, etc.
points = regular_polygon(Point(400, 400), radius=150, sides=6)
canvas.polygon(points, fill="lightgreen", stroke="darkgreen")
```

### Circle
```python
canvas.circle(Point(400, 400), radius=100, fill="pink", stroke="red")
```

### Line
```python
canvas.line(Point(100, 100), Point(700, 700), stroke="blue", stroke_width=3)
```

## Transformations

### Rotate
```python
rotated = rotate_points(points, math.pi/4, origin=Point(400, 400))
```

### Scale
```python
scaled = scale_points(points, factor=1.5, origin=Point(400, 400))
```

### Translate
```python
moved = translate_points(points, dx=50, dy=100)
```

## Fractals & Recursion

### Sierpinski Triangle
```python
p1, p2, p3 = Point(400, 100), Point(100, 700), Point(700, 700)
sierpinski_triangle(canvas, p1, p2, p3, depth=6)
```

### Custom Recursive
```python
def fractal(canvas, center, size, depth):
    if depth == 0:
        canvas.circle(center, size, fill=f"hsl({depth*30}, 70%, 60%)")
        return
    
    canvas.circle(center, size, fill="none", stroke="black")
    
    # Recurse in 4 directions
    for angle in [0, π/2, π, 3*π/2]:
        offset = size * 0.7
        new_center = Point(
            center.x + offset * cos(angle),
            center.y + offset * sin(angle)
        )
        fractal(canvas, new_center, size * 0.4, depth - 1)
```

## Colors

### HSL (Recommended for programmatic color)
```python
fill=f"hsl({hue}, 70%, 60%)"  # hue: 0-360
```

### RGB
```python
fill="rgb(100, 150, 255)"
```

### Named Colors
```python
fill="lightblue"
stroke="navy"
```

### Opacity
```python
fill="rgba(100, 150, 255, 0.5)"  # 50% transparent
fill_opacity=0.5
```

## Common Patterns

### Grid
```python
for row in range(10):
    for col in range(10):
        center = Point(col*60 + 30, row*60 + 30)
        canvas.circle(center, 20, fill=f"hsl({(row+col)*20}, 70%, 60%)")
```

### Radial
```python
for i in range(12):
    angle = (2 * math.pi * i) / 12
    x = 400 + 200 * math.cos(angle)
    y = 400 + 200 * math.sin(angle)
    canvas.circle(Point(x, y), 15, fill="purple")
```

### Parametric Curve
```python
points = []
for t in range(360):
    angle = t * math.pi / 180
    r = 100 + 50 * math.sin(5 * angle)
    x = 400 + r * math.cos(angle)
    y = 400 + r * math.sin(angle)
    points.append(Point(x, y))
canvas.polygon(points, fill="none", stroke="orange", stroke_width=2)
```

## Math Constants

```python
import math

math.pi         # 3.14159...
math.tau        # 6.28318... (2π)
math.e          # 2.71828...

phi = (1 + math.sqrt(5)) / 2  # 1.618... (golden ratio)

# Common angles
π/6 = 30°
π/4 = 45°
π/3 = 60°
π/2 = 90°
π = 180°
2π = 360°
```

## Point Operations

```python
p1 = Point(100, 200)
p2 = Point(300, 400)

# Arithmetic
p3 = p1 + p2           # Add
p4 = p2 - p1           # Subtract
p5 = p1 * 2            # Scale by scalar

# Rotation
p6 = p1.rotate(math.pi/4, origin=Point(0, 0))

# Distance
dist = p1.distance_to(p2)
```

## Workflow

1. **Create** canvas: `canvas = SVGCanvas(800, 800)`
2. **Add** shapes: `canvas.polygon(...)`
3. **Save** output: `canvas.save("/mnt/user-data/outputs/name.svg")`
4. **View** in browser: Open `viewer.html` and refresh

## Debugging Tips

```python
# Visualize center points
canvas.circle(center, 3, fill="red")

# Visualize construction lines
canvas.line(p1, p2, stroke="red", stroke_width=0.5)

# Print coordinates
print(f"Point: ({p.x:.2f}, {p.y:.2f})")

# Color by depth/iteration
color = f"hsl({depth * 40}, 70%, 60%)"
```

## Pro Tips

- **Start simple**: Test basic shapes before adding recursion
- **Use depth limits**: Prevent runaway recursion (e.g., `if depth == 0`)
- **Parameterize**: Make values into function arguments
- **Keep viewer open**: Edit code → Run → Refresh browser
- **Small stroke widths**: Use 0.5-2 for clean lines
- **HSL for gradients**: Vary hue (0-360) for rainbow effects
- **Golden ratio**: Use `phi = 1.618` for natural proportions

## File Structure
```
/home/claude/
├── svg_generator.py          # Core framework (don't usually edit)
├── experiment_template.py    # Copy this to start new experiments
├── advanced_examples.py      # Reference examples
├── research_examples.py      # Research-oriented patterns
└── your_custom_file.py       # Your experiments

/mnt/user-data/outputs/
├── viewer.html              # Open this in browser
└── *.svg                    # All generated files
```

## Example Complete Script
```python
from svg_generator import *
import math

canvas = SVGCanvas(800, 800)

# Create a mandala
center = Point(400, 400)
for ring in range(5):
    radius = 50 + ring * 50
    petals = 6 + ring * 2
    
    for i in range(petals):
        angle = (2 * math.pi * i) / petals
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        
        hue = (ring * 60 + i * 10) % 360
        canvas.circle(Point(x, y), 15, 
                     fill=f"hsl({hue}, 70%, 60%)",
                     stroke="white", stroke_width=1)

canvas.save("/mnt/user-data/outputs/my_mandala.svg")
print("✓ Done!")
```
