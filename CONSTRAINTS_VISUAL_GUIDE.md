# FlowAngle Constraints Manager - Visual Guide

## User Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔍 FlowAngle Constraints Manager                                            │
│ [Triquetra] [Flower] [Star] [Smooth]  │  n: 3  Curve: -0.66  Angle: 60°    │
│ [☐ Show Guides]  [☑ Highlight Problems]                                     │
└─────────────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────┬──────────────────────────────────────┐
│                                      │                                      │
│  ┌────────────────────┐              │  CURRENT LIMITS                      │
│  │     100%           │              │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  │  VALIDITY SCORE    │              │  Sides (n): 3                        │
│  │                    │              │  Curve Range: -3.00 to 1.00          │
│  │  ✓ All checks pass │              │  Angle Range: 10° to 170°            │
│  └────────────────────┘              │  Safe Curve: -2.50 to 0.65           │
│                                      │  Safe Angle: 20° to 120°             │
│                                      │                                      │
│                                      │  [💾 Capture Current Limits]         │
│         [SHAPE PREVIEW]              │                                      │
│                                      │  RECOMMENDATIONS                     │
│      Triquetra shape with            │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│      smooth curves shown             │  ✓ Current parameters produce        │
│      in center of canvas             │    valid geometry                    │
│                                      │                                      │
│                                      │  SAVED CONSTRAINTS (PER N)           │
│                                      │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                      │  ┌─────────────────────────────┐    │
│                                      │  │ n = 3                       │    │
│                                      │  │ Curve: -0.66                │    │
│                                      │  │ Angle: 60°                  │    │
│                                      │  │ [Apply] [Delete]            │    │
│                                      │  └─────────────────────────────┘    │
│                                      │                                      │
│                                      │  DETECTION DETAILS                   │
│                                      │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                      │  Vertices: 3                         │
│                                      │  Triangles: 3                        │
│                                      │  ✓ All checks passed                 │
│                                      │  Issues: 0                           │
│                                      │  Warnings: 0                         │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## Validity States Visual Reference

### 🟢 GREEN STATE (100-70% Valid)

**Appearance:**
```
┌────────────────────┐
│      100%          │  <- Large green text
│  VALIDITY SCORE    │
│                    │
│  ✓ All checks pass │  <- Green checkmark
└────────────────────┘

Shape Preview:
- Stroke: #4ade80 (bright green)
- Fill: rgba(74, 222, 128, 0.3) (light green)
- Width: 2px
- Appearance: Clean, smooth curves
```

**When You See This:**
- Parameters are in safe range
- No geometric issues detected
- Shape is ready to use
- All validation checks passed

---

### 🟡 YELLOW STATE (69-40% Warning)

**Appearance:**
```
┌────────────────────┐
│       65%          │  <- Large yellow text
│  VALIDITY SCORE    │
│                    │
│  ⚠️ Extreme curve  │  <- Yellow warning icon
│     factor value   │
│                    │
│  ⚠️ Control point  │
│     near edge      │
└────────────────────┘

Shape Preview:
- Stroke: #fbbf24 (bright yellow)
- Fill: rgba(251, 191, 36, 0.3) (light yellow)
- Width: 2px
- Appearance: Stressed geometry, still connected
```

**When You See This:**
- Parameters approaching limits
- Geometry is valid but stressed
- Consider adjusting values
- Check recommendations panel

---

### 🔴 RED STATE (39-0% Error)

**Appearance:**
```
┌────────────────────┐
│       25%          │  <- Large red text
│  VALIDITY SCORE    │
│                    │
│  ❌ Triangle edges │  <- Red X icon
│     intersect      │
│                    │
│  ❌ Curve self-    │
│     intersects     │
│                    │
│  ❌ Multiple lobes │
│     broken         │
└────────────────────┘

Shape Preview:
- Stroke: #ef4444 (bright red)
- Fill: rgba(239, 68, 68, 0.3) (light red)
- Width: 3px (thicker)
- Appearance: Broken, crossed curves, invalid
```

**When You See This:**
- Critical geometric errors
- Shape is invalid/broken
- Do not use these parameters
- Follow recommendations to fix

---

## Guide Visualization Examples

### With Guides ENABLED

```
      Shape with visible guides:

         ▲ (apex)              Triangle edges shown as
        /│\                    dashed cyan lines (#6cf)
       / │ \
      /  │  \                  Control points shown as:
     /   ●   \                 - Red dots (cp1)
    / ●     ● \                - Green dots (cp2)
   /           \
  ●─────────────●              Dashed lines connect
 (v1)         (v2)             vertices to control points

  Curved line shows            Shape curve is the
  final bezier path            thick colored line
```

