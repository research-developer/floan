# Flowangle Specification

**Date:** November 8, 2025
**Status:** ✅ Implemented and Validated

---

## Overview

A **flowangle** is a new geometric primitive similar to a triquetra, defined by smoothly curved bezier segments connecting the vertices of a regular polygon. The shape is parameterized by two key values: **flow** (curvature intensity) and **angle** (handle orientation).

---

## Mathematical Definition

### Core Parameters

1. **n** - Number of sides (3 for triquetra-like shapes)
2. **size** - Radius from center to vertices
3. **flow** - Control handle distance as multiplier of size (0.0-2.0)
   - `flow_distance = size × flow`
4. **angle** - Handle rotation in degrees relative to center-vertex line (-180° to 180°)

### Geometry

Starting from a regular n-sided polygon:

1. **Vertices**: Positioned at equal angles around center
   ```
   vertex_angle = start_angle + (i × 2π/n)
   x = center.x + size × cos(vertex_angle)
   y = center.y + size × sin(vertex_angle)
   ```

2. **Bezier Segments**: Connect consecutive vertices with cubic bezier curves
   ```
   For segment from vertex[i] to vertex[i+1]:

   start = vertex[i]
   end = vertex[i+1]

   control1_angle = angle_from_center_to_start + angle_parameter
   control1 = start + flow_distance × (cos(control1_angle), sin(control1_angle))

   control2_angle = angle_from_center_to_end - angle_parameter
   control2 = end + flow_distance × (cos(control2_angle), sin(control2_angle))
   ```

---

## Parameterization Results

### Hand-Graphed Analysis

Original hand-graphed 3n-flowangle decomposition revealed:

**Base Triangle:**
- Center: (973.68, 623.30)
- Vertices equidistant: 577.35 units from center
- Perfect equilateral: all sides = 1000 units
- Vertex angles: -90°, 150°, 30° (from center)

**Control Points:**
- Flow distances: ~605, ~480, ~574 units (varying)
- Relative angles: ±105°, ±90°, ±75° patterns
- Average flow: ~1.05 × size
- Optimal angle: ~105° (for classic triquetra)

**Winner Configuration:**
- **angle = 60°**
- **flow = 1.5**
- Creates perfectly balanced triquetra-like form
- Smooth curves with elegant proportions

---

## Parameter Space Exploration

### Flow Range (0.5 - 1.5)

- **0.5**: Tight curves, barely extends from polygon
- **0.75**: Subtle curves, gentle organic feel
- **1.0**: Balanced curves, natural appearance
- **1.25**: Bold curves, pronounced flow
- **1.5**: Maximum smooth curves, highly organic (WINNER for 60°)

### Angle Range (60° - 135°)

- **60°**: Rounded, triquetra-like (WINNER with flow=1.5)
- **75°**: Soft curves, organic
- **90°**: Balanced symmetric curves
- **105°**: Classic triquetra appearance
- **120°**: Pronounced directionality
- **135°**: Sharp transitions, angular character

---

## n-Variations

Using winner parameters (60° × 1.5):

| n | Shape | Character |
|---|-------|-----------|
| 3 | 3n-Flowangle | Triquetra-like, rounded triangle |
| 4 | 4n-Flowangle | Quatrefoil-like, rounded square |
| 5 | 5n-Flowangle | Pentagonal flower |
| 6 | 6n-Flowangle | Hexagonal snowflake |
| 8 | 8n-Flowangle | Octagonal star |

---

## Implementation

### Core Functions

**`src/flowangle.py`** - Main implementation

```python
create_flowangle(n, size, flow, angle, center)
  → Returns (vertices, bezier_segments)

flowangle_to_svg(n, size, flow, angle, center, **style)
  → Returns SVG path string

create_parameter_grid(n)
  → Generates exploration grid
```

### Usage Examples

