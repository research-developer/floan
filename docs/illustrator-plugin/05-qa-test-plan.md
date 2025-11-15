# QA Test Plan & Report: FloAng Illustrator Plugin

**Test Plan Version**: 1.0
**Date**: 2025-11-11
**QA Engineer**: BMAD QA Engineer
**Feature**: floang-illustrator-plugin
**Review Status Reference**: Pass with Risk (Y-axis bug fixed, UXP platform accepted)

---

## Executive Summary

This test plan provides comprehensive test cases for the FloAng Illustrator Plugin. The plugin has been implemented using Adobe's UXP (Unified Extensibility Platform) and requires Illustrator 2021 or later.

**CRITICAL NOTE**: This test plan is designed for manual execution by a QA tester with Adobe Illustrator installed. The test environment (Claude Code) does not have access to Illustrator, so all tests are marked as **NOT EXECUTED** with detailed procedures for human testers to follow.

### Test Environment Requirements
- **Software**: Adobe Illustrator 2021, 2022, 2023, or 2024
- **Operating Systems**: macOS 10.15+ or Windows 10 (version 1809+)
- **Plugin Installation**: UXP plugin loaded via developer mode or ZXP installation
- **Test Data**: Reference SVG files from FloAng.html web version

### Key Focus Areas (Per Review Report)
1. **Y-axis Coordinate Correctness** (CRITICAL - bug was fixed)
2. **Algorithm Accuracy vs. FloAng.html Reference** (HIGH PRIORITY)
3. **All 4 Preset Configurations** (HIGH PRIORITY)
4. **Parameter Validation and Error Handling** (MEDIUM PRIORITY)
5. **UI Responsiveness and Feedback** (MEDIUM PRIORITY)

---

## Test Coverage Summary

| Category | Test Cases | Priority | Status |
|----------|-----------|----------|--------|
| Algorithm Accuracy | 12 | CRITICAL | NOT EXECUTED |
| Coordinate System Validation | 8 | CRITICAL | NOT EXECUTED |
| Preset Functionality | 5 | HIGH | NOT EXECUTED |
| Parameter Edge Cases | 15 | HIGH | NOT EXECUTED |
| UI Controls & Responsiveness | 10 | MEDIUM | NOT EXECUTED |
| Error Handling | 8 | MEDIUM | NOT EXECUTED |
| Cross-Platform Compatibility | 6 | MEDIUM | NOT EXECUTED |
| Performance & Scalability | 5 | LOW | NOT EXECUTED |
| **TOTAL** | **69** | - | **NOT EXECUTED** |

---

## Section 1: Algorithm Accuracy Testing

### Test Suite 1.1: Triquetra Preset (n=3) - Reference Validation

**Test ID**: QA-ALG-001
**Priority**: CRITICAL
**Category**: Algorithm Accuracy
**Status**: ❌ NOT EXECUTED - Requires Illustrator

#### Prerequisites
- Adobe Illustrator open with 600×600pt artboard
- FloAng plugin loaded and accessible
- Reference SVG from FloAng.html web version for Triquetra preset

#### Test Steps
1. Open Adobe Illustrator
2. Create new document: File → New → 600×600pt artboard
3. Open FloAng plugin panel (Window → Extensions → FloAng)
4. Click "Triquetra" preset button
5. Verify parameters loaded:
   - Sides: 3
   - Flow: -0.66
   - Angle: 60°
   - Rotation: -30°
6. Click "Generate" button
7. Export generated pattern: File → Export → SVG
8. Compare with reference FloAng.html Triquetra SVG

#### Expected Results
- ✅ Pattern generates without errors
- ✅ Pattern has exactly 3 vertices forming triangle
- ✅ Curves flow smoothly between vertices with inward curvature
- ✅ Pattern is NOT vertically flipped (topmost vertex should be at top)
- ✅ Overlay test with web version shows <5px deviation
- ✅ Mathematical orientation correct: Y-axis points upward from center

#### Pass Criteria
- Visual comparison passes (no vertical flip, no rotation errors)
- Overlay test deviation < 5 pixels
- Vertex positions match calculated expectations

#### Actual Results
**NOT EXECUTED** - Requires Illustrator testing environment

#### Notes for Tester
This is THE most critical test. The Y-axis bug fix means patterns should NO LONGER be vertically flipped. If pattern appears upside-down compared to web version, the bug has regressed.

---

### Test Suite 1.2: Flower Preset (n=6) - Hexagonal Symmetry

**Test ID**: QA-ALG-002
**Priority**: CRITICAL
**Category**: Algorithm Accuracy
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 800×800pt artboard
- FloAng plugin loaded