### With Guides DISABLED

```
      Clean shape view:

    Just the final curved
    shape is shown with
    no helper geometry

    Perfect for seeing
    the actual result
    without clutter
```

---

## Preset Visual Reference

### Triquetra (n=3)
```
     ●
    / \
   /   \        Three-lobed Celtic knot
  ●─────●       Smooth, balanced curves
   \   /        Parameters: curve=-0.66, angle=60°
    \ /         Score: 100% ✓
     ●
```

### Flower (n=6)
```
    ●   ●
   ●  ●  ●       Six-petaled flower
  ●   ●   ●      Gentle inward curves
   ●  ●  ●       Parameters: curve=-0.8, angle=30°
    ●   ●        Score: 100% ✓
```

### Star (n=5)
```
      ●
    ●   ●        Five-pointed star
   ●     ●       Pronounced curves
  ●       ●      Parameters: curve=-1.2, angle=36°
   ●     ●       Score: 95-100% ✓
    ●   ●
      ●
```

### Smooth (n=8)
```
  ●   ●   ●
 ●    ●    ●    Eight-sided smooth blob
●     ●     ●   Very gentle curves
 ●    ●    ●    Parameters: curve=-0.5, angle=22.5°
  ●   ●   ●     Score: 100% ✓
```

---

## Control Panel Visual States

### Curve Factor Slider

**Safe Range:**
```
┌─────────────────────────────────────────┐
│ Curve Factor: -0.66                     │
├─────────────────────────────────────────┤
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│   ^                                      │
│   Current position                       │
│                                          │
│ Safe Range for n=3: -2.50 to 0.65       │
└─────────────────────────────────────────┘

Color zones (if visible):
RED  | YELLOW | GREEN | YELLOW | RED
-3.0   -2.5    -2.0     0.5     1.0
```

### Handle Angle Slider

**Safe Range:**
```
┌─────────────────────────────────────────┐
│ Handle Angle: 60°                        │
├─────────────────────────────────────────┤
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│       ^                                  │
│       Current position                   │
│                                          │
│ Safe Range for n=3: 20° to 120°         │
└─────────────────────────────────────────┘

Color zones (if visible):
RED  | YELLOW | GREEN  | YELLOW | RED
10°    20°     30°       120°    170°
```

---

## Issue Message Examples

### ✓ Good Messages (Green Background)
```
┌────────────────────────────────────────┐
│ ✓ All checks passed                    │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ ✓ Current parameters produce valid     │
│   geometry                             │
└────────────────────────────────────────┘
```

### ⚠️ Warning Messages (Yellow Background)
```
┌────────────────────────────────────────┐
│ ⚠️ Extreme curve factor value          │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ ⚠️ Lobe 2: Control points outside      │
│    triangle                            │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ ⚠️ Lobe 1: Control point near edge     │
└────────────────────────────────────────┘
```

### ❌ Error Messages (Red Background)
```
┌────────────────────────────────────────┐
│ ❌ Guide triangle edges intersect      │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ ❌ Lobe 3: Curve self-intersects       │
└────────────────────────────────────────┘
```

---

## Recommendation Examples

### For Valid State
```
┌────────────────────────────────────────┐
│ RECOMMENDATIONS                        │
├────────────────────────────────────────┤
│ ✓ Current parameters produce valid     │
│   geometry                             │
└────────────────────────────────────────┘
```

### For Warning State
```
┌────────────────────────────────────────┐
│ RECOMMENDATIONS                        │
├────────────────────────────────────────┤
│ ⚠️ For n=12, try curve factor between  │
│    -1.15 and 0.20                      │
│                                        │
│ ⚠️ For n=12, try handle angle between  │
│    38° and 75°                         │
└────────────────────────────────────────┘
```

---

## Saved Constraint Card

```
┌─────────────────────────────────────┐
│ n = 6                    [Apply] [×] │
├─────────────────────────────────────┤
│ Curve: -0.80                        │
│ Angle: 30°                          │
│ Rotation: 0°                        │
└─────────────────────────────────────┘
```

**Hover State:**
```
┌─────────────────────────────────────┐
│ n = 6                    [APPLY] [×] │ <- Buttons highlight
├─────────────────────────────────────┤
│ Curve: -0.80                        │
│ Angle: 30°                          │
│ Rotation: 0°                        │
└─────────────────────────────────────┘
^ Card background slightly lighter
```

