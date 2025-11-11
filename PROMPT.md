# FloAng Illustrator Plugin Development

## Project Context

**FloAng** (Flowangle) is a web-based SVG generator that creates geometric patterns using a mathematical algorithm based on regular polygons with Bézier curve handles. The algorithm generates sacred geometry patterns, mandalas, stars, and other flowing geometric shapes by manipulating handle angles and flow factors around polygon vertices.

### Current Implementation

The web application (`FloAng.html`) is a single-file application that:
- Generates SVG paths using Bézier curves
- Supports dynamic parameters: sides (n), flow factor, handle angle, rotation
- Features an orthogonal angle system where each polygon has a natural "centered" handle angle based on interior angles: `(n-2) × 180 / n`
- Includes preset configurations (triquetra, flower, star, smooth)
- Provides real-time preview and localStorage persistence
- Exports SVG and PNG formats

### Core Algorithm Location

The main generation logic is in `FloAng.html` in the `generateFlowAngle()` function (approximately lines 750-900). Key mathematical concepts:

```javascript
// Calculate polygon vertices
const angleStep = (2 * Math.PI) / sides;
const vertices = [];
for (let i = 0; i < sides; i++) {
  const angle = i * angleStep + rotation;
  vertices.push({
    x: centerX + radius * Math.cos(angle),
    y: centerY + radius * Math.sin(angle)
  });
}

// Calculate Bézier control points using flowFactor and handleAngle
// This is the core "flowangle" innovation
```

## Mission: Create Adobe Illustrator Plugin

**Objective:** Develop a UXP (Unified Extensibility Platform) plugin for Adobe Illustrator that brings the FloAng algorithm into a professional vector design environment.

### Why UXP?

- Modern JavaScript (ES6+) - can directly port current code
- HTML/CSS panel UI - can reuse existing interface design
- Better performance than legacy CEP
- Adobe's current direction (future-proof)
- Native integration with Illustrator's scripting API

## Technical Requirements

### Phase 1: Core Functionality (MVP)

**Goal:** Working plugin that generates basic flowangle patterns in Illustrator

**Deliverables:**
1. UXP plugin scaffold with proper manifest.json
2. Core algorithm ported to create Illustrator PathItems
3. Basic panel UI with essential controls:
   - Sides slider (1-12)
   - Flow slider (-3 to 1)
   - Angle slider (dynamic range based on orthogonal)
   - Rotation slider (0-360°)
4. "Generate" button that creates grouped paths on active artboard
5. Preset buttons (triquetra, flower, star, smooth)

**Technical Specifications:**

```javascript
// Illustrator API path creation
var doc = app.activeDocument;
var layer = doc.activeLayer;
var pathItem = layer.pathItems.add();

// Set anchor points
pathItem.setEntirePath(arrayOfPoints);

// Set Bézier handles
for (var i = 0; i < pathItem.pathPoints.length; i++) {
  pathItem.pathPoints[i].leftDirection = [x1, y1];
  pathItem.pathPoints[i].rightDirection = [x2, y2];
  pathItem.pathPoints[i].pointType = PointType.SMOOTH;
}

pathItem.closed = true;
pathItem.stroked = true;
pathItem.filled = false;
```

**Coordinate System Considerations:**
- Illustrator uses bottom-left origin (SVG uses top-left)
- Y-axis is inverted: `illustratorY = artboardHeight - svgY`
- Units: convert from pixels to points (1 point = 1/72 inch)

### Phase 2: Advanced Features

**Deliverables:**
1. **Pattern Rotation System:**
   - Generate n rotated copies of the base segment
   - Group into single compound path or separate objects (user choice)
   - Proper center-point rotation around artboard center

2. **Break Apart Functionality:**
   - "Ungroup" button to separate pattern elements
   - "Isolate Segment" to extract single petal/element
   - Maintain editability of individual paths

3. **Real-time Preview:**
   - Lightweight preview rendering in panel
   - Update on slider change (throttled to 200ms)
   - Optional: create temporary guide layer in Illustrator

4. **Enhanced UI:**
   - Orthogonal indicator with green highlight
   - Value displays matching web version
   - Keyboard shortcuts (arrow keys for fine-tuning)

### Phase 3: Professional Polish

**Deliverables:**
1. **Configuration Management:**
   - Save/load custom presets
   - Import/export .json configurations
   - Share configurations via URL (similar to web version)

2. **Advanced Generation Options:**
   - Color/stroke settings
   - Layer naming conventions
   - Scaling options (auto-fit to artboard, custom size)
   - Multi-artboard generation

3. **Documentation:**
   - In-panel help tooltips
   - User guide (PDF)
   - Video tutorial (optional)

## File Structure

```
illustrator-flowangle-plugin/
├── manifest.json              # UXP plugin metadata
├── src/
│   ├── main.js               # Plugin entry point & Illustrator API bridge
│   ├── flowangle-core.js     # Ported algorithm (from FloAng.html)
│   ├── illustrator-adapter.js # SVG → Illustrator path conversion
│   └── ui/
│       ├── panel.html        # Main UI (adapt from FloAng.html)
│       ├── panel.js          # UI event handlers
│       └── styles.css        # Panel styling
├── icons/                     # Plugin icons (24x24, 48x48, etc.)
├── README.md                 # Development documentation
└── package.json              # Dependencies
```