#### Test Steps
1. Create 800×800pt artboard
2. Click "Flower" preset button
3. Verify parameters:
   - Sides: 6
   - Flow: -0.8
   - Angle: 30°
   - Rotation: 0°
4. Click "Generate"
5. Measure pattern with Illustrator's measurement tools

#### Expected Results
- ✅ Pattern has exactly 6 vertices
- ✅ Perfect hexagonal symmetry (120° between vertices)
- ✅ Inward-flowing curves (negative flow)
- ✅ Pattern centered on artboard
- ✅ No vertical flip (top vertex at top)

#### Pass Criteria
- 6 vertices evenly distributed
- Symmetry axis alignment correct
- Visual comparison with web version passes

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 1.3: Star Preset (n=5) - Pentagonal Pattern

**Test ID**: QA-ALG-003
**Priority**: HIGH
**Category**: Algorithm Accuracy
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 600×600pt artboard
- FloAng plugin loaded

#### Test Steps
1. Create 600×600pt artboard
2. Click "Star" preset
3. Verify parameters:
   - Sides: 5
   - Flow: -1.8
   - Angle: 72°
   - Rotation: -18°
4. Generate pattern
5. Visually inspect star-like formation

#### Expected Results
- ✅ 5-pointed star-like pattern
- ✅ Strong inward curves (flow = -1.8)
- ✅ 72° handle angles create sharp star points
- ✅ Rotation of -18° positions one point upward
- ✅ No coordinate system errors

#### Pass Criteria
- Pentagonal symmetry maintained
- Star points clearly defined
- Rotation applied correctly

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 1.4: Smooth Preset (n=6) - Outward Flow

**Test ID**: QA-ALG-004
**Priority**: HIGH
**Category**: Algorithm Accuracy
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 600×600pt artboard

#### Test Steps
1. Create artboard
2. Click "Smooth" preset
3. Verify parameters:
   - Sides: 6
   - Flow: 1.0
   - Angle: 120°
   - Rotation: 0°
4. Generate pattern

#### Expected Results
- ✅ Smooth outward-flowing curves (positive flow)
- ✅ 120° angles create very smooth curves
- ✅ Hexagonal structure visible
- ✅ Pattern looks "blooming" outward

#### Pass Criteria
- Positive flow visible (outward curves)
- Smooth transitions between segments
- No coordinate transformation errors

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 1.5: Circle Case (n=1) - Special Case Handling

**Test ID**: QA-ALG-005
**Priority**: HIGH
**Category**: Algorithm Accuracy - Edge Cases
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 400×400pt artboard

#### Test Steps
1. Create artboard
2. Manually set Sides slider to 1
3. Click Generate
4. Verify circle created

#### Expected Results
- ✅ Perfect circle rendered
- ✅ Circle centered on artboard
- ✅ Radius calculated appropriately (artboard size × 0.25)
- ✅ Stroke applied (no fill)
- ✅ No algorithm errors for n=1 edge case

#### Pass Criteria
- Circle is mathematically perfect (not oval)
- Positioned at exact artboard center
- Appropriate size relative to artboard

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 1.6: Quadratic Curve (n=2) - Two-Point Edge Case

**Test ID**: QA-ALG-006
**Priority**: HIGH
**Category**: Algorithm Accuracy - Edge Cases
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 600×600pt artboard

#### Test Steps
1. Create artboard
2. Set Sides slider to 2
3. Set Flow to various values: -2, 0, 0.5
4. Generate patterns for each flow value
5. Observe curve behavior

#### Expected Results
- ✅ Single curved line connecting two points
- ✅ Curve direction changes with flow factor
- ✅ Path is OPEN (not closed)
- ✅ Perpendicular offset calculation correct
- ✅ No coordinate system errors

#### Pass Criteria
- Quadratic curve visible
- Control point positioning logical
- Flow factor affects curve as expected

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 1.7: Mathematical Verification - Vertex Positions

**Test ID**: QA-ALG-007
**Priority**: CRITICAL
**Category**: Algorithm Accuracy - Coordinate Verification
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 1000×1000pt artboard
- Calculator for coordinate verification

#### Test Steps
1. Create 1000×1000pt artboard (center at 500, 500)
2. Generate Triquetra (n=3, rotation=0°)
3. Select pattern with Direct Selection Tool (A)
4. Measure top vertex Y-coordinate using Transform panel

#### Expected Mathematical Results
```
Artboard center: (500, 500)
Radius: 250 (default 0.25 × 1000)
For n=3, rotation=0°:
- Vertex 0 (right): (500 + 250*cos(0°), 500 + 250*sin(0°)) = (750, 500)
- Vertex 1 (top-left): (500 + 250*cos(120°), 500 + 250*sin(120°)) = (375, 716.5)
- Vertex 2 (top-right): (500 + 250*cos(240°), 500 + 250*sin(240°)) = (375, 283.5)
```

