# Feedback Mode & Constraint System Documentation

## Overview

The Feedback Mode system for FlowAngle Studio allows users to explore parameter ranges freely and then capture custom constraint boundaries for specific n-values. This creates an adaptive interface that guides future exploration within user-defined safe zones.

## Architecture

### Components

1. **ConstraintManager** (`constraints_manager.js`)
   - Core constraint storage and management
   - localStorage persistence
   - Import/Export functionality
   - Event system for UI updates

2. **Constraint Functions** (`constraint_functions.js`)
   - UI interaction handlers
   - Range updates and animations
   - Notification system
   - Table management

3. **FlowAngle Studio Integration** (`flowangle_animation.html`)
   - Feedback Mode toggle
   - Set Min/Max buttons per parameter
   - Constraint Manager modal panel
   - Range indicators

## Features

### 1. Feedback Mode Toggle

**Location:** Main control panel

**Function:**
- **OFF (Normal Mode):** Standard parameter ranges
  - Curve Factor: -3 to 1
  - Handle Angle: 10° to 170°
  - Rotation: 0° to 360°

- **ON (Feedback Mode):** Generous exploration ranges
  - Curve Factor: -10 to 10
  - Handle Angle: 1° to 179°
  - Rotation: 0° to 360°

**Visual Feedback:**
- Orange border around Feedback Mode container when active
- Range indicators change color to orange
- Constraint capture buttons appear

### 2. Constraint Capture

**How to use:**
1. Enable Feedback Mode
2. Adjust sliders to desired minimum or maximum value
3. Click "Set Min" or "Set Max" button
4. Constraint is saved for current n-value

**Example Workflow:**
```
1. Set n=3 (triangle)
2. Move Curve Factor to -2.0
3. Click "Set Min" → Saves min=-2.0 for n=3
4. Move Curve Factor to 0.5
5. Click "Set Max" → Saves max=0.5 for n=3
6. Disable Feedback Mode
7. Range is now constrained to [-2.0, 0.5] for n=3
```

### 3. Constraint Manager Panel

**Access:** Click "Manage Constraints" button

**Features:**

#### Statistics Dashboard
- Total N Values: Number of n-values with constraints
- Total Constraints: Total constraint entries
- Mode: Current mode (Normal/Feedback)

#### Constraints Table
- View all constraints organized by n-value
- Shows parameter name, min, max values
- Action buttons for each constraint:
  - **Clear Min:** Remove minimum constraint
  - **Clear Max:** Remove maximum constraint
  - **Delete:** Remove entire constraint

#### Import/Export
- **Export to Clipboard:** Copy constraints as JSON
- **Import from Clipboard:** Load constraints from clipboard
- **Import from JSON:** Paste JSON manually

#### Management Actions
- **Clear All:** Remove all constraints (with confirmation)
- **Reset to Defaults:** Reset everything including feedback mode

### 4. Constraint Data Structure

```javascript
{
  "3": {
    "curveFactor": [-2.0, 0.5],
    "handleAngle": [30, 120],
    "rotation": [0, 180]
  },
  "4": {
    "curveFactor": [-1.5, 0.8]
  },
  "6": {
    "handleAngle": [20, 90]
  }
}
```

- Each n-value can have constraints for any combination of parameters
- Constraints are [min, max] arrays
- `null` values mean no constraint for that boundary

## User Guide

### Setting Up Constraints

**Scenario:** You want to explore triangles (n=3) but keep them within aesthetic bounds.

1. **Enable Feedback Mode**
   - Check the "Feedback Mode" checkbox
   - Notice sliders now have wider ranges

2. **Explore Freely**
   - Move sliders to find interesting extremes
   - Note which values create pleasing shapes

3. **Capture Lower Bound**
   - Set Curve Factor to -2.0 (your preferred minimum)
   - Click "Set Min" next to Curve Factor
   - You'll see a notification confirming the capture

4. **Capture Upper Bound**
   - Set Curve Factor to 0.5 (your preferred maximum)
   - Click "Set Max" next to Curve Factor
   - Notification confirms the capture

5. **Repeat for Other Parameters**
   - Set Handle Angle range: 30° to 120°
   - Set Rotation range: 0° to 180°

6. **Return to Normal Mode**
   - Uncheck "Feedback Mode"
   - Sliders now respect your custom ranges for n=3
   - Ranges are highlighted in normal mode

7. **Repeat for Other N-Values**
   - Change n=4 and set different constraints
   - Each n-value can have its own ranges

### Sharing Constraints

**Export:**
```javascript
// Click "Export to Clipboard" in Constraint Manager
// Produces JSON like:
{
  "3": {
    "curveFactor": [-2.0, 0.5],
    "handleAngle": [30, 120]
  },
  "4": {
    "curveFactor": [-1.5, 0.8]
  }
}
```

