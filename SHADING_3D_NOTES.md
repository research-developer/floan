# FlowAngle 3D Depth Shading Explorer - Technical Notes

**Team 2 Deliverable**
**Date:** November 9, 2025
**File:** `shading_test_3d.html`

---

## Overview

This implementation creates realistic 3D depth and lighting effects for FlowAngle curves using simulated surface normals, virtual light sources, and physically-based lighting calculations (Phong reflection model).

---

## Core Approach

### 1. Surface Normal Calculation

**Method:** Calculate tangent vectors along the Bezier curves, then derive perpendicular normals.

```javascript
function calculateSurfaceNormal(t, points, tangents) {
    const tangent = tangents[Math.floor(t * (tangents.length - 1))];

    // Normal is perpendicular to tangent (2D rotation by 90°)
    const normal = {
        x: -tangent.y,  // Perpendicular vector
        y: tangent.x
    };

    // Normalize to unit vector
    const len = Math.sqrt(normal.x * normal.x + normal.y * normal.y);
    return { x: normal.x / len, y: normal.y / len };
}
```

**Key Insight:** The curve's tangent direction determines the surface orientation. Sharper handle angles create more dramatic normal changes, resulting in stronger lighting effects.

---

### 2. 3D Lighting Model (Phong Reflection)

**Components:**

1. **Ambient Light** - Base illumination (no directional dependence)
2. **Diffuse Reflection** - Lambertian shading (matte surface)
3. **Specular Highlights** - Phong specular (glossy reflections)

```javascript
function calculateLighting(point, normal, lightPos, intensity, ambient, spec, shine) {
    // 1. Vector from surface to light
    const toLight = normalize({
        x: lightPos.x - point.x,
        y: lightPos.y - point.y,
        z: lightPos.z
    });

    // 2. Extend 2D normal into 3D space
    const normal3d = normalize({
        x: normal.x,
        y: normal.y,
        z: depthAmount / 100.0  // Surface "pops out" of page
    });

    // 3. Diffuse component (Lambert's cosine law)
    const diffuse = max(0, dot(normal3d, toLight));

    // 4. Specular component (Phong reflection)
    const reflect = 2 * dot(normal3d, toLight) * normal3d - toLight;
    const viewDir = {x: 0, y: 0, z: 1};  // Camera looks down
    const specular = pow(max(0, dot(reflect, viewDir)), shine);

    // 5. Combine all lighting
    return ambient + (diffuse * intensity) + (specular * spec * intensity);
}
```

---

### 3. Virtual Light Source

**Position Control:** 9 preset positions (top-left, center, etc.) plus elevation (Z-axis)

```javascript
function getLightPosition3D(size = 600) {
    const positions = {
        'top-left': { x: size * 0.2, y: size * 0.2 },
        'top-center': { x: size * 0.5, y: size * 0.2 },
        // ... 7 more positions
    };

    return {
        x: positions[selection].x,
        y: positions[selection].y,
        z: elevation  // Height above canvas
    };
}
```

**Effect:** Higher elevation = softer, more diffuse lighting. Lower elevation = sharper, more dramatic shadows.

---

### 4. Rendering Strategy

**Challenge:** SVG doesn't support per-pixel lighting, so we approximate with segmented gradients.

**Solution:** Break each Bezier curve into 50 small line segments, calculate lighting per segment, and color accordingly.

```javascript
// 50 segments per curve for smooth gradients
const segments = 50;

for (let i = 0; i < allPoints.length - 1; i++) {
    const lighting = calculateLighting(point, normal, lightPos, ...);

    // Map lighting value (0-1) to color gradient
    if (lighting < 0.5) {
        color = interpolate(shadowColor, baseColor, lighting * 2);
    } else {
        color = interpolate(baseColor, highlightColor, (lighting - 0.5) * 2);
    }

    // Draw colored segment
    svg += `<line stroke="${color}" ... />`;
}
```

---

## Effect Modes

### 1. **Embossed (Raised)**
- Normals point outward from curve
- Light hits "raised" surfaces → highlights
- Shadowed on opposite side
- **Best for:** Buttons, raised text, coins

### 2. **Debossed (Recessed)**
- Normals reversed (inverted)
- Creates "carved in" appearance
- Shadows where embossed has highlights
- **Best for:** Engraving, stamped effects

