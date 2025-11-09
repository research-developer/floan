# FlowAngle Constraints Manager - Testing Guide

## Quick Start

Open the constraints manager:
```bash
open /Users/preston/research-developer/svGen/flowangle_constraints.html
```

## Interactive Test Scenarios

### Scenario 1: Valid Triquetra (Baseline)
**Purpose:** Establish a known-good baseline configuration

**Steps:**
1. Click "Triquetra" preset button
2. Observe validity overlay

**Expected Results:**
- Validity Score: 100%
- Status: "All checks passed"
- Green color coding
- Message: "Current parameters produce valid geometry"
- Shape: Classic triquetra with smooth curves

**Parameters:**
- n = 3
- Curve Factor = -0.66
- Handle Angle = 60°
- Rotation = 0°

---

### Scenario 2: Extreme Negative Curve (Warning State)
**Purpose:** Test warning detection for extreme curve values

**Steps:**
1. Set n = 3
2. Drag Curve Factor slider to -2.5
3. Keep Handle Angle at 60°
4. Observe changes in validity display

**Expected Results:**
- Validity Score: 85-95%
- Warning: "Extreme curve factor value"
- Yellow color coding
- Recommendation: "For n=3, try curve factor between -2.50 and 0.65"
- Shape: Very pronounced inward curves, but still valid

**What to Look For:**
- Validity overlay changes to yellow
- Warning message appears
- Shape remains connected but curves are extreme
- No red error messages

---

### Scenario 3: Triangle Edge Intersection (Critical Error)
**Purpose:** Test critical error detection

**Steps:**
1. Set n = 5
2. Set Curve Factor to -2.8
3. Set Handle Angle to 150°
4. Enable "Show Guides" checkbox
5. Enable "Highlight Problems" checkbox

**Expected Results:**
- Validity Score: 0-40% (CRITICAL)
- Error: "Guide triangle edges intersect"
- Multiple errors: "Curve self-intersects"
- Red color coding
- Shape stroke becomes red and thick (3px)
- Shape fill becomes light red

**What to Look For:**
- Guide triangles visibly overlap (red dashed lines)
- Curves cross over themselves
- Shape is clearly broken/invalid
- Multiple red error messages in validity overlay
- Detection Details shows multiple issues

---

### Scenario 4: Control Points Outside Bounds (Warning)
**Purpose:** Test boundary checking

**Steps:**
1. Set n = 12
2. Set Curve Factor to -1.5
3. Set Handle Angle to 15°
4. Enable "Show Guides"

**Expected Results:**
- Validity Score: 60-80%
- Warnings: "Control points outside triangle" (multiple lobes)
- Yellow color coding
- Recommendation: "Try handle angle between 38° and 65°"

**What to Look For:**
- Red and green control point circles outside triangle bounds
- Yellow warning messages for each affected lobe
- Shape still connected but geometry is stressed
- Safe ranges shown in "Current Limits" section

---

### Scenario 5: Many-Sided Shape Constraints
**Purpose:** Test adaptive safe ranges for high n values

**Steps:**
1. Set n = 12
2. Try different curve factors from -3 to 1
3. Try different handle angles from 10° to 170°
4. Watch recommendations update

**Expected Results:**
- Safe Curve range narrows: approximately -1.65 to 0.55
- Safe Angle range narrows: approximately 38° to 75°
- Recommendations become more restrictive
- Easier to trigger warnings with extreme values

**What to Look For:**
- "Current Limits" panel shows tighter safe ranges
- More warnings as you move outside safe zones
- Shape becomes more sensitive to parameter changes
- Recommendations guide you back to safe ranges

---

### Scenario 6: Capture and Apply Constraints
**Purpose:** Test constraint storage system

**Steps:**
1. Set n = 6
2. Set Curve Factor = -0.8
3. Set Handle Angle = 30°
4. Set Rotation = 0°
5. Click "Capture Current Limits" button
6. Change n to 3
7. Adjust parameters randomly
8. Change n back to 6
9. Find saved constraint in "Saved Constraints" section
10. Click "Apply" button

**Expected Results:**
- After capture: "Current Capture" section briefly highlights green
- Constraint card appears in "Saved Constraints" with n=6
- After Apply: All parameters restore to captured values
- Multiple constraints can be saved for different n values

**What to Look For:**
- Saved constraint shows all parameter values
- Apply button restores exact configuration
- Delete button removes constraint
- Constraints sorted by n value

---

### Scenario 7: Control Point Proximity Warning
**Purpose:** Test edge proximity detection

**Steps:**
1. Set n = 4
2. Set Curve Factor = -0.3
3. Set Handle Angle = 170°
4. Enable "Show Guides"

**Expected Results:**
- Validity Score: 70-90%
- Warnings: "Control point near edge"
- Control points visible very close to triangle edges
- Yellow warning state

**What to Look For:**
- Control points (red/green dots) very close to triangle edges
- Warning in validity messages
- Shape is valid but geometry is cramped
- Recommendation to adjust handle angle

---

### Scenario 8: Preset Comparison
**Purpose:** Test all presets and compare validity

**Steps:**
1. Click "Triquetra" preset
2. Note validity score
3. Click "Flower" preset
4. Note validity score
5. Click "Star" preset
6. Note validity score
7. Click "Smooth" preset
8. Note validity score

**Expected Results:**
- Triquetra: 100% (n=3, curve=-0.66, angle=60°)
- Flower: 100% (n=6, curve=-0.8, angle=30°)
- Star: 95-100% (n=5, curve=-1.2, angle=36°)
- Smooth: 100% (n=8, curve=-0.5, angle=22.5°)

