# Constraint Manager UI - Complete Integration Guide

**Version**: 1.0.0
**Author**: svGen Team 3 - Agent 4
**Date**: 2025-11-09

## Overview

The Constraint Manager UI provides a comprehensive, polished interface for managing parameter constraints in the FlowAngle Animation Studio. It allows users to:

- View and edit constraints for the current n value
- Manage constraints across all n values (1-12) in a table format
- Switch between different constraint modes (Recommended, Extended, Unlimited, Custom)
- Export and import constraint configurations
- Apply preset profiles for different use cases
- Persist settings to localStorage

---

## File Structure

The Constraint Manager consists of three main files:

1. **`constraints_manager.js`** - Core constraint management logic (already exists)
2. **`constraint_manager_ui.js`** - UI component and interface layer (NEW)
3. **`flowangle_animation.html`** - Main application file (requires integration)

---

## Integration Steps

### Step 1: Include Required Scripts

Add the following script tags to your HTML file's `<head>` section:

```html
<script src="constraints_manager.js"></script>
<script src="constraint_manager_ui.js"></script>
```

### Step 2: Add CSS Styles

The UI requires additional CSS styles for the constraint panel. Add these to your `<style>` section:

```css
/* Constraints Panel - Right Sidebar */
#constraints-panel {
    width: 400px;
    background: #1a1a1a;
    border-left: 2px solid #333;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: width 0.3s ease;
}

#constraints-panel.collapsed {
    width: 0;
    border: none;
}

#constraints-header {
    padding: 15px 20px;
    background: #222;
    border-bottom: 2px solid #333;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#constraints-toggle-btn {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    background: #6cf;
    color: #000;
    border: none;
    padding: 40px 8px;
    cursor: pointer;
    border-radius: 4px 0 0 4px;
    font-weight: bold;
    z-index: 10;
    transition: all 0.2s;
}

/* ... (see full CSS in constraint_manager_ui.js comment header) */
```

### Step 3: Initialize Constraint Manager

Add initialization code to your JavaScript:

```javascript
// Initialize Constraint Manager
let constraintManager = null;
let constraintManagerUI = null;

document.addEventListener('DOMContentLoaded', () => {
    // Create constraint manager instance
    constraintManager = new ConstraintManager('svgen_constraints');

    // Create UI instance
    constraintManagerUI = new ConstraintManagerUI(constraintManager);

    // Listen to n value changes
    document.getElementById('sides').addEventListener('change', () => {
        constraintManagerUI.updateSliderLimits();
        constraintManagerUI.renderCurrentConstraints();
    });
});
```

### Step 4: Update Main Content Layout

Modify your main content area to support the constraints panel:

```html
<div id="main-content">
    <div id="canvas-area">
        <div id="svg-preview"></div>
    </div>
    <!-- Constraints panel will be injected here by the UI -->
</div>
```

---

## Features

### 1. Current Constraints Tab

Displays constraints for the currently selected n value with:
- Visual range bars showing min/max boundaries
- Current value indicator
- Quick edit fields for adjusting min/max values
- Reset button per parameter

**Parameters shown:**
- Curve Factor
- Handle Angle
- Rotation

### 2. All Constraints Table

A comprehensive table view showing all constraints for n=1 to n=12:
- Editable cells (click to edit)
- Color coding:
  - Green: Default values
  - Yellow: User-modified values
  - Red: Invalid/problematic values
- Bulk actions: Reset All, Export, Import

### 3. Settings Tab

**Constraint Modes:**
- **Recommended**: Tight, safe ranges proven to produce valid shapes
- **Extended**: Wider valid ranges for more exploration
- **Unlimited**: Full parameter exploration without limits
- **Custom**: User-defined constraints

**Preferences:**
- Auto-Clamping: Automatically constrain slider values to valid ranges
- Show Range Indicators: Display range information on sliders
- Constraint Strictness: Slider to control how strictly constraints are enforced (0-100%)