#### Expected Results
- ✅ Top-left vertex Y-coordinate ≈ 716.5 (ABOVE center)
- ✅ Bottom-right vertex Y-coordinate ≈ 283.5 (BELOW center)
- ✅ Right vertex Y-coordinate = 500 (AT center level)
- ✅ X-coordinates match calculations within ±2px
- ✅ Y-coordinates match calculations within ±2px

#### Pass Criteria
- Measured coordinates match calculated values ±2px
- Y-axis orientation correct (higher Y = higher position)
- NO vertical flip detected

#### Actual Results
**NOT EXECUTED**

**CRITICAL VERIFICATION NOTE**: This test directly validates the Y-axis bug fix from code review Iteration 2. If this test fails, the coordinate transformation bug has regressed.

---

## Section 2: Coordinate System Validation

### Test Suite 2.1: Y-Axis Orientation Verification

**Test ID**: QA-COORD-001
**Priority**: CRITICAL
**Category**: Coordinate System Validation
**Status**: ❌ NOT EXECUTED

#### Test Objective
Verify that patterns are NOT vertically flipped and Y-axis orientation is mathematically correct.

#### Prerequisites
- Illustrator with 600×600pt artboard
- Reference ruler or grid enabled (View → Show Grid)

#### Test Steps
1. Enable Illustrator grid: View → Show Grid
2. Generate Triquetra preset (n=3, rotation=-30°)
3. Visual inspection: Identify topmost vertex
4. Measure Y-coordinate of topmost vertex
5. Compare with artboard center Y-coordinate

#### Expected Results
- ✅ Topmost vertex has Y-coordinate > artboard center Y
- ✅ Pattern extends UPWARD from center (positive Y direction)
- ✅ Pattern is NOT upside-down compared to web version
- ✅ Visual inspection confirms no vertical flip

#### Pass Criteria
- Y-axis orientation mathematically correct
- Visual comparison with web version identical
- No vertical flip detected in any preset

#### Actual Results
**NOT EXECUTED**

#### Failure Analysis (If Test Fails)
If this test fails, the Y-axis coordinate transformation bug from code review has regressed. Check:
1. `coordinate-transform.js` line 41: Should be `svgPoint.y` (NOT `artboardHeight - svgPoint.y`)
2. Algorithm input: Verify centerY is from artboard, not inverted

---

### Test Suite 2.2: Rotation Parameter Correctness

**Test ID**: QA-COORD-002
**Priority**: HIGH
**Category**: Coordinate System Validation
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 800×800pt artboard

#### Test Steps
1. Create artboard
2. Generate pattern with: n=4, flow=-0.66, angle=90°, rotation=0°
3. Note position of top vertex
4. Change rotation to 45°
5. Generate new pattern
6. Measure rotation difference

#### Expected Results
- ✅ Pattern rotates 45° clockwise
- ✅ Rotation direction consistent with mathematical convention
- ✅ All vertices rotate uniformly
- ✅ Pattern remains centered

#### Pass Criteria
- Rotation angle accurate within ±2°
- Rotation direction correct (positive = counter-clockwise)
- Center position unchanged

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 2.3: Multi-Artboard Centering

**Test ID**: QA-COORD-003
**Priority**: MEDIUM
**Category**: Coordinate System Validation
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator document with 3 artboards of different sizes

#### Test Steps
1. Create document with artboards:
   - Artboard 1: 600×600pt
   - Artboard 2: 1000×800pt
   - Artboard 3: 400×400pt
2. Activate each artboard sequentially
3. Generate Triquetra on each
4. Verify centering

#### Expected Results
- ✅ Pattern centered on each artboard
- ✅ Pattern size scales appropriately (25% of min dimension)
- ✅ No coordinate system errors across artboards

#### Pass Criteria
- Visual centering perfect on all artboards
- Scale calculation correct for each size

#### Actual Results
**NOT EXECUTED**

---

## Section 3: Preset Functionality Testing

### Test Suite 3.1: Preset Button Loading

**Test ID**: QA-PRESET-001
**Priority**: HIGH
**Category**: Preset Functionality
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- FloAng plugin panel open

#### Test Steps
1. Manually set parameters to random values
2. Click "Triquetra" preset button
3. Observe parameter changes in UI
4. Repeat for "Flower", "Star", "Smooth" presets

#### Expected Results
For each preset click:
- ✅ All sliders update immediately
- ✅ Parameter values displayed match preset
- ✅ No UI lag or freezing
- ✅ Preset button highlights as active

#### Pass Criteria
- All 4 presets load correct parameter values
- UI updates smoothly
- Values match specification (see Test ID QA-ALG-001-004)

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 3.2: Preset Visual Output Consistency

