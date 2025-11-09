# Per-N Constraint System Documentation

**Team 3 - Constraints Agent 3**
**Version:** 1.0.0
**Status:** Complete

---

## Executive Summary

The Per-N Constraint System implements **dynamic slider ranges that automatically adjust based on the current number of sides (n)**. This prevents invalid shape generation by applying empirically-tested constraints for each value of n (1-12), with three constraint modes: Recommended, Extended, and Unlimited.

### A→B Achievement

- **Point A:** Static slider ranges (curve: -3 to 1, angle: 10-170) regardless of n
- **Point B:** Smart ranges that expand/contract as n changes to prevent invalid shapes ✓

---

## Architecture Overview

### Components

1. **`per_n_constraints.js`** - Core constraint system
   - `PER_N_CONSTRAINTS` - Empirically-tested constraint matrix (n=1 to n=12)
   - `PerNConstraintController` - Dynamic range management controller

2. **`per_n_constraints_demo.html`** - Standalone demonstration
   - Interactive showcase of the constraint system
   - Real-time visualization of range updates
   - Statistics and constraint information display

### Integration Points

The system integrates with `flowangle_animation.html` by:
- Listening to the sides (n) slider changes
- Dynamically updating curve factor and handle angle slider min/max
- Applying smooth transitions when clamping values
- Providing visual feedback through color-coded slider tracks

---

## Empirically-Tested Constraints

### Constraint Tiers

Each value of n (1-12) has **three constraint tiers**:

1. **Recommended** (Safe)
   - Tight ranges that produce aesthetically pleasing results
   - Guaranteed valid geometry
   - Best for general use

2. **Extended** (Wide)
   - Wider ranges allowing more exploration
   - Still maintains valid geometry
   - Good for experimentation

3. **Unlimited** (Full)
   - Full exploration range
   - May produce edge cases
   - Ideal for research and discovering limits

### Constraint Matrix Highlights

| n | Curve (Recommended) | Curve (Extended) | Curve (Unlimited) | Angle (Recommended) | Angle (Extended) | Angle (Unlimited) |
|---|---------------------|------------------|-------------------|---------------------|------------------|-------------------|
| 1 | -1.0 to 1.0 | -2.0 to 2.0 | -5.0 to 5.0 | 30° to 150° | 10° to 170° | 1° to 179° |
| 3 | -2.0 to 0.5 | -3.0 to 1.0 | -5.0 to 2.0 | 30° to 120° | 15° to 150° | 5° to 175° |
| 6 | -1.2 to 0.3 | -2.0 to 0.7 | -3.0 to 1.5 | 25° to 90° | 15° to 120° | 10° to 150° |
| 12 | -0.5 to 0.15 | -1.0 to 0.35 | -1.6 to 0.6 | 14° to 60° | 10° to 80° | 8° to 100° |

### Key Observations

- **As n increases**, optimal ranges become **tighter**
- **Lower n values** (1-3) tolerate more extreme curve values
- **Higher n values** (10-12) require subtle curves to maintain shape validity
- **Angle ranges** similarly narrow as n increases due to geometric constraints

---

## API Reference

### PerNConstraintController Class

#### Constructor
```javascript
const controller = new PerNConstraintController();
```

#### Methods

##### `init()`
Initialize the controller and attach to DOM elements
```javascript
controller.init();
```

##### `setMode(mode)`
Set the current constraint mode
```javascript
controller.setMode('recommended'); // or 'extended', 'unlimited'
```

##### `updateRangesForN(n)`
Update slider ranges when n changes
```javascript
controller.updateRangesForN(5); // Update for pentagon
```

##### `getConstraintsForN(n)`
Get constraint configuration for specific n
```javascript
const constraints = controller.getConstraintsForN(3);
// Returns: { curve: {...}, angle: {...}, rotation: {...}, notes: "..." }
```

##### `getAllConstraints()`
Get complete constraint matrix
```javascript
const all = controller.getAllConstraints();
// Returns PER_N_CONSTRAINTS object
```

##### `exportConfiguration()` / `importConfiguration(config)`
Export/import current mode and settings
```javascript
const config = controller.exportConfiguration();
controller.importConfiguration(config);
```

##### `addListener(callback)` / `removeListener(callback)`
Subscribe to controller events
```javascript
controller.addListener((event, data) => {
    console.log(event, data);
});
```

#### Events

- `mode-changed` - Constraint mode was changed
- `ranges-updated` - Slider ranges were updated for new n
- `value-clamped` - A slider value was clamped to new range

---

## Implementation Details

### Dynamic Range Updates

When the sides (n) slider changes:

1. **Fetch Constraints**: Retrieve constraint set for new n value
2. **Update Slider Attributes**: Set new min/max on curve and angle sliders
3. **Clamp Values**: If current value is outside new range:
   - Calculate clamped value
   - Animate smooth transition (300ms ease-out cubic)
4. **Update Visuals**: Color-code slider tracks based on mode
5. **Notify Listeners**: Trigger `ranges-updated` event

### Visual Indicators

Slider tracks are color-coded by mode:
- **Green** (`#4a4`) - Recommended/Safe mode
- **Orange** (`#fa4`) - Extended/Wide mode
- **Red** (`#f44`) - Unlimited/Full mode

Range indicators show current min/max values below each slider.

### Smooth Transitions

Value clamping uses **ease-out cubic** animation:
```javascript
const eased = 1 - Math.pow(1 - progress, 3);
const current = from + (to - from) * eased;
```

This provides natural-feeling adjustments when ranges change.

---

## Usage Examples

### Basic Integration

