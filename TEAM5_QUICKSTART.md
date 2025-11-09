# Team 5: Multi-Layer Shading Explorer - Quick Start

## What We Built

A powerful multi-layer shading system that creates depth and dimension for FlowAngle shapes through strategic layering, color gradients, and SVG effects.

## How to Use

### 1. Open the File
```bash
open /Users/preston/research-developer/svGen-shading/shading_test_layers.html
```

Or navigate to the svGen-shading directory and open `shading_test_layers.html` in your browser.

### 2. Try the Effect Presets

Click any of these buttons to see instant results:

- **Inner Shadow** - Creates a carved, recessed appearance
- **Outer Glow** - Adds a luminous halo effect
- **Depth Effect** - Stacks layers for dramatic 3D depth (recommended!)
- **Emboss** - Simulates a raised, sculptural surface

### 3. Experiment with Controls

**Shape Controls:**
- Sides: Change the polygon (3-12 sides)
- Curve Factor: Adjust the curve intensity
- Handle Angle: Modify the shape geometry

**Layer Controls:**
- Layer Count: 1-10 layers (try 7-10 for best results)
- Offset Distance: How far layers separate (8-15px optimal)
- Blend Mode: Try different compositing modes

**Shape Presets:**
- Triquetra (3-sided Celtic knot)
- Flower (6-petaled)
- Star (5-pointed)

### 4. Download Your Creation

Click "Download SVG" to save your layered artwork as a scalable vector graphic.

## Key Features

✨ **4 Distinct Effects**
- Inner Shadow (multiply blend, inward layers)
- Outer Glow (screen blend, outward halos)
- Depth (10-color gradient, stacked layers)
- Emboss (shadow + highlight positioning)

🎨 **10 Blend Modes**
- Normal, Multiply, Screen, Overlay
- Darken, Lighten, Color Dodge, Color Burn
- Hard Light, Soft Light

🔧 **SVG Filters**
- Gaussian blur (light, medium, heavy)
- Drop shadows
- Inner shadows

📐 **Parametric Control**
- Real-time preview
- Smooth gradients
- Optimal presets

## Technical Highlights

**Layering Strategy:**
```
Back Layer (darkest) → → → Front Layer (brightest)
     Offset -40px              Offset 0px
     Opacity 60%               Opacity 90%
```

**Color Gradients:**
- 10-step palette from dark blue to light cyan
- Automatic interpolation between layers
- Smooth, natural transitions

**SVG Filters:**
- Shared filter definitions (efficient)
- Gaussian blur for soft edges
- Drop/inner shadows for depth

## Best Practices

### For Inner Shadow:
- Use 7+ layers
- Offset: 10-15px
- Blend mode: Multiply
- Great for: Carved effects, recessed buttons

### For Outer Glow:
- Use 8+ layers
- Offset: 15-20px
- Blend mode: Screen
- Great for: Neon signs, luminous objects

### For Depth (Recommended):
- Use 10 layers
- Offset: 8-12px
- Blend mode: Normal
- Great for: 3D layered look, dimensional art

### For Emboss:
- Use 5-7 layers
- Offset: 10-12px
- Blend mode: Overlay
- Great for: Relief effects, textured surfaces

## Files Included

1. **shading_test_layers.html** (24KB)
   - Full interactive application
   - 628 lines of HTML/CSS/JavaScript
   - Self-contained, no dependencies

2. **SHADING_LAYERS_NOTES.md** (this file's companion)
   - Complete technical documentation
   - 452 lines of detailed explanations
   - Mathematical foundations
   - Code snippets and examples

3. **TEAM5_QUICKSTART.md** (this file)
   - Quick reference guide
   - Usage instructions
   - Best practices

## Quick Examples

### Example 1: Glowing Triquetra
```
1. Click "Triquetra" preset
2. Click "Outer Glow" effect
3. Set Layer Count to 10
4. Set Offset Distance to 20
5. Blend Mode: Screen
```

### Example 2: Carved Flower
```
1. Click "Flower" preset
2. Click "Inner Shadow" effect
3. Set Layer Count to 8
4. Set Offset Distance to 12
5. Blend Mode: Multiply
```

### Example 3: 3D Star
```
1. Click "Star" preset
2. Click "Depth Effect"
3. Set Layer Count to 10
4. Set Offset Distance to 10
5. Blend Mode: Normal
```

## Troubleshooting

**Layers look too faint:**
- Increase Layer Count
- Decrease Offset Distance
- Try a darker Blend Mode (Multiply, Darken)

**Effect too strong:**
- Decrease Layer Count
- Increase Offset Distance
- Try Blend Mode: Normal

**Want smoother gradients:**
- Increase Layer Count to 10
- Decrease Offset Distance
- Use the Depth Effect preset

## Next Steps

After exploring the basics:

1. **Combine effects** by manually adjusting after loading a preset
2. **Try extreme values** for layer count and offset
3. **Test all blend modes** with each effect
4. **Create your own shapes** with custom n/curve/angle values
5. **Export and edit** SVGs in vector graphics software

## Technical Architecture

```
┌─────────────────────────────────────┐
│   User Controls (HTML/CSS)          │
├─────────────────────────────────────┤
│   State Management (JavaScript)     │
├─────────────────────────────────────┤
│   Path Generation Engine            │
│   ├─ generateFlowAnglePath()        │
│   └─ Offset calculation             │
├─────────────────────────────────────┤
│   Effect Generators                 │
│   ├─ generateInnerShadowLayers()    │
│   ├─ generateOuterGlowLayers()      │
│   ├─ generateDepthLayers()          │
│   └─ generateEmbossLayers()         │
├─────────────────────────────────────┤
│   SVG Composition                   │
│   ├─ Filter definitions             │
│   ├─ Layer rendering                │
│   └─ Blend mode application         │
├─────────────────────────────────────┤
│   SVG Output (Download)             │
└─────────────────────────────────────┘
```

## Performance Notes

- **Optimal layer count:** 5-10 layers
- **Real-time updates:** Smooth on modern browsers
- **SVG file size:** ~2-10KB depending on layers
- **No external dependencies:** Pure HTML/CSS/JavaScript

## Credits

**Team 5: Multi-Layer Shading Explorer**
- Developed as part of FlowAngle research project
- Focus: Depth through strategic layering
- Date: November 9, 2025

## Learn More

See `SHADING_LAYERS_NOTES.md` for:
- Detailed technical explanations
- Mathematical foundations
- Code architecture
- Performance optimizations
- Future enhancement ideas

---

**Ready to create stunning layered FlowAngle art!** 🎨✨
