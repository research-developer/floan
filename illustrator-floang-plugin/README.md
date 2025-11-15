# FloAng Illustrator Plugin

A UXP plugin for Adobe Illustrator that generates geometric patterns using the FloAng algorithm - creating sacred geometry, mandalas, and flowing shapes with mathematically precise Bézier curves.

## Features

- **Core Algorithm**: Direct port of the proven FloAng web application algorithm
- **4 Parameter Controls**:
  - **Sides** (1-12): Number of polygon vertices
  - **Flow** (-3 to 1): Bézier handle distance multiplier
  - **Angle** (dynamic): Handle angle with orthogonal snapping
  - **Rotation** (-360° to 360°): Pattern orientation
- **Built-in Presets**: Triquetra, Flower, Star, Smooth
- **Real-time Preview**: Parameter persistence across sessions
- **Debug Menu**: Cmd+Shift+D (Mac) / Ctrl+Shift+D (Windows)

## Installation

### Prerequisites
- Adobe Illustrator CC 2022 (26.0) or later
- UXP Developer Tool (for development)

### Development Installation

1. **Clone/Navigate to plugin directory**:
   ```bash
   cd illustrator-floang-plugin
   ```

2. **Install UXP Developer Tool**:
   - Download from [Adobe Developer Console](https://developer.adobe.com/photoshop/uxp/devtool/)
   - Install and launch

3. **Load plugin in UXP Developer Tool**:
   - Click "Add Plugin"
   - Navigate to `illustrator-floang-plugin` folder
   - Select the folder containing `manifest.json`
   - Choose "Adobe Illustrator" as target application
   - Click "Load"

4. **Launch in Illustrator**:
   - Open Adobe Illustrator
   - Go to Window > Extensions > FloAng
   - Plugin panel should appear

### Production Installation (Future)

The plugin will be packaged as a `.ccx` file for distribution via:
- Adobe Creative Cloud Desktop App
- Adobe Exchange Marketplace
- Direct download from releases

## Usage

### Basic Workflow

1. **Open or create an Illustrator document**
2. **Open FloAng panel**: Window > Extensions > FloAng
3. **Choose a preset** or adjust parameters manually:
   - Use sliders to adjust Sides, Flow, Angle, Rotation
   - Values update in real-time
4. **Click "Generate Pattern"**
5. **Edit the generated path** using Illustrator's tools

### Presets

- **Triquetra** (n=3): Classic Celtic trinity knot shape
- **Flower** (n=6): Six-petaled mandala pattern
- **Star** (n=5): Five-pointed star with flowing curves
- **Smooth** (n=6): Smooth hexagonal flow pattern

### Parameter Guide

#### Sides (n)
- **Range**: 1-12
- **Effect**: Number of polygon vertices
- **Special cases**:
  - n=1: Circle
  - n=2: Curved line
  - n≥3: Full flowangle algorithm

#### Flow Factor
- **Range**: -3.0 to 1.0
- **Effect**: Controls Bézier handle distance
  - Negative values: Inward curves (concave)
  - Positive values: Outward curves (convex)
  - Around -0.66: Smooth flowing shapes

#### Handle Angle
- **Range**: Dynamic (orthogonal ±50°)
- **Effect**: Curve character and symmetry
- **Orthogonal angle**: Natural "centered" angle for each polygon
  - Formula: `(n-2) × 180 / n`
  - Highlighted in green on slider

#### Rotation
- **Range**: -360° to 360°
- **Effect**: Global pattern orientation

## Technical Architecture

### Layer Structure

```
Layer 1: Core Geometric Engine (Pure Math)
├── flowangle-core.js        # Algorithm implementation
└── Mathematical formulas    # No Illustrator dependencies

Layer 2: Coordinate Transformation
├── coordinate-transform.js  # SVG ↔ Illustrator conversion
└── Artboard calculations    # Y-axis inversion, scaling

Layer 3: Illustrator Adapter
├── illustrator-adapter.js   # PathItem creation
└── UXP APIs                 # Native Illustrator integration
```

### Key Files

- `manifest.json`: Plugin metadata and permissions
- `src/main.js`: Plugin entry point and event handling
- `src/flowangle-core.js`: Core algorithm (ported from FloAng.html)
- `src/coordinate-transform.js`: SVG ↔ Illustrator coordinate conversion
- `src/illustrator-adapter.js`: PathItem generation
- `src/ui/panel.html`: UI panel structure
- `src/ui/panel.js`: UI event handlers
- `src/ui/styles.css`: Panel styling

## Development

### Debugging

**Enable Debug Menu**: Press `Cmd+Shift+D` (Mac) or `Ctrl+Shift+D` (Windows)

The debug menu shows:
- Current parameter values
- Calculated orthogonal angle
- Real-time state inspection

### Testing Checklist

- [ ] Basic pattern generation works
- [ ] All presets match web version visually
- [ ] Orthogonal angle system functions correctly
- [ ] Paths are editable with Direct Selection Tool (A)
- [ ] Parameter persistence works across sessions
- [ ] Performance is acceptable (< 1 second for generation)
- [ ] Works on various artboard sizes

### Known Issues

- **Performance**: Large patterns (n=12) may take 1-2 seconds to generate
- **Coordinate precision**: Minor differences (<0.1px) from web version due to floating point
- **UXP limitations**: Some ES2020+ features not supported (use ES6)

## Algorithm Reference

### Orthogonal Angle Formula
```
orthogonalAngle = (n - 2) × 180 / n
```

### Bézier Control Point Calculation
1. Calculate polygon vertices around center
2. Build triangles for each edge
3. Calculate triangle apex based on handle angle
4. Position control points using flow factor: `cp = vertex + (apex - vertex) × flowFactor`

### Special Cases
- **n=1**: Circle (radius-based)
- **n=2**: Quadratic Bézier curve
- **n≥3**: Cubic Bézier segments forming closed path

## Contributing

### Development Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test in Illustrator
4. Commit with descriptive messages
5. Push and create Pull Request

### Code Standards

- ES6 modules for all JavaScript
- JSDoc comments for all functions
- Consistent naming (camelCase for functions, PascalCase for classes)
- Error handling at all API boundaries
- No console.log in production builds

## License

[Add license information]

## Credits

- **Algorithm**: Based on the FloAng web application
- **Original Concept**: [Add original author if applicable]
- **UXP Implementation**: [Add contributors]

## Resources

- [UXP for Adobe Illustrator](https://developer.adobe.com/illustrator/uxp/)
- [Illustrator Scripting Reference](https://ai-scripting.docsforadobe.dev/)
- [FloAng Web Version](./FloAng.html) (reference implementation)
- [Bézier Curve Mathematics](https://pomax.github.io/bezierinfo/)

## Support

For issues, questions, or feature requests:
- Open an issue in the GitHub repository
- Check existing issues for solutions
- Include Illustrator version and steps to reproduce

## Roadmap

### Phase 1: MVP (Current)
- [x] Core algorithm port
- [x] Basic UI with 4 parameters
- [x] 4 presets
- [x] Generate button
- [x] Debug menu

### Phase 2: Advanced Features
- [ ] Pattern rotation system (n rotated copies)
- [ ] Break apart functionality
- [ ] Real-time preview canvas
- [ ] Enhanced UI with keyboard shortcuts
- [ ] Custom preset save/load

### Phase 3: Professional Polish
- [ ] Configuration import/export
- [ ] Color/stroke styling options
- [ ] Multi-artboard generation
- [ ] Adobe Exchange submission
- [ ] Comprehensive documentation

---

**Version**: 1.0.0
**Last Updated**: 2025-01-11
**Target Platform**: Adobe Illustrator CC 2022+ (UXP)