**Test ID**: QA-PRESET-002
**Priority**: HIGH
**Category**: Preset Functionality
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- Illustrator with 600×600pt artboard

#### Test Steps
1. Generate Triquetra preset 5 times (delete between each)
2. Export each as SVG
3. Compare all 5 SVG files

#### Expected Results
- ✅ All 5 outputs are IDENTICAL (byte-for-byte if possible)
- ✅ No randomness in generation
- ✅ Deterministic output for same parameters

#### Pass Criteria
- 100% consistency across multiple generations
- No variation in vertex positions or curves

#### Actual Results
**NOT EXECUTED**

---

## Section 4: Parameter Edge Case Testing

### Test Suite 4.1: Flow Factor Extremes

**Test ID**: QA-PARAM-001
**Priority**: HIGH
**Category**: Parameter Validation
**Status**: ❌ NOT EXECUTED

#### Test Matrix

| Test Case | Sides | Flow | Angle | Rotation | Expected Result |
|-----------|-------|------|-------|----------|-----------------|
| 4.1.A | 3 | -3.0 | 60 | 0 | Strong inward curves, no errors |
| 4.1.B | 6 | -2.5 | 120 | 0 | Moderate inward, stable |
| 4.1.C | 3 | 0.0 | 60 | 0 | Straight lines (degenerate handles) |
| 4.1.D | 6 | 0.5 | 120 | 0 | Slight outward bulge |
| 4.1.E | 5 | 1.0 | 108 | 0 | Maximum outward flow |

#### Test Steps
1. For each test case, set parameters as specified
2. Click Generate
3. Observe pattern output
4. Check for errors or visual anomalies

#### Expected Results
- ✅ All extreme values handled without crashes
- ✅ Flow=-3.0: Very sharp inward curves (may approach center)
- ✅ Flow=0.0: Nearly straight line segments
- ✅ Flow=1.0: Smooth outward bulges
- ✅ No coordinate overflow or NaN values

#### Pass Criteria
- No errors for any valid flow value
- Visual output logical for each flow setting
- No coordinate system errors

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 4.2: Handle Angle Extremes

**Test ID**: QA-PARAM-002
**Priority**: MEDIUM
**Category**: Parameter Validation
**Status**: ❌ NOT EXECUTED

#### Test Matrix

| Test Case | Sides | Flow | Angle | Expected Result |
|-----------|-------|------|-------|-----------------|
| 4.2.A | 3 | -0.66 | 10° | Very sharp triangle apex |
| 4.2.B | 6 | -0.8 | 45° | Moderate apex angle |
| 4.2.C | 5 | -1.0 | 90° | Right-angle triangle apex |
| 4.2.D | 4 | -0.5 | 150° | Very flat triangle apex |
| 4.2.E | 3 | -0.66 | 170° | Nearly straight baseline |

#### Expected Results
- ✅ All angle values generate valid patterns
- ✅ Low angles: Sharp curve transitions
- ✅ High angles: Smooth, gradual curves
- ✅ No mathematical errors (division by zero, tan() overflow)

#### Pass Criteria
- Successful generation for all angles 0°-180°
- Curve character changes appropriately with angle
- No algorithm failures

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 4.3: Sides Parameter Range

**Test ID**: QA-PARAM-003
**Priority**: HIGH
**Category**: Parameter Validation
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Test each value of Sides from 1 to 12
2. For each value, generate pattern with default parameters
3. Verify vertex count and symmetry

#### Expected Results

| Sides | Pattern Type | Vertices | Symmetry | Special Notes |
|-------|--------------|----------|----------|---------------|
| 1 | Circle | N/A | Radial | Perfect circle |
| 2 | Quadratic | 2 | Bilateral | Open path |
| 3 | Triangle | 3 | 3-fold | Triquetra base |
| 4 | Square | 4 | 4-fold | 90° rotational symmetry |
| 5 | Pentagon | 5 | 5-fold | Star patterns possible |
| 6 | Hexagon | 6 | 6-fold | Flower patterns |
| 7 | Heptagon | 7 | 7-fold | Rare geometry |
| 8 | Octagon | 8 | 8-fold | High symmetry |
| 9-12 | Polygons | 9-12 | N-fold | Complex patterns |

#### Pass Criteria
- All values 1-12 generate without errors
- Vertex count matches Sides parameter
- Appropriate symmetry for each polygon

#### Actual Results
**NOT EXECUTED**

---

## Section 5: UI Controls & Responsiveness

### Test Suite 5.1: Slider Interaction

**Test ID**: QA-UI-001
**Priority**: MEDIUM
**Category**: UI Responsiveness
**Status**: ❌ NOT EXECUTED

