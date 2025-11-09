# Per-N Constraint System - Quick Integration Guide

## Step-by-Step Integration with flowangle_animation.html

### 1. Add Script Reference

Add this line in the `<head>` section, after `constraints_manager.js`:

```html
<script src="per_n_constraints.js"></script>
```

### 2. Initialize the Controller

Add this to your main script section (after existing state variables):

```javascript
// Initialize Per-N Constraint Controller
let perNController = null;
document.addEventListener('DOMContentLoaded', () => {
    perNController = new PerNConstraintController();
    perNController.init();

    // Listen for constraint updates
    perNController.addListener((event, data) => {
        if (event === 'ranges-updated') {
            console.log(`Constraints updated for n=${data.n}`);
            updateRangeIndicators();
        }
    });
});
```

### 3. Update Range Indicators (Optional but Recommended)

Add this function to update the range indicator displays:

```javascript
function updateRangeIndicators() {
    const curveSlider = document.getElementById('curve-factor');
    const angleSlider = document.getElementById('handle-angle');
    const rotationSlider = document.getElementById('rotation');

    // Update curve factor indicator
    const curveIndicator = document.getElementById('curve-range-indicator');
    if (curveIndicator) {
        curveIndicator.textContent = `[${parseFloat(curveSlider.min).toFixed(2)} to ${parseFloat(curveSlider.max).toFixed(2)}]`;
    }

    // Update angle indicator
    const angleIndicator = document.getElementById('angle-range-indicator');
    if (angleIndicator) {
        angleIndicator.textContent = `[${angleSlider.min}° to ${angleSlider.max}°]`;
    }

    // Update rotation indicator
    const rotationIndicator = document.getElementById('rotation-range-indicator');
    if (rotationIndicator) {
        rotationIndicator.textContent = `[${rotationSlider.min}° to ${rotationSlider.max}°]`;
    }
}
```

### 4. That's It!

The `PerNConstraintController` will automatically:
- Create mode toggle buttons (Safe/Wide/Full) in your controls panel
- Listen to the sides slider and update ranges
- Clamp values smoothly when ranges change
- Apply color-coded visual styling to sliders
- Add range indicators below sliders

## Testing the Integration

### 1. Test the Demo First

Open `per_n_constraints_demo.html` in a browser to see the system in action:

```bash
# From the svGen directory
open per_n_constraints_demo.html
# or
python3 -m http.server 8000
# then visit http://localhost:8000/per_n_constraints_demo.html
```

### 2. Verify Features

- Change the sides (n) slider - ranges should update
- Switch between Safe/Wide/Full modes - ranges should change
- Watch for smooth animations when values get clamped
- Check slider color changes by mode

### 3. Test Integration

After integrating into `flowangle_animation.html`:

1. **Test Basic Functionality**
   ```
   - Change sides from 1 to 12
   - Verify curve and angle ranges update
   - Check that current values clamp smoothly
   ```

2. **Test Mode Switching**
   ```
   - Click Safe mode → verify tight ranges
   - Click Wide mode → verify wider ranges
   - Click Full mode → verify unlimited ranges
   ```

3. **Test Edge Cases**
   ```
   - Set n=1 (circle) → verify special handling
   - Set n=2 (curved line) → verify constraints
   - Set n=12 (dodecagon) → verify tight ranges
   ```

4. **Test Integration Points**
   ```
   - URL sharing still works
   - Keyframe animation still works
   - Pulse mode still works
   - Preset buttons still work
   ```

## Troubleshooting

### Issue: Mode buttons don't appear

**Solution:** Check that `controls-panel` element exists in DOM before init() is called. You may need to wrap initialization in `DOMContentLoaded`.

### Issue: Sliders don't update

**Solution:** Verify slider IDs match expected values:
- `sides` - Sides slider
- `curve-factor` - Curve factor slider
- `handle-angle` - Handle angle slider

### Issue: Visual styling doesn't apply

**Solution:** Ensure `per_n_constraints.js` is loaded before controller initialization. The controller injects CSS automatically.

### Issue: Values jump around

**Solution:** The controller smoothly animates clamping. If values are jumping, check that `updatePreview()` isn't being called too frequently during animation.

## Customization

### Change Animation Duration

Edit the controller initialization:

```javascript
perNController.animationDuration = 500; // milliseconds (default: 300)
```

### Customize Mode Names

Edit the mode button creation in `per_n_constraints.js`:

```javascript
// Line ~158
<button class="mode-btn recommended" ... >
    Your Name Here
</button>
```

### Add Custom Constraints

Override constraints for specific n:

```javascript
// After initialization
PER_N_CONSTRAINTS[13] = {
    curve: {
        recommended: { min: -0.4, max: 0.1 },
        extended: { min: -0.8, max: 0.3 },
        unlimited: { min: -1.4, max: 0.5 }
    },
    // ... similar for angle and rotation
};
```

## Advanced Integration

### Persist Mode Selection

Save mode to localStorage:

```javascript
perNController.addListener((event, data) => {
    if (event === 'mode-changed') {
        localStorage.setItem('constraintMode', data.mode);
    }
});

// On load:
const savedMode = localStorage.getItem('constraintMode');
if (savedMode) {
    perNController.setMode(savedMode);
}
```

### Integrate with URL Parameters

Add mode to URL sharing:

```javascript
function encodeStateToURL(includeKeyframes = false) {
    const params = new URLSearchParams();
    // ... existing params
    params.set('mode', perNController.currentMode);
    return '#' + params.toString();
}

function loadFromURL() {
    const params = new URLSearchParams(window.location.hash.substring(1));
    if (params.has('mode')) {
        perNController.setMode(params.get('mode'));
    }
    // ... rest of loading
}
```

### Custom Event Handlers

React to specific events:

```javascript
perNController.addListener((event, data) => {
    switch(event) {
        case 'ranges-updated':
            console.log(`New ranges for n=${data.n}`);
            break;
        case 'mode-changed':
            console.log(`Mode switched to ${data.mode}`);
            break;
        case 'value-clamped':
            console.log(`Value clamped on ${data.param}`);
            break;
    }
});
```

## Verification Checklist

After integration, verify:

- [ ] Mode buttons appear in controls panel
- [ ] Clicking Safe/Wide/Full changes slider ranges
- [ ] Changing sides (n) updates curve and angle ranges
- [ ] Values clamp smoothly (animated, not instant)
- [ ] Sliders show color coding (green/orange/red)
- [ ] Range indicators show current min/max
- [ ] No console errors
- [ ] Existing features still work:
  - [ ] Presets load correctly
  - [ ] Keyframes work
  - [ ] Pulse animations work
  - [ ] URL sharing works
  - [ ] SVG generation works

## Support

For issues or questions:
1. Check the demo file works standalone
2. Review console for errors
3. Verify script load order
4. Check DOM element IDs match expectations

**Integration Complete!** The system should now dynamically adjust slider ranges based on n.