```python
from flowangle import create_flowangle, flowangle_to_svg
from svg_generator import Point

# Create winner flowangle
svg = flowangle_to_svg(
    n=3,
    size=300,
    flow=1.5,
    angle=60,
    center=Point(400, 400),
    fill='rgba(0, 255, 204, 0.1)',
    stroke='#00ffcc',
    stroke_width=3
)

# Generate parameter exploration grid
from flowangle import create_parameter_grid
create_parameter_grid(n=3)  # Creates 5×6 grid of variations
```

---

## Generated Outputs

### Visualization Files

1. **`flowangle_decomposition.svg`** - Decomposed hand-graphed example
   - Shows three bezier segments in different colors
   - Control points and construction lines visible
   - Validates decomposition approach

2. **`flowangle_test.svg`** - Single flowangle with construction
   - Parameters: n=3, flow=1.05, angle=105°
   - Shows control points, center, and handle lines
   - Useful for understanding geometry

3. **`flowangle_parameter_grid.svg`** - REPL exploration grid
   - 5 flow values × 6 angle values = 30 variations
   - Systematic parameter space visualization
   - Used to discover winner configuration

4. **`flowangle_winner.svg`** - High-resolution winner (60° × 1.5)
   - Large format: 1200×1200
   - Dark background with cyan stroke
   - Subtitle glow effects

5. **`flowangle_showcase.svg`** - Curated collection
   - 6 notable configurations with labels
   - Winner, Classic, Sharp, Soft, Bold, Geometric
   - Multi-color presentation

6. **`flowangle_n_variations.svg`** - Different n values
   - Shows n=3,4,5,6,8 with winner parameters
   - Demonstrates generalization to other polygons

---

## Key Discoveries

### What Worked

✅ **Decomposition approach** - Breaking hand-graphed path into thirds
✅ **Parameterization** - Flow and angle capture full design space
✅ **Normalization** - Size-relative flow creates consistent appearance
✅ **REPL grid** - Visual exploration revealed optimal parameters
✅ **Generalization** - Same algorithm works for any n-sided polygon

### Optimal Parameters Found

**3n-Flowangle Winner:**
- angle = 60°
- flow = 1.5
- Produces: "Perfectly balanced triquetra-like form with smooth curves and elegant proportions"

**Classic Triquetra:**
- angle = 105°
- flow = 1.05
- Produces: Traditional triquetra appearance

---

## Design Patterns

### Triquetra-like Shapes (n=3)
- Use flow ≥ 1.0 for pronounced curves
- Angles 60°-105° for organic appearance
- Lower angles (60-75°) create rounder forms
- Higher angles (105-135°) create sharper transitions

### Symmetric Flowers (n≥4)
- Winner parameters (60° × 1.5) generalize well
- Creates petal-like lobes for any n
- Increase flow for more pronounced petals
- Decrease angle for softer, rounder petals

### Construction Visualization
- Red dots: vertices
- Blue dots: control points
- Light blue lines: control handles
- Gray lines: center to vertices

---

## Future Extensions

### Potential Enhancements

1. **Variable flow per segment** - Different flow values for each side
2. **Variable angle per segment** - Asymmetric variations
3. **Nested flowangles** - Recursive patterns
4. **Animated transitions** - Morph between parameter values
5. **3D extrusion** - Convert to 3D shapes
6. **Pattern fills** - Interior decoration patterns
7. **Interactive editor** - Real-time parameter manipulation

### Integration Ideas

- Add to `editor.html` as new pattern type
- Create flowangle-based mandalas
- Use as basis for logo generation
- Combine with existing sacred geometry patterns

---

## References

### Source Files
- `src/flowangle.py` - Core implementation
- `src/flowangle_research.py` - Analysis and decomposition
- `src/flowangle_showcase.py` - Visualization generation

### Key Commits
- Initial decomposition and analysis
- Parameterization implementation
- Parameter grid generation
- Winner showcase creation

---

## Conclusion

The flowangle primitive successfully generalizes triquetra-like shapes through systematic parameterization. The **60° × 1.5** configuration emerged as the winner, producing beautifully balanced organic curves. The implementation is complete, validated, and ready for integration into the svGen ecosystem.

**Status:** ✅ All objectives achieved
**Quality:** Production-ready
**Documentation:** Complete