#### Prerequisites
- FloAng plugin panel open

#### Test Steps
1. Interact with each slider:
   - Flow slider: Drag from -3 to 1
   - Angle slider: Drag full range
   - Spin slider: Drag from -360 to 360
   - Sides slider: Step through 1-12
2. Observe value display updates
3. Test keyboard controls (arrow keys)
4. Test rapid dragging

#### Expected Results
- ✅ Sliders respond smoothly with no lag
- ✅ Value display updates in real-time
- ✅ Keyboard arrow keys adjust values
- ✅ No UI freezing during interaction
- ✅ Values constrain to valid ranges

#### Pass Criteria
- <50ms response time for slider updates
- Value display always synchronized with slider
- No visual glitches

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 5.2: Generate Button Behavior

**Test ID**: QA-UI-002
**Priority**: MEDIUM
**Category**: UI Responsiveness
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Click Generate button with valid parameters
2. Observe button state during generation
3. Test rapid clicking (5 clicks in 2 seconds)
4. Generate with no document open
5. Generate with locked layer

#### Expected Results
- ✅ Button shows loading/processing state during generation
- ✅ Pattern appears on artboard after generation
- ✅ Rapid clicking doesn't create duplicate patterns
- ✅ Error message shown if no document
- ✅ Clear error message if layer locked

#### Pass Criteria
- Button disabled during generation
- Appropriate error messages displayed
- No crashes from edge case interactions

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 5.3: Debug Menu (Cmd+Shift+D)

**Test ID**: QA-UI-003
**Priority**: LOW
**Category**: UI Functionality - Debug Features
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Open plugin panel
2. Press Cmd+Shift+D (macOS) or Ctrl+Shift+D (Windows)
3. Verify debug display appears
4. Check parameter values shown
5. Toggle debug mode off

#### Expected Results
- ✅ Debug menu appears on keyboard shortcut
- ✅ Current parameter values displayed
- ✅ Debug mode can be toggled
- ✅ No impact on pattern generation functionality

#### Pass Criteria
- Keyboard shortcut works
- Debug information accurate
- Toggle functional

#### Actual Results
**NOT EXECUTED**

#### Known Limitation (Per Review Report)
File-based logging and performance profiling are NOT implemented in MVP. Debug menu shows only current parameters.

---

## Section 6: Error Handling Testing

### Test Suite 6.1: No Document Open

**Test ID**: QA-ERROR-001
**Priority**: HIGH
**Category**: Error Handling
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Close all Illustrator documents
2. Open FloAng plugin
3. Set parameters
4. Click Generate

#### Expected Results
- ✅ Clear error message: "No document open. Please create or open a document."
- ✅ No plugin crash
- ✅ UI remains responsive
- ✅ Error message dismissible

#### Pass Criteria
- User-friendly error message
- No console errors
- Plugin recovers gracefully

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 6.2: Locked Layer

**Test ID**: QA-ERROR-002
**Priority**: HIGH
**Category**: Error Handling
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Open document
2. Lock active layer (Layer panel → Lock icon)
3. Attempt to generate pattern

#### Expected Results
- ✅ Error message: "Active layer is locked. Please unlock the layer to generate patterns."
- ✅ No crash
- ✅ Generation blocked

#### Pass Criteria
- Clear error message displayed
- No pattern created on locked layer
- Plugin remains functional

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 6.3: Invalid Parameter Validation

**Test ID**: QA-ERROR-003
**Priority**: MEDIUM
**Category**: Error Handling
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Attempt to set invalid parameter values (beyond slider ranges)
2. Test boundary conditions:
   - Sides: 0, 13, -1
   - Flow: -4, 2, NaN
   - Angle: -10, 200
   - Rotation: 400, -400

#### Expected Results
- ✅ UI prevents invalid values (sliders constrained)
- ✅ If invalid value entered, validation error shown
- ✅ No pattern generation with invalid parameters
- ✅ Clear error messages for each validation failure

#### Pass Criteria
- All invalid inputs rejected
- Error messages helpful and specific
- Plugin doesn't crash on invalid input

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 6.4: Zero or Negative Artboard Dimensions

**Test ID**: QA-ERROR-004
**Priority**: LOW
**Category**: Error Handling - Edge Cases
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Create document with malformed artboard (if possible)
2. Attempt to generate pattern
3. Observe error handling

#### Expected Results
- ✅ Error message if artboard invalid
- ✅ No division by zero errors
- ✅ Graceful failure

#### Pass Criteria
- Defensive error handling present
- No crashes

#### Actual Results
**NOT EXECUTED**

#### Note for Tester
This test may be difficult to execute as Illustrator prevents creating invalid artboards. Test by modifying document properties if possible.

---

## Section 7: Cross-Platform Compatibility

