# Parametric Shading Explorer - Documentation

**Team 3: Parametric Shading Explorer**
**Goal:** Create shading that dynamically responds to FlowAngle parameters

## Overview

The Parametric Shading Explorer creates a **visual language** where FlowAngle parameters can be "read" directly from the colors and shading of the generated shapes. This makes the abstract mathematical parameters (curveFactor, handleAngle, sides) immediately perceivable and intuitive.

## Core Concept

Instead of arbitrary aesthetic choices, every color decision encodes specific parameter information:

- **Hue/Color Temperature** → Curve Factor
- **Brightness/Lightness** → Handle Angle
- **Saturation** → Number of Sides
- **Hue Rotation** → Segment Position (optional)

## Implementation Details

### 1. Color Mapping System

#### Curve Factor → Hue (Color Temperature)
**Range:** -3.0 to +1.0
**Visual Encoding:** Cool → Warm spectrum

The curve factor determines the base color temperature using interpolation through predefined color schemes:

```javascript
// Example: Thermal scheme
curveFactor: -3.0  → Deep Blue (cold/inward curve)
curveFactor: -1.0  → Cyan/Green
curveFactor:  0.0  → Yellow (neutral)
curveFactor: +0.5  → Orange
curveFactor: +1.0  → Red (hot/outward curve)
```

**Why This Works:**
- Negative curves (inward) feel "cold" and contracting → blues/cyans
- Positive curves (outward) feel "warm" and expanding → oranges/reds
- Creates intuitive visual metaphor for curve direction

#### Handle Angle → Brightness
**Range:** 10° to 170°
**Visual Encoding:** Dark (sharp) → Bright (gentle)

Handle angle controls the lightness component of the HSL color:

```javascript
brightness = 20% + (angleNorm * 60%)  // Maps 10°-170° to 20%-80% lightness
```

**Why This Works:**
- Sharp angles (10°-40°) = darker colors = "intense/focused"
- Gentle angles (140°-170°) = brighter colors = "soft/diffuse"
- Visual analogy to lighting: sharp angles create shadows, gentle curves reflect light

#### Sides Count → Saturation
**Range:** 3 to 12 sides
**Visual Encoding:** Desaturated → Vibrant

Side count controls color saturation:

```javascript
saturation = 30% + (sidesNorm * 70%)  // Maps 3-12 sides to 30%-100% saturation
```

**Why This Works:**
- Fewer sides (3-4) = simpler shapes = muted colors
- More sides (10-12) = complex shapes = rich, saturated colors
- Reflects the increasing visual richness of the form

### 2. Color Schemes

Five carefully designed schemes provide different visual contexts:

#### Thermal (Default)
**Best for:** General exploration, understanding curve direction
**Colors:** Deep Blue → Cyan → Yellow → Orange → Red
**Use case:** Most intuitive for beginners

#### Ocean
**Best for:** Subtle, cohesive palettes
**Colors:** Deep Ocean → Turquoise → Shallow Water
**Use case:** Calming, nature-inspired designs

#### Sunset
**Best for:** Warm, dramatic visuals
**Colors:** Deep Purple → Violet → Coral → Golden Orange
**Use case:** Artistic, atmospheric compositions

#### Forest
**Best for:** Monochromatic green exploration
**Colors:** Dark Forest Green → Light Green → Pale Green
**Use case:** Focused study of brightness and saturation effects

#### Rainbow
**Best for:** Maximum color variation
**Colors:** Violet → Blue → Green → Yellow → Orange → Red
**Use case:** Teaching, demonstrations, high-energy designs

### 3. Per-Segment Shading

When enabled, each segment receives a subtle hue rotation based on its position:

```javascript
hueShift = baseHue + (segmentIndex / totalSides) * 30°  // Up to 30° rotation
```

**Effect:**
- Creates a rainbow/gradient effect around the shape
- Makes individual segments distinguishable
- Adds depth and dimensionality
- Useful for analyzing segment-level geometry

### 4. Technical Implementation

#### Color Interpolation
Uses linear interpolation in RGB space for smooth transitions between color stops:

```javascript
function interpolateColor(color1, color2, t) {
    rgb1 = hexToRgb(color1)
    rgb2 = hexToRgb(color2)

    r = rgb1.r + (rgb2.r - rgb1.r) * t
    g = rgb1.g + (rgb2.g - rgb1.g) * t
    b = rgb1.b + (rgb2.b - rgb1.b) * t

    return rgbToHex(r, g, b)
}
```

#### HSL Manipulation
Final color adjustments use HSL for perceptual uniformity:

```javascript
function getColorForParams(curveFactor, handleAngle, sides, scheme, segmentIndex) {
    // 1. Get base hue from curve factor
    baseColor = interpolateFromScheme(curveFactor, scheme)
    hsl = rgbToHSL(baseColor)

    // 2. Calculate brightness from handle angle
    lightness = 20 + (angleNormalized * 60)

    // 3. Calculate saturation from sides
    saturation = 30 + (sidesNormalized * 70)

    // 4. Optional segment hue shift
    if (perSegmentShading) {
        hsl.h = (hsl.h + segmentOffset) % 360
    }

    return hsl(hsl.h, saturation%, lightness%)
}
```