### 3. **Beveled Edge**
- Modulates lighting based on curve position
- Creates edge-like highlights
- Formula: `lighting = lighting * 0.7 + edgeFactor * 0.3`
- **Best for:** Borders, frames, badges

---

## Parameter Effects on Shading

### Handle Angle Impact

**Sharper angles (10°-30°):**
- Rapid normal changes
- High contrast lighting
- Dramatic 3D effect
- Sharp highlights and deep shadows

**Wider angles (140°-170°):**
- Gradual normal changes
- Soft, smooth shading
- Subtle 3D effect
- Gentle gradients

### Curve Factor Impact

**Negative values (-3 to -0.5):**
- Inward curves
- Concave surfaces
- Collect light differently than convex

**Positive values (0 to 1):**
- Outward bulges
- Convex surfaces
- Broader highlight areas

---

## Lighting Controls Explained

| Control | Range | Effect |
|---------|-------|--------|
| **Light Position** | 9 positions | Direction of highlights/shadows |
| **Light Intensity** | 0 - 2.0 | Brightness of diffuse/specular |
| **Light Elevation** | 0 - 500 | Height above surface (Z) |
| **Ambient Light** | 0 - 1.0 | Base brightness (no shadows) |
| **Depth Amount** | 0 - 100 | Surface "pops out" strength |
| **Specularity** | 0 - 1.0 | Glossiness (shininess) |
| **Shininess** | 1 - 50 | Specular highlight focus |

---

## Visual Presets

### Dramatic Light
```javascript
{
    position: 'top-left',
    intensity: 1.5,
    elevation: 150,
    ambient: 0.1,      // Low ambient = dark shadows
    spec: 0.8,         // High specularity
    shine: 20,         // Focused highlights
    depth: 50          // Strong 3D pop
}
```

### Soft Light
```javascript
{
    position: 'center',
    intensity: 0.8,
    elevation: 300,    // High elevation = soft
    ambient: 0.5,      // High ambient = gentle
    spec: 0.2,         // Low specularity
    shine: 5,          // Diffuse highlights
    depth: 20          // Subtle depth
}
```

### Metallic
```javascript
{
    spec: 1.0,         // Maximum specularity
    shine: 30,         // Very focused highlights
    ambient: 0.2       // Dark base for contrast
}
```

### Stone
```javascript
{
    spec: 0.1,         // Minimal specularity (matte)
    shine: 3,          // Very diffuse
    ambient: 0.4       // Medium base light
}
```

---

## Technical Implementation Details

### Bezier Curve Derivative (for Tangents)

For cubic Bezier with control points P0, P1, P2, P3:

```
Point(t) = (1-t)³P0 + 3(1-t)²t·P1 + 3(1-t)t²·P2 + t³·P3

Tangent(t) = dP/dt = 3(1-t)²(P1-P0) + 6(1-t)t(P2-P1) + 3t²(P3-P2)
```

This gives us the curve direction at any point `t`, from which we derive the perpendicular normal.

### Color Interpolation

```javascript
function interpolateColor(color1, color2, factor) {
    const c1 = hexToRgb(color1);
    const c2 = hexToRgb(color2);

    return {
        r: c1.r + (c2.r - c1.r) * factor,
        g: c1.g + (c2.g - c1.g) * factor,
        b: c1.b + (c2.b - c1.b) * factor
    };
}
```

**Gradient mapping:**
- `lighting < 0.5` → Shadow to Base color
- `lighting >= 0.5` → Base to Highlight color

---

## Debugging Features

### Show Surface Normals
- Toggle to visualize normal vectors
- Pink lines perpendicular to curve
- Helps understand lighting direction
- Update frequency: every 5th segment

### Show Light Position
- Displays glowing indicator at light position
- Visual aid for understanding light angle
- Positioned as percentage of canvas size

---

## Performance Considerations

**Segment Count:** Currently 50 segments per curve
- **Higher (100+):** Smoother gradients, slower rendering
- **Lower (20-30):** Faster, more "banded" appearance
- **Sweet spot:** 40-60 for most cases