### Test Suite 7.1: macOS vs Windows Behavior

**Test ID**: QA-PLATFORM-001
**Priority**: MEDIUM
**Category**: Cross-Platform Compatibility
**Status**: ❌ NOT EXECUTED

#### Test Matrix

| Feature | macOS | Windows | Expected |
|---------|-------|---------|----------|
| Plugin loads | ? | ? | Identical |
| UI renders | ? | ? | Identical |
| Keyboard shortcuts | ? | ? | Platform-appropriate (Cmd vs Ctrl) |
| Slider interaction | ? | ? | Identical |
| Pattern generation | ? | ? | Identical output |
| File paths | ? | ? | OS-appropriate |

#### Test Steps
1. Install plugin on both macOS and Windows
2. Test all core functionality on both platforms
3. Generate identical patterns on both
4. Export and compare SVG files

#### Expected Results
- ✅ Plugin functions identically on both platforms
- ✅ Generated patterns are identical (byte-for-byte SVG comparison)
- ✅ UI renders correctly on both platforms
- ✅ No platform-specific bugs

#### Pass Criteria
- 100% functional parity between platforms
- Generated patterns identical

#### Actual Results
**NOT EXECUTED ON MACOS**
**NOT EXECUTED ON WINDOWS**

---

### Test Suite 7.2: Illustrator Version Compatibility

**Test ID**: QA-PLATFORM-002
**Priority**: MEDIUM
**Category**: Cross-Platform Compatibility
**Status**: ❌ NOT EXECUTED

#### Test Matrix

| Illustrator Version | Plugin Loads | Basic Generation | All Features | Notes |
|---------------------|--------------|------------------|--------------|-------|
| Illustrator 2021 | ? | ? | ? | Minimum required version |
| Illustrator 2022 | ? | ? | ? | |
| Illustrator 2023 | ? | ? | ? | |
| Illustrator 2024 | ? | ? | ? | Latest stable |
| Illustrator 2025 Beta | ? | ? | ? | If available |

#### Test Steps
1. Install plugin on each Illustrator version
2. Test core functionality:
   - Load plugin
   - Generate Triquetra preset
   - Test all parameter controls
   - Verify pattern accuracy
3. Document any version-specific issues

#### Expected Results
- ✅ Plugin loads on Illustrator 2021+
- ✅ All features functional across versions
- ✅ No API compatibility issues
- ✅ Pattern output identical across versions

#### Pass Criteria
- Works on all versions 2021+
- No version-specific bugs

#### Actual Results
**NOT EXECUTED - Requires testing across multiple Illustrator installations**

---

## Section 8: Performance & Scalability

### Test Suite 8.1: Generation Time Benchmarks

**Test ID**: QA-PERF-001
**Priority**: LOW
**Category**: Performance
**Status**: ❌ NOT EXECUTED

#### Test Matrix

| Pattern | Sides | Expected Time | Actual Time | Pass/Fail |
|---------|-------|---------------|-------------|-----------|
| Simple | 3 | <1 second | ? | ? |
| Medium | 6 | <1 second | ? | ? |
| Complex | 12 | <2 seconds | ? | ? |
| Circle | 1 | <0.5 seconds | ? | ? |

#### Test Steps
1. For each pattern type:
2. Start timer
3. Click Generate
4. Measure time until pattern appears on artboard
5. Record timing

#### Expected Results (Per PRD)
- ✅ Standard patterns (n=3-8): <1 second
- ✅ Complex patterns (n=9-12): <2 seconds
- ✅ UI remains responsive throughout generation

#### Pass Criteria
- All patterns meet performance targets
- No UI freezing

#### Actual Results
**NOT EXECUTED**

---

### Test Suite 8.2: Rapid Generation Stress Test

**Test ID**: QA-PERF-002
**Priority**: LOW
**Category**: Performance - Stress Testing
**Status**: ❌ NOT EXECUTED

#### Test Steps
1. Generate 50 consecutive patterns without closing Illustrator
2. Delete patterns periodically to avoid document bloat
3. Monitor for:
   - Memory leaks
   - Performance degradation
   - UI responsiveness
   - Errors

#### Expected Results
- ✅ No memory leaks after 50 generations
- ✅ Generation time remains consistent
- ✅ No crashes or errors
- ✅ UI remains responsive

#### Pass Criteria
- 50+ consecutive generations without issues
- Performance stable throughout

#### Actual Results
**NOT EXECUTED**

---

## Section 9: Known Issues & Limitations (Per Review Report)

### Issue 1: Missing Undo Grouping
**Severity**: MODERATE
**Impact**: User Experience

**Description**: Pattern generation does not create an Illustrator undo group. Users must undo individual path operations rather than the entire generation in one undo step.