## User Interface

### Control Panel
- **Parameter Controls:** Real-time sliders for all FlowAngle parameters
- **Color Scheme Selector:** Dropdown to switch between 5 color schemes
- **Display Options:**
  - Show Guides: Reveals geometric construction
  - Per-Segment Shading: Enables positional color variation
  - Show Stroke: Adds outline for clarity

### Info Panel (Right Side)

#### Current Parameters
Displays exact numerical values for all active parameters

#### Color Encoding Legend
Shows three gradient bars explaining the mapping:
1. **Curve Factor → Hue** (with -3.0 to +1.0 labels)
2. **Handle Angle → Brightness** (10° to 170° labels)
3. **Sides Count → Saturation** (3 to 12 labels)

#### "How to Read" Guide
Explains the visual encoding system in plain language

#### Active Color Display
Shows the current base color with hex code

## How to "Read" a Shape

### Quick Visual Analysis

1. **Look at the overall color temperature:**
   - Cool blues/cyans → Negative curve (flowing inward)
   - Warm oranges/reds → Positive curve (flowing outward)

2. **Check the brightness:**
   - Dark colors → Sharp handle angles (pointed features)
   - Bright colors → Gentle angles (smooth curves)

3. **Observe saturation:**
   - Muted/pastel → Few sides (3-5)
   - Vibrant/rich → Many sides (8-12)

4. **If per-segment shading is on:**
   - Rainbow effect → Consistent parameters across segments
   - Position in gradient → Which segment you're looking at

### Example Readings

**Deep Blue, Dark, Highly Saturated:**
- Curve: -2.0 to -3.0 (strong inward curve)
- Angle: 10°-30° (very sharp)
- Sides: 10-12 (complex polygon)
- **Form:** Complex star-like shape with tight curves

**Yellow, Medium Brightness, Medium Saturation:**
- Curve: ~0.0 (nearly neutral)
- Angle: ~90° (moderate)
- Sides: ~6 (hexagon)
- **Form:** Balanced, flower-like pattern

**Light Orange, Bright, Low Saturation:**
- Curve: +0.5 to +1.0 (outward bulging)
- Angle: 150°-170° (very gentle)
- Sides: 3-4 (simple)
- **Form:** Soft, rounded triangular/square shape

## Design Philosophy

### Information Before Aesthetics
While the results are visually pleasing, **every color choice carries meaning**. This isn't decoration—it's **data visualization through color**.

### Perceptual Consistency
Mappings follow natural human perception:
- Temperature metaphor (cold ← → warm)
- Light metaphor (dark ← → bright)
- Richness metaphor (muted ← → vibrant)

### Layered Encoding
Three independent visual channels (hue, lightness, saturation) allow **simultaneous display of three parameters** without interference.

### Educational Tool
The system teaches users to **see mathematics**. After working with the tool, users develop an intuitive sense of how parameters affect form.

## Use Cases

### 1. Parameter Exploration
Quickly understand the relationship between parameters by seeing color patterns emerge

### 2. Teaching & Learning
Demonstrate FlowAngle concepts with immediate visual feedback

### 3. Design Workflow
Use colors to organize and categorize different parameter ranges

### 4. Pattern Analysis
Identify similar shapes across different configurations by color similarity

### 5. Debugging
Quickly spot parameter anomalies through unexpected colors

## Technical Specifications

### File
- **Location:** `/Users/preston/research-developer/svGen-shading/shading_test_parametric.html`
- **Type:** Standalone HTML with embedded CSS and JavaScript
- **Dependencies:** None (vanilla JavaScript)
- **Size:** ~23KB

### Browser Compatibility
- Modern browsers with ES6 support
- SVG rendering support
- CSS Grid and Flexbox

### Performance
- Real-time rendering for parameter changes
- Efficient SVG path generation
- No external libraries or heavy computations

## Future Enhancements

### Potential Additions
1. **Gradient Fills:** Smooth color transitions within segments
2. **Animation:** Color morphing between states
3. **Custom Schemes:** User-defined color palettes
4. **Export:** Save color-coded SVGs with embedded parameter data
5. **Comparison Mode:** Side-by-side shapes with different encodings
6. **Accessibility:** Patterns/textures in addition to color for colorblind users

### Advanced Features
1. **3D Shading Simulation:** Lighting/shadow effects based on geometry
2. **Multi-parameter Encoding:** Encode more than 3 parameters using textures
3. **Interactive Legend:** Click colors to set parameters
4. **Inverse Mapping:** Click shape to read parameters

## Conclusion

The Parametric Shading Explorer transforms FlowAngle from a tool that generates shapes into a **visual language** where form and color unite to communicate mathematical relationships. It demonstrates that algorithmic art can be both beautiful and informative—where every hue has a reason and every shade tells a story.

---

**Created:** November 9, 2024
**Team:** Team 3 - Parametric Shading Explorer
**Status:** ✅ Complete and Functional
