# FlowAngle Pattern & Texture Shading Notes

**Team 4: Pattern & Texture Shading Explorer**

## Overview

This implementation creates FlowAngle shapes with pattern-based fills and textures that respond dynamically to the curve geometry. The patterns become denser and adapt their properties based on the `curveFactor`, creating an organic relationship between the shape's curvature and its internal texture.

## Implementation Details

### File Location
- **Main File**: `/Users/preston/research-developer/svGen-shading/shading_test_patterns.html`
- **Source**: Adapted from `flowangle_animation.html` in the main svGen directory

### Pattern Types Implemented

#### 1. **Solid Fill** (Baseline)
- Standard solid color fill (#87ceeb sky blue)
- No pattern overlay
- Serves as the reference for comparing other patterns

#### 2. **Dots Pattern**
- Regular circular dots arranged in a grid
- Dot size: 20% of pattern tile size
- Opacity: 0.6 for subtle texture
- **Curve Response**: Pattern density increases with tighter curves (higher |curveFactor|)

#### 3. **Lines Pattern**
- Vertical lines that rotate based on curveFactor
- Line rotation: `abs(curveFactor) * 45 degrees`
- Line width: 10% of pattern tile size
- **Curve Response**: Lines angle more dramatically with tighter curves

#### 4. **Crosshatch Pattern**
- Diagonal lines crossing at 90 degrees
- Creates classic hatching effect
- Line width: 5% of pattern tile size for finer detail
- **Curve Response**: Pattern scale adjusts to curve tightness

#### 5. **Stippling Effect**
- Random dots with varying sizes
- Simulates hand-drawn stippling technique
- Number of dots: Base 15, multiplied by density factor
- Dot radius: 3% of tile with ±50% random variation
- **Curve Response**: More stipple dots appear in tighter curves

#### 6. **Waves Pattern**
- Quadratic Bezier curve creating wave effect
- Wave amplitude: 30% of pattern tile size
- Double-width tiles to create continuous waves
- **Curve Response**: Wave frequency influenced by curveFactor

#### 7. **Gradient + Dots**
- Combines radial gradient with dot overlay
- Gradient: Sky blue to navy blue
- Dots at 25% of tile size
- Creates depth and texture simultaneously

### Adaptive Pattern Density

The key innovation is the **curve-responsive pattern density**:

```javascript
const densityFactor = Math.abs(curveFactor) * 0.5 + 1;
const adjustedSize = baseSize / (state.patternDensity * densityFactor);
```

This formula ensures:
- Tighter curves (higher |curveFactor|) → smaller pattern tiles → denser patterns
- The effect is scaled by 0.5 to prevent overly aggressive density changes
- Minimum density factor of 1.0 (when curveFactor = 0)
- User can further adjust via Pattern Density slider (0.3x to 3x)

### UI Controls

#### Pattern Controls
1. **Pattern Type** (dropdown): Select from 7 pattern options
2. **Pattern Scale** (slider): 0.5x to 3x base scale
   - Affects the overall size of pattern tiles
   - Independent of curve-based adaptation
3. **Pattern Density** (slider): 0.3x to 3x density multiplier
   - Additional control over pattern repetition
   - Combines with curve-based density

#### FlowAngle Controls (Preserved)
- Sides (n): 1 to 12
- Curve Factor: -3.0 to 1.0
- Handle Angle: 10° to 170°
- Rotation: 0° to 360°
- Show Guides: Toggle construction geometry visibility

### SVG Pattern Implementation

Patterns are defined using SVG `<pattern>` elements with `patternUnits="userSpaceOnUse"` for consistent sizing. The implementation:

1. Creates pattern definitions in `<defs>` section
2. Applies pattern as fill via `url(#pattern-id)`
3. Overlays pattern with reduced opacity (0.7) for blending
4. Maintains stroke outline for shape definition

```javascript
// Main shape with base color
<path d="..." fill="#87ceeb" stroke="#000080" />

// Pattern overlay
<path d="..." fill="url(#pattern-dots)" opacity="0.7" />
```

### Technical Achievements

#### 1. Curve-Aware Patterns
- Patterns automatically adjust to shape geometry
- Tighter curves → denser, more detailed patterns
- Creates visual harmony between form and texture

#### 2. Layered Rendering
- Base fill provides fallback color
- Pattern overlay adds texture
- Stroke maintains clean edges
- Guides show construction (when enabled)

#### 3. Pattern Variety
- 7 distinct pattern types
- Each optimized for visual effect
- Mix of geometric and organic styles
- Includes modern (gradients) and traditional (stippling) techniques

#### 4. User Control
- Independent pattern scale control
- Density multiplier for fine-tuning
- Real-time preview of changes
- Preserves all FlowAngle shape parameters

### Download Functionality

Both SVG and PNG downloads preserved from original:
- **Download SVG**: Vector file with embedded patterns
- **Download PNG**: Rasterized 2x resolution for quality
- Filenames include shape parameters for organization

### Code Organization

```
createPatternDefs(state, size, curveFactor)
  ├─> Calculates adaptive density factor
  ├─> Generates SVG pattern definition
  └─> Returns {patternId, patternDef}

generateFlowAngle(state, size)
  ├─> Calculate vertices and triangles
  ├─> Create pattern definitions
  ├─> Build curved path data
  ├─> Apply pattern fills
  └─> Return complete SVG string
```

### Removed Features (from original)

To focus on pattern shading:
- Pulse animations
- Keyframe timeline
- Animation controls
- URL sharing
- Constraint manager
- Feedback mode

These removals simplified the UI and codebase while maintaining core FlowAngle generation.

### Success Criteria Met

✅ **Working HTML file** with pattern-filled FlowAngle shapes
✅ **4+ different pattern types** (implemented 7)
✅ **Patterns complement curved geometry** via adaptive density
✅ **Documentation** of approach and implementation

### Visual Examples

The patterns work especially well with:
- **Triquetra** (n=3, c=-0.66): Dots and stippling highlight curved lobes
- **Flower** (n=6, c=-0.8): Crosshatch creates petal-like texture
- **Star** (n=5, c=-1.2): Lines emphasize pointed geometry
- **Smooth** (n=8, c=-0.5): Waves create flowing texture

### Future Enhancements

Potential additions:
- Custom color selection for patterns
- Pattern rotation independent of curve
- Blend modes (multiply, overlay, etc.)
- Radial vs linear pattern arrangements
- Animation of pattern parameters
- Export patterns as reusable SVG assets

### Technical Notes

- SVG patterns use `userSpaceOnUse` for absolute sizing
- Random stippling uses Math.random() - non-deterministic
- Pattern IDs use pattern type to ensure uniqueness
- Gradient patterns require nested `<defs>` structure
- PNG export renders patterns correctly via canvas

---

**Created by**: Team 4 - Pattern & Texture Shading Explorer
**Date**: November 2025
**Based on**: FlowAngle Animation Studio v1.0
