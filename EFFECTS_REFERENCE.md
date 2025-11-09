# FlowAngle Multi-Layer Shading - Effects Reference

## Visual Guide to All 4 Effects

This guide shows the key characteristics of each shading effect and when to use them.

---

## 1. Inner Shadow Effect

### Visual Characteristics
```
┌─────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ ← Outer edge (lighter)
│ ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░ │
│ ░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░ │
│ ░░▒▒▓▓████████████████▓▓▒▒░░ │
│ ░░▒▒▓▓████░░░░░░██████▓▓▒▒░░ │ ← Inner core (darker)
│ ░░▒▒▓▓████████████████▓▓▒▒░░ │
│ ░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░ │
│ ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└─────────────────────────────────┘
```

### Technical Parameters
- **Layer Count:** 7
- **Offset Direction:** Inward (negative)
- **Offset Distance:** 12px
- **Blend Mode:** Multiply
- **Color Range:** Dark (RGB 100) → Light (RGB 200)
- **Opacity Range:** 0.2 → 0.8

### Layering Strategy
```
Layer 7 (innermost):  offset = -12px  |  color = rgb(200, 200, 250)  |  opacity = 0.8
Layer 6:              offset = -10px  |  color = rgb(183, 183, 233)  |  opacity = 0.7
Layer 5:              offset = -8px   |  color = rgb(166, 166, 216)  |  opacity = 0.6
Layer 4:              offset = -6px   |  color = rgb(149, 149, 199)  |  opacity = 0.5
Layer 3:              offset = -4px   |  color = rgb(133, 133, 183)  |  opacity = 0.4
Layer 2:              offset = -2px   |  color = rgb(116, 116, 166)  |  opacity = 0.3
Layer 1 (outermost):  offset = 0px    |  color = rgb(100, 100, 150)  |  opacity = 0.2
Top Shape:            offset = 0px    |  color = #4a90e2            |  opacity = 0.9
```

### Best Use Cases
- Recessed buttons or panels
- Carved text or symbols
- Inset decorative elements
- "Pressed" or "hollow" appearance

### Tips
- Use higher layer counts (8-10) for smoother gradients
- Multiply blend mode creates natural shadow darkening
- Increase offset for more dramatic depth

---

## 2. Outer Glow Effect

### Visual Characteristics
```
┌─────────────────────────────────┐
│ ::::::::::::::::::::::::::::::::│ ← Faint outer glow
│ ::::::░░░░░░░░░░░░░░░░░░░::::::│
│ ::::░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░::::  │
│ ::░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░::  │
│ ::░░▒▒▓▓████████████▓▓▒▒░░::  │ ← Bright core
│ ::░░▒▒▓▓████████████▓▓▒▒░░::  │
│ ::░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░::  │
│ ::::░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░::::  │
│ ::::::░░░░░░░░░░░░░░░░░░░::::::│
│ ::::::::::::::::::::::::::::::::│
└─────────────────────────────────┘
```

### Technical Parameters
- **Layer Count:** 8
- **Offset Direction:** Outward (positive)
- **Offset Distance:** 15px
- **Blend Mode:** Screen
- **Color Range:** Medium (RGB 100) → Bright (RGB 255)
- **Opacity Range:** 0.5 → 0.1
- **Filter:** Blur (light)

### Layering Strategy
```
Layer 8 (outermost):  offset = 15px  |  color = rgb(100, 150, 200)  |  opacity = 0.1  |  blur
Layer 7:              offset = 13px  |  color = rgb(114, 164, 214)  |  opacity = 0.15 |  blur
Layer 6:              offset = 11px  |  color = rgb(128, 178, 228)  |  opacity = 0.2  |  blur
Layer 5:              offset = 9px   |  color = rgb(142, 192, 242)  |  opacity = 0.25 |  blur
Layer 4:              offset = 7px   |  color = rgb(156, 206, 255)  |  opacity = 0.3
Layer 3:              offset = 5px   |  color = rgb(170, 220, 255)  |  opacity = 0.35
Layer 2:              offset = 3px   |  color = rgb(184, 234, 255)  |  opacity = 0.4
Layer 1 (innermost):  offset = 1px   |  color = rgb(198, 248, 255)  |  opacity = 0.45
Core Shape:           offset = 0px   |  color = #87ceeb            |  opacity = 0.95
```

### Best Use Cases
- Neon signs or luminous objects
- Ethereal or magical effects
- Light emanation or energy fields
- Glowing UI elements

### Tips
- Screen blend mode creates additive light
- Blur filters on outer layers enhance glow
- Higher layer counts create smoother halos

---

## 3. Depth Effect (Primary Innovation)