**Workaround**: Use Edit → Undo multiple times, or select and delete pattern manually.

**Recommendation**: Add to Phase 2 polish.

---

### Issue 2: No Edge Case Validation for Artboard Dimensions
**Severity**: LOW
**Impact**: Rare edge case crashes

**Description**: Plugin does not validate artboard dimensions for negative or zero values. Malformed documents could cause crashes.

**Workaround**: Ensure artboards are valid before using plugin.

**Recommendation**: Add defensive validation in next release.

---

### Issue 3: No File-Based Logging
**Severity**: LOW
**Impact**: Developer debugging only

**Description**: Debug menu shows only current parameters. No performance profiling or file-based logging available.

**Workaround**: Use browser console for debugging (Cmd+Option+I in Illustrator UXP).

**Recommendation**: Phase 2 feature.

---

## Test Execution Checklist for Human QA Tester

### Pre-Testing Setup
- [ ] Install Adobe Illustrator 2021 or later
- [ ] Install FloAng UXP plugin (developer mode or ZXP)
- [ ] Download reference SVG files from FloAng.html web version
- [ ] Prepare test artboards (600×600, 800×800, 1000×1000pt)
- [ ] Enable Illustrator grid and rulers (View menu)
- [ ] Have calculator ready for coordinate verification

### Critical Priority Tests (Execute First)
- [ ] QA-ALG-001: Triquetra Preset Reference Validation
- [ ] QA-ALG-007: Mathematical Verification - Vertex Positions
- [ ] QA-COORD-001: Y-Axis Orientation Verification
- [ ] QA-ALG-002: Flower Preset Hexagonal Symmetry
- [ ] QA-ALG-003: Star Preset Pentagonal Pattern
- [ ] QA-ALG-004: Smooth Preset Outward Flow

### High Priority Tests
- [ ] QA-ALG-005: Circle Case (n=1)
- [ ] QA-ALG-006: Quadratic Curve (n=2)
- [ ] QA-COORD-002: Rotation Parameter Correctness
- [ ] QA-PRESET-001: Preset Button Loading
- [ ] QA-PRESET-002: Preset Visual Output Consistency
- [ ] QA-PARAM-001: Flow Factor Extremes
- [ ] QA-PARAM-003: Sides Parameter Range
- [ ] QA-ERROR-001: No Document Open
- [ ] QA-ERROR-002: Locked Layer

### Medium Priority Tests
- [ ] QA-COORD-003: Multi-Artboard Centering
- [ ] QA-PARAM-002: Handle Angle Extremes
- [ ] QA-UI-001: Slider Interaction
- [ ] QA-UI-002: Generate Button Behavior
- [ ] QA-ERROR-003: Invalid Parameter Validation
- [ ] QA-PLATFORM-001: macOS vs Windows Behavior
- [ ] QA-PLATFORM-002: Illustrator Version Compatibility

### Low Priority Tests
- [ ] QA-UI-003: Debug Menu
- [ ] QA-ERROR-004: Zero or Negative Artboard Dimensions
- [ ] QA-PERF-001: Generation Time Benchmarks
- [ ] QA-PERF-002: Rapid Generation Stress Test

---

## Bug Report Template

When reporting bugs, use this template:

```markdown
**Bug ID**: [Unique identifier]
**Test ID**: [Associated test case]
**Severity**: Critical / High / Medium / Low
**Status**: Open

**Environment**:
- OS: [macOS/Windows version]
- Illustrator: [Version]
- Plugin Version: [Version]

**Description**:
[Clear description of the bug]

**Steps to Reproduce**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result**:
[What should happen]

**Actual Result**:
[What actually happened]

**Screenshots/Files**:
[Attach screenshots, SVG exports, or error logs]

**Workaround**:
[If available]

**Additional Notes**:
[Any other relevant information]
```

---

## Test Sign-Off

### QA Engineer Sign-Off

**Tested By**: _______________________
**Date**: _______________________
**Illustrator Version**: _______________________
**Operating System**: _______________________

**Overall Test Result**: ⚠️ NOT EXECUTED
- Critical Tests Passed: __ / __
- High Priority Passed: __ / __
- Medium Priority Passed: __ / __
- Low Priority Passed: __ / __
- **Total Passed**: __ / 69
- **Pass Rate**: __%

**Recommendation**:
- [ ] Approve for release
- [ ] Approve with known issues documented
- [ ] Return to Dev for critical bug fixes
- [ ] Requires additional testing in areas: _______________

**Critical Bugs Found**: 0 (not tested)
**High Priority Bugs**: 0 (not tested)
**Medium Priority Bugs**: 0 (not tested)
**Low Priority Bugs**: 0 (not tested)