## Key Technical Challenges & Solutions

### Challenge 1: Coordinate System Transformation
**Problem:** SVG uses top-left origin, Illustrator uses bottom-left
**Solution:**
```javascript
function svgToIllustratorCoords(svgPoint, artboardHeight) {
  return [
    svgPoint.x,
    artboardHeight - svgPoint.y
  ];
}
```

### Challenge 2: Bézier Handle Calculation
**Problem:** Need to preserve exact curve mathematics from SVG
**Solution:**
- Port `calculateControlPoint()` function exactly
- Test output visually matches web version
- Use Illustrator's `PointType.SMOOTH` for continuous curves

### Challenge 3: Real-time Preview Performance
**Problem:** Illustrator API calls can be slow
**Solution:**
- Debounce slider inputs (200ms delay)
- Render preview in HTML canvas first
- Only create Illustrator paths on explicit "Generate" click
- Provide "Live Mode" toggle for power users

### Challenge 4: Path Grouping & Rotation
**Problem:** Creating n rotated segments around center
**Solution:**
```javascript
function createPattern(params) {
  var group = app.activeDocument.groupItems.add();
  var centerX = 500; // artboard center
  var centerY = 500;

  for (var i = 0; i < params.sides; i++) {
    var segment = createSegment(params);
    var angle = (360 / params.sides) * i;

    // Rotate around center point
    var matrix = app.getRotationMatrix(angle);
    segment.transform(matrix, true, false, false, false, centerX, centerY);

    segment.move(group, ElementPlacement.PLACEATEND);
  }

  return group;
}
```

## Development Workflow

### Setup
1. Install Adobe UXP Developer Tool
2. Clone this repository/worktree
3. Study current `FloAng.html` implementation
4. Review Adobe Illustrator UXP documentation
5. Set up plugin development environment

### Iteration Cycle
1. Port one feature at a time from web version
2. Test in Illustrator using UXP Developer Tool
3. Validate visual output matches web version exactly
4. Commit incremental progress
5. Document any deviations or adaptations needed

### Testing Checklist
- [ ] Basic pattern generation works
- [ ] All presets match web version visually
- [ ] Orthogonal angle system functions correctly
- [ ] Paths are editable with Illustrator's Direct Selection Tool
- [ ] Break apart creates individual paths
- [ ] Rotation pattern creates symmetric design
- [ ] Performance is acceptable (< 1 second for generation)
- [ ] Works on multiple artboard sizes

## Resources

### Adobe Documentation
- [UXP for Adobe Illustrator](https://developer.adobe.com/illustrator/uxp/)
- [Illustrator Scripting Reference](https://ai-scripting.docsforadobe.dev/)
- [PathItem API](https://ai-scripting.docsforadobe.dev/#/Illustrator/PathItem)
- [UXP Developer Tool](https://developer.adobe.com/photoshop/uxp/devtool/)

### Mathematical Reference
- Interior angle formula: `(n - 2) × 180 / n`
- Bézier curve mathematics: [Pomax Bézier Curves Primer](https://pomax.github.io/bezierinfo/)
- SVG path specification: [MDN SVG Paths](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths)

### Existing Codebase
- Study `generateFlowAngle()` function in `FloAng.html`
- Review `updateSidesAndAngleRange()` for orthogonal angle logic
- Check preset configurations in `loadPreset()` function

## Success Criteria

### Minimum Viable Product (Phase 1)
✅ Plugin installs and runs in Illustrator
✅ Generates patterns that visually match web version
✅ All four presets work correctly
✅ Basic UI is functional and intuitive
✅ Paths are fully editable in Illustrator

### Production Ready (Phase 3)
✅ Professional UI with help documentation
✅ Stable performance (no crashes)
✅ Configuration save/load works
✅ Code is documented and maintainable
✅ Ready for Adobe Exchange submission

## Getting Started

Begin by:
1. Reading the UXP quickstart guide
2. Creating a minimal "Hello World" Illustrator plugin
3. Porting just the triquetra preset as proof-of-concept
4. Validating the visual output matches the web version exactly
5. Expanding to full parameter system once PoC works

**First Milestone:** Create a UXP plugin that generates a static triquetra (sides=3, flow=-0.66, angle=60°, rotation=-30°) as an editable Illustrator path.

## Questions to Resolve

- Should pattern be compound path or grouped paths?
- How to handle stroke/fill defaults?
- Layer naming convention?
- Undo/redo integration approach?
- Distribution strategy (Adobe Exchange vs. direct)?

---

**Branch:** `refactor/new-framework`
**Primary Goal:** Working Illustrator UXP plugin with core FloAng functionality
**Timeline:** Phase 1 target: 2-3 weeks of focused development
**Contact:** Document all architectural decisions and blockers in commit messages