### Visual Characteristics
```
┌─────────────────────────────────┐
│                                 │
│    ██████████████████████       │ ← Layer 10 (lightest, front)
│   █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█      │ ← Layer 9
│  █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█     │ ← Layer 8
│  █▓▒░░░░░░░░░░░░░░░░░░░▒▓█     │ ← Layer 7
│ █▓▒░::::::::::::::::::::░▒▓█    │ ← Layer 6
│ █▓▒░:...................░▒▓█    │ ← Layer 5
│ █▓▒░::::::::::::::::::::░▒▓█    │ ← Layer 4
│  █▓▒░░░░░░░░░░░░░░░░░░░▒▓█     │ ← Layer 3
│  █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█     │ ← Layer 2
│   █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█      │ ← Layer 1 (darkest, back)
│    ██████████████████████       │
│                                 │
└─────────────────────────────────┘
```

### Technical Parameters
- **Layer Count:** 10
- **Offset Direction:** Backward (negative, parallel)
- **Offset Distance:** 8px
- **Blend Mode:** Normal
- **Color Palette:** 10 carefully chosen colors
- **Opacity Range:** 0.6 → 0.9
- **Strokes:** Subtle black borders between layers

### Color Palette (Dark to Light)
```
Layer 1:  #1a2332  ███  (darkest - deep blue)
Layer 2:  #2c3e50  ███  (dark blue-grey)
Layer 3:  #34495e  ███  (medium dark)
Layer 4:  #4a6280  ███  (steel blue)
Layer 5:  #5a7a9f  ███  (mid blue)
Layer 6:  #6a8fc0  ███  (medium blue)
Layer 7:  #7aa5d5  ███  (light blue)
Layer 8:  #87ceeb  ███  (sky blue)
Layer 9:  #9dd8f0  ███  (lighter sky)
Layer 10: #b3e5fc  ███  (lightest - pale cyan)
```

### Layering Strategy
```
Layer 10 (front):   offset = 0px   |  color = #b3e5fc  |  opacity = 0.9  |  highlight stroke
Layer 9:            offset = -1px  |  color = #9dd8f0  |  opacity = 0.86 |  subtle stroke
Layer 8:            offset = -2px  |  color = #87ceeb  |  opacity = 0.82 |  subtle stroke
Layer 7:            offset = -3px  |  color = #7aa5d5  |  opacity = 0.78
Layer 6:            offset = -4px  |  color = #6a8fc0  |  opacity = 0.74
Layer 5:            offset = -5px  |  color = #5a7a9f  |  opacity = 0.70
Layer 4:            offset = -6px  |  color = #4a6280  |  opacity = 0.66
Layer 3:            offset = -7px  |  color = #34495e  |  opacity = 0.62
Layer 2:            offset = -8px  |  color = #2c3e50  |  opacity = 0.58
Layer 1 (back):     offset = -9px  |  color = #1a2332  |  opacity = 0.6  |  base layer
```

### Best Use Cases
- **Primary use:** Dramatic 3D dimensional art
- Stacked paper effects
- Layered card designs
- Architectural depth
- Abstract geometric art

### Innovation Points
- **10-color gradient:** Most sophisticated color progression
- **Parallel offset:** Creates true "stacked" appearance
- **Layer separation strokes:** Defines boundaries between layers
- **Top highlight:** White stroke adds final dimension
- **Carefully tuned opacity:** Each layer perfectly weighted

### Tips
- This is the recommended effect for best results
- Use full 10 layers for maximum impact
- Normal blend mode preserves color fidelity
- Offset of 8-10px creates optimal layer spacing

---

## 4. Emboss Effect

### Visual Characteristics
```
┌─────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░           │ ← Highlight (top-left)
│ ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            │
│ ░▓██████████████████            │
│ ░▓██████████████████            │
│  ▓██████████████████            │
│  ████████████████████▓░         │ ← Main surface
│  ████████████████████▓▓░        │
│  ████████████████████▓▓░        │
│            ████████████▓▓░░     │ ← Shadow (bottom-right)
│             ░░░░░░░░░░░░░░      │
└─────────────────────────────────┘
```

### Technical Parameters
- **Layer Count:** 5
- **Offset Direction:** Multi-directional
- **Offset Distance:** 10px
- **Blend Mode:** Overlay
- **Components:** Shadow + Mid-tones + Highlight
- **Filters:** Medium blur on shadow/highlight

### Three-Layer System

**1. Shadow Layer (Bottom-Right)**
```
Position:    transform="translate(10px, 10px)"
Color:       #1a1a1a (very dark)
Opacity:     0.6
Filter:      blur-medium (4px)
Purpose:     Creates depth below surface
```