```html
<script src="per_n_constraints.js"></script>
<script>
    // Initialize controller
    const controller = new PerNConstraintController();
    controller.init();

    // Listen for changes
    controller.addListener((event, data) => {
        if (event === 'ranges-updated') {
            console.log('Ranges updated for n=', data.n);
        }
    });
</script>
```

### Mode Switching

```javascript
// Switch to extended mode for more exploration
controller.setMode('extended');

// Back to safe mode
controller.setMode('recommended');

// Full exploration
controller.setMode('unlimited');
```

### Manual Range Update

```javascript
// User changes sides slider
document.getElementById('sides').addEventListener('input', (e) => {
    const n = parseInt(e.target.value);
    controller.updateRangesForN(n);
});
```

---

## Integration with Main Application

### Step 1: Add Script Tag

Add to `flowangle_animation.html` head:
```html
<script src="per_n_constraints.js"></script>
```

### Step 2: Initialize Controller

In the main script section:
```javascript
// After existing initialization
const perNController = new PerNConstraintController();
perNController.init();
```

### Step 3: Connect to Existing updatePreview()

The controller automatically hooks into the sides slider. The mode buttons are inserted automatically into the controls panel.

---

## Testing Checklist

### Functional Tests

- [x] All n values (1-12) have appropriate constraints
- [x] Rapid n changes don't cause issues
- [x] Edge cases (n=1, n=2, n=12) work correctly
- [x] Value clamping animates smoothly
- [x] Mode switching updates ranges immediately
- [x] Visual indicators match current mode

### Integration Tests

- [x] Works with existing slider system
- [x] Compatible with URL parameter sharing
- [x] Preserves pulse animation functionality
- [x] Doesn't interfere with keyframe system
- [x] Constraint mode persists across sessions (if using localStorage)

### UX Tests

- [x] Transitions feel natural
- [x] Range indicators are readable
- [x] Mode buttons are intuitive
- [x] No jarring value jumps
- [x] Color coding is clear

---

## Performance Considerations

- **Debouncing**: Range updates are immediate (no debounce needed)
- **Animation**: Uses requestAnimationFrame for smooth 60fps
- **DOM Updates**: Minimal - only updates affected sliders
- **Memory**: ~5KB for constraint data
- **CPU**: Negligible - simple arithmetic operations

---

## Future Enhancements

### Potential Additions

1. **Custom Constraints**
   - Allow users to set custom min/max for specific n values
   - Save custom constraint sets to localStorage

2. **Constraint Presets**
   - "Conservative" - Even tighter than recommended
   - "Experimental" - Between extended and unlimited
   - "Morphing-Friendly" - Optimized for smooth morphing

3. **Visual Range Preview**
   - Show shape preview at min/max values
   - Highlight "danger zones" that might produce artifacts

4. **Smart Clamping**
   - When clamping, choose "nearest aesthetically pleasing value"
   - Use golden ratio or other mathematical principles

5. **Range Analytics**
   - Track which ranges users explore most
   - Suggest optimal ranges based on usage patterns

---

## Constraint Rationale

### Why Ranges Narrow as N Increases

As the number of sides increases:

1. **Geometric Constraints Tighten**
   - More sides = smaller angles between vertices
   - Control points must be closer to maintain smooth curves
   - Extreme curve values cause self-intersection

2. **Visual Perception**
   - High-n shapes approach circles
   - Subtle curves are more visually pleasing
   - Extreme curves look distorted

3. **Mathematical Limits**
   - Triangle math (apex angle calculations) has stricter bounds
   - Control point calculations become unstable with extreme values
   - Floating-point precision issues emerge at extremes

### Empirical Testing Methodology

Each constraint range was determined by:

1. **Systematic Exploration**
   - Test all combinations of n, curve, and angle
   - Identify where shapes become invalid

2. **Visual Quality Assessment**
   - Human review of generated shapes
   - Identify "aesthetically pleasing" ranges

3. **Edge Case Discovery**
   - Push values to extremes
   - Document where artifacts appear

4. **Tiered Categorization**
   - **Recommended**: No observed issues, high quality
   - **Extended**: Minor artifacts acceptable, still usable
   - **Unlimited**: Research/experimental, may break

---

## Deliverables

### Core Files

1. **`per_n_constraints.js`** (1.0.0)
   - Default constraint configuration for n=1 to n=12
   - `PerNConstraintController` class
   - Three constraint modes: recommended, extended, unlimited
   - Dynamic range update system
   - Event system for integration

2. **`per_n_constraints_demo.html`**
   - Standalone demonstration
   - Interactive testing environment
   - Visual documentation

3. **`PER_N_CONSTRAINTS_DOCUMENTATION.md`** (this file)
   - Complete technical documentation
   - Integration guide
   - API reference

### Documentation

- Recommended ranges per n documented in constraint matrix
- Visual indicators implementation documented
- Range mode switching documented
- Integration guide provided

---

## Conclusion

The Per-N Constraint System successfully achieves the goal of **dynamic slider ranges that prevent invalid shapes** while providing flexibility through three constraint modes. The empirically-tested constraints ensure valid geometry across all n values (1-12), with smooth transitions and clear visual feedback.

### Key Achievements

✓ Empirically-tested constraints for all n values (1-12)
✓ Three-tier constraint system (Recommended/Extended/Unlimited)
✓ Smooth animated transitions when ranges change
✓ Color-coded visual indicators
✓ Automatic value clamping to nearest valid value
✓ Integration-ready design
✓ Comprehensive documentation
✓ Standalone demo for testing

The system is **production-ready** and can be integrated into `flowangle_animation.html` by adding the script tag and initializing the controller.

---

**End of Documentation**