**Calculation Complexity:**
- O(n × segments) where n = number of sides
- Each segment: ~15 floating point operations
- Real-time updates work smoothly up to n=12

---

## Future Enhancements

1. **Gradient meshes** - True SVG gradients instead of segments
2. **Shadow casting** - Inter-shape shadows
3. **Environment mapping** - Reflections from virtual environment
4. **Texture mapping** - Apply images with lighting
5. **Normal mapping** - Fine-detail bumps without geometry
6. **Subsurface scattering** - For translucent materials
7. **Global illumination** - Bounced light between surfaces

---

## Usage Examples

### Creating Embossed Logo
1. Set handleAngle to 45° (moderate sharpness)
2. Select "Embossed" mode
3. Light position: "top-left"
4. Intensity: 1.2
5. Depth: 40
6. Specularity: 0.6

### Simulating Carved Stone
1. Set handleAngle to 30° (sharp details)
2. Select "Debossed" mode
3. Light position: "top-center"
4. Preset: "Stone"
5. Base color: #8B7355 (tan)
6. Shadow color: #5C4033 (brown)

### Metallic Badge
1. Set handleAngle to 60°
2. Select "Beveled" mode
3. Preset: "Metallic"
4. Base color: #C0C0C0 (silver)
5. Highlight color: #FFFFFF (white)
6. Shadow color: #404040 (dark gray)

---

## Mathematical Foundations

### Dot Product (for lighting calculations)
```
a · b = ax·bx + ay·by + az·bz = |a||b|cos(θ)
```
Used for:
- Diffuse lighting: `max(0, normal · lightDir)`
- Specular lighting: `max(0, reflect · viewDir)^shininess`

### Vector Reflection
```
R = 2(N · L)N - L

Where:
  R = reflected vector
  N = surface normal
  L = light direction
```

### Lambert's Cosine Law
```
Intensity = I₀ × cos(θ)

Where θ is angle between normal and light direction
```

---

## Color Theory in 3D Shading

**Three-color gradient system:**
1. **Shadow Color** - Darkest areas (lighting < 0.5)
2. **Base Color** - Mid-tone (lighting ≈ 0.5)
3. **Highlight Color** - Brightest spots (lighting > 0.5)

**Recommended combinations:**

**Natural Stone:**
- Shadow: Dark brown (#5C4033)
- Base: Tan (#D2B48C)
- Highlight: Cream (#F5DEB3)

**Metal:**
- Shadow: Dark gray (#404040)
- Base: Silver (#C0C0C0)
- Highlight: White (#FFFFFF)

**Plastic:**
- Shadow: 50% darker than base
- Base: Any saturated color
- Highlight: 80% white blend

---

## Known Limitations

1. **No self-shadowing** - Curves don't cast shadows on themselves
2. **No occlusion** - Overlapping areas don't block light
3. **Discrete segments** - Not true continuous gradients
4. **2D-to-3D mapping** - Depth is simulated, not geometric
5. **Single light source** - No multi-light scenarios (yet)

---

## Conclusion

This implementation successfully creates convincing 3D depth effects using:
- Surface normal calculation from curve tangents
- Physically-based Phong lighting model
- Multi-component color gradients
- Interactive light positioning

**Key achievement:** The handleAngle parameter directly impacts lighting drama - sharper angles create more pronounced 3D effects, validating the core design goal.

**Success metrics:**
✅ Working 3D-looking FlowAngle shapes
✅ Controllable light source position (9 positions + elevation)
✅ Realistic highlights and shadows
✅ Responsive to handleAngle changes
✅ Three effect modes (embossed/debossed/beveled)
✅ Material presets (dramatic/soft/metallic/stone)
✅ Debug visualization (normals + light position)

---

## File Location

**Primary File:** `/Users/preston/research-developer/svGen-shading/shading_test_3d.html`

**How to Use:**
1. Open `shading_test_3d.html` in a modern web browser
2. Adjust shape parameters (sides, curve factor, handle angle, rotation)
3. Modify lighting controls to see real-time 3D effects
4. Try preset combinations for different materials
5. Enable "Show Surface Normals" to understand the math
6. Enable "Show Light Position" to visualize light source

**Dependencies:** None - fully self-contained HTML file

---

**Team 2 - Mission Accomplished! 🎨✨**