---

## Detection Details Panel

### Valid State
```
┌────────────────────────────────────────┐
│ DETECTION DETAILS                      │
├────────────────────────────────────────┤
│ Geometry:                              │
│ Vertices: 3                            │
│ Triangles: 3                           │
│                                        │
│ Checks Run:                            │
│ ✓ Triangle edge intersections          │
│ ✓ Control points in bounds             │
│ ✓ Bezier self-intersection             │
│ ✓ Control point proximity              │
│ ✓ Parameter extremes                   │
│                                        │
│ Result:                                │
│ Score: 100%                            │
│ Issues: 0                              │
│ Warnings: 0                            │
└────────────────────────────────────────┘
```

### Error State
```
┌────────────────────────────────────────┐
│ DETECTION DETAILS                      │
├────────────────────────────────────────┤
│ Geometry:                              │
│ Vertices: 5                            │
│ Triangles: 5                           │
│                                        │
│ Checks Run:                            │
│ ✓ Triangle edge intersections          │
│ ✓ Control points in bounds             │
│ ✓ Bezier self-intersection             │
│ ✓ Control point proximity              │
│ ✓ Parameter extremes                   │
│                                        │
│ Result:                                │
│ Score: 25%                             │
│ Issues: 4                              │
│ Warnings: 3                            │
└────────────────────────────────────────┘
```

---

## Color Palette Reference

### Validity Colors
```
Valid (Green):      #4ade80  █████
Warning (Yellow):   #fbbf24  █████
Error (Red):        #ef4444  █████
```

### UI Colors
```
Primary Accent:     #6cf     █████  (Cyan blue)
Background Dark:    #0f0f0f  █████  (Almost black)
Panel Background:   #1a1a1a  █████  (Dark gray)
Section Background: #2a2a2a  █████  (Medium gray)
Border Color:       #333     █████  (Light gray)
Text Primary:       #e0e0e0  █████  (Light gray)
Text Secondary:     #888     █████  (Medium gray)
```

### Guide Colors
```
Triangle Guides:    #6cf (with opacity)  █████
Control Point 1:    #f66 (red)           █████
Control Point 2:    #6f6 (green)         █████
```

---

## Responsive Behavior

### Desktop (1920x1080)
- Canvas area: ~1200px width
- Constraints panel: 350px width
- Validity overlay: Top-left, fixed
- All controls visible

### Laptop (1440x900)
- Canvas area: ~900px width
- Constraints panel: 350px width
- Validity overlay: Scales slightly smaller
- All features functional

### Tablet (1024x768) - Future consideration
- Canvas area: Full width
- Constraints panel: Collapsible
- Validity overlay: Top-right
- Touch-friendly controls

---

## Animation & Transitions

### Validity Score Change
```
100% (green) → 85% (yellow)
Smooth color transition over 300ms
Number animates smoothly
```

### Shape Highlighting
```
When "Highlight Problems" toggled:
- Stroke color fades in 200ms
- Fill color fades in 200ms
- Width changes instantly
```

### Constraint Capture
```
On button click:
1. Card border turns green
2. Hold for 1 second
3. Fade back to normal
4. New card appears with slide-down
```

---

## Keyboard Shortcuts (Future Enhancement)

Potential shortcuts:
- `Space`: Toggle guides
- `H`: Toggle highlight problems
- `C`: Capture current constraints
- `1-4`: Load presets
- `←→`: Adjust curve factor
- `↑↓`: Adjust handle angle

---

## Accessibility Features

### Current
- High contrast colors
- Large text for scores
- Clear icons (✓, ⚠️, ❌)
- Readable fonts

### Future Enhancements
- ARIA labels
- Keyboard navigation
- Screen reader support
- Focus indicators
- High contrast mode

---

## Print Layout (If Printed)

```
Page 1: Current state screenshot
Page 2: Validity overlay details
Page 3: Saved constraints list
Page 4: Detection details
```

---

## Mobile Considerations (Future)

Portrait mode layout:
```
┌──────────────────┐
│ Controls (top)   │
├──────────────────┤
│                  │
│  Shape Preview   │
│     (square)     │
│                  │
├──────────────────┤
│ Validity Overlay │
├──────────────────┤
│ Constraints      │
│ (scrollable)     │
└──────────────────┘
```

---

This visual guide provides a comprehensive overview of what users will see and experience when using the FlowAngle Constraints Manager. All visual states, colors, and layouts are documented for reference.
