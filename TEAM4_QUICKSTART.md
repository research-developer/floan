# Team 4: Pattern & Texture Shading - Quick Start Guide

## Your Mission
Create FlowAngle shapes with **pattern-based fills and textures** that respond dynamically to the curve geometry.

## What You've Got

### Main File
📄 **`shading_test_patterns.html`** - Your working demo with 7 pattern types

### Documentation
📖 **`SHADING_PATTERNS_NOTES.md`** - Complete technical documentation

## How to Run

### Quick Start
```bash
# Open the file directly in your browser
open shading_test_patterns.html

# OR start a development server
python3 dev_simple.py
# Then visit: http://localhost:8000/shading_test_patterns.html
```

## What's Implemented

### 7 Pattern Types

1. **Solid Fill** - Baseline (no pattern)
2. **Dots** - Regular circular dots
3. **Lines** - Rotating lines based on curve
4. **Crosshatch** - Diagonal crossing lines
5. **Stippling** - Random organic dots
6. **Waves** - Flowing wave patterns
7. **Gradient + Dots** - Combined radial gradient with dots

### Key Feature: Curve-Responsive Patterns

The patterns automatically **adapt to the curve tightness**:
- Tighter curves → Denser patterns
- Looser curves → More spacious patterns

Formula: `densityFactor = abs(curveFactor) * 0.5 + 1`

## Controls

### Pattern Controls
- **Pattern Type**: Choose from dropdown menu
- **Pattern Scale**: 0.5x to 3x (base size)
- **Pattern Density**: 0.3x to 3x (additional multiplier)

### FlowAngle Controls
- **Sides (n)**: 1-12 vertices
- **Curve Factor**: -3.0 to 1.0 (curve tightness)
- **Handle Angle**: 10-170° (vertex sharpness)
- **Rotation**: 0-360° (shape orientation)
- **Show Guides**: Toggle construction geometry

## Try These Examples

### Dotted Triquetra
1. Click "Triquetra" preset
2. Select "Dots" pattern
3. Adjust Pattern Density to 1.5
4. Watch dots cluster in tighter curves

### Stippled Flower
1. Click "Flower" preset
2. Select "Stipple" pattern
3. Adjust Curve Factor to -1.0
4. See organic texture emerge

### Lined Star
1. Click "Star" preset
2. Select "Lines" pattern
3. Watch lines rotate with curve angle
4. Adjust Pattern Scale for effect

### Wave Smooth
1. Click "Smooth" preset
2. Select "Waves" pattern
3. Set Pattern Density to 2.0
4. Flowing texture follows curves

## Technical Highlights

### SVG Pattern System
```javascript
<pattern id="pattern-dots" patternUnits="userSpaceOnUse">
  <circle cx="..." cy="..." r="..." />
</pattern>

<path d="..." fill="url(#pattern-dots)" opacity="0.7"/>
```

### Adaptive Density
```javascript
const densityFactor = Math.abs(curveFactor) * 0.5 + 1;
const adjustedSize = baseSize / (density * densityFactor);
```

### Layered Rendering
1. Base fill (solid color)
2. Pattern overlay (reduced opacity)
3. Stroke outline (crisp edges)
4. Guides (when enabled)

## What Makes This Special

### 1. Geometric Harmony
Patterns aren't just decoration - they **respond to the shape's geometry**:
- Tighter curves = denser patterns
- Pattern rotation follows curve direction (Lines pattern)
- Wave patterns flow with shape curvature

### 2. User Control
Three levels of pattern control:
- **Type**: Choose pattern style
- **Scale**: Adjust overall size
- **Density**: Fine-tune repetition

### 3. Real-Time Preview
Every parameter change instantly updates the pattern rendering.

## Downloads

Both download options work with patterns:
- **Download SVG**: Vector file with embedded pattern definitions
- **Download PNG**: Rasterized 2x resolution

Filenames include parameters: `flowangle-n3-c-0.66-a60.svg`

## What's Different from Original

**Removed** (to focus on patterns):
- Pulse animations
- Keyframe timeline
- URL sharing
- Constraint manager

**Added**:
- 7 pattern types
- Adaptive pattern density
- Pattern scale control
- Pattern density control
- Curve-responsive behavior

## Explore the Patterns

### Dots Pattern
- Perfect for highlighting lobes and petals
- Clean, modern look
- Great for n=3 to n=8

### Lines Pattern
- Emphasizes direction and flow
- Angle adapts to curve
- Excellent for angular shapes (n=5, n=7)

### Crosshatch
- Classic engraving style
- Creates depth and shading effect
- Works well with all shapes

### Stippling
- Organic, hand-drawn feel
- Random variation adds character
- Beautiful with flower patterns

### Waves
- Flowing, dynamic texture
- Follows curve naturally
- Best with smooth curves (c > -1.0)

### Gradient + Dots
- Modern hybrid approach
- Adds depth with gradients
- Dots provide texture detail

## Next Steps

### Experiment with:
1. **Extreme Density**: Try 3.0 density on Triquetra with Stippling
2. **Large Scale**: Set scale to 3.0 with Waves on Flower
3. **Tight Curves**: Use c=-2.0 with Crosshatch to see adaptive density
4. **Guide Mode**: Enable guides to see how patterns interact with geometry

### Ideas to Explore:
- Try all patterns with each preset
- Find the "sweet spot" for each pattern type
- Combine extreme parameters (high sides + tight curve + dense pattern)
- Compare solid fill to patterns on same shape

## Tips

1. **Start Simple**: Begin with Triquetra + Dots
2. **Adjust Gradually**: Change one parameter at a time
3. **Use Guides**: They help understand pattern placement
4. **Save Your Work**: Download SVGs of interesting combinations
5. **Try Extremes**: Don't be afraid to max out density or scale

## Questions?

Check **`SHADING_PATTERNS_NOTES.md`** for:
- Detailed pattern implementation
- SVG code examples
- Technical specifications
- Formula explanations
- Future enhancement ideas

---

**Have fun creating textured FlowAngle shapes!** 🎨

Your patterns respond to the curves, creating a unique relationship between form and texture that makes each shape visually interesting and geometrically cohesive.