**What to Look For:**
- All presets should be valid or near-valid
- Different shapes demonstrate different parameter ranges
- Safe ranges adjust automatically with n
- Recommendations minimal or absent for presets

---

### Scenario 9: Real-Time Detection During Dragging
**Purpose:** Test performance and real-time updates

**Steps:**
1. Set n = 5
2. Enable "Show Guides" and "Highlight Problems"
3. Slowly drag Curve Factor slider from -3 to 1
4. Watch validity score and color changes
5. Slowly drag Handle Angle slider from 10° to 170°

**Expected Results:**
- Validity score updates in real-time
- Color transitions smoothly: green → yellow → red
- Issues appear and disappear as parameters change
- No lag or stuttering
- Shape updates immediately

**What to Look For:**
- Smooth transitions between states
- Instant feedback on every slider movement
- Detection is fast enough for real-time use
- Messages update immediately
- No performance issues

---

### Scenario 10: Detection Details Analysis
**Purpose:** Verify all detection checks are running

**Steps:**
1. Set n = 3, curve = -0.66, angle = 60° (Triquetra)
2. Scroll to "Detection Details" section in right panel
3. Review all information
4. Change to invalid parameters (n=5, curve=-2.8, angle=150°)
5. Review updated detection details

**Expected Results:**

**Valid State:**
```
Geometry:
Vertices: 3
Triangles: 3

Checks Run:
✓ Triangle edge intersections
✓ Control points in bounds
✓ Bezier self-intersection
✓ Control point proximity
✓ Parameter extremes

Result:
Score: 100%
Issues: 0
Warnings: 0
```

**Invalid State:**
```
Geometry:
Vertices: 5
Triangles: 5

Checks Run:
✓ Triangle edge intersections
✓ Control points in bounds
✓ Bezier self-intersection
✓ Control point proximity
✓ Parameter extremes

Result:
Score: 25%
Issues: 3-6
Warnings: 2-5
```

---

## Checklist for Complete Testing

### Functionality Tests
- [ ] Valid shapes show 100% score
- [ ] Warning shapes show 40-69% score
- [ ] Error shapes show 0-39% score
- [ ] Triangle intersection detection works
- [ ] Bezier self-intersection detection works
- [ ] Control point boundary checking works
- [ ] Control point proximity detection works
- [ ] Parameter extreme detection works

### Visual Feedback Tests
- [ ] Green color for valid states
- [ ] Yellow color for warning states
- [ ] Red color for error states
- [ ] Shape highlighting works
- [ ] Guide triangle coloring works
- [ ] Control points visible in guide mode
- [ ] Problem highlighting toggle works

### Constraint System Tests
- [ ] Safe ranges calculate correctly for each n
- [ ] Recommendations appear when needed
- [ ] Recommendations are helpful and accurate
- [ ] Capture constraints button works
- [ ] Saved constraints display correctly
- [ ] Apply constraint restores parameters
- [ ] Delete constraint removes from list
- [ ] Multiple constraints can coexist

### UI/UX Tests
- [ ] Validity overlay is readable
- [ ] Issue messages are clear
- [ ] Constraints panel is organized
- [ ] Controls are responsive
- [ ] Sliders update smoothly
- [ ] Preset buttons work
- [ ] Toggle switches work
- [ ] No visual glitches

### Performance Tests
- [ ] Real-time updates are smooth
- [ ] No lag when dragging sliders
- [ ] Detection runs without delay
- [ ] Shape renders immediately
- [ ] No browser freezing
- [ ] Works with n=1 to n=12

## Success Criteria

All tests should pass with:
1. ✅ Accurate detection of all invalid states
2. ✅ Clear visual feedback for all states
3. ✅ Helpful recommendations for improvements
4. ✅ Smooth real-time performance
5. ✅ Reliable constraint storage/retrieval
6. ✅ Intuitive user interface

## Troubleshooting

### Issue: Validity score seems wrong
- Check that all detection functions are running (see Detection Details)
- Verify parameters are within expected ranges
- Try preset shapes to establish baseline

### Issue: Visual feedback not showing
- Ensure "Highlight Problems" is checked
- Verify browser supports SVG rendering
- Check browser console for errors

### Issue: Constraints not saving
- Check JavaScript console for errors
- Verify capture button is clickable
- Try different parameter combinations

### Issue: Performance is slow
- Reduce n value (higher n = more triangles = more checks)
- Disable "Show Guides" for better performance
- Close other browser tabs

## Developer Notes

### Adding New Test Scenarios
To add a new test scenario:
1. Define clear parameters
2. Document expected validity score
3. List expected issues/warnings
4. Describe what to look for visually
5. Add to checklist above

### Debugging Detection
All detection functions log to console:
```javascript
console.log('Triangle intersection detected', triangleIndex);
console.log('Bezier self-intersection', lobeIndex);
console.log('Control point outside', lobeIndex, controlPoint);
```

Enable verbose logging by uncommenting debug statements in the code.

### Validity Score Breakdown
```javascript
Base: 100%
- Triangle edge intersection: -40%
- Bezier self-intersection: -15% per lobe
- Control point outside: -5% per lobe
- Control point proximity: -3% per lobe
- Extreme parameters: -5%

Minimum: 0%
Maximum: 100%
```

## Conclusion

This comprehensive testing guide ensures all features of the FlowAngle Constraints Manager are thoroughly validated. Complete all scenarios to verify the system meets all requirements.

**Recommended Testing Order:**
1. Start with Scenario 1 (baseline)
2. Test Scenarios 2-4 (different error types)
3. Test Scenarios 5-7 (edge cases)
4. Test Scenarios 8-10 (integration features)
5. Complete full checklist
6. Verify success criteria

**Estimated Testing Time:** 30-45 minutes for complete coverage
