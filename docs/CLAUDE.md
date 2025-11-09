# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an algorithmic SVG generator framework for creating geometrically precise, fractal-friendly graphics through functional composition. It's designed for research visualizations including tensor manifolds, harmonic relationships, biological patterns, and fractal structures.

## Core Architecture

### Directory Structure

```
svGen/
├── src/                    # Source code
│   ├── __init__.py         # Package initialization
│   └── svg_generator.py    # Core library
├── examples/               # Example implementations
│   ├── advanced_examples.py
│   └── research_examples.py
├── templates/              # User templates
│   └── experiment_template.py
├── outputs/                # Generated SVGs (gitignored)
├── docs/                   # Documentation
│   ├── README.md
│   ├── QUICK_REFERENCE.md
│   └── CLAUDE.md
├── viewer.html             # Viewer utility
├── .gitignore
└── requirements.txt
```

### Three-Layer Design

1. **Foundation Layer** (`src/svg_generator.py`)
   - `Point` dataclass: Immutable 2D coordinates with rotation, distance, and arithmetic operations
   - `SVGCanvas`: Stateful element accumulator with rendering methods (polygon, circle, line, path, group)
   - Geometric primitives: `regular_polygon()`, `equilateral_triangle()`, `sierpinski_triangle()`, `koch_snowflake()`
   - Transform functions: `scale_points()`, `rotate_points()`, `translate_points()`

2. **Example Layer** (`examples/`)
   - `advanced_examples.py`: Mandalas, golden spirals, L-systems, sacred geometry, Penrose tilings
   - `research_examples.py`: Specialized functions for harmonic circles, manifold projections, alphabet kernels, tensor subdivisions

3. **User Layer** (`templates/`)
   - `experiment_template.py`: Starter template with example patterns
   - Custom experiment files created by users

### Key Design Patterns

**Functional Composition**: Complex shapes are built by composing simple primitives. Functions return `List[Point]` or mutate the canvas directly.

**Recursive Drawing**: Fractal functions typically follow this pattern:
```python
def fractal(canvas, center, size, depth):
    if depth == 0:
        # Base case: draw primitive
        canvas.circle(center, size, ...)
        return
    # Recursive case: draw and subdivide
    canvas.circle(center, size, ...)
    for angle in [angles]:
        new_center = calculate_offset(center, size, angle)
        fractal(canvas, new_center, size * scale_factor, depth - 1)
```

**Point Transformation Pipeline**: Points are immutable; transformations return new points:
```python
points = regular_polygon(center, radius, 6)
points = rotate_points(points, math.pi/4, origin=center)
points = scale_points(points, 1.5, origin=center)
canvas.polygon(points, ...)
```

## Development Workflow

### Quick Start: Live Development Environment

**Recommended for interactive development:**

```bash
# Start dev server + file watcher (auto-reload)
python dev.py
```

This starts:
1. HTTP server on `http://localhost:8000`
2. File watcher that auto-regenerates on save
3. Open `http://localhost:8000/viewer.html` in browser

**Workflow:**
1. Edit Python files in `examples/` or `templates/`
2. Save file → Auto-runs script → Refresh browser to see changes

### Alternative: Manual Workflow

```bash
# Run individual scripts manually
python examples/advanced_examples.py
python examples/research_examples.py
python templates/experiment_template.py

# Start just the HTTP server (no auto-reload)
python dev_server.py

# Start just the file watcher (no server)
python watch.py
```

### Creating New Patterns

1. Copy `templates/experiment_template.py` to a new file (can be in root or templates/)
2. Modify the `main()` function or add custom shape functions
3. Run the script to generate SVG (outputs automatically go to `outputs/`)
4. View in browser at `http://localhost:8000/viewer.html` (or open `viewer.html` directly)

### Testing

There are no formal tests. Visual inspection via `viewer.html` is the primary validation method.

## Common Development Patterns

### Adding Custom Primitives

Add new primitive functions to `src/svg_generator.py` following this signature:
```python
def new_shape(center: Point, size: float, **params) -> List[Point]:
    """Generate points for new shape"""
    # Calculate points using trigonometry
    return points
```

### Color Strategies

- **Depth-based**: `f"hsl({depth * 40}, 70%, 60%)"` for recursive structures
- **Position-based**: `f"hsl({(point.x / canvas.width) * 360}, 70%, 60%)"`
- **Parametric**: Use mathematical functions to map values to hue (0-360)

### Recursion Depth Limits

Always include a depth base case to prevent infinite recursion. Typical depths:
- Simple fractals: 4-6
- Dense fractals: 7-10
- Complex patterns: 3-5

## File Paths

All file paths have been refactored to use relative paths:

- Source code is in `src/`
- Examples are in `examples/`
- Templates are in `templates/`
- All SVG outputs go to `outputs/` (automatically created, gitignored)
- The `viewer.html` file is in the repository root

**Import Pattern**: All example and template files use:
```python
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from svg_generator import *
```

**Output Pattern**: All files save to `outputs/` using:
```python
output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(output_dir, exist_ok=True)
canvas.save(os.path.join(output_dir, 'filename.svg'))
```

## Mathematical Constants

The framework uses `math.pi` extensively. Common values:
- `math.pi / 6` = 30°
- `math.pi / 4` = 45°
- `math.pi / 3` = 60°
- `math.pi / 2` = 90°
- `math.pi` = 180°
- `2 * math.pi` (or `math.tau`) = 360°

Golden ratio: `phi = (1 + math.sqrt(5)) / 2` ≈ 1.618

## Research-Specific Features

### Manifold Projections
Use `manifold_projection_2d()` in `examples/research_examples.py` to project multi-dimensional data onto radial 2D plots. Each dimension becomes a spoke.

### Harmonic Relationships
Use `harmonic_circle_projection()` to visualize frequency ratios and musical intervals.

### Alphabet Kernels
See `alphabet_kernel_visualization()` for semantic structure mapping.

### Tensor Subdivisions
See `tensor_subdivision_grid()` for multi-scale grid-based tensor visualizations.

## Extending the Framework

When adding new functionality:

1. **Keep primitives pure**: Geometric functions should return `List[Point]`, not mutate canvas
2. **Canvas methods for drawing**: Only `SVGCanvas` methods should generate SVG elements
3. **Parameterize everything**: Make constants into function parameters for reusability
4. **Document with examples**: Add usage examples in docstrings
5. **Maintain mathematical precision**: Avoid approximations; use actual trigonometric calculations