**2. Mid-Tone Layers (5 layers)**
```
Layer 5:  offset = 0px    |  color = rgb(200, 200, 220)  |  opacity = 0.8
Layer 4:  offset = -0.6px |  color = rgb(184, 184, 204)  |  opacity = 0.725
Layer 3:  offset = -1.2px |  color = rgb(168, 168, 188)  |  opacity = 0.65
Layer 2:  offset = -1.8px |  color = rgb(152, 152, 172)  |  opacity = 0.575
Layer 1:  offset = -2.4px |  color = rgb(136, 136, 156)  |  opacity = 0.5
Layer 0:  offset = -3px   |  color = rgb(120, 120, 140)  |  opacity = 0.5
```

**3. Highlight Layer (Top-Left)**
```
Position:    transform="translate(-3px, -3px)"
Color:       #ffffff (white stroke only)
Opacity:     0.6
Filter:      blur-light (2px)
Stroke:      2px white
Fill:        none
Purpose:     Creates raised edge effect
```

### Layering Strategy
```
Step 1: Draw shadow (bottom-right, blurred)
Step 2: Draw 5 mid-tone gradient layers
Step 3: Draw highlight stroke (top-left, blurred)
Step 4: Draw main shape outline
```

### Best Use Cases
- Bas-relief or carved surfaces
- Raised buttons or panels
- Sculptural appearance
- Tactile or textured effects
- Metallic or stone surfaces

### Tips
- Overlay blend mode integrates all layers
- Fewer layers (5) works well for this effect
- Shadow and highlight positioning creates light direction
- Blur filters soften edges for realism

---

## Comparison Matrix

| Feature | Inner Shadow | Outer Glow | Depth | Emboss |
|---------|-------------|------------|-------|--------|
| **Layers** | 7 | 8 | 10 | 5 |
| **Offset** | Inward | Outward | Backward | Multi |
| **Distance** | 12px | 15px | 8px | 10px |
| **Blend** | Multiply | Screen | Normal | Overlay |
| **Filters** | None | Blur | None | Blur |
| **Colors** | 2 gradient | 2 gradient | 10 palette | 3 zones |
| **Opacity** | 0.2-0.8 | 0.1-0.5 | 0.6-0.9 | 0.5-0.8 |
| **Complexity** | Medium | Medium | High | High |
| **Best For** | Recessed | Luminous | 3D Depth | Relief |

---

## Effect Selection Guide

### Choose Inner Shadow for:
- ❌ Recessed buttons
- ❌ Carved text
- ❌ "Pressed in" appearance
- ❌ Hollow or inset elements

### Choose Outer Glow for:
- ✨ Neon effects
- ✨ Luminous objects
- ✨ Energy fields
- ✨ Glowing UI elements

### Choose Depth for:
- 🎨 Maximum dimensional impact
- 🎨 Artistic stacked effects
- 🎨 Dramatic 3D appearance
- 🎨 Professional results

### Choose Emboss for:
- 🗿 Sculptural surfaces
- 🗿 Raised elements
- 🗿 Tactile appearance
- 🗿 Metallic finishes

---

## Quick Reference: Parameter Cheat Sheet

### Inner Shadow Quick Config
```javascript
layers: 7
offset: 12
blend: 'multiply'
shape: any (works with all)
```

### Outer Glow Quick Config
```javascript
layers: 8
offset: 15
blend: 'screen'
shape: smooth curves work best
```

### Depth Quick Config (Recommended)
```javascript
layers: 10
offset: 8
blend: 'normal'
shape: any (optimal for all)
```

### Emboss Quick Config
```javascript
layers: 5
offset: 10
blend: 'overlay'
shape: simple shapes work best
```

---

## Advanced Tips

### Combining Effects
While the tool focuses on one effect at a time, you can manually create combinations:

1. Load an effect preset
2. Manually adjust parameters
3. Try different blend modes
4. Export and layer in vector editor

### Optimizing for Different Shapes

**For n=3 (Triquetra):**
- Depth effect shows curves beautifully
- Higher offset (10-12px) for dramatic effect

**For n=5 (Star):**
- Emboss works great for sharp points
- Lower offset (6-8px) for defined edges

**For n=6+ (Flower):**
- Outer glow creates ethereal petals
- Medium offset (12-15px) for smooth halos

### Performance Considerations

**Fast rendering (1-5 layers):**
- Quick updates
- Simpler effects
- Good for experimentation

**Balanced (6-8 layers):**
- Good quality
- Smooth gradients
- Recommended for most uses

**Maximum quality (9-10 layers):**
- Smoothest results
- Slight lag on updates
- Best for final export

---

**Ready to explore all four effects!** 🎨