**Import:**
1. Copy constraint JSON from colleague/team
2. Click "Manage Constraints"
3. Click "Import from Clipboard" or "Import from JSON"
4. Paste JSON and click "Import JSON"
5. Constraints are applied immediately

### Managing Constraints

**View All Constraints:**
- Click "Manage Constraints"
- Table shows all n-values and their constraints

**Edit Single Constraint:**
- Find the constraint in the table
- Click "Clear Min" or "Clear Max" to adjust
- Re-enter Feedback Mode to set new values

**Remove Parameter Constraint:**
- Click "Delete" next to the constraint row
- Both min and max are removed

**Remove All Constraints for N-Value:**
- Clear each parameter individually or
- Export, edit JSON, and re-import

**Reset Everything:**
- Click "Reset to Defaults" in Constraint Manager
- Confirms before wiping all data

## Technical Details

### Persistence

- Constraints stored in `localStorage`
- Key: `flowangle_constraints`
- Automatically saves on every change
- Survives browser refresh

### Range Resolution

Priority order:
1. User-defined constraints (if exist)
2. Feedback mode ranges (if enabled)
3. Normal mode ranges (default)

### Events

The ConstraintManager emits events:
- `constraint-set`: When min/max is captured
- `constraint-cleared`: When constraint removed
- `constraints-cleared`: When all cleared for an n
- `import-success`: After successful import
- `import-error`: After failed import
- `export-success`: After successful export
- `export-error`: After failed export
- `feedback-mode-changed`: When mode toggled
- `reset-complete`: After reset to defaults

### Animation Transitions

When switching modes or changing n:
- Sliders fade to 50% opacity
- Ranges update
- Sliders fade back to 100%
- Values clamped if outside new range
- Duration: 300ms

## Best Practices

### For Exploration

1. Start in Feedback Mode for new n-values
2. Push parameters to extremes
3. Note when shapes become uninteresting
4. Capture those boundaries
5. Switch to Normal Mode for refined work

### For Collaboration

1. Export constraints after exploration session
2. Share JSON with team
3. Team imports and builds on findings
4. Iterate and refine ranges together

### For Different Use Cases

**Strict Constraints (Design System):**
```javascript
{
  "3": { "curveFactor": [-0.7, -0.6], "handleAngle": [59, 61] }
}
```

**Generous Constraints (Exploration):**
```javascript
{
  "3": { "curveFactor": [-5, 2], "handleAngle": [10, 170] }
}
```

**Asymmetric Constraints:**
```javascript
{
  "3": { "curveFactor": [-10, 0.5] }  // Allow extreme negatives, mild positives
}
```

## Troubleshooting

**Constraints Not Applying:**
- Check if Feedback Mode is OFF (constraints only work in Normal Mode)
- Verify n-value matches saved constraint
- Check browser console for errors

**Cannot Import JSON:**
- Validate JSON syntax (use jsonlint.com)
- Ensure structure matches format
- Check for null values vs missing keys

**Lost Constraints:**
- Check localStorage wasn't cleared
- Try Export immediately after creating constraints
- Keep backup JSON files

**Slider Stuck at Edge:**
- You may have set min=max
- Clear constraint and reset
- Re-capture with proper range

## API Reference

### ConstraintManager Class

```javascript
// Initialize
const cm = new ConstraintManager('storage_key');

// Set constraint
cm.setConstraint(n, param, value, type);
// n: number (sides)
// param: 'curveFactor' | 'handleAngle' | 'rotation'
// value: number
// type: 'min' | 'max'

// Get constraints for n
const constraints = cm.getConstraints(n);

// Get effective range
const range = cm.getEffectiveRange(n, param);
// Returns: { min, max, step }

// Clear specific constraint
cm.clearConstraint(n, param, type);
// type: 'min' | 'max' | 'both'

// Export/Import
const json = cm.exportToJSON();
const success = cm.importFromJSON(json);

// Reset
cm.resetToDefaults();

// Events
cm.addListener((event, data) => {
  console.log(event, data);
});
```

## Future Enhancements

Potential additions:
- Constraint templates (presets)
- Visual constraint history
- Constraint recommendations based on usage
- Range validation warnings
- Constraint inheritance (copy n=3 to n=4)
- Animated constraint visualization
- Export constraints with current state

## Changelog

### v1.0.0 - Initial Release
- Feedback Mode toggle
- Constraint capture (Set Min/Max)
- Constraint Manager panel
- Import/Export functionality
- localStorage persistence
- Range animations
- Event system
- Statistics dashboard