**Notes**:
_This test plan was generated by the QA Engineer agent but NOT EXECUTED due to environment limitations (no Illustrator access in Claude Code). All tests are marked as NOT EXECUTED and require manual testing by a human QA engineer with Illustrator installed._

---

## Appendix A: Reference Coordinate Calculations

### Triquetra (n=3, rotation=-30°) on 600×600pt Artboard

**Artboard Dimensions**:
- Width: 600pt
- Height: 600pt
- Center: (300, 300)
- Radius: 150pt (600 × 0.25)

**Rotation**: -30° = -π/6 radians

**Vertex Calculations**:
```
angleStep = 2π / 3 = 120° = 2.0944 radians
rotRad = -30° * (π/180) = -0.5236 radians

Vertex 0:
  angle = -0.5236 + 0 * 2.0944 = -0.5236 rad
  x = 300 + 150 * cos(-0.5236) = 300 + 150 * 0.866 = 429.9
  y = 300 + 150 * sin(-0.5236) = 300 + 150 * (-0.5) = 225.0

Vertex 1:
  angle = -0.5236 + 1 * 2.0944 = 1.5708 rad (90°)
  x = 300 + 150 * cos(1.5708) = 300 + 0 = 300.0
  y = 300 + 150 * sin(1.5708) = 300 + 150 = 450.0

Vertex 2:
  angle = -0.5236 + 2 * 2.0944 = 3.6652 rad
  x = 300 + 150 * cos(3.6652) = 300 + 150 * (-0.866) = 170.1
  y = 300 + 150 * sin(3.6652) = 300 + 150 * (-0.5) = 225.0
```

**Expected Vertex Positions** (within ±2px):
- Vertex 0: (430, 225) - Right-bottom
- Vertex 1: (300, 450) - Top (HIGHEST Y-coordinate)
- Vertex 2: (170, 225) - Left-bottom

**KEY VERIFICATION**: Top vertex Y=450 should be ABOVE center Y=300. If measured Y < 300, pattern is vertically flipped (Y-axis bug regression).

---

## Appendix B: Test Data Files

### Required Test Files

1. **Reference SVG Files** (from FloAng.html):
   - `triquetra-reference.svg` (n=3, flow=-0.66, angle=60, rotation=-30)
   - `flower-reference.svg` (n=6, flow=-0.8, angle=30, rotation=0)
   - `star-reference.svg` (n=5, flow=-1.8, angle=72, rotation=-18)
   - `smooth-reference.svg` (n=6, flow=1.0, angle=120, rotation=0)

2. **Test Illustrator Documents**:
   - `test-600x600.ai` (600×600pt artboard)
   - `test-800x800.ai` (800×800pt artboard)
   - `test-1000x1000.ai` (1000×1000pt artboard)
   - `test-multi-artboard.ai` (3 artboards: 600×600, 1000×800, 400×400)

3. **Overlay Test Template**:
   - `overlay-template.ai` (for visual comparison with web version)

---

## Appendix C: Automated Test Scaffold (Future Work)

### Unit Test Framework Recommendation

For future automated testing (Phase 2+), consider implementing unit tests for the core algorithm:

```javascript
// Example unit test structure (not implemented in MVP)
import { generateFlowAngleData, calculateOrthogonalAngle } from '../src/flowangle-core.js';

describe('FloAng Core Algorithm', () => {
    describe('calculateOrthogonalAngle', () => {
        it('should calculate correct orthogonal angle for n=3', () => {
            expect(calculateOrthogonalAngle(3)).toBe(60);
        });

        it('should calculate correct orthogonal angle for n=6', () => {
            expect(calculateOrthogonalAngle(6)).toBe(120);
        });
    });

    describe('generateFlowAngleData', () => {
        it('should generate 3 vertices for Triquetra', () => {
            const result = generateFlowAngleData({
                sides: 3,
                flowFactor: -0.66,
                handleAngle: 60,
                rotation: -30,
                centerX: 300,
                centerY: 300,
                radius: 150
            });

            expect(result.vertices).toHaveLength(3);
            expect(result.type).toBe('bezier');
        });

        it('should generate circle for n=1', () => {
            const result = generateFlowAngleData({
                sides: 1,
                flowFactor: 0,
                handleAngle: 0,
                rotation: 0,
                centerX: 300,
                centerY: 300,
                radius: 150
            });

            expect(result.type).toBe('circle');
            expect(result.radius).toBe(150);
        });
    });
});
```

---

**End of QA Test Plan**

**Document Status**: Complete but NOT EXECUTED
**Reason**: Requires Adobe Illustrator testing environment
**Next Step**: Human QA tester to execute test plan manually
**Priority**: Execute Critical and High Priority tests first
**Estimated Testing Time**: 8-12 hours for comprehensive testing