**Preset Profiles:**
- Conservative: Very tight constraints for guaranteed valid shapes
- Artistic: Balanced constraints allowing creative exploration
- Experimental: Wide ranges for discovering new patterns
- Precise: Fine-grained control with narrow ranges

---

## API Reference

### ConstraintManagerUI Class

#### Constructor
```javascript
new ConstraintManagerUI(constraintManager)
```

**Parameters:**
- `constraintManager`: Instance of ConstraintManager class

#### Methods

##### `switchTab(tabName)`
Switches between tabs in the constraints panel.
- **tabName**: 'current' | 'all' | 'settings'

##### `setMode(mode)`
Changes the constraint mode.
- **mode**: 'recommended' | 'extended' | 'unlimited' | 'custom'

##### `updateConstraint(n, param, value, type)`
Updates a specific constraint.
- **n**: Number of sides (1-12)
- **param**: 'curveFactor' | 'handleAngle' | 'rotation'
- **value**: New constraint value
- **type**: 'min' | 'max'

##### `resetConstraint(n, param)`
Resets constraints for a parameter at a specific n value.

##### `resetAllConstraints()`
Resets all constraints to default values.

##### `exportConstraints()`
Exports constraints to a JSON file (downloads).

##### `importConstraints()`
Imports constraints from a JSON file (file picker).

##### `togglePanel()`
Toggles the constraints panel visibility.

##### `updateSliderLimits()`
Updates the min/max values of parameter sliders based on current constraints.

---

## Usage Examples

### Example 1: Programmatically Set Constraints

```javascript
// Set tight constraints for n=3
constraintManagerUI.updateConstraint(3, 'curveFactor', -2, 'min');
constraintManagerUI.updateConstraint(3, 'curveFactor', 0.5, 'max');
constraintManagerUI.updateConstraint(3, 'handleAngle', 45, 'min');
constraintManagerUI.updateConstraint(3, 'handleAngle', 75, 'max');
```

### Example 2: Switch to Extended Mode

```javascript
// Switch to extended mode for wider exploration
constraintManagerUI.setMode('extended');
```

### Example 3: Export Constraints

```javascript
// Export current constraints to file
constraintManagerUI.exportConstraints();
```

### Example 4: Listen to Constraint Changes

```javascript
// Listen to constraint manager events
constraintManager.addListener((event, data) => {
    console.log(`Constraint event: ${event}`, data);

    if (event === 'constraint-set') {
        // Update UI or perform validation
        console.log(`Constraint set for n=${data.n}, param=${data.param}`);
    }
});
```

---

## Constraint Mode Definitions

### Recommended Mode

Safe, proven ranges for each n value:

| n | Curve Factor | Handle Angle | Rotation |
|---|--------------|--------------|----------|
| 1 | -3 to 1 | 10° to 170° | 0° to 360° |
| 2 | -3 to 1 | 10° to 170° | 0° to 360° |
| 3 | -3 to 1 | 30° to 90° | 0° to 360° |
| 4 | -3 to 1 | 20° to 70° | 0° to 360° |
| 5 | -3 to 1 | 15° to 55° | 0° to 360° |
| 6 | -3 to 1 | 12° to 45° | 0° to 360° |
| 7 | -3 to 1 | 10° to 40° | 0° to 360° |
| 8 | -3 to 1 | 10° to 35° | 0° to 360° |
| 9 | -3 to 1 | 8° to 30° | 0° to 360° |
| 10 | -3 to 1 | 8° to 28° | 0° to 360° |
| 11 | -3 to 1 | 7° to 25° | 0° to 360° |
| 12 | -3 to 1 | 7° to 23° | 0° to 360° |

### Extended Mode

Wider ranges allowing more exploration while maintaining validity:

| n | Curve Factor | Handle Angle |
|---|--------------|--------------|
| 3 | -5 to 3 | 15° to 120° |
| 6 | -5 to 3 | 7° to 60° |
| 12 | -5 to 3 | 3° to 30° |

### Unlimited Mode

Full parameter ranges for complete freedom:
- **Curve Factor**: -10 to 10
- **Handle Angle**: 1° to 179°
- **Rotation**: 0° to 360°

---

## Data Persistence

### localStorage Schema

Constraints and settings are automatically saved to localStorage:

**Constraint Data** (`svgen_constraints`):
```json
{
  "3": {
    "curveFactor": [-2, 0.5],
    "handleAngle": [45, 75]
  },
  "6": {
    "curveFactor": [-1.5, 0],
    "handleAngle": [20, 40]
  }
}
```

**UI Settings** (`svgen_constraint_ui_settings`):
```json
{
  "mode": "recommended",
  "autoClampingEnabled": true,
  "showRangeIndicators": true,
  "strictness": 100
}
```

---

## Export/Import Format

### JSON Format

Constraints can be exported and imported in JSON format:

```json
{
  "1": {
    "curveFactor": [-3, 1],
    "handleAngle": [10, 170],
    "rotation": [0, 360]
  },
  "3": {
    "curveFactor": [-2, 0.5],
    "handleAngle": [45, 75],
    "rotation": [0, 360]
  },
  "6": {
    "curveFactor": [-1.5, 0],
    "handleAngle": [20, 40],
    "rotation": [0, 360]
  }
}
```

**Format Rules:**
- Keys are n values (1-12)
- Each n contains parameter constraints
- Each constraint is a `[min, max]` array
- `null` values mean no constraint for that boundary

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl/Cmd + ]` | Toggle constraints panel |
| `Tab` | Switch between constraint tabs |
| `Enter` | Confirm cell edit in table |
| `Escape` | Cancel cell edit in table |

---

## Best Practices

### 1. Start with Recommended Mode
Begin with the recommended constraint mode and gradually relax constraints as needed.

### 2. Test After Changes
Always test your shapes after modifying constraints to ensure they remain valid.

### 3. Export Before Experimenting
Export your constraints before making significant changes so you can revert if needed.

### 4. Use Auto-Clamping
Keep auto-clamping enabled to prevent invalid parameter combinations.

### 5. Document Custom Constraints
When creating custom constraints, document why specific ranges were chosen.

---

## Troubleshooting

### Issue: Constraints not applying to sliders
**Solution**: Ensure `updateSliderLimits()` is called after constraint changes.

### Issue: Exported constraints not importing
**Solution**: Verify JSON format matches the expected schema.

### Issue: Panel not visible
**Solution**: Check that CSS is properly loaded and `#main-content` exists.

### Issue: localStorage quota exceeded
**Solution**: Clear old constraints or reduce the number of custom constraints.

---

## Future Enhancements

Planned features for future versions:

1. **Learn from History**: Analyze user's preferred ranges and suggest constraints
2. **Validity Detection**: Automatic detection of problematic parameter combinations
3. **Constraint Profiles**: Shareable constraint profiles for different artistic styles
4. **Undo/Redo**: Support for undoing constraint changes
5. **Batch Operations**: Apply constraints to multiple n values at once
6. **Visual Constraint Editor**: Drag-and-drop interface for setting constraints
7. **Constraint Templates**: Pre-built templates for common use cases

---

## Support

For issues or questions:
- Review this documentation
- Check console for error messages
- Verify all required files are loaded
- Test in a clean browser profile to rule out extension conflicts

---

## License

Part of the svGen project. See main project LICENSE for details.

---

## Changelog

### v1.0.0 (2025-11-09)
- Initial release
- Three-tab interface (Current, All, Settings)
- Four constraint modes (Recommended, Extended, Unlimited, Custom)
- Export/Import functionality
- localStorage persistence
- Preset profiles
- Auto-clamping support
- Range indicators
- Strictness control
